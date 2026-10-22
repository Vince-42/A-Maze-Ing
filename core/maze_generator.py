# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import utils.color as color
import random
from utils.design import MAZE
from utils import error as err

# ######### class   ##########

# I NEED TO HAVE ONLY MAZE GENERATOR

class MazeGenerator():
    def __init__(self, conf: object):
        self.maze = conf
        self.entry = conf._entry
        self.exit = conf._exit
        self.width = conf._width
        self.height = conf._height
        self.output_name = conf._output_file
        self.perfect = conf._perfect
        self.output_txt = ""

    def cell_gen(self):
        generator = CellGenerator(0, 0, width=self.width, height=self.height)
        generator.fill(self.entry, self.exit)
        generator.create()
        generator.print_maze(False)
        # create a IF here if perfect backtracker if not perfect UNPERFECT algo.
        if self.perfect:
            generator.backtracker()
        else:
            generator.backtracker_imperfect()
        print("\n\n")
        generator.print_maze(True)
        self.output_txt = generator.print_data(self.output_name)
        
        ## Call your Maze Solver Class / Method from HERE
        return generator

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
        self.blocked = False
        self.coordinate = (x, y)
        self._all_cells = []
        self.solution = False

    
    def fill(self, entry_m: tuple[int, int], exit_m: tuple):
        self.entry_maze = entry_m
        self.exit_maze = exit_m

    def create(self):
        for i in range(self.height):
            for ii in range(self.width):
                new = CellGenerator(ii, i, self.width, self.height)
                self._all_cells.append(new)
    
    def print_data(self, file: str) -> str:
        count = 0
        maze_heza = ""
        for height in range(self.height):
            for width in range(self.width):
                current_cell = self.ret_cell((width,height))
                if count == self.width:
                    maze_heza += "\n"
                    count = 0
                sn = 0 if current_cell.stateN else 1
                se = 0 if current_cell.stateE else 1
                ss = 0 if current_cell.stateS else 1
                sw = 0 if current_cell.stateW else 1
                str_bi = str(sn) + str(se) + str(ss) + str(sw)
                hexa = int(str_bi, 2)
                maze_heza += f"{hexa:x}"
                count += 1
        maze_heza += "\n\n"
        data_entry = str(self.entry_maze).replace("(", "")
        maze_heza += f"{data_entry.replace(")", "")}"
        maze_heza += "\n"
        data_exit = str(self.exit_maze).replace("(", "")
        maze_heza += f"{data_exit.replace(")", "")}"
        with open(file, "w") as f:
            print(maze_heza, file=f)
        return maze_heza

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
        offset_row = (cols - 6) // 2
        offset_col = (rows - 7) // 2
        display = [
            ["wall"] * rows
            for _ in range(cols)
                ]
        if self.height <= 7 or self.width <= 7:
            return display
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

    def print_maze(self, printing: bool):
        display = self.create_fortytwo()
        # create the path
        for x in range(self.width):
            for y in range(self.height):
                cell = self.ret_cell((x, y))
                ligne = 2 * x + 1
                col = 2 * y + 1
                # open the middle part of the displays
                if display[ligne][col] != "fortytwo" and\
                    display[ligne + 1][col] != "fortytwo" and\
                    display[ligne - 1][col] != "fortytwo":
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
                    if self.entry_maze == ((x,y)) or self.exit_maze == ((x,y)):
                        raise err.FortyTwoError("entry within 42 logo.")

        # start & end
        display[2 * self.entry_maze[0] + 1][2 * self.entry_maze[1] + 1] = "start"
        display[2 * self.exit_maze[0] + 1][2 * self.exit_maze[1] + 1] = "end"
        if printing:
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
        while current_cell.fortytwo is True:
            current_cell = random.choice(self._all_cells)
        # print(f"Coordinate Starting Maze Cell : {current_cell.coordinate}")
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
                if unvisited_ok_cell:
                    # 5. Choose a random unvisited neighbor to move to
                    next_cell = random.choice(unvisited_ok_cell)
                    # Breaking the Wall between cell
                    # define diff between x,y of current/next cell
                    d_x = next_cell.coordinate[0] - current_cell.coordinate[0]
                    d_y = next_cell.coordinate[1] - current_cell.coordinate[1]
                    if d_y == 1:  # This means moving East / Right
                        current_cell.stateE = True
                        next_cell.stateW = True
                    elif d_y == -1:  # This means moving West / Left
                        current_cell.stateW = True
                        next_cell.stateE = True
                    elif d_x == 1:  # This means moving South / Down
                        current_cell.stateS = True
                        next_cell.stateN = True
                    elif d_x == -1:  # This means moving North / Up
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

    def imperfect_helper(self):
        current_cell = random.choice(self._all_cells)
        while current_cell.fortytwo is True or current_cell.blocked is True:
            current_cell = random.choice(self._all_cells)
        current_cell.blocked = True
        cell_x = current_cell.coordinate[0]
        cell_y = current_cell.coordinate[1]
        # get info on cell next to current cell 
        lst_et = [
            self.ret_cell((cell_x, cell_y + 1)),  # Right
            self.ret_cell((cell_x + 1, cell_y)),  # Down
            self.ret_cell((cell_x - 1, cell_y)),  # Up
            self.ret_cell((cell_x, cell_y - 1))   # Left
                        ]
        unvisited_ok_cell = [obj for obj in lst_et if obj is not None]
        if unvisited_ok_cell:
            next_cell = random.choice(unvisited_ok_cell)
            d_x = next_cell.coordinate[0] - current_cell.coordinate[0]
            d_y = next_cell.coordinate[1] - current_cell.coordinate[1]
            if d_y == 1:  # This means moving East / Right
                current_cell.stateE = True
                next_cell.stateW = True
            elif d_y == -1:  # This means moving West / Left
                current_cell.stateW = True
                next_cell.stateE = True
            elif d_x == 1:  # This means moving South / Down
                current_cell.stateS = True
                next_cell.stateN = True
            elif d_x == -1:  # This means moving North / Up
                current_cell.stateN = True
                next_cell.stateS = True
            next_cell.blocked = True
    
    def backtracker_imperfect(self):
        # cell to start the maze generation
        current_cell = random.choice(self._all_cells)
        while current_cell.fortytwo is True:
            current_cell = random.choice(self._all_cells)
        current_cell.visit = True
        visited_stack = [current_cell]
        while len(visited_stack) > 0:
            try:
                cell_x = current_cell.coordinate[0]
                cell_y = current_cell.coordinate[1]
                lst_et = [
                    self.ret_cell((cell_x, cell_y + 1)),  # Right
                    self.ret_cell((cell_x + 1, cell_y)),  # Down
                    self.ret_cell((cell_x - 1, cell_y)),  # Up
                    self.ret_cell((cell_x, cell_y - 1))   # Left
                ]
                unvisited_ok_cell = [obj for obj in lst_et if obj is not None
                                     and not obj.visit]
                if unvisited_ok_cell:
                    next_cell = random.choice(unvisited_ok_cell)
                    d_x = next_cell.coordinate[0] - current_cell.coordinate[0]
                    d_y = next_cell.coordinate[1] - current_cell.coordinate[1]
                    if d_y == 1:  # This means moving East / Right
                        current_cell.stateE = True
                        next_cell.stateW = True
                    elif d_y == -1:  # This means moving West / Left
                        current_cell.stateW = True
                        next_cell.stateE = True
                    elif d_x == 1:  # This means moving South / Down
                        current_cell.stateS = True
                        next_cell.stateN = True
                    elif d_x == -1:  # This means moving North / Up
                        current_cell.stateN = True
                        next_cell.stateS = True
                    visited_stack.append(current_cell)
                    current_cell.visit = True
                    current_cell = next_cell
                    current_cell.visit = True
                else:
                    current_cell = visited_stack.pop()
            except ImportError:
                print("ERR")
        for _ in range((self.width * self.height) // 2):
            self.imperfect_helper()

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

    def get_all_cells(self):
        return self._all_cells
