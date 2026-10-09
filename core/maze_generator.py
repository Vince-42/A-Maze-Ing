# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import utils.color as color


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
        generator = CellGenerator(0, 0, width=self.width, height=self.height)
        generator.fill(self.entry, self.exit)
        generator.create()
        generator.print_maze()

        pass

    def get_entry(self) -> tuple:
        return self.entry

class CellGenerator(MazeGenerator):
    entry_maze = ()
    exit_maze = ()

    def __init__(self, x: int, y: int, width: int, height: int):
        self._color = "██"  # The color of the cell on the maze
        self._stateN = False  # True = Open | False = Wall
        self._stateE = False  # True = Open | False = Wall
        self._stateS = False  # True = Open | False = Wall
        self._stateW = False  # True = Open | False = Wall
        self.entry = False
        self.exit = False
        self.width = width
        self.height = height
        self.coordinate = (x, y)
        self._all_cells = []

    def fill(self, entry_m: tuple[int, int], exit_m: tuple):
        self.entry_maze = entry_m
        self.exit_maze = exit_m
        print(f"entry {self.entry_maze} | exit {self.exit_maze}")
        pass

    def create(self):
        # count = 1
        for i in range(self.width):
            for ii in range(self.height):
                # print(f"i={i} | ii={ii} | cell #{count}")
                # count += 1
                new = CellGenerator(i, ii, self.width, self.height)
                self._all_cells.append(new)

    def print_maze(self):
        for obj in self._all_cells:
            if obj.coordinate[1] == 0:
                obj._stateE = True
                obj._color = color.BLACK
                print("\n", end="")
            elif obj.coordinate[0] == 0:
                obj._color = color.BLACK
                obj._stateS = True
            elif obj.coordinate[0] == obj.width - 1:
                obj._stateN = True
                obj._color = color.BLACK
            elif obj.coordinate[1] == obj.width - 1:
                obj._color = color.BLACK
                obj._stateW = True
            # print(f"obj coordinate {type(obj.coordinate[0])} | obj entry {type(self.entry_maze[0])}")
            if obj.coordinate == self.entry_maze:
                obj._color = color.BLUE
                obj.entry = True
            if obj.coordinate == self.exit_maze:
                obj._color = color.BLUE
                obj.entry = True
            print(obj._color, end="")