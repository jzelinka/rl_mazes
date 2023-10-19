# Reinforcement learning in mazes

The presented mazes are probabilistic and thus the planning induces new set of challanges which can be solved using some reinforcement learning methods. Mazes contain walls `#`, start `S`, end `E` and delays `D`. Reaching the goal grants the agent a reward 200, hitting delay -50 and a step taken in the maze -1 as well. The agent can move in 4 directions and the probability of moving in the desired direction is 0.7. The probability of moving in the other directions is 0.15 and the agent can't move through walls and the delay.

```
7 7
#######
#S    #
###D# #
# #   #
#   ###
#    E#
#######
```

The maze and algorithms were implemented in `Python`. Necessary packages can be installed from `src/requirements.txt`. Experiments can be run using the `main.py` file in the `src` directory. It will test both implemented methods on a single maze, `maze-25-A2.txt`, to reduce the time needed to verify the implementation. The generated data is output in the `src/logs` directory, with more mazes in `src/dataset`.

Files `ffreplan.py` and `value_iteration.py` contain the methods for probabilistic planning, which handle the `Maze` object representing the maze Pepa has to navigate through.

### FFreplan
First plans a deterministic path using the A* algorithm and starts carrying it out. In case the agent behaves differently than the plan states, the plan is replanned again. This is repeated until the agent reaches the goal. FFreplan provides fast planning times and doesn't require many resources to initialize. However, the path taken by the agent is not optimal.

### Value iteration
The algorithm is based on the Bellman equation and is used to find the optimal policy for the agent. The policy is then used to navigate the agent through the maze. The algorithm needs a lot of resources in case of bigger mazes to propagate the updates through the entire maze. However, after successful learning the path taken by the agent is optimal.


_This project was created as an implementation of an assignment at CTU Prague._