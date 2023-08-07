import random
import pygame

# Define variables
CELL_SIZE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = []
        for _ in range(row_length):
            row = [0] * row_length
            self.board.append(row)
        self.box_length = int(row_length ** 0.5)  # Square root of row_length

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(row)

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    def valid_in_col(self, col, num):
        return num not in [self.board[i][col] for i in range(self.row_length)]

    def valid_in_box(self, row_start, col_start, num):
        for i in range(self.box_length):
            for j in range(self.box_length):
                if self.board[row_start + i][col_start + j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (
                self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(row - row % self.box_length, col - col % self.box_length, num)
        )

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)

        num_index = 0
        for i in range(self.box_length):
            for j in range(self.box_length):
                self.board[row_start + i][col_start + j] = nums[num_index]
                num_index += 1

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        cells_to_remove = self.removed_cells
        while cells_to_remove > 0:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen

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


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = []
        self.selected_cell = None

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.value = generated_sudoku_board[cell.row][cell.col]
                cell.draw()
