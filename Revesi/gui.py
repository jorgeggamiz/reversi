import pygame
from pygame import mixer
from reversi import valid_play, get_valid_plays, make_a_play, is_game_over
from ai_player import intelligent_play
from board import new_board, restart_board
from score import score
from colors import *
from config import *

# Load images
player_flag = pygame.transform.scale(pygame.image.load("assets/spain.png"), (CELL_SIZE, CELL_SIZE))
ai_flag = pygame.transform.scale(pygame.image.load("assets/poland.png"), (CELL_SIZE, CELL_SIZE))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Reversi")

# Font for score display
FONT = pygame.font.Font(None, 36)

# For the sounds
mixer.init()
sounds = {"move" : mixer.Sound("assets/sound.mp3"),
          "lost" : mixer.Sound("assets/lost.mp3")}
for sound in sounds.values():
    sound.set_volume(VOLUME)


# Function to draw the game board
def draw_board(screen, board, valid_moves=None, hover_pos=None):
    screen.fill(BROWN)  # Background color for the board

    for row in range(SIZE):
        for col in range(SIZE):
            # Define the rectangle for the cell
            rect = pygame.Rect(
                col * (CELL_SIZE + MARGIN) + MARGIN,
                row * (CELL_SIZE + MARGIN) + MARGIN + 50,  # Offset for score display
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, BROWN2, rect)  # Draw the cell background
            
            # Draw player or AI pieces
            if board[row][col] == 'X':
                screen.blit(player_flag, rect.topleft)
            elif board[row][col] == 'O':
                screen.blit(ai_flag, rect.topleft)

            # Highlight valid moves for the current player
            if valid_moves and (row, col) in valid_moves:
                # pygame.draw.circle(screen, GRAY, rect.center, CELL_SIZE // 4)
                color = WHITE if (hover_pos and rect.collidepoint(hover_pos)) else GRAY
                pygame.draw.circle(
                    screen,
                    color,
                    rect.center,
                    CELL_SIZE // 5,
                )


# Function to draw the score
def draw_score(screen, board):
    # Calculate scores
    player_score, ai_score = score(board)['X'], score(board)['O']
    
    # Create text surfaces
    player_text = FONT.render("Player", True, WHITE)
    player_score_text = FONT.render(str(player_score), True, WHITE)
    ai_score_text = FONT.render(str(ai_score), True, WHITE)
    ai_text = FONT.render("AI", True, WHITE)

    # Load and scale images for tokens
    player_token_img = pygame.transform.scale(player_flag, (25, 25))
    ai_token_img = pygame.transform.scale(ai_flag, (25, 25))

    # Calculate total width for centering
    total_width = (
        player_token_img.get_width() + player_text.get_width() + 
        player_score_text.get_width() + ai_score_text.get_width() +
        ai_text.get_width() + ai_token_img.get_width() + 90  # Space for separators and extra padding
    )
    start_x = (BOARD_SIZE - total_width) // 2  # Center horizontally

    # Clear previous score area
    screen.fill(BLACK, (0, 0, BOARD_SIZE, 50))

    # Draw Player section
    screen.blit(player_token_img, (start_x, 12))  # Player token
    player_text_x = start_x + player_token_img.get_width() + 10
    screen.blit(player_text, (player_text_x, 10))  # "Player"
    
    separator0_x = player_text_x + player_text.get_width() + 10
    separator0 = FONT.render("|", True, WHITE)
    screen.blit(separator0, (separator0_x, 10))  # First "|"

    player_score_x = separator0_x + separator0.get_width() + 10
    screen.blit(player_score_text, (player_score_x, 10))  # Player score

    # Draw separator " - "
    separator1_x = player_score_x + player_score_text.get_width() + 10
    separator1 = FONT.render("-", True, WHITE)
    screen.blit(separator1, (separator1_x, 10))

    # Draw AI score
    ai_score_x = separator1_x + separator1.get_width() + 10
    screen.blit(ai_score_text, (ai_score_x, 10))  # AI score

    separator2_x = ai_score_x + ai_score_text.get_width() + 10
    separator2 = FONT.render("|", True, WHITE)
    screen.blit(separator2, (separator2_x, 10))  # Final "|"

    # Draw AI section
    ai_text_x = separator2_x + separator2.get_width() + 10
    screen.blit(ai_text, (ai_text_x, 10))  # "AI"
    ai_token_x = ai_text_x + ai_text.get_width() + 10
    screen.blit(ai_token_img, (ai_token_x, 12))  # AI token



