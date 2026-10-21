# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import utils.color as color
import random
from utils.design import MAZE
from utils import error as err

random.seed()

# ######### class   ##########

# I NEED TO HAVE ONLY MAZE GENERATOR

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
        # generator.create_fortytwo()
        generator.print_maze()
        generator.backtracker()
        # generator.check_maze()
        print("\n\n")
        generator.print_maze()

    def get_entry(self) -> tuple:
        return self.entry


def chg_state(Cell):
    Cell.visit = True

def chgstateN(Cell):
    Cell.stateN = True



class CellGenerator(MazeGenerator):
    entry_maze = ()
    exit_maze = ()

    def __init__(self, x: int, y: int, width: int, height: int):
        self._color = "██"  # The color of the cell on the maze
        self.stateN = False  # True = Open | False = Wall
        self.stateE = False  # True = Open | False = Wall
        self.stateS = False  # True = Open | False = Wall
        self.stateW = False  # True = Open | False = Wall
        self.visit = False  # False = closed
        self.entry = False
        self.exit = False
        self.width = width
        self.height = height
        self.fortytwo = False
        self.coordinate = (x, y)
        self._all_cells = []
    
    def fill(self, entry_m: tuple[int, int], exit_m: tuple):
        self.entry_maze = entry_m
        self.exit_maze = exit_m

    def create(self):
        for i in range(self.width):
            for ii in range(self.height):
                new = CellGenerator(i, ii, self.width, self.height)
                self._all_cells.append(new)

    def update_fortytwo(self, coordinate: tuple):
        cell_forty = self.ret_cell(coordinate)
        if cell_forty:
            cell_forty.visit = True
            cell_forty.stateN = False
            cell_forty.stateE = False
            cell_forty.stateS = False
            cell_forty.stateW = False
            cell_forty.fortytwo = True

    def create_fortytwo(self) -> list:
        rows = 2 * self.height + 1
        cols = 2 * self.width + 1
        offset_row = (rows - 6) // 2
        offset_col = (cols - 7) // 2
        display = [
                    ["wall"] * rows
                    for _ in range(cols)
                ]
        if self.height < 3 or self.width < 3:
            return display
        # raise err.FortyTwoError("42 logo can not be displayed on a maze with x or y inferior to 3.")
        for i in range(3):
            display[3 + offset_row][i + offset_col] = "fortytwo"
            # self.update_fortytwo((3 + offset_row, i + offset_col))
            display[i + 1 + offset_row][6 + offset_col] = "fortytwo"
            # self.update_fortytwo((i + 1 + offset_row, 6 + offset_col))
            display[i + 3 + offset_row][4 + offset_col] = "fortytwo"
            # self.update_fortytwo((i + 3 + offset_row, 4 + offset_col))
            display[offset_row + 1][i + 4 + offset_col] = "fortytwo"
            # self.update_fortytwo((offset_row, i + 4 + offset_col))
            display[i + 1 + offset_row][offset_col] = "fortytwo"
        for i in range(1, 6):
            display[i + offset_row][2 + offset_col] = "fortytwo"
            # self.update_fortytwo((i + offset_row, 2 + offset_col))
        display[3 + offset_row][5 + offset_col] = "fortytwo"
        # self.update_fortytwo((3 + offset_row, 5 + offset_col))
        display[5 + offset_row][5 + offset_col] = "fortytwo"
        # self.update_fortytwo((5 + offset_row, 5 + offset_col))
        display[5 + offset_row][6 + offset_col] = "fortytwo"
        # self.update_fortytwo((5 + offset_row, 6 + offset_col))
        return display

    def print_maze(self):
        # create matrix - visualisation *3 - better
        # display = [
        #    ["wall"] * (2 * self.width + 1) 
        #     for _ in range(2 * self.height + 1)
        # ]
        display = self.create_fortytwo()
        # Test out the display
        for ligne in display:
            print("".join(MAZE[pixel] for pixel in ligne))
        print()
        # create the path
        for x in range(self.height):
            for y in range(self.width):
                cell = self.ret_cell((x, y))
                ligne = 2 * x + 1
                col = 2 * y + 1
                # open the middle part of the display
                if display[ligne][col] != "fortytwo" and display[ligne + 1][col] != "fortytwo" and display[ligne - 1][col] != "fortytwo":
                    display[ligne][col] = "path"
                    # open next cell if true
                    if cell.stateN and display[ligne - 1][col] != "fortytwo":
                        display[ligne - 1][col] = "path"
                    if cell.stateE and display[ligne][col + 1] != "fortytwo":
                        display[ligne][col + 1] = "path"
                    if cell.stateS and display[ligne + 1][col] != "fortytwo":
                        display[ligne + 1][col] = "path"
                    if cell.stateW and display[ligne][col - 1] != "fortytwo":
                        display[ligne][col - 1] = "path"
                else:
                    self.update_fortytwo((x, y))
        # start & end
        display[2 * self.entry_maze[0] + 1][2 * self.entry_maze[0] + 1] = "start"
        display[2 * self.exit_maze[0] + 1][2 * self.exit_maze[1] + 1] = "end"
        for ligne in display:
            print("".join(MAZE[pixel] for pixel in ligne))

