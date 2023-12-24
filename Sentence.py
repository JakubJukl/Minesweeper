import random


class Sentence():
    """
    Logical statement about a Minesweeper game. Consists of cells and how many of them are mines.
    Example: From cells (A, B, C) exactly 2 are mines.
        If we know that A and B are mines, then C is safe.
        If we know that A and C are mines, then B is safe.
        If we know that B and C are mines, then A is safe.
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
        """Returns cells, that are known to be mines."""
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """Returns cells, that are known to be safe."""
        if self.count == 0:
            return self.cells
        return set()

    def mark_mines(self, mines: set[tuple[int, int]]) -> bool:
        """Removes mines from cells and updates count. Returns True if new mines were marked."""
        len_of_cells_with_mines = len(self.cells)
        self.cells -= mines
        len_of_cells = len(self.cells)
        self.count -= len_of_cells_with_mines - len_of_cells
        return len_of_cells_with_mines != len_of_cells

    def mark_safes(self, safes: set[tuple[int, int]]) -> bool:
        """Removes safes from cells. Returns True if new safes were marked."""
        len_of_cells_with_safes = len(self.cells)
        self.cells -= safes
        return len_of_cells_with_safes != len(self.cells)

    def mark_mine(self, cell):
        """Marks a cell as a mine. Updates internal knowledge representation."""
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """Marks a cell as safe. Updates internal knowledge representation."""
        if cell in self.cells:
            self.cells.remove(cell)

    def is_resolved(self):
        """
        Returns True if the sentence is solved. 
        1) Number of mines is equal to number of cells.
        2) Count of mines is 0.
        """
        return len(self.cells) == self.count or self.count == 0

    def is_subset(self, other):
        """
        Given: 
            Sentence 1 with cells (A, B, C) and count 2
            Sentence 2 with cells (A, B) and count 1
        Sentence 2 is a subset of Sentence 1, because all cells of Sentence 2 are in Sentence 1.
        """
        return self.cells.issubset(other.cells)

    def minus_subset(self, subset):
        """
        Sentence 1 with cells (A, B, C) and count 2
        Sentence 2 with cells (A, B) and count 1
        Sentence 1 minus Sentence 2 is a sentence with cells (C) and count 1.
        """
        self.cells -= subset.cells
        self.count -= subset.count

    def mine_probability(self):
        """Returns probability of choosing a mine, when choosing a random cell from the sentence."""
        cell_count = len(self.cells)
        if (cell_count == 0):
            print("Error: cell count is 0")
            return 1  # return 1 as a highest chance
        return self.count / cell_count

    def get_random_cell(self):
        """Returns a random cell from the sentence."""
        return random.choice(tuple(self.cells))
