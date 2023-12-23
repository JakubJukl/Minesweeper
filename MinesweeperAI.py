from Sentence import Sentence
from collections import deque

class MinesweeperAI():

    # if AI shouldn't know about number of mines, pass 0
    def __init__(self, height: int, width: int, mines: int = 0):
        # Set initial width and height of the board and optional number of mines
        self.height = height
        self.width = width
        self.num_of_mines = mines

        # to keep track of moves made and flags placed
        self.moves_made = set()
        self.flags_placed = set()

        # discovered mines and safes
        self.mines = set()
        self.safes = set()

        # knowledge base -> set of sentences
        self.knowledge : set[Sentence] = set()

        # if True, calculation of safe moves happens as soon as possible
        self.search_asap = True

        # initialize board, so we can access random moves faster
        self.board = set()
        for i in range(self.height):
            for j in range(self.width):
                self.board.add((i, j))
        
        # if we know number of mines, add sentence with all cells and number of mines
        if self.num_of_mines > 0:
            self.knowledge.add(Sentence(self.board.copy(), self.num_of_mines))

    def __get_neighbours(self, cell: tuple[int, int]) -> set[tuple[int, int]]:
        """Returns a set of all neighbours of a cell"""
        neighbours = set()
        y, x = cell
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if (i, j) in self.board and (i, j) != cell:
                    neighbours.add((i, j))
        return neighbours

    def add_knowledge(self, cell: tuple[int, int], count: int):
        """Notify AI that cell is a neighbour of (count) mines"""
        self.moves_made.add(cell)
        self.safes.add(cell)
        neighbours = self.__get_neighbours(cell)
        sentence = Sentence(neighbours, count)
        sentence.mark_safes(self.safes)
        sentence.mark_mines(self.mines)
        if not len(sentence.cells) == 0:
            self.knowledge.add(sentence)

        if self.search_asap:
            self.__find_safes()

    def __find_safes(self):
        subset_any_last_run = True
        while (self.search_asap or (len(self.__get_safe_moves()) == 0)) and subset_any_last_run:
            self.__remove_known()

            if self.search_asap or (len(self.__get_safe_moves()) == 0):
                subset_any_last_run = self.__create_subsets()

    def __remove_known(self) -> bool:
        # store sentences, that were not traversed with current known set of mines and safes in a deque
        # so they can be traversed in an order
        to_traverse = deque(self.knowledge)
        traversed = set()
        resolved_any = False

        while len(to_traverse) > 0:
            sentence = to_traverse.pop()
            sentence.mark_safes(self.safes)
            sentence.mark_mines(self.mines)
            if sentence.is_resolved():
                # if sentence is resolved, we do not wish to add it to the knowledge base
                # but we do wish to update the knowledge base with the new safes and mines
                resolved_any = True
                self.safes.update(sentence.known_safes())
                self.mines.update(sentence.known_mines())
                # since we updated known mines and safes, we need to recheck all previously traversed sentences
                # so we add them to the deque and reset the traversed set
                to_traverse.extendleft(traversed)
                traversed = set()
            else:
                traversed.add(sentence)

        self.knowledge = set(traversed)
        return resolved_any

    def __create_subsets(self) -> bool:
        subset_any_last_run = False
        for sentence_i in self.knowledge:
            for sentence_j in self.knowledge:
                if not sentence_j == sentence_i and sentence_i.is_subset(sentence_j):
                    sentence_j.minus(sentence_i)
                    subset_any_last_run = True
        self.knowledge = set(self.knowledge)
        return subset_any_last_run


    def __get_safe_moves(self):
        return self.safes - self.moves_made

    def move(self, try_again: bool = True):
        non_marked_mines = self.mines - self.flags_placed
        if len(non_marked_mines) > 0:
            return non_marked_mines.pop(), True
        safe_moves = self.__get_safe_moves()
        if len(safe_moves) > 0:
            return safe_moves.pop(), False
        else:
            self.__find_safes()
            if try_again:
                return self.move(False)
            else:
                return self.__get_random_move(), False
            
    def __get_random_move(self):
        available_moves = self.board - self.moves_made - self.mines - self.flags_placed
        if (len(available_moves) == 0):
            available_moves = self.board - self.moves_made - self.mines
        if (len(available_moves) == 0):
            return None
        else:
            print("making random move")
            return available_moves.pop()
            
    def flag_placed(self, cell: tuple[int, int]):
        self.flags_placed.add(cell)

    def flag_removed(self, cell: tuple[int, int]):
        self.flags_placed.remove(cell)
