# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

# from utils import error

import numpy as np

# ######### class   ##########

class MazeGenerator():
    def __init__(self, conf: object):
        self.maze = conf
        self._all_cells = []
        self.entry = conf._entry
        self.exit = conf._exit
        self.width = conf._width
        self.height = conf._height

    def print_config(self):
        print(f"\nEntry self = {self.entry}")
        print(f"Exit  self = {self.exit}")
        arr = np.array([[self.exit[0]], [self.exit[1]]])
        for case in arr:
            print(case)
        print(np.matrix(arr))

    def cell_gen(self):
        generator = CellGenerator(x=0,y=0)
        generator.create()
        pass


class CellGenerator(MazeGenerator):
    def __init__(self, x: int, y: int):
        self._color = "#FFFFFFF" # The color of the cell on the maze
        self._state = True # True = Open cell | False = Wall cell
        self._coordinate = (x, y)
        self._all_cells = []

    def create(self):
        for i in range(5):
            for ii in range(5):
                new = CellGenerator(i, ii)
                self._all_cells.append(new)

        for obj in self._all_cells:
            print(obj._coordinate)
