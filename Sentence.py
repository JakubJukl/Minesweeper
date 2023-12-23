
class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells: set[tuple[int, int]], count: int):
        self.cells = cells
        self.count = count

    def __hash__(self):
        return hash((tuple(self.cells), self.count))
        
    def __eq__(self, other):
        return self.cells == other.cells

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
        if self.count == 0:
            return self.cells
        return set()
    
    def mark_mines(self, mines: set[tuple[int, int]]) -> bool:
        len_of_cells_with_mines = len(self.cells)
        self.cells -= mines
        len_of_cells = len(self.cells)
        self.count -= len_of_cells_with_mines - len_of_cells
        return len_of_cells_with_mines != len_of_cells

    def mark_safes(self, safes: set[tuple[int, int]]) -> bool:
        len_of_cells_with_safes = len(self.cells)
        self.cells -= safes
        return len_of_cells_with_safes != len(self.cells)


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
                
    def is_resolved(self):
        return len(self.cells) == self.count or self.count == 0
    
    def is_subset(self, other):
        return self.cells.issubset(other.cells)
    
    def minus(self, subset):
        self.cells -= subset.cells
        self.count -= subset.count