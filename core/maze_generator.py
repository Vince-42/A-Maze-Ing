# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import random
import time
from utils.design import MAZE
from utils import error as err
from core.maz_solver import MazSolver
# from a_maze_ing import counter_sleep

# ######### class   ##########



class MazeGenerator():
    counter_time = 0
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
        generator.print_maze(False, False)
        if self.perfect:
            generator.backtracker()
        else:
            generator.backtracker_imperfect()
        print("\n\n")
        # returning maze txt in var
        self.output_txt = generator.print_data(self.output_name)
        solver = MazSolver(
            generator.get_all_cells(),
            generator.entry_maze,
            generator.exit_maze
        )
        generator.solution_path = solver.solve()
        for coordinate in generator.solution_path:
            generator.ret_cell(coordinate).solution = True
        # Print maze with solution true
        generator.print_maze(True, False)

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
        self.imperfect_help = False
    def fill(self, entry_m: tuple[int, int], exit_m: tuple):
        self.entry_maze = entry_m
        self.exit_maze = exit_m

    def create(self):
        for x in range(self.width):
            for y in range(self.height):
                new = CellGenerator(x, y, self.width, self.height)
                self._all_cells.append(new)

    def print_data(self, file: str) -> str:
        count = 0
        maze_heza = ""
        for height in range(self.height):
            for width in range(self.width):
                current_cell = self.ret_cell((width, height))
                if count == self.width:
                    maze_heza += "\n"
                    count = 0
                sn = 0 if current_cell.stateN else 1
                se = 0 if current_cell.stateE else 1
                ss = 0 if current_cell.stateS else 1
                sw = 0 if current_cell.stateW else 1
                str_bi = str(sw) + str(ss) + str(se) + str(sn)
                hexa = int(str_bi, 2)
                maze_heza += f"{hexa:x}"
                count += 1
        maze_heza += "\n\n"
        data_entry = str(self.entry_maze).replace("(", "")
        # maze_heza += f"{data_entry.replace(")", "")}"
        maze_heza += data_entry.replace(")", "")
        maze_heza += "\n"
        data_exit = str(self.exit_maze).replace("(", "")
        # maze_heza += f"{data_exit.replace(")", "")}"
        maze_heza += data_exit.replace(")", "")
        with open(file, "w") as f:
            print(maze_heza, file=f)
        return maze_heza

    def update_fortytwo(self, coordinate: tuple):
        cell_forty = self.ret_cell(coordinate)
        if cell_forty:
            cell_x = cell_forty.coordinate[0]
            cell_y = cell_forty.coordinate[1]
            # get info on cell next to current cell
            lst_et = [
                    self.ret_cell((cell_x, cell_y + 1)),  # Right
                    self.ret_cell((cell_x + 1, cell_y)),  # Down
                    self.ret_cell((cell_x - 1, cell_y)),  # Up
                    self.ret_cell((cell_x, cell_y - 1))   # Left
            ]
            cell_forty.visit = True
            cell_forty.fortytwo = True
            ok_cell = [obj for obj in lst_et if obj is not None]
            count = 0
            for cell in ok_cell:
                # TO BE CHECKED HERE
                # cell.blocked = True
                cell.fortytwo = True
                if count > 0:
                    pass
                    # cell.visit = True
                count += 1

    def create_fortytwo(self) -> list:
        rows = 2 * self.height + 1
        cols = 2 * self.width + 1
        offset_row = (rows - 6) // 2
        offset_col = (cols - 7) // 2
        display = [
            ["wall"] * cols
            for _ in range(rows)
                ]
        if self.height <= 7 or self.width <= 7:
            return display
        for i in range(3):
            # Barre 4
            display[2 + offset_row][i + offset_col] = "fortytwo"
            # Barres 2
            display[offset_row][i + 4 + offset_col] = "fortytwo"
            display[2 + offset_row][i + 4 + offset_col] = "fortytwo"
            display[4 + offset_row][i + 4 + offset_col] = "fortytwo"
        # Partie gauche du 4
        for i in range(0, 3):
            display[i + offset_row][offset_col] = "fortytwo"
        # Partie droite du 4
        for i in range(5):
            display[i + offset_row][2 + offset_col] = "fortytwo"
        # Parties verticales du 2
        display[1 + offset_row][6 + offset_col] = "fortytwo"
        display[3 + offset_row][4 + offset_col] = "fortytwo"
        return display

    def create_fortytwo2(self) -> list:
        rows = 2 * self.height + 1
        cols = 2 * self.width + 1
        offset_row = (rows - 6) // 2
        offset_col = (cols - 7) // 2
        display = [
            ["wall"] * cols
            for _ in range(rows)
                ]
        if self.height <= 7 or self.width <= 7:
            return display
        # quatre
        # haut
        display[offset_row + 2][offset_col] = "fortytwo"
        display[offset_row + 1][offset_col] = "fortytwo"
        display[offset_row][offset_col] = "fortytwo"
        # middle middle
        display[offset_row + 2][offset_col + 1] = "fortytwo"
        display[offset_row + 2][offset_col + 2] = "fortytwo"
        display[offset_row + 3][offset_col + 2] = "fortytwo"
        display[offset_row + 4][offset_col + 2] = "fortytwo"
        # bassolution
        # deux
        # haut gauche
        display[offset_row][offset_col + 6] = "fortytwo"
        display[offset_row + 2][offset_col + 6] = "fortytwo"
        display[offset_row + 4][offset_col + 6] = "fortytwo"
        # bas gauche
        # haut droite
        display[offset_row][offset_col + 8] = "fortytwo"
        display[offset_row + 2][offset_col + 8] = "fortytwo"
        display[offset_row + 4][offset_col + 8] = "fortytwo"
        # bas droite
        # middle haut
        display[offset_row][offset_col + 7] = "fortytwo"
        # droite middle
        display[offset_row + 1][offset_col + 8] = "fortytwo"
        # middle middle
        display[offset_row + 2][offset_col + 7] = "fortytwo"
        # gauche middle
        display[offset_row + 3][offset_col + 6] = "fortytwo"
        # middle bas
        display[offset_row + 4][offset_col + 7] = "fortytwo"
        return display

    def print_maze(self, printing: bool, solution: bool):
        display = self.create_fortytwo2()
        # create the path
        for x in range(self.width):
            for y in range(self.height):
                cell = self.ret_cell((x, y))
                ligne = 2 * y + 1
                col = 2 * x + 1
                # print(f"cell {x},{y}")
                if solution:
                    if (cell.solution == True):
                        display[ligne][col] = "solution"
                        if cell.stateN and display[ligne - 1][col] == "wall":
                            display[ligne - 1][col] = "solution"
                        if cell.stateE and display[ligne][col + 1] == "wall":
                            display[ligne][col + 1] = "solution"
                        if cell.stateS and display[ligne + 1][col] == "wall":
                            display[ligne + 1][col] = "solution"
                        if cell.stateW and display[ligne][col - 1] == "wall":
                            display[ligne][col - 1] = "solution"
                        continue

                # open the middle part of the displays
                if display[ligne][col] == "fortytwo" or\
                    display[ligne - 1][col] == "fortytwo" or\
                        display[ligne][col + 1] == "fortytwo":
                    if not printing:
                        self.update_fortytwo((x, y))
                    if (
                        self.entry_maze == ((x, y))
                        or self.exit_maze == ((x, y))
                    ):
                        raise err.FortyTwoError("entry within 42 logo.")
                else:
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
        # start & end
        display[2 * self.entry_maze[1] + 1][2 * self.entry_maze[0] + 1] = \
            "start"
        display[2 * self.exit_maze[1] + 1][2 * self.exit_maze[0] + 1] = "end"
        if printing:
            for ligne in display:
                print("".join(MAZE[elem] for elem in ligne))
