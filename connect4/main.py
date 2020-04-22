import numpy as np
import pygame
import sys


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


def create_board():
    return np.zeros((ROWS, COLS))


def drop_piece(r, c, piece):
    board[r][c] = piece


def is_valid_location(c):
    return board[ROWS-1][c] == 0


def get_next_open_row(c):
    for r in range(ROWS):
        if board[r][c] == 0:
            return r


def print_board():
    print(np.flip(board, 0))


def draw_board():
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int((c+0.5)*SQUARESIZE), int((r+1.5)*SQUARESIZE)), RADIUS)

    for c in range(COLS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int((c + 0.5) * SQUARESIZE), size[0]-int((r + 0.5) * SQUARESIZE)),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int((c + 0.5) * SQUARESIZE), size[0]-int((r + 0.5) * SQUARESIZE)),
                                   RADIUS)


def check_won(piece):
    # check horizontals
    for c in range(COLS-3):
        for r in range(ROWS):
            if min(board[r][c+i] == piece for i in range(4)) > 0:
                return True
    # check verticals
    for c in range(COLS):
        for r in range(ROWS-3):
            if min(board[r+i][c] == piece for i in range(4)) > 0:
                return True
    # check diagonals, up slope
    for c in range(COLS-3):
        for r in range(ROWS-3):
            if min(board[r+i][c+i] == piece for i in range(4)) > 0:
                return True
    # check diagonals, down slope slope
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if min(board[r - i][c + i] == piece for i in range(4)) > 0:
                return True
    # if no one has won...
    return False


ROWS, COLS = 6, 7
board = create_board()
game_over = False
turn = 0

pygame.init()
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2)-2
size = (ROWS+1)*SQUARESIZE, COLS*SQUARESIZE
screen = pygame.display.set_mode(size)
draw_board()
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 70)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            pygame.draw.rect(screen, BLACK, (0, 0, size[0], SQUARESIZE))
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            elif turn == 1:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            col = int(np.floor(event.pos[0]/SQUARESIZE))
            if is_valid_location(col):
                row = get_next_open_row(col)
                drop_piece(row, col, turn+1)
            turn = (turn+1) % 2
            draw_board()
            pygame.display.update()
            if check_won(1):
                label = myfont.render("Player one wins!", 1, RED)
                pygame.draw.rect(screen, BLACK, (0, 0, size[0], SQUARESIZE))
                screen.blit(label, (10, 10))
                pygame.display.update()
                game_over = True
            if check_won(2):
                label = myfont.render("Player two wins!", 1, YELLOW)
                pygame.draw.rect(screen, BLACK, (0, 0, size[0], SQUARESIZE))
                screen.blit(label, (10, 10))
                pygame.display.update()
                game_over = True
            if game_over:
                pygame.time.wait(3000)
