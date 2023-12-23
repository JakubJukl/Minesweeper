import random

from Sentence import Sentence
from NewAI import NewAI


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8, mines=8):

        self.newAI = NewAI(height, width, mines)

        # Set initial height and width, number of mines on the playfield
        self.height = height
        self.width = width
        self.num_of_mines = mines

        # Keep track of which cells have been clicked on
        self.moves_made = set()
        self.flags_placed = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        """
        If we presume, that our agent is well informed, he has to 
        know how many mines are there. If he shouldn't be that well 
        informed, we can just comment it out. It just makes one huge 
        sentence of all cells in the field and there has to be exactly 
        'x' mines in them.  
        BTW: The AI takes huge performance hit in certain situations, 
        since it can have 70+ subsets (sentences) in midgame.
        Creates board, so the ai can compute random moves efficiently.
        """
        self.board = set()
        for i in range(self.height):
            for j in range(self.width):
                self.board.add((i, j))
        self.knowledge.append(Sentence(self.board, self.num_of_mines))

    def make_move(self) -> tuple[int, int]:
        """
        returns a move to make on the Minesweeper board.
        """
        move = self.make_safe_move()
        if move is None:
            move = self.make_random_move()
            if move is None:
                print("No moves left to make.")
            else:
                print("AI making random move.")
        else:
            print("AI making safe move.")

        s = self.newAI.move()
        print("making move: ", s)
        return s
        #return move

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge  
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.newAI.add_knowledge(cell, count)

        neighboring = set()
        self.moves_made.add(cell)
        self.mark_safe(cell)

        y, x = cell

        # create set of neighboring cells
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                # I don't think the jumps behave like hidden traps, but more as preconditions
                # Ignore the cell itself
                if (i, j) in self.board and not (i, j) == cell:
                    neighboring.add((i, j))

        neighboring -= self.safes
        neighboring_with_mines = neighboring.copy()
        neighboring -= self.mines
        count -= len(neighboring_with_mines) - len(neighboring)

        # if there is at least one cell in the set
        if len(neighboring) > 0:
            # add sentence about neighboring cells
            self.knowledge.append(Sentence(neighboring, count))
            self.update_knowledge()

    def known_safes(self, sentence):
        return sentence.known_safes().copy()
    
    def known_mines(self, sentence):
        return sentence.known_mines().copy()

    def update_knowledge(self):
        """
        Updates knowledge with regards to newly gained information.
        """
        num_of_changed = 1
        while num_of_changed > 0:
            num_of_changed = 0
            num_of_changed += self.mark(self.known_safes, self.mark_safe)
            num_of_changed += self.mark(self.known_mines, self.mark_mine)
            num_of_changed += self.create_subsets()

    def create_subsets(self):
        """
        Creates subset out of a set and another subset. subset2 = set - subset1
        """
        num_of_changed = 0
        length = len(self.knowledge)
        i = 0
        # for every sentence in knowledge
        while i < length:
            sentence = self.knowledge[i]
            # remove duplicates of the sentence
            length -= self.remove_duplicates(sentence)
            j = 0
            # for every sentence in knowledge again
            while j < length:
                subset_sentence = self.knowledge[j]
                # unless it's the same sentence
                if not sentence == subset_sentence:
                    if subset_sentence.cells.issubset(sentence.cells):
                        differ = Sentence(sentence.cells.difference(
                            subset_sentence.cells), sentence.count - subset_sentence.count)
                        # if subset2 (differ) is not present in knowledge
                        if not differ in self.knowledge:
                            self.knowledge.append(differ)
                            length += 1
                            num_of_changed += 1
                j += 1
            i += 1
        return num_of_changed

    def mark(self, known_set_fce, fce):
        """
        Marks every cell, that is known to be safe/mine.
        Made because both mark_safe and mark_mine require looping
        through sentences and the functions just looked pretty similiar
        if made separate.
        """
        num_of_changed = 0
        i = 0
        length = len(self.knowledge)
        while i < length:
            sentence = self.knowledge[i]
            known_set = known_set_fce(sentence)
            for safe in known_set:
                fce(safe)
                num_of_changed += 1
            length -= self.remove_if_empty(sentence)
            i += 1
        return num_of_changed

    def remove_duplicates(self, sentence) -> int:
        """
        Removes duplicate sentences from knowledge.
        """
        length = 0
        while self.knowledge.count(sentence) > 1:
            self.knowledge.remove(sentence)
            length += 1
        return length

    def remove_if_empty(self, sentence) -> int:
        """
        Removes sentence from knowledge, if it's empty.
        """
        if len(sentence.cells) < 1:
            self.knowledge.remove(sentence)
            return 1
        return 0

    def make_safe_move(self) -> tuple[int, int]:
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        not_made_safes = self.safes - self.moves_made
        if len(not_made_safes) > 0:
            return not_made_safes.pop()
        else:
            return None

    def make_random_move(self) -> tuple[int, int]:
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # creates list of all possible moves
        possible_moves = list(self.board - self.moves_made - self.mines)
        length = len(possible_moves)
        if length > 0:
            return possible_moves[random.randrange(length)]
        return None

    def flag_placed(self, cell: tuple[int, int]):
        self.flags_placed.add(cell)
        self.newAI.flag_placed(cell)

    def flag_removed(self, cell: tuple[int, int]):
        self.flags_placed.remove(cell)
        self.newAI.flag_removed(cell)