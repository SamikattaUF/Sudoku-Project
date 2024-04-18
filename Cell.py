from sudoku_generator import  *
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        cell_x = self.col * CELL_SIZE
        cell_y = self.row * CELL_SIZE
        cell_rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self.screen, WHITE, cell_rect, border_radius=6)
        # Draw cell's value or sketched value
        font = pygame.font.Font(None, 36)
        text_color = BLACK if self.value != 0 else (150, 150, 150)  # Gray for empty cells
        value = str(self.value) if self.value != 0 else str(self.sketched_value)
        text_surface = font.render(value, True, text_color)
        text_rect = text_surface.get_rect(center=cell_rect.center)

        self.screen.blit(text_surface, text_rect)