def game_over_screen(screen, player_score, ai_score):
    screen.fill((153, 76, 0))  # Background color for the game over screen

    # Determine the winner
    if player_score > ai_score:
        winner_text = "Player Wins!"
    elif player_score < ai_score:
        winner_text = "AI Wins!"
    else:
        winner_text = "It's a Tie!"

    # Display winner
    winner_surface = FONT.render(winner_text, True, WHITE)
    winner_rect = winner_surface.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 3))
    screen.blit(winner_surface, winner_rect)
    
    # Load and scale token images
    player_token_img = pygame.transform.scale(player_flag, (30, 30))
    ai_token_img = pygame.transform.scale(ai_flag, (30, 30))

    # Render the text
    player_text = FONT.render("Player", True, WHITE)
    player_score_text = FONT.render(str(player_score), True, WHITE)
    ai_text = FONT.render("AI", True, WHITE)
    ai_score_text = FONT.render(str(ai_score), True, WHITE)

    # Calculate total width for centering
    total_width = (
        player_token_img.get_width() + player_text.get_width() +
        player_score_text.get_width() + ai_score_text.get_width() +
        ai_text.get_width() + ai_token_img.get_width() + 90  # Space for separators
    )
    start_x = (BOARD_SIZE - total_width) // 2  # Center horizontally

    # Draw Player section
    screen.blit(player_token_img, (start_x, BOARD_SIZE // 2 - 15))  # Player token
    player_text_x = start_x + player_token_img.get_width() + 10
    screen.blit(player_text, (player_text_x, BOARD_SIZE // 2 - 20))  # "Player"
    
    separator0_x = player_text_x + player_text.get_width() + 10
    separator0 = FONT.render("|", True, WHITE)
    screen.blit(separator0, (separator0_x, BOARD_SIZE // 2 - 20))  # First "|"

    player_score_x = separator0_x + separator0.get_width() + 10
    screen.blit(player_score_text, (player_score_x, BOARD_SIZE // 2 - 20))  # Player score

    # Draw separator " - "
    separator1_x = player_score_x + player_score_text.get_width() + 10
    separator1 = FONT.render("-", True, WHITE)
    screen.blit(separator1, (separator1_x, BOARD_SIZE // 2 - 20))

    # Draw AI score
    ai_score_x = separator1_x + separator1.get_width() + 10
    screen.blit(ai_score_text, (ai_score_x, BOARD_SIZE // 2 - 20))  # AI score

    separator2_x = ai_score_x + ai_score_text.get_width() + 10
    separator2 = FONT.render("|", True, WHITE)
    screen.blit(separator2, (separator2_x, BOARD_SIZE // 2 - 20))  # Final "|"

    # Draw AI section
    ai_text_x = separator2_x + separator2.get_width() + 10
    screen.blit(ai_text, (ai_text_x, BOARD_SIZE // 2 - 20))  # "AI"
    ai_token_x = ai_text_x + ai_text.get_width() + 10
    screen.blit(ai_token_img, (ai_token_x, BOARD_SIZE // 2 - 15))  # AI token

    # Display restart message
    restart_text = "Press 'R' to Restart or 'ESC' to Quit"
    restart_surface = FONT.render(restart_text, True, WHITE)
    restart_rect = restart_surface.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE * 2 // 3))
    screen.blit(restart_surface, restart_rect)

    pygame.display.flip()  # Update the display

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    waiting = False
                if event.key == pygame.K_ESCAPE:  # Quit the game
                    pygame.quit()
                    exit()

# Function to get the cell clicked by the player
def get_cell(pos):
    x, y = pos
    col = x // (CELL_SIZE + MARGIN)
    row = (y - 50) // (CELL_SIZE + MARGIN)  # Adjust for score display offset
    if col < SIZE and row < SIZE and row >= 0:
        return row, col
    return None


# Main function
def main():
    main_board = new_board()
    restart_board(main_board)

    token_player = 'X'
    token_ai = 'O'
    running = True
    turn = 'Player'

    while running:
        valid_moves = None
        hover_pos = pygame.mouse.get_pos()  # Get mouse position

        if turn == 'Player':
            valid_moves = get_valid_plays(main_board, token_player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_l: game_over_screen(screen, score(main_board)['X'], score(main_board)['O'])

            if turn == 'Player' and event.type == pygame.MOUSEBUTTONDOWN:
                if not valid_moves:
                    turn='AI'
                cell = get_cell(event.pos)
                if cell:
                    row, col = cell
                    if valid_play(main_board, token_player, row, col):
                        make_a_play(main_board, token_player, row, col)
                        sounds["move"].play()

                        # Update the screen after player's move
                        draw_board(screen, main_board, None, None)
                        draw_score(screen, main_board)
                        pygame.display.flip()

                        # Wait before AI's move
                        pygame.time.wait(AI_DELAY_MS)
                        turn = 'AI'

        # AI Turn
        if turn == 'AI':
            valid_moves = get_valid_plays(main_board, token_ai)
            if valid_moves:
                #move = valid_moves[0]  # Simple AI picking the first valid move
                #move = random_play(main_board, token_ai)
                move = intelligent_play(main_board, token_ai)
                make_a_play(main_board, token_ai, move[0], move[1])
                sounds["move"].play()
                turn = 'Player'
            else: 
                turn = 'Player'

        # Check if the game is over
        if is_game_over(main_board):
            sounds["lost"].play()
            game_over_screen(screen, score(main_board)['X'], score(main_board)['O'])
            main_board = new_board()  # Restart the board
            restart_board(main_board)  # Reset the game state
            turn = 'Player'  # Reset turn to player

        # Draw the board and score
        draw_board(screen, main_board, valid_moves, hover_pos)
        draw_score(screen, main_board)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()