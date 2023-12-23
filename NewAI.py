from Sentence import Sentence
from collections import deque


class NewAI():

    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.num_of_mines = mines

        self.moves_made = set()
        self.flags_placed = set()

        self.mines = set()
        self.safes = set()

        self.knowledge : set[Sentence] = set()
        self.unpro: set[Sentence] = set()

        self.board = set()
        for i in range(self.height):
            for j in range(self.width):
                self.board.add((i, j))
        self.knowledge.add(Sentence(self.board.copy(), self.num_of_mines))

    def __get_neighbours(self, cell: tuple[int, int]):
        neighbours = set()
        y, x = cell
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if (i, j) in self.board and (i, j) != cell:
                    neighbours.add((i, j))
        return neighbours

    def add_knowledge(self, cell: tuple[int, int], count: int):
        self.moves_made.add(cell)
        self.safes.add(cell)
        neighbours = self.__get_neighbours(cell)
        sentence = Sentence(neighbours, count)
        # print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
        # print("got: ", cell, count, sentence)
        # print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
        sentence.mark_safes(self.safes)
        sentence.mark_mines(self.mines)
        # print("after marking: ", sentence)
        # print("------------------------------")
        # skip if empty
        if not len(sentence.cells) == 0:
            self.knowledge.add(sentence)
            # print("added ", sentence)
        # print("------------------------------")
        self.__find_safes()
        # print("safes: ", self.__get_safe_moves())
        # print("mines: ", self.mines)

    def __find_safes(self):
        resolved_any_last_run = True
        subset_any_last_run = True
        # while len(self.__get_safe_moves()) == 0 and (resolved_any_last_run or subset_any_last_run):
        while resolved_any_last_run or subset_any_last_run:
            resolved_any_last_run = self.__remove_known()

            # if len(self.__get_safe_moves()) == 0:
            subset_any_last_run = self.__create_subsets()

    def __remove_known(self) -> bool:
        to_traverse = deque(self.knowledge)
        traversed = set()
        resolved_any = False

        while len(to_traverse) > 0:
            sentence = to_traverse.pop()
            sentence.mark_safes(self.safes)
            sentence.mark_mines(self.mines)
            if sentence.is_resolved():
                resolved_any = True
                self.safes.update(sentence.known_safes())
                self.mines.update(sentence.known_mines())
                to_traverse.extendleft(traversed)
                traversed = set()
                print("resolved ", sentence)
            else:
                # print("not resolved ", sentence) 
                traversed.add(sentence)

        self.knowledge = set(traversed)
        return resolved_any

    def __create_subsets(self) -> bool:
        subset_any_last_run = False
        for sentence_i in self.knowledge:
            for sentence_j in self.knowledge:
                if not sentence_j == sentence_i and sentence_i.is_subset(sentence_j):
                    # print("subset:", sentence_i, " is subset of ", sentence_j)
                    sentence_j.minus(sentence_i)
                    # print("after minus: ", sentence_j)
                    subset_any_last_run = True
        self.knowledge = set(self.knowledge)
        return subset_any_last_run


    def __get_safe_moves(self):
        return self.safes - self.moves_made

    def move(self, try_again: bool = True):
        non_marked_mines = self.mines - self.flags_placed
        if len(non_marked_mines) > 0:
            return non_marked_mines.pop(), True
        # print("..............................")
        self.__find_safes()
        safe_moves = self.__get_safe_moves()
        if len(safe_moves) > 0:
            return safe_moves.pop(), False
        else:
            # self.__find_safes()
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
