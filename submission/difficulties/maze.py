import pygame
from pygame.sprite import Sprite
from random import shuffle
import Timer as Timer
import math


class Maze:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.keep_going = 1

        self.wall_thickness = 10  # Define thickness of the walls

        self.maze = {}
        for y in range(rows):
            for x in range(cols):
                cell = {'south': 1, 'east': 1, 'visited': 0}
                self.maze[(x, y)] = cell

    def generate(self, start_cell=None, stack=[]):
        if start_cell is None:
            start_cell = self.maze[(self.cols - 1, self.rows - 1)]

        if not self.keep_going:
            return

        self.check_finished()
        neighbors = []

        if len(stack) == 0:
            stack.append(start_cell)

        curr_cell = stack[-1]
        neighbors = self.get_neighbors(curr_cell)
        shuffle(neighbors)

        for neighbor in neighbors:
            if neighbor['visited'] == 0:
                neighbor['visited'] = 1
                stack.append(neighbor)
                self.knock_wall(curr_cell, neighbor)

                self.generate(start_cell, stack)

    def get_coords(self, cell):
        coords = (-1, -1)
        for k in self.maze:
            if self.maze[k] is cell:
                coords = (k[0], k[1])
                break
        return coords

    def get_neighbors(self, cell):
        neighbors = []

        (x, y) = self.get_coords(cell)
        if (x, y) == (-1, -1):
            return neighbors

        north = (x, y - 1)
        south = (x, y + 1)
        east = (x + 1, y)
        west = (x - 1, y)

        if north in self.maze:
            neighbors.append(self.maze[north])
        if south in self.maze:
            neighbors.append(self.maze[south])
        if east in self.maze:
            neighbors.append(self.maze[east])
        if west in self.maze:
            neighbors.append(self.maze[west])

        return neighbors

    def knock_wall(self, cell, neighbor):
        xc, yc = self.get_coords(cell)
        xn, yn = self.get_coords(neighbor)

        if xc == xn and yc == yn + 1:
            neighbor['south'] = 0
        elif xc == xn and yc == yn - 1:
            cell['south'] = 0
        elif xc == xn + 1 and yc == yn:
            neighbor['east'] = 0
        elif xc == xn - 1 and yc == yn:
            cell['east'] = 0

    def check_finished(self):
        done = 1
        for k in self.maze:
            if self.maze[k]['visited'] == 0:
                done = 0
                break
        if done:
            self.keep_going = 0

    def draw_maze(self, screen):
        wall_color = (0, 0, 255)  # Define color of the walls

        cell_width = screen.get_width() // self.cols
        cell_height = screen.get_height() // self.rows

        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.maze[(x, y)]

                # Draw walls for the cell
                if cell['south'] == 1:
                    pygame.draw.rect(maze_image, wall_color, (x * cell_width, y * cell_height + cell_height - self.wall_thickness, cell_width, self.wall_thickness))
                if cell['east'] == 1:
                    pygame.draw.rect(maze_image, wall_color, (x * cell_width + cell_width - self.wall_thickness, y * cell_height, self.wall_thickness, cell_height))





def gameover():
    None

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200,800))
    maze_image=pygame.Surface((1600,1600))
    pygame.display.set_caption("Maze")

    maze = Maze()
    maze.generate()
    timer = Timer.Timer(100)
    
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
            if event.type == pygame.USEREVENT + 1:
                if not paused :
                    timer.update()
        screen.fill((255, 255, 255))
        display_surface = pygame.Rect(0,0,1200,800)
        part_maze=maze_image.subsurface(display_surface)
        maze.draw_maze(maze_image)
        screen.blit(part_maze,(0,0))

        #timer

        text_rect = timer.timer_text.get_rect(center = (100,100))
        screen.blit(timer.timer_text, text_rect)
        if timer.counter > 60 :
            timer.drawArc(screen, (255, 255, 255), (100, 100), 90, 10, 2*math.pi*timer.counter/100)
        elif timer.counter >20:
            timer.drawArc(screen, (255,255, 0), (100, 100), 90, 10, 2*math.pi*timer.counter/100)
        else:
            timer.drawArc(screen, (255, 0, 0), (100, 100), 90, 10, 2*math.pi*timer.counter/100)

        if paused:
            # Display paused message
            font = pygame.font.Font(None, 36)
            text = font.render("Paused. Press SPACE to resume.", True, (255, 0, 0))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
        
    pygame.quit()
