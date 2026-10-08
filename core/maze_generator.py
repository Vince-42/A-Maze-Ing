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

    def cell_gen(self):
        generator = CellGenerator(x=0, y=0)
        generator.create(5, 5)
        pass


class CellGenerator(MazeGenerator):
    def __init__(self, x: int, y: int):
        self._color = "#FFFFFFF"  # The color of the cell on the maze
        self._stateN = True  # True = Open | False = Wall
        self._stateE = True  # True = Open | False = Wall
        self._stateS = True  # True = Open | False = Wall
        self._stateW = True  # True = Open | False = Wall
        self.coordinate = (x, y)
        self._all_cells = []

    def create(self, x: int, y: int):
        count = 1
        for i in range(x):
            for ii in range(y):
                print(f"i={i} | ii={ii} | cell #{count}")
                count += 1
                new = CellGenerator(i, ii)
                self._all_cells.append(new)
        print("\n")
        for obj in self._all_cells:
            self.printing(obj.coordinate[0], obj.coordinate[1])
            # print(f"Cell located at coordinate : {obj.coordinate}.")
        print("\n")

    def printing(self, x: int, y: int):
        if x == 1 and y == 0 or x == 2 and y == 0 or x == 3 and y == 0 or x == 4 and y ==0:
            print("\n", end="")
        print("\u2588\u2588", end="")
