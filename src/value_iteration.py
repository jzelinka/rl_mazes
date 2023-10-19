from maze import Maze
import numpy as np
import logging

class ValueIteration():
    def __init__(self, maze: Maze, discount_factor=0.99999, epsilon=0.1):
        self.maze = maze
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.performed_iterations = -1
        self.value_function = self.value_iteration()
        self.optimal_policy = self.get_optimal_policy()
    
    def get_optimal_policy(self):
        num_rows, num_cols = self.value_function.shape

        optimal_policy = []

        for row in range(num_rows):
            optimal_policy.append([])
            for col in range(num_cols):
                if self.maze.maze[row][col] == '#':
                    # Wall cell, skip
                    optimal_policy[row].append('#') 
                else:
                    # Initialize the best action and its value
                    best_action = None
                    best_value = float('-inf')

                    for action in self.maze.get_actions():
                        value = 0
                        for p, (next_row, next_col) in self.maze.get_action_results(action, (row, col)):
                            reward = self.maze.get_reward((next_row, next_col))

                            # goal state terminates
                            if self.maze.is_goal((next_row, next_col)):
                                next_value = 0
                            elif self.maze.maze[next_row][next_col] == "#":
                                next_value = self.value_function[row][col]
                            else:
                                next_value = self.value_function[next_row][next_col]
                            value += p * (reward + self.discount_factor * next_value)

                        if value > best_value:
                            best_action = action
                            best_value = value

                    # Assign the best action to the optimal policy
                    optimal_policy[row].append(best_action) 

        return optimal_policy

    def value_iteration(self):
        num_rows = len(self.maze.maze)
        num_cols = len(self.maze.maze[0])

        # Initialize the value function
        value_function = np.zeros((num_rows, num_cols))

        self.performed_iterations = 0

        while True:
            delta = 0

            for row in range(num_rows):
                for col in range(num_cols):
                    if self.maze.maze[row][col] != '#':
                        max_value = float('-inf')

                        # get the surrounding fields
                        # working with deterministic actions so far
                        for action in self.maze.get_actions():
                            total = 0
                            for p, (next_row, next_col) in self.maze.get_action_results(action, (row, col)):
                                reward = self.maze.get_reward((next_row, next_col))

                                # goal state terminates
                                if self.maze.is_goal((next_row, next_col)):
                                    next_value = 0
                                # hit wall, not moving anywhere, getting my valuefunction
                                elif self.maze.maze[next_row][next_col] == "#":
                                    next_value = value_function[row][col]
                                else:
                                    next_value = value_function[next_row][next_col]
                                total += p * (reward + self.discount_factor * next_value)

                            # Update the maximum value
                            max_value = max(max_value, total)

                        # Update the value function
                        delta = max(delta, abs(max_value - value_function[row][col]))
                        value_function[row][col] = max_value
                self.performed_iterations += 1

            if self.performed_iterations % 100 == 0:
                print(f"\rPerformed iterations: {self.performed_iterations:8}, with delta {delta:.5f}", end="")

            if delta < self.epsilon:
                break
        print()
        return value_function

    def get_iterations(self):
        return self.performed_iterations

    def reset(self):
        # don't need reseting
        pass
    
    def execute(self):
        # use the optimal policy to reach the goal and collect the best rewards
        reward = 0
        
        while True:
            cur_row, cur_col = self.maze.get_position() 
            direction = self.optimal_policy[cur_row][cur_col]
            reward += self.maze.move(direction)
            
            if self.maze.goal_reached():
                logging.debug("Goal was reached.")
                break

        return reward