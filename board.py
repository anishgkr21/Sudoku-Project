import pygame
import pygame.freetype
from sudoku_generator import *
from Cells import *

# Dimensions
width = 600
height = 600
cell_spacing = 60
group_size = 180
line = (40, 40, 40)

# Colors
olive = (128, 128, 0)
teal = (0, 128, 128)
yellow = (255, 255, 0)
purple = (128, 0, 128)
navy = (0, 0, 128)
silver = (192, 192, 192)


class Board:
    cells = {}
    
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.reset_rect = None
        self.restart_rect = None
        self.exit_rect = None
        self.board = generate_sudoku(9, self.difficulty)
        for columns in range(9):
            self.cells[columns] = {}
            for rows in range(9):
                self.cells[columns][rows] = Cell(f"{self.board[columns][rows]}", rows, columns, screen)
    def draw(self):
        for i in range(1, 3):
            pygame.draw.line(self.screen, "Blue", (0, group_size * i), (self.width, group_size * i), 6)
        for i in range(1, 9):
            pygame.draw.line(self.screen, "Blue", (0, cell_spacing * i), (self.width, cell_spacing * i), 2)

        for i in range(1, 3):
            pygame.draw.line(self.screen, "Blue", (group_size * i, 0), (group_size * i, self.height), 6)
        for i in range(1, 9):
            pygame.draw.line(self.screen, "Blue", (cell_spacing * i, 0), (cell_spacing * i, self.height), 2)

        pygame.draw.line(self.screen, (0, 125, 200), (0, group_size + 56 * 8), (self.width, group_size + 56 * 8), 6)


        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()
        button_font = pygame.freetype.Font("AovelSansRounded-rdDL.ttf", 30)

        reset_text = button_font.render("Reset", "black")
        restart_text = button_font.render("Restart", "black")
        exit_text = button_font.render("Exit", "black")

        reset_surface, rect = reset_text
        self.screen.blit(reset_surface, (35, 556))
        self.reset_rect = reset_surface.get_rect(center=(35, 556))

        restart_surface, rect = restart_text
        self.screen.blit(restart_surface, (194, 556))
        self.restart_rect = restart_surface.get_rect(center=(194, 556))

        exit_surface, rect = exit_text
        self.screen.blit(exit_surface, (390, 556))
        self.exit_rect = exit_surface.get_rect(center=(390, 556))

    def generate_board(self):
        self.board = generate_sudoku(9, self.difficulty)
        for x in range(9):
            for y in range(9):
                value = self.board[x][y]
                if value != 0:
                    self.cells[x][y].set_value(value)

    def draw_grid(self):
        for i in range(4):
            bold_line_width = 6 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, "Blue", (i * group_size, 0), (i * group_size, self.height),
                             bold_line_width)
            pygame.draw.line(self.screen, "Blue", (0, i * group_size), (self.width, i * group_size),
                             bold_line_width)


    def select(self, x, y):
        if self.selected_cell:
            self.selected_cell.unselect()
        self.selected_cell = self.cells[x][y]
        self.selected_cell.select()

    def click(self, x, y):
        x = y // cell_spacing
        y = x // cell_spacing
        if 0 <= x < 9 and 0 <= y < 9:
            return x, y
        else:
            return None

    def clear(self):
        if self.selected_cell and self.selected_cell.user_filled:
            self.selected_cell.clear()

    def sketch(self, value):
        if self.selected_cell:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.selected_cell.user_filled:
            self.selected_cell.set_value(value)

    def reset_to_original(self):
        for x in self.cells:
            for cell in x:
                if cell.original_value != 0:
                    cell.set_value(cell.original_value)
                else:
                    cell.clear()

    def is_full(self):
        for x in self.cells:
            for cell in x:
                if cell.value == "":
                    return False
        return True

    def update_board(self):
        for x in range(9):
            for y in range(9):
                self.board[x][y] = self.cells[x][y].value

    def find_empty(self):
        for x in range(9):
            for y in range(9):
                if self.cells[x][y].value == "":
                    return x, y
        return None

    def check_board(self):
        for i in range(9):
            if not self.valid_in_x(i) or not self.valid_in_y(i) or not self.valid_in_box(i):
                return False
        return True
    def update_value(self, row, col, num):
            self.cells[col][row].set_sketched_value(num)

