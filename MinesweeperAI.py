import random

from Sentence import Sentence

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial height and width, number of mines on the playfield
        self.height = height
        self.width = width
        self.num_of_mines = mines

        # Keep track of which cells have been clicked on
        self.moves_made = set()

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
                self.board.add((i,j))
        self.knowledge.append(Sentence(self.board,self.num_of_mines))
               

    def move(self):
        """
        """


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
        possible_moves = list(self.board.difference(self.moves_made).difference(self.mines)) 
        length = len(possible_moves)
        if length > 0:    
            return possible_moves[random.randrange(length)]
        return None
    
    
