# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import utils.color as color
import random


# ######### class   ##########

# I NEED TO HAVE ONLY MAZE GENERATOR

idea = (color.BLACK, color.BLUE)

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
        self.check_maze()
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
                obj._color = color.PURPLE
                obj.entry = True
            if obj.coordinate == self.exit_maze:
                obj._color = color.PURPLE
                obj.exit = True
            print(obj._color, end="")
        self.check_maze()

    def check_maze(self):
        print("\n")
        for obj in self._all_cells:
            try:
                cell_x = obj.coordinate[0]
                cell_y = obj.coordinate[1]
                droite = self.ret_state((cell_x + 1, cell_y))
                bas = self.ret_state((cell_x, cell_y + 1))
                haut = self.ret_state((cell_x, cell_y - 1))
                print(f"IN OBJ cell ({cell_x},{cell_y}) ||"
                    f"\nRIGHT cell({cell_x + 1},{cell_y}) - East: {self.ret_state((cell_x + 1, cell_y))._stateE}, North: {self.ret_state((cell_x + 1, cell_y))._stateN}, South: {self.ret_state((cell_x + 1, cell_y))._stateS}, WEST: {self.ret_state((cell_x + 1, cell_y))._stateW}"
                    f"\nDOWN cell({cell_x},{cell_y + 1}) - East: {self.ret_state((cell_x, cell_y + 1))._stateE}, North: {self.ret_state((cell_x, cell_y + 1))._stateN}, South: {self.ret_state((cell_x, cell_y + 1))._stateS}, WEST: {self.ret_state((cell_x, cell_y + 1))._stateW}"
                    f"\nLEFT cell({cell_x - 1},{cell_y}) - East: {self.ret_state((cell_x - 1, cell_y))._stateE}, North: {self.ret_state((cell_x - 1, cell_y))._stateN}, South: {self.ret_state((cell_x - 1, cell_y))._stateS}, WEST: {self.ret_state((cell_x - 1, cell_y))._stateW}"
                    f"\nUP cell({cell_x},{cell_y - 1}) - East: {self.ret_state((cell_x, cell_y - 1))._stateE}, North: {self.ret_state((cell_x, cell_y - 1))._stateN}, South: {self.ret_state((cell_x, cell_y - 1))._stateS}, WEST: {self.ret_state((cell_x, cell_y - 1))._stateW}")
                    # obj._color = random.choice(idea)
            except AttributeError as e:
                print(f"error when checking : ({cell_x + 1},{cell_y}) ")
                continue

    def ret_state(self, coordinate: tuple):
        for obj in self._all_cells:
            if obj.coordinate == coordinate:
                return obj
