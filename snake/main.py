import pygame
import random
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    global rows, width

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx, self.dirny = dirnx, dirny
        self.color = color
        self.rows = rows

    def move(self, dirnx, dirny):
        self.dirnx, self.dirny = dirnx, dirny
        if dirnx == -1 and self.pos[0] <= 0:
            self.pos = (rows - 1, self.pos[1])  # if going off left -> wrap
        elif dirnx == 1 and self.pos[0] >= rows - 1:
            self.pos = (0, self.pos[1])
        elif dirny == -1 and self.pos[1] <= 0:
            self.pos = (self.pos[0], rows - 1)
        elif dirny == 1 and self.pos[1] >= rows - 1:
            self.pos = (self.pos[0], 0)
        else:
            self.pos = (self.pos[0] + dirnx, self.pos[1] + dirny)


    def draw(self, surface, eyes=False):
        dis = width // rows
        i, j = self.pos

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis//2
            radius = 3
            circle_middle = (i*dis+centre-radius, j*dis+8)
            circle_middle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.dirnx = 1
        self.dirny = 0
        self.head = Cube(pos, dirnx=self.dirnx, dirny=self.dirny)
        self.body.append(self.head)


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.dirnx is not 1:
                self.dirnx, self.dirny = -1, 0
                self.turns[self.head.pos] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT] and self.dirnx is not -1:
                self.dirnx, self.dirny = 1, 0
                self.turns[self.head.pos] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP] and self.dirny is not 1:
                self.dirnx, self.dirny = 0, -1
                self.turns[self.head.pos] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN] and self.dirny is not -1:
                self.dirnx, self.dirny = 0, 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        turn_to_rem = None
        for i, seg in enumerate(self.body):
            if seg.pos in self.turns:
                if i == len(self.body)-1:
                    turn_to_rem = seg.pos
                seg.move(*self.turns[seg.pos])
            else:
                seg.move(seg.dirnx, seg.dirny)
        if turn_to_rem is not None:
            self.turns.pop(turn_to_rem)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 1
        self.dirny = 0

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    size_btwn = width // rows  # integer division

    x, y = (0, 0)
    for l in range(rows):
        x, y = (x + size_btwn, y + size_btwn)
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    global width, rows, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(item):
    global rows
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if max([z.pos == (x, y) for z in positions]) > 0:
            continue
        else:
            break
    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


if __name__ == "__main__":
    global width, rows, s, snack
    width = 400
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake(color=(255, 0, 0), pos=(10, 10))
    snack = Cube(random_snack(s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        clock.tick(15)  # max frames/s
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(s), color=(0, 255, 0))
        for i, seg in enumerate(s.body):
            if seg.pos in [seg2.pos for seg2 in s.body[i+1:]]:
                print(f"Score: {len(s.body)}")
                message_box("You Lost!", "Play again...")
                s.reset((10, 10))
                break

        redraw_window(win)
