from sudoku_generator import *
from Cell import  *
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
