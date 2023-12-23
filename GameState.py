from Minesweeper import Minesweeper
from MinesweeperAI import MinesweeperAI

class GameState():
    game: Minesweeper
    ai: MinesweeperAI
    # Keep track of revealed cells, flagged cells, and if a mine was hit
    revealed: set
    flags: set
    lost: bool

    def __init__(self, height, width, mines) -> None:
        self.game = Minesweeper(height, width, mines)
        self.ai = MinesweeperAI(height, width, mines)
        self.revealed = set()
        self.flags = set()
        self.lost = False