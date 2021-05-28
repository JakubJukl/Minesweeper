import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
                return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #safes = set()
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
                
            


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []


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
        neighboring = set()
        self.moves_made.add(cell)
        self.mark_safe(cell)
        #create set of neighboring cells, that are not already safe or mines
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):   
                # I don't think the jumps behave like hidden traps, but more as preconditions
                # Ignore the cell itself
                if i > self.height - 1 or i < 0 or j > self.width - 1 or j < 0:
                    continue
                if (i,j) in self.safes:                
                    continue
                if (i,j) in self.mines:             
                    count-=1
                    continue
                neighboring.add((i,j))
                
        #if there is at least one cell in the set
        if len(neighboring) > 0:
            #add sentence about neighboring cells
            self.knowledge.append(Sentence(neighboring,count))
            self.update_knowledge()


                                
    def update_knowledge(self):
        """
        Updates knowledge with regards to newly gained information.
        """
        num_of_changed = 1
        while num_of_changed > 0:
            num_of_changed = 0
            num_of_changed+=self.mark("known_safes()", self.mark_safe)
            num_of_changed+=self.mark("known_mines()",self.mark_mine)
            num_of_changed+=self.create_subsets()

    def create_subsets(self):
        """
        Creates subset out of a set and another subset. subset2 = set - subset1
        """
        num_of_changed = 0
        length = len(self.knowledge)
        i = 0
        #for every sentence in knowledge
        while i < length:      
            sentence = self.knowledge[i]
            #remove duplicates of the sentence
            length-= self.remove_duplicates(sentence)
            j = 0
            #for every sentence in knowledge again
            while j < length:
                subset_sentence = self.knowledge[j]
                #unless it's the same sentence
                if not sentence == subset_sentence:
                    if subset_sentence.cells.issubset(sentence.cells):
                        differ = Sentence(sentence.cells.difference(subset_sentence.cells),sentence.count - subset_sentence.count)
                        #if subset2 (differ) is not present in knowledge
                        if not differ in self.knowledge:
                            self.knowledge.append(differ)
                            length+=1
                            num_of_changed+=1
                j+=1
            i+=1
        return num_of_changed
        
    def mark(self, str_known_set, fce):
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
            known_set = eval("sentence."+str_known_set+".copy()")
            for safe in known_set:     
                fce(safe)
                num_of_changed+=1
            length-=self.remove_if_empty(sentence)   
            i+=1
        return num_of_changed
        
                
    def remove_duplicates(self, sentence):
        """
        Removes duplicate sentences from knowledge.
        """
        length = 0
        while self.knowledge.count(sentence) > 1:
                self.knowledge.remove(sentence)
                length+=1
        return length
            
                    
    def remove_if_empty(self, sentence):
        """
        Removes sentence from knowledge, if it's empty.
        """
        if len(sentence.cells) < 1:
                self.knowledge.remove(sentence)
                return 1
        return 0

    def print_empty_sentences(self):
        a = 0
        for sentence in self.knowledge:
            if len(sentence.cells) < 1:
                a+=1
                print(a,". prazdna veta ")

        
    def print_sentences(self):
        a = 0
        for sentence in self.knowledge:
            a+=1
            print(a,". veta je: ")
            print("pocet je... ",sentence.count)
            for cell in sentence.cells:           
                print("y=",cell[0]," x=",cell[1])
    
    def print_number_duplicate_sentences(self):
        for sentence in self.knowledge:
            a = -1
            for duplicate in self.knowledge:
                if sentence == duplicate:
                    a+=1
            if a > 0:
                print("veta: ",sentence," se nachazi ",a)
    
    def print_mines(self):
        print("miny jsou: ")
        for cell in self.mines:           
            print("y=",cell[0]," x=",cell[1])
            
    def print_safes(self):
        print("safe jsou: ")
        for cell in self.safes:           
            print("y=",cell[0]," x=",cell[1])
            
    def print_possible_safes(self):
        print("mozne safe pohyby jsou: ")
        for cell in self.safes: 
            if not cell in self.moves_made:
                print("y=",cell[0]," x=",cell[1])
                
    def find_sentence(self,y,x):
        for sentence in self.knowledge:
            for cell in sentence.cells:
                if cell == (y,x):
                    print(sentence)
    
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if not safe in self.moves_made: 
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """     
        #creates list of all possible moves
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                if not (i,j) in self.moves_made and not (i,j) in self.mines:
                    possible_moves.append((i,j))
        length = len(possible_moves)
        if length > 0:    
            pdb.set_trace()
            return possible_moves[random.randrange(length)]
        return None
    
    
    
    