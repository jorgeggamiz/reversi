#Size of the board
SIZE = 8 # not changeable

# Constants for Pygame display
CELL_SIZE = 60
MARGIN = 10
BOARD_SIZE = SIZE * CELL_SIZE + (SIZE + 1) * MARGIN
WINDOW_SIZE = (BOARD_SIZE, BOARD_SIZE + 50)  # Extra space for score display

# Delay in milliseconds between the player's move and AI's move
AI_DELAY_MS = 1000  # 1 second

VOLUME = 0.5