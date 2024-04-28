from pygame import *
import sys
from sudoku_generator import generate_sudoku
from Cells import Cell
from board import Board
from board import *

running = True
# Dimensions
width = 600
height = 600
cell_spacing = 60
group_size = 180
line = (40, 40, 40)

# colors
olive = (128, 128, 0)
teal = (0, 128, 128)
yellow = (255, 255, 0)
purple = (128, 0, 128)
navy = (0, 0, 128)
silver = (192, 192, 192)

board = generate_sudoku(9, 30)



def main_screen(screen):

    game_screen = 0

    screen.fill(olive)

    if game_screen == 0:
        pygame.draw.rect(screen, yellow, pygame.Rect(0, 540, 599, 60))
        pygame.draw.rect(screen, teal, pygame.Rect(0, 540, 599, 60), width=6)
        pygame.draw.line(screen, teal, (179,540), (179, 599),width=4)
        pygame.draw.line(screen, teal, (359,540), (359, 599),width=4)
        pygame.draw.line(screen, teal, (537,540), (537, 599),width=4)

        title_font = pygame.freetype.Font("AovelSansRounded-rdDL.ttf", 100)
        title_surface, rect = title_font.render("Sudoku", purple)

        screen.blit(title_surface, (40, 200))
        title_font2 = pygame.freetype.Font("AovelSansRounded-rdDL.ttf", 30)
        button_font = pygame.freetype.Font("AovelSansRounded-rdDL.ttf", 35)
        title_surface2, rect = title_font2.render("Select Game Mode", purple)

        center = width // 2, height // 2
        screen.blit(title_surface2, (85, 450))
        easy_text = button_font.render("Easy", teal)
        medium_text = button_font.render("Medium", teal)
        hard_text = button_font.render("Hard", teal)

        easy_surface, easy_rect = easy_text
        screen.blit(easy_surface, (35, 556))
        medium_surface, medium_rect = medium_text
        screen.blit(medium_surface, (194, 556))
        hard_surface, hard_rect = hard_text
        screen.blit(hard_surface, (390, 556))

        easy_rectangle = easy_surface.get_rect(center=(35, 556))
        medium_rectangle = medium_surface.get_rect(center=(194, 556))
        hard_rectangle = hard_surface.get_rect(center=(390, 556))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rectangle.collidepoint(event.pos):
                        return 30
                    elif medium_rectangle.collidepoint(event.pos):
                        return 40
                    elif hard_rectangle.collidepoint(event.pos):
                        return 50
            pygame.display.update()

def winner_screen(screen):
    screen.fill(navy)
    font = pygame.freetype.Font("AovelSansRounded-rdDL.ttf", 100)
    winner_surface, rect = font.render("WIN", purple)
    screen.blit(winner_surface, (40, 200))
def loser_screen(screen):
    screen.fill(navy)
    font = pygame.freetype.Font("AovelSansRounded-rdDL.ttf", 100)
    loser_surface, rect = font.render("LOSE", purple)
    screen.blit(loser_surface, (40, 200))
def check_if_winner(screen, board):
    if_win = True
    for rows in range(9):
        for columns in range(9):
            board.board[rows][columns] = 0
            if not board.is_valid(rows, columns, board.cells[rows][columns].sketch_value):
                if_win = False
            board.board[rows][columns] = board.cells[rows][columns].sketch_value
            if board.cells[rows][columns].value == "0" and board.cells[rows][columns].sketch_value == 0:
                if_win = False
    if if_win:
        winner_screen(screen)
    else:
        loser_screen(screen)
def sudo_buttons(board, screen, event, difficulty):
    result = True
    if board.reset_rect.collidepoint(event.pos):
        screen.fill(teal)
        board = Board(width, height, screen, difficulty)
        board.draw()
        pygame.display.update()
    elif board.restart_rect.collidepoint(event.pos):
        main()
    elif board.exit_rect.collidepoint(event.pos):
        sys.exit()
    else:
        result = False
    return [result, board]
def set_value(board, rows, columns, key):
    board.update_value(rows, columns, key)
    board.board[rows][columns] = key
def main():
    pygame.init()
    pygame.display.set_caption("Sudoku Game")
    screen = pygame.display.set_mode(([width, height]))
    num_removed_cell = main_screen(screen)
    screen.fill((81, 75, 35))

    board = Board(width, height, screen, num_removed_cell)
    board.draw()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    check_if_winner(screen, board)
                    break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons = sudo_buttons(board, screen, event, num_removed_cell)
                board = buttons[1]
                if not buttons[0]:
                    for rows in board.cells:
                        for columns in board.cells[rows]:
                            if board.cells[rows][columns].value_rect.collidepoint(event.pos):
                                go = True
                                while go:
                                    board.cells[rows][columns].enable_selection()
                                    for event2 in pygame.event.get():
                                        if event2.type == pygame.KEYDOWN:
                                            if event2.key == pygame.K_DOWN:
                                                board.cells[rows][columns].disable_selection()
                                                columns += 1 if columns != 8 else 0
                                            elif event2.key == pygame.K_UP:
                                                board.cells[rows][columns].disable_selection()
                                                columns -= 1 if columns != 0 else 0
                                            elif event2.key == pygame.K_RIGHT:
                                                board.cells[rows][columns].disable_selection()
                                                rows += 1 if rows != 8 else 0
                                            elif event2.key == pygame.K_LEFT:
                                                board.cells[rows][columns].disable_selection()
                                                rows -= 1 if rows != 0 else 0
                                            elif pygame.K_1 <= event2.key <= pygame.K_9:
                                                set_value(board, rows, columns, event2.key - pygame.K_0)
                                                go = False
                                                break
                                        if event2.type == pygame.QUIT:
                                            sys.exit()
                                        if event2.type == pygame.MOUSEBUTTONDOWN:
                                            board = sudo_buttons(board, screen, event2, num_removed_cell)[1]
                                    board.draw()  # Update display after making changes
                                board.cells[rows][columns].disable_selection()

        pygame.display.update()

if __name__ == "__main__":
    main()