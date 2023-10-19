import tkinter as tk
import random
from PIL import Image
import logging
import numpy as np

class Maze:
    def __init__(self, maze_name, vis=False):
        self.cell_size = 20
        self.maze_name = maze_name
        self.maze = []
        self.cur_row, self.cur_col = None, None
        self.start_row, self.start_col = None, None
        self.end_row, self.end_col = None, None
        self.__read_maze__()

        self.actions = ["left", "right", "up", "down"]

        self.vis = vis
        if self.vis:
            self.window = tk.Tk()
            self.canvas = tk.Canvas(self.window, width=len(self.maze[0]) * 20, height=len(self.maze) * 20)
            self.canvas.pack()
            self.draw_maze()
    
    def at_the_start(self):
        return self.start_col == self.cur_col and self.start_row == self.cur_row

    def __read_maze__(self):
        with open(self.maze_name, 'r') as file:
            file.readline()
            for row, line in enumerate(file):
                maze_row = list(line.strip())
                if 'S' in maze_row:
                    self.cur_row = row
                    self.cur_col = maze_row.index('S')
                    self.start_row = row
                    self.start_col = maze_row.index('S')
                if 'E' in maze_row:
                    self.end_row = row
                    self.end_col = maze_row.index('E')
                self.maze.append(maze_row)
    
    def reset(self):
        self.cur_col = self.start_col
        self.cur_row = self.start_row

    def draw_maze(self):
        if not self.vis:
            logging.error("Visualizing, you didn't wanted to.")
            return 

        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if self.maze[row][col] == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
                elif self.maze[row][col] == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')
                elif self.maze[row][col] == 'E':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                elif self.maze[row][col] == 'D':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='orange')

    def get_position(self):
        return (self.cur_row, self.cur_col)
    
    def goal_reached(self):
        return self.cur_row == self.end_row and self.cur_col == self.end_col

    def is_goal(self, pos):
        row, col = pos
        return row == self.end_row and col == self.end_col
    
    def get_surrounding_fields(self, pos):
        row, col = pos
        return [(row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col) ]

    def get_actions(self):
        return self.actions

    def get_action_results(self, action, pos):
        row, col = pos
        if action == "left":
            return [(0.7, (row, col - 1)), (0.15, (row + 1, col)), (0.15, (row - 1, col))]
        elif action == "right":
            return [(0.7, (row, col + 1)), (0.15, (row + 1, col)), (0.15, (row - 1, col))]
        elif action == "up":
            return [(0.7, (row - 1, col)), (0.15, (row, col + 1)), (0.15, (row, col - 1))]
        elif action == "down":
            return [(0.7, (row + 1, col)), (0.15, (row, col + 1)), (0.15, (row, col - 1))]
        else:
            return []

    def visualize_path(self, path):
        if not self.vis:
            logging.error("Visualizing, you didn't wanted to.")
            return 

        for row, col in path:
            x1 = col * self.cell_size + 3
            y1 = row * self.cell_size + 3
            x2 = x1 + self.cell_size - 6
            y2 = y1 + self.cell_size - 6
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='burlywood2')

    def save_vis(self, fname):
        if not self.vis:
            logging.error("Visualizing, you didn't wanted to.")
            return 

        self.canvas.update()
        post_script_fname = fname + '.ps'
        self.canvas.postscript(file=post_script_fname, colormode='color')
        image = Image.open(post_script_fname)
        image.save(fname + '.png', 'png')
    
    def next_to_direction(self, move):
        row, col = move
        # Check if the given position is adjacent to the current position
        if (row == self.cur_row and abs(col - self.cur_col) == 1) or \
                (col == self.cur_col and abs(row - self.cur_row) == 1):
            # Determine the direction based on the relative position
            if row < self.cur_row:
                return 'up'
            elif row > self.cur_row:
                return 'down'
            elif col < self.cur_col:
                return 'left'
            elif col > self.cur_col:
                return 'right'
        return None
    
    def get_reward(self, move):
        row, col = move
        if row == self.end_row and col == self.end_col:
            return 200
        elif self.maze[row][col] == 'D':
            return -50
        else:
            return -1
    
    def draw_arrow_in_pos(self, pos, direction, color):
        if not self.vis:
            logging.error("Visualizing, you didn't wanted to.")
            return 

        row, col = pos
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if direction == 'up':
            x1 += self.cell_size / 2
            y1 += self.cell_size
            x2 -= self.cell_size / 2
            y2 -= self.cell_size
        elif direction == 'down':
            x1 += self.cell_size / 2
            x2 -= self.cell_size / 2
        elif direction == 'left':
            x1 += self.cell_size
            y1 += self.cell_size / 2
            x2 -= self.cell_size
            y2 -= self.cell_size / 2
        elif direction == 'right':
            y1 += self.cell_size / 2
            y2 -= self.cell_size / 2

        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color)
    
    def draw_move(self, direction, succesfull):
        if succesfull:
            color = "black"
        else:
            color = "red"
        self.draw_arrow_in_pos((self.cur_row, self.cur_col), direction, color)
    
    def visualize_opt_policy(self, optimal_policy):
        num_rows = len(optimal_policy)
        num_cols = len(optimal_policy[0])
        if len(self.maze) == num_rows and len(self.maze[0]) == num_cols:
            for row in range(num_rows):
                for col in range(num_cols):
                    if optimal_policy[row][col] == "#":
                        continue
                    self.draw_arrow_in_pos((row, col), optimal_policy[row][col], color="black")
            # show the astar path
        else:
            logging.error("Optimal policy and maze don't have the same dimensions.")

    def move(self, direction):
        row, col = self.cur_row, self.cur_col
        
        successful = False
        if random.random() < 0.7:  # Move in the given direction
            successful = True
            if direction == 'up':
                row -= 1
            elif direction == 'down':
                row += 1
            elif direction == 'left':
                col -= 1
            elif direction == 'right':
                col += 1
        elif random.random() < 0.5:  # Move left
            if direction == 'up':
                col -= 1
            elif direction == 'down':
                col += 1
            elif direction == 'left':
                row += 1
            elif direction == 'right':
                row -= 1
        else:  # Move right
            if direction == 'up':
                col += 1
            elif direction == 'down':
                col -= 1
            elif direction == 'left':
                row -= 1
            elif direction == 'right':
                row += 1

        if self.vis:
            self.draw_move(self.next_to_direction((row, col)), successful)
        
        if (
            row < 0
            or row >= len(self.maze)
            or col < 0
            or col >= len(self.maze[0])
            or self.maze[row][col] == '#'
        ):
            logging.debug("Wall was hit.")
            return -1

        self.cur_row, self.cur_col = row, col

        return self.get_reward((row, col))