# 1 Départ : Choisir une case au hasard. Marquer comme Visité.
# 2. Boucle : Tant qu'il reste des cases non visitées dans le labyrinthe :
#	• Regardez autour : Listez les cases voisines de la case actuelle (haut, bas, gauche, droite) qui sont encore Non visitées.
#	• Choix 1 : S'il y a des voisins non visités :
#		1. Choisissez-en un au hasard.
#		2. Abattez le mur entre la case actuelle et ce voisin choisi.
#		3. Ajoutez la case actuelle à la Pile.
#		4. Déplacez-vous sur le voisin, et marquez-le comme Visité.
#	• Choix 2 : Si tous les voisins sont déjà visités (Cul-de-sac) :
#		1. Sortez la dernière case de la Pile (on revient en arrière).
#		2. Cette case redevient votre case actuelle.

    def backtracker(self):
        # cell to start the maze generation
        current_cell = random.choice(self._all_cells)
        # current_cell = self.ret_cell(self.entry_maze)
        current_cell.visit = True
        # visited cell in list
        visited_stack = [current_cell]
        while len(visited_stack) > 0:
            try:
                cell_x = current_cell.coordinate[0]
                cell_y = current_cell.coordinate[1]
                # get info on cell next to current cell 
                lst_et = [
                    self.ret_cell((cell_x, cell_y + 1)),  # Right
                    self.ret_cell((cell_x + 1, cell_y)),  # Down
                    self.ret_cell((cell_x - 1, cell_y)),  # Up
                    self.ret_cell((cell_x, cell_y - 1))   # Left
                ]
                # filtered None return from next to current cell
                unvisited_ok_cell = [obj for obj in lst_et if obj is not None
                                     and not obj.visit]
                print(unvisited_ok_cell)
                if unvisited_ok_cell:
                    # 5. Choose a random unvisited neighbor to move to
                    next_cell = random.choice(unvisited_ok_cell)
                    # Breaking the Wall between cell
                    # define diff between x,y of current/next cell
                    d_x = next_cell.coordinate[0] - current_cell.coordinate[0]
                    d_y = next_cell.coordinate[1] - current_cell.coordinate[1]
                    if d_y == 1:  # This means moving East / Right
                        print("E")
                        current_cell.stateE = True
                        next_cell.stateW = True
                    elif d_y == -1:  # This means moving West / Left
                        print("W")
                        current_cell.stateW = True
                        next_cell.stateE = True
                    elif d_x == 1:  # This means moving South / Down
                        print("S")
                        current_cell.stateS = True
                        next_cell.stateN = True
                    elif d_x == -1:  # This means moving North / Up
                        print("N")
                        current_cell.stateN = True
                        next_cell.stateS = True
                    # 6. Push the current cell to the stack, move to next, mark visited
                    visited_stack.append(current_cell)
                    current_cell = next_cell
                    current_cell.visit = True
                else:
                    # This is a dead end
                    current_cell = visited_stack.pop()
            except ImportError:
                print("ERR")

    def ret_cell(self, coordinate: tuple):
        try:
            for obj in self._all_cells:
                if obj.coordinate == coordinate:
                    return obj
        except Exception:
            return None

    def ret_state(self, coordinate: tuple):
        for obj in self._all_cells:
            if obj.coordinate == coordinate:
                return obj.visit
        return None

    def ret_rdm(self):
        nbr = (1, 2, 3, 4)
        return random.choice(nbr)
