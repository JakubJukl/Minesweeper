from Sentence import Sentence


class NewAI():

    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.num_of_mines = mines

        self.moves_made = set()
        self.flags_placed = set()

        self.mines = set()
        self.safes = set()

        self.knowledge = set()

        self.board = set()
        for i in range(self.height):
            for j in range(self.width):
                self.board.add((i, j))
        self.knowledge.append(Sentence(self.board, self.num_of_mines))

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
        neighbours = self.__get_neighbours(cell)
        neighbours -= self.safes
        neighbours_with_mines = neighbours.copy()
        neighbours -= self.mines
        count -= len(neighbours_with_mines) - len(neighbours)

        # skip if empty
        if len(neighbours) == 0:
            return

        sentence = Sentence(neighbours, count)
        self.knowledge.add(sentence)

    def __remove_known(self):
        for knowledge_sentence in self.knowledge:
            knowledge_sentence.mark_safes(self.safes)
            knowledge_sentence.mark_minem(self.mines)
            if knowledge_sentence.is_resolved():
                self.knowledge.remove(knowledge_sentence)
                self.safes.update(knowledge_sentence.known_safes())
                self.mines.update(knowledge_sentence.known_mines())
        

    def move(self):
        safe_moves = self.safes - self.moves_made
        if len(safe_moves) > 0:
            return safe_moves.pop()
        else:
            self.__remove_known()
            if len(self.knowledge) == 0:
                return None
            else:
                sentence = self.knowledge.pop()
                return sentence.cells.pop()