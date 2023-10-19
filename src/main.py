import logging
import random
import numpy as np
import os
import pandas as pd

from maze import Maze
from ffreplan import ffreplan
from value_iteration import ValueIteration
import experiments

num_rollouts = 200

def validate_single_maze(maze_path, alg_clas):
    """Runs algorithm multiple times to get information about the average rewards."""
    logging.info("Running validation for: %s", maze_path)
    rewards = np.zeros(num_rollouts)
    maze = Maze(maze_path)
    algorithm = alg_clas(maze)
    for i in range(num_rollouts):
        random.seed(i)
        maze.reset()
        algorithm.reset()
        rewards[i] = algorithm.execute()
        print(f"\rRollout: {i + 1}/{num_rollouts}", end="")
    print()
    return (np.average(rewards), algorithm.get_iterations())

def extract_number(fname):
    return int(fname.split('-')[1])

def validate_alg(dataset_path, out_folder, alg_name, alg):
    """Runs algorithm on each maze in dataset.
    Saves the average rewards into .csv file."""
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    mazes = list(filter(lambda maze: "maze" in maze,os.listdir(dataset_path)))
    mazes.sort(key=lambda x: int(x.split('-')[1]))
    logging.info("Getting rewards for algorithm %s", alg_name)
    results = list(map(lambda maze: validate_single_maze(os.path.join(dataset_path, maze), alg), mazes))
    all_rewards = list(map(lambda r: r[0], results))
    iters = list(map(lambda r: r[1], results))
    data = {'Maze file': mazes, 'Total Reward': all_rewards, 'Iterations': iters}
    df = pd.DataFrame(data)
    df.sort_values(by='Maze file')
    out_fname =os.path.join(out_folder, alg_name + ".csv")
    df.to_csv(out_fname, index=False)
    logging.info("Logs are saved to: %s", out_fname)
    logging.info("Finished validation.")

def compare_vi_and_shortest_path(dataset_path, out_folder):
    """Overlays policy of value iteration and shortest path to hightlight the differentces."""
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    mazes = list(filter(lambda maze: "maze" in maze,os.listdir(dataset_path)))
    for maze_fname in mazes:
        maze_name = os.path.splitext(maze_fname.split('/')[-1])[0]
        logging.info("Creating comparison of vi and shortest path for maze: %s", maze_name)
        maze = Maze(os.path.join(dataset_path, maze_fname), vis=True)
        maze.draw_maze()
        alg = ValueIteration(maze, discount_factor=1)
        maze.visualize_path(ffreplan(maze).path)
        maze.visualize_opt_policy(alg.optimal_policy)
        maze.save_vis(os.path.join(out_folder, maze_name + "_compare"))
        maze.window.destroy()


def show_ff_replan(dataset_path, out_folder):
    """Shows how ff_replan behaved on all mazes presented in a directory."""
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    mazes = list(filter(lambda maze: "maze" in maze,os.listdir(dataset_path)))
    for maze_fname in mazes:
        maze_name = os.path.splitext(maze_fname.split('/')[-1])[0]
        logging.info("Creating ffreplan showcase for maze: %s", maze_name)
        maze = Maze(os.path.join(dataset_path, maze_fname), vis=True)
        maze.draw_maze()
        maze.visualize_path(ffreplan(maze).path)
        alg = ffreplan(maze)
        alg.execute()
        maze.save_vis(os.path.join(out_folder, maze_name + "_ffreplan"))
        maze.window.destroy()

def mazes_vis(dataset_path, out_folder):
    """Prepare pictures of plain mazes."""
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    mazes = list(filter(lambda maze: "maze" in maze,os.listdir(dataset_path)))
    for maze_fname in mazes:
        maze_name = os.path.splitext(maze_fname.split('/')[-1])[0]
        logging.info("Creating maze pic: %s", maze_name)
        maze = Maze(os.path.join(dataset_path, maze_fname), vis=True)
        maze.draw_maze()
        maze.save_vis(os.path.join(out_folder, maze_name + "_maze_vis"))
        maze.window.destroy()
    

if __name__=="__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    dataset = "one_maze_test"

    show_ff_replan(dataset, "logs")

    compare_vi_and_shortest_path(dataset, "logs")

    # collects rewards for ffreplan
    validate_alg(dataset, 'logs', "ffreplan", ffreplan)

    # collects rewards for valueiteration
    validate_alg(dataset, 'logs', "async_vi", ValueIteration)

    vi = "logs/async_vi.csv"
    replan = "logs/ffreplan.csv"
    experiments.output_barplots(vi, replan, "logs/average_rewards.pdf")
