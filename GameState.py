from Minesweeper import Minesweeper
from MinesweeperAI import MinesweeperAI

class GameState():
    game: Minesweeper
    ai: MinesweeperAI
    # Keep track of revealed cells, flagged cells, and if a mine was hit
    revealed: set
    flags: set
    lost: bool
    losing_move: tuple[int, int]

    def __init__(self, height, width, mines, ai_knows_number_of_mines, ai_search_asap) -> None:
        self.game = Minesweeper(height, width, mines)
        ai_mines = mines if ai_knows_number_of_mines else 0
        self.ai = MinesweeperAI(height, width, ai_mines, ai_search_asap)
        self.revealed = set()
        self.flags = set()
        self.lost = False
        self.losing_move = None