# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

# from utils import error

import numpy as np

# ######### class   ##########

class MazeGenerator():
    def __init__(self, conf: object):
        self.maze = conf
        self.entry = conf._entry
        self.exit = conf._exit

    def print_config(self):
        for i in self.maze.__dict__:
            print(i)
        print(f"Entry self = {self.entry}")
        print(f"Exit  self = {self.exit}")
        arr = np.array([[self.exit[0]], [self.exit[1]]])
        for case in arr:
            print(f"case {case[0][0]}")

        print(f"ARR = {arr[0][0]}")
        print(f"ARR = {arr[1][0]}")

        print(np.matrix(arr))
