import re

WINDOW_WIDTH_KEY = "WINDOW_WIDTH"
WINDOW_HEIGHT_KEY = "WINDOW_HEIGHT"
HEIGHT_KEY = "HEIGHT_TILES"
WIDTH_KEY = "WIDTH_TILES"
MINES_KEY = "MINE_TILES"
AI_KNOWS_NUMBER_OF_MINES_KEY = "AI_KNOWS_NUMBER_OF_MINES"
AI_SEARCH_ASAP_KEY = "AI_SEARCH_ASAP"


class Config():
    __config_line_regex = re.compile(r"(.*)\s=\s?(\d+)")

    window_width: int = None
    window_height: int = None
    height: int = None
    width: int = None
    mines: int = None
    ai_knows_number_of_mines: bool = None
    ai_search_asap: bool = None

    def __init__(self) -> None:
        pass

    def set_from_file(self, line: str):
        match = re.search(self.__config_line_regex, line)
        if match:
            key = match.group(1)
            value = int(match.group(2))
            if key == WINDOW_WIDTH_KEY:
                self.window_width = value
            elif key == WINDOW_HEIGHT_KEY:
                self.window_height = value
            elif key == HEIGHT_KEY:
                self.height = value
            elif key == WIDTH_KEY:
                self.width = value
            elif key == MINES_KEY:
                self.mines = value
            elif key == AI_KNOWS_NUMBER_OF_MINES_KEY:
                self.ai_knows_number_of_mines = bool(value)
            elif key == AI_SEARCH_ASAP_KEY:
                self.ai_search_asap = bool(value)
            else:
                print(f"Unknown config key: '{key}'")

    def is_setup(self) -> bool:
        return (
            self.height is not None and
            self.width is not None and
            self.mines is not None and
            self.window_width is not None and
            self.window_height is not None and
            self.ai_knows_number_of_mines is not None and
            self.ai_search_asap is not None
        )
