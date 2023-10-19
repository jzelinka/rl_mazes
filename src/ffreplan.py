from queue import PriorityQueue
from maze import Maze
import logging

class ffreplan():
    def __init__(self, maze: Maze):
        self.maze = maze
        self.path = self.astar()

    def get_iterations(self):
        return 0
    
    def reset(self):
        # check if the maze was reset
        if not self.maze.at_the_start():
            logging.error("Maze was not reset.")
        self.path = self.astar()

    def heuristic(self, row, col):
        # Calculate the Manhattan distance heuristic from (row, col) to the goal
        return abs(row - self.maze.end_row) + abs(col - self.maze.end_col)
    
    def execute(self):
        reward = 0
        
        while self.path:
            move_goal = self.path.pop(0)
            direction = self.maze.next_to_direction(move_goal)
            reward += self.maze.move(direction)
            pos_after_move = self.maze.get_position() 

            if pos_after_move != move_goal:
                logging.debug("Replanning.")
                self.path = self.astar()
            
            if self.maze.goal_reached():
                logging.debug("Goal was reached.")
                break

        return reward

    def astar(self):
        open_set = PriorityQueue()
        open_set.put((0, self.maze.cur_row, self.maze.cur_col))

        came_from = {}
        g_score = {(row_i, col_i): float('inf') for row_i in range(len(self.maze.maze)) for col_i in range(len(self.maze.maze[row_i]))}
        g_score[(self.maze.cur_row, self.maze.cur_col)] = 0

        while not open_set.empty():
            _, current_row, current_col = open_set.get()

            if current_row == self.maze.end_row and current_col == self.maze.end_col:
                # Reconstruct the path and return it
                path = []
                pos = (current_row, current_col)
                while pos in came_from:
                    path.append(pos)
                    pos = came_from[pos]
                path.reverse()
                return path

            neighbors = [(current_row - 1, current_col), (current_row + 1, current_col),
                         (current_row, current_col - 1), (current_row, current_col + 1)]

            for neighbor_row, neighbor_col in neighbors:
                if (
                    neighbor_row < 0
                    or neighbor_row >= len(self.maze.maze)
                    or neighbor_col < 0
                    or neighbor_col >= len(self.maze.maze[0])
                    or self.maze.maze[neighbor_row][neighbor_col] == '#'
                    # or self.maze.maze[neighbor_row][neighbor_col] == 'D'
                ):
                    continue

                # handle guide the search from the delays with g score
                tentative_g_score = g_score[(current_row, current_col)] - self.maze.get_reward((neighbor_row, neighbor_col)) 

                if tentative_g_score < g_score[(neighbor_row, neighbor_col)]:
                    came_from[(neighbor_row, neighbor_col)] = (current_row, current_col)
                    g_score[(neighbor_row, neighbor_col)] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor_row, neighbor_col)
                    open_set.put((f_score, neighbor_row, neighbor_col))
