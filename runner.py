import pygame
import sys
import time

from GameState import GameState

HEIGHT = 8
WIDTH = 8
MINES = 12

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Rules
RULES = [
    "Click a cell to reveal it.",
    "Right-click a cell to mark it as a mine.",
    "Mark all mines successfully to win!"
]

# Create game
pygame.init()
size = width, height = WINDOW_WIDTH, WINDOW_HEIGHT
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

gameState = GameState(height=HEIGHT, width=WIDTH, mines=MINES)

# Show instructions initially
instructions = True

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        for i, rule in enumerate(RULES):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if gameState.game.is_mine((i, j)) and gameState.lost:
                if (i, j) == gameState.losing_move:
                    red_background = mine.copy() # just for size
                    red_background.fill((255, 0, 0, 100))
                    screen.blit(red_background, rect)
                    screen.blit(mine, rect)
                else:
                    screen.blit(mine, rect)
            elif (i, j) in gameState.flags:
                screen.blit(flag, rect)
            elif (i, j) in gameState.revealed:
                neighbors = smallFont.render(
                    str(gameState.game.nearby_mines((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # AI Move button
    aiButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Move", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiButton.center
    pygame.draw.rect(screen, WHITE, aiButton)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    def isGameWon(gameState: GameState):
        return gameState.game.mines == gameState.flags or (gameState.game.width * gameState.game.height - len(gameState.game.mines)) == len(gameState.revealed)

    # Display text
    text = "Lost" if gameState.lost else "Won" if isGameWon(gameState) else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None
    place_flag = False

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not gameState.lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in gameState.revealed:
                    if (i, j) in gameState.flags:
                        gameState.flags.remove((i, j))
                        gameState.ai.flag_removed((i, j))
                    else:
                        gameState.flags.add((i, j))
                        gameState.ai.flag_placed((i, j))
                    time.sleep(0.3)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        # If AI button clicked, make an AI move
        if aiButton.collidepoint(mouse) and not gameState.lost:
            move, place_flag = gameState.ai.move()
            time.sleep(0.3)

        # Reset game state
        elif resetButton.collidepoint(mouse):
            gameState = GameState(height=HEIGHT, width=WIDTH, mines=MINES)
            continue

        # User-made move
        elif not gameState.lost:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse)
                            and (i, j) not in gameState.flags
                            and (i, j) not in gameState.revealed):
                        move = (i, j)

    # Make move and update AI knowledge
    if move:
        if place_flag:
            gameState.flags.add(move)
            gameState.ai.flag_placed(move)
        else:
            if gameState.game.is_mine(move):
                gameState.lost = True
                gameState.losing_move = move
            else:
                nearby = gameState.game.nearby_mines(move)
                gameState.revealed.add(move)
                gameState.ai.add_knowledge(move, nearby)

    pygame.display.flip()