<<<<<<< HEAD
                time.sleep(0.1)
=======
                time.sleep(MazeGenerator.counter_time)
>>>>>>> 3dec980e52c73586e27f163825c6b1c4a8390f41

# 1 Départ : Choisir une case au hasard. Marquer comme Visité.
# 2. Boucle : Tant qu'il reste des cases non visitées dans le labyrinthe :
# • Regardez autour : Listez les cases voisines de la case actuelle
# (haut, bas, gauche, droite) qui sont encore Non visitées.
# • Choix 1 : S'il y a des voisins non visités :
# 1. Choisissez-en un au hasard.
# 2. Abattez le mur entre la case actuelle et ce voisin choisi.
# 3. Ajoutez la case actuelle à la Pile.
# 4. Déplacez-vous sur le voisin, et marquez-le comme Visité.
# • Choix 2 : Si tous les voisins sont déjà visités (Cul-de-sac) :
# 1. Sortez la dernière case de la Pile (on revient en arrière).
# 2. Cette case redevient votre case actuelle.

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
                    if d_y == 1:  # This means moving SOUTH / BAS
                        current_cell.stateS = True
                        next_cell.stateN = True
                    elif d_y == -1:  # This means moving NORD / UP
                        current_cell.stateN = True
                        next_cell.stateS = True
                    elif d_x == 1:  # This means moving EAST / DROITE
                        current_cell.stateE = True
                        next_cell.stateW = True
                    elif d_x == -1:  # This means moving WEST / GAUCHE
                        current_cell.stateW = True
                        next_cell.stateE = True
                        # 6. Push the current cell to the stack,
                        # move to next, mark visited
                    visited_stack.append(current_cell)
                    current_cell = next_cell
                    current_cell.visit = True
                else:
                    # This is a dead end
                    current_cell = visited_stack.pop()
            except ImportError:
                print("ERR")

    def imperfect_helper(self, dead_cell: list):
        all_cell = self.get_all_cells()
