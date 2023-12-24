from Sentence import Sentence
from collections import deque

class MinesweeperAI():

    # if AI shouldn't know about number of mines, pass 0
    def __init__(self, height: int, width: int, mines: int, search_asap: bool):
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
        self.search_asap = search_asap

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
        """Attempts to find new safes and mines using the knowledge base"""
        subset_any_last_run = True
        while (self.search_asap or (len(self.__get_safe_moves()) == 0)) and subset_any_last_run:
            self.__remove_known()

            if self.search_asap or (len(self.__get_safe_moves()) == 0):
                subset_any_last_run = self.__reduce_supersets()

    def __remove_known(self) -> bool:
        """Resolves sentences by removing known safes and mines from them"""
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

    def __reduce_supersets(self) -> bool:
        """Finds superset and subset combinations and removes subset cells from the superset"""
        subset_any_last_run = False
        for sentence_i in self.knowledge:
            for sentence_j in self.knowledge:
                # iterate through all combinations of sentences and check for subsets
                if not sentence_j == sentence_i and sentence_i.is_subset(sentence_j):
                    sentence_j.minus_subset(sentence_i)
                    subset_any_last_run = True
        # reassign knowledge to rehash the set
        self.knowledge = set(self.knowledge)
        return subset_any_last_run


    def __get_safe_moves(self) -> set[tuple[int, int]]:
        """Returns known safe moves that have not been made yet"""
        return self.safes - self.moves_made
    
    def move(self) -> tuple[tuple[int, int], bool]:
        """Returns a move to be made and a boolean indicating if it should be flag placing move"""
        return self.__move(True)

    def __move(self, try_again: bool) -> tuple[tuple[int, int], bool]:
        """Can be called recursively, so if there are no safe moves, it will try to find new safes and mines"""
        non_marked_mines = self.mines - self.flags_placed
        if len(non_marked_mines) > 0:
            return non_marked_mines.pop(), True
        safe_moves = self.__get_safe_moves()
        if len(safe_moves) > 0:
            return safe_moves.pop(), False
        else:
            self.__find_safes()
            if try_again:
                return self.__move(False)
            else:
                return self.__get_random_move(), False
            

    def __get_random_move(self) -> tuple[int, int]:
        """Returns a random move that has not been made yet"""
        available_moves = self.board - self.moves_made - self.mines - self.flags_placed

        if len(available_moves) == 0:
            # in case flags were placed where they shouldn't be
            available_moves = self.board - self.moves_made - self.mines
        if len(available_moves) == 0:
            return None
        
        # if we know number of mines, we can calculate the probability of getting a mine when making a random move without any knowledge
        number_of_mines = len(available_moves) if self.num_of_mines == 0 else self.num_of_mines - len(self.mines)
        safest_sentence = Sentence(available_moves, number_of_mines)
        safest_sentence_probability = safest_sentence.mine_probability()

        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                print("empty sentence in making random move -> shouldn't happen")
                continue
            current_sentence_probability = sentence.mine_probability()
            if current_sentence_probability < safest_sentence_probability:
                safest_sentence = sentence
                safest_sentence_probability = current_sentence_probability
        
        if (safest_sentence_probability == 1):
            print("Making a random move, but can't calculate probability, because of unknown number of mines")
        else:
            print(f"Making a random move with probability of finding mine: {round(safest_sentence_probability, 2) * 100 : .0f}%")
        return safest_sentence.get_random_cell()
            
    def flag_placed(self, cell: tuple[int, int]):
        self.flags_placed.add(cell)

    def flag_removed(self, cell: tuple[int, int]):
        self.flags_placed.remove(cell)
