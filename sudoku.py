from sudoku_generator import SudokuGenerator, Cell, Board, generate_sudoku
import pygame


def main():
    # Initialize Pygame
    pygame.init()

    # Define screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255,165,0)

    # Initialize the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Game")

    # Define game states
    GAME_START = 0
    GAME_IN_PROGRESS = 1
    GAME_OVER = 2

    # Set the initial game state
    current_state = GAME_START

    ''' Define font '''
    font = pygame.font.Font(None, 36)

    # Define button dimensions
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    # Define button positions
    EASY_BUTTON_POS = (50, 400)
    MEDIUM_BUTTON_POS = (300, 400)
    HARD_BUTTON_POS = (550, 400)

    # Define difficulty levels
    EASY = 0
    MEDIUM = 1
    HARD = 2

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle mouse clicks and other events based on the current game state

        # Draw the appropriate screen based on the current game state
        if current_state == GAME_START:
            # Draw background
            background_image = pygame.image.load("menu_background.jpg")
            screen.blit(background_image, (0, 0))

            # Draw title
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("Welcome to Sudoku", True, WHITE)
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
            screen.blit(title_text, title_text_rect)

            # Draw "Select Game Mode" text
            mode_text_font = pygame.font.Font(None, 36)
            mode_text = mode_text_font.render("Select Game Mode:", True, WHITE)
            mode_text_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
            screen.blit(mode_text, mode_text_rect)

            # Draw difficulty buttons
            pygame.draw.rect(screen, ORANGE, (*EASY_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(screen, ORANGE, (*MEDIUM_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.rect(screen, ORANGE, (*HARD_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT))

            # Render button text
            easy_text = font.render("Easy", True, BLACK)
            medium_text = font.render("Medium", True, BLACK)
            hard_text = font.render("Hard", True, BLACK)

            screen.blit(easy_text, (EASY_BUTTON_POS[0] + 20, EASY_BUTTON_POS[1] + 15))
            screen.blit(medium_text, (MEDIUM_BUTTON_POS[0] + 10, MEDIUM_BUTTON_POS[1] + 15))
            screen.blit(hard_text, (HARD_BUTTON_POS[0] + 20, HARD_BUTTON_POS[1] + 15))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if the mouse click was within the button bounds
                if (EASY_BUTTON_POS[0] < mouse_x < EASY_BUTTON_POS[0] + BUTTON_WIDTH and
                        EASY_BUTTON_POS[1] < mouse_y < EASY_BUTTON_POS[1] + BUTTON_HEIGHT):
                    current_state = GAME_IN_PROGRESS
                    difficulty = EASY
                    # Start a new game with the selected difficulty

                elif (MEDIUM_BUTTON_POS[0] < mouse_x < MEDIUM_BUTTON_POS[0] + BUTTON_WIDTH and
                      MEDIUM_BUTTON_POS[1] < mouse_y < MEDIUM_BUTTON_POS[1] + BUTTON_HEIGHT):
                    current_state = GAME_IN_PROGRESS
                    difficulty = MEDIUM
                    # Start a new game with the selected difficulty

                elif (HARD_BUTTON_POS[0] < mouse_x < HARD_BUTTON_POS[0] + BUTTON_WIDTH and
                      HARD_BUTTON_POS[1] < mouse_y < HARD_BUTTON_POS[1] + BUTTON_HEIGHT):
                    current_state = GAME_IN_PROGRESS
                    difficulty = HARD
                    # Start a new game with the selected difficulty

        elif current_state == GAME_IN_PROGRESS:
            # Draw background
            screen.fill(WHITE)

            # Create Sudoku board
            sudoku_board = Board(9, 9, screen, difficulty)

            # Generate the Sudoku board
            generated_sudoku_board = generate_sudoku(9, 30)  # Adjust size and removed cells as needed


            # Draw Sudoku board
            sudoku_board.draw()

            # Draw bottom bar
            pygame.draw.line(screen, BLACK, (0, 500), (800, 500), 5)

            # Draw game buttons
            pygame.draw.rect(screen, ORANGE, (200, 525, 100, 50))
            pygame.draw.rect(screen, ORANGE, (350, 525, 100, 50))
            pygame.draw.rect(screen, ORANGE, (500, 525, 100, 50))

            # Render button text
            reset_text = font.render("Reset", True, BLACK)
            restart_text = font.render("Restart", True, BLACK)
            exit_text = font.render("Exit", True, BLACK)

            screen.blit(reset_text, (215, 540))
            screen.blit(restart_text, (358, 540))
            screen.blit(exit_text, (525, 540))

            # Handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if sudoku_board.selected_cell is not None:
                        selected_row = sudoku_board.selected_cell.row
                        selected_col = sudoku_board.selected_cell.col

                    # Handle button clicks
                    if 200 < mouse_x < 300 and 525 < mouse_y < 575:
                        # Handle reset button click
                        sudoku_board.reset()
                    elif 350 < mouse_x < 450 and 525 < mouse_y < 575:
                        # Handle restart button click
                        current_state = GAME_START
                    elif 500 < mouse_x < 600 and 525 < mouse_y < 575:
                        current_state = GAME_START  # Return to the main menu

            # Draw Sudoku board
            sudoku_board.draw()



        elif current_state == GAME_OVER:
            pass
        # Draw the game over screen
        # Display win or lose message and options to restart or exit

        pygame.display.flip()

    # Clean up and exit
    pygame.quit()


if __name__ == '__main__':
    main()