<<<<<<< HEAD
        dead_end = [cell for cell in all_cell if (cell.stateN + cell.stateE + cell.stateS + cell.stateW) == 1 and cell.blocked is False]
        # dead_end3 = [cell for cell in all_cell if (cell.stateN + cell.stateE + cell.stateS + cell.stateW) == 3 and cell.blocked is False]
=======
        for cell in all_cell:
            print(cell.coordinate)
        print()
        dead_end = [
            cell for cell in all_cell
            if (
                cell.stateN + cell.stateE + cell.stateS + cell.stateW
                ) == 1
            and cell.blocked is False
        ]
        for cell in dead_end:
            print(f"{cell.coordinate}")
        dead_end3 = [
            cell for cell in all_cell
            if (
                cell.stateN + cell.stateE + cell.stateS + cell.stateW
                ) == 3
            and cell.blocked is False
        ]
        print()
        for cell in dead_end3:
            print(f"{cell.coordinate}")
        print(f"DEAD END1 LIST = {len(dead_end)}")
        print(f"DEAD END3 LIST = {len(dead_end3)}")

>>>>>>> e3be7b5a9c095b536039439182c5418c650d0f51
        current_cell = random.choice(dead_end)
        while len(dead_end) > 1:
            dead_end = [cell for cell in all_cell if (cell.stateN + cell.stateE + cell.stateS + cell.stateW) == 1 and cell.fortytwo is False]
            helper = 0
<<<<<<< HEAD
            while current_cell.fortytwo is True or current_cell.imperfect_help is True:
=======
            print("loop")
            while (
                current_cell.fortytwo is True
                or current_cell.imperfect_help is True
            ):
>>>>>>> e3be7b5a9c095b536039439182c5418c650d0f51
                current_cell = random.choice(dead_end)
                helper += 1
                if helper >= 20:
                    break
            print(len(dead_end))
            current_cell.imperfect_help = True
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
                total = next_cell.stateN + next_cell.stateE + next_cell.stateS + next_cell.stateW
                totalcur = current_cell.stateN + current_cell.stateE + current_cell.stateS + current_cell.stateW
                print(f"current cell nord {current_cell.stateN} | east {current_cell.stateE} | south {current_cell.stateS} | west {current_cell.stateW} | total = {totalcur} |coordinate {current_cell.coordinate}")
                print(f"next cell nord {next_cell.stateN} | east {next_cell.stateE} | south {next_cell.stateS} | west {next_cell.stateW} | total = {total} |coordinate {next_cell.coordinate}")
                d_x = next_cell.coordinate[0] - current_cell.coordinate[0]
                d_y = next_cell.coordinate[1] - current_cell.coordinate[1]
                if d_y == 1:  # This means moving SOUTH / BAS
                    print("break SOUTH")
                    current_cell.stateS = True
                    next_cell.stateN = True
                elif d_y == -1:  # This means moving West / Left
                    print("break NORD")
                    current_cell.stateN = True
                    next_cell.stateS = True
                elif d_x == 1:  # This means moving EAST / DROITE
                    print("break EAST")
                    current_cell.stateE = True
                    next_cell.stateW = True
                elif d_x == -1:  # This means moving WEST / GAUCHE
                    print("break WEST")
                    current_cell.stateW = True
                    next_cell.stateE = True
                current_cell = next_cell
<<<<<<< HEAD
                current_cell = dead_end.pop()
    
=======

>>>>>>> e3be7b5a9c095b536039439182c5418c650d0f51
    def backtracker_imperfect(self):
        dead_cell = []
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
                    if d_y == 1:  # This means moving SOUTH / BAS
                        current_cell.stateS = True
                        next_cell.stateN = True
                    elif d_y == -1:  # This means moving West / Left
                        current_cell.stateN = True
                        next_cell.stateS = True
                    elif d_x == 1:  # This means moving EAST / DROITE
                        current_cell.stateE = True
                        next_cell.stateW = True
                    elif d_x == -1:  # This means moving WEST / GAUCHE
                        current_cell.stateW = True
                        next_cell.stateE = True
                    # 6. Push the current cell to the stack,
                    # move to next, mark visited
                    visited_stack.append(current_cell)
                    current_cell = next_cell
                    current_cell.visit = True
                else:
                    # This is a dead end
                    dead_cell.append(current_cell)
                    current_cell = visited_stack.pop()
            except ImportError:
                print("ERR")
        self.imperfect_helper(dead_cell)

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
