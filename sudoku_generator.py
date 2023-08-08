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
        self.box_length = row_length / 3

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


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = []
        self.INITIAL_CELLS = []
        self.selected_cell = None

        # Create cells for the board
        for row in range(9):
            cell_row = []
            for col in range(9):
                cell = Cell(0, row, col, self.screen)
                cell_row.append(cell)
            self.cells.append(cell_row)
            self.INITIAL_CELLS.append(cell_row)

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()

                # Draw thick lines to delineate 3x3 boxes
                if cell.row % 3 == 0 and cell.row != 0:
                    pygame.draw.line(self.screen, BLACK, (0, cell.row * CELL_SIZE), (cell.col * CELL_SIZE, cell.row * CELL_SIZE), 5)
                if cell.col % 3 == 0 and cell.col != 0:
                    pygame.draw.line(self.screen, BLACK, (cell.col * CELL_SIZE, 0), (cell.col * CELL_SIZE, cell.row * CELL_SIZE), 5)

    def select(self, row, col):
        self.selected_cell = self.cells[row][col]

    def click(self, x, y):
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < 9 and 0 <= col < 9:
            return row, col
        return None

    def clear(self):
        self.selected_cell.set_cell_value(0)
        self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        for row in self.cells:
            for cell in row:
                if cell.value != 0:
                    cell.set_cell_value(self.INITIAL_CELLS[cell.row][cell.col])

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        pass

    def find_empty(self):
        for row in self.cells:
            for cell in row:
                if self.cells[cell.row][cell.col].value == 0:
                    return cell.row, cell.col
        return None

    def check_board(self):
        for row in self.cells:
            for cell in row:
                if not SudokuGenerator.is_valid(cell.row, cell.col, self.cells[cell.row][cell.col].value):
                    return False
        return True
