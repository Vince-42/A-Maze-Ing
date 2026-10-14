# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import utils.color as color
import random

random.seed()

# ######### class   ##########

# I NEED TO HAVE ONLY MAZE GENERATOR

idea = (color.BLACK, color.BLUE)
verite = (True, False)

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
        generator.backtracker()
        # generator.check_maze()
        print("\n\n")
        generator.print_maze()

    def get_entry(self) -> tuple:
        return self.entry


def chg_state(Cell):
    Cell.visit = True


class CellGenerator(MazeGenerator):
    entry_maze = ()
    exit_maze = ()

    def __init__(self, x: int, y: int, width: int, height: int):
        self._color = "██"  # The color of the cell on the maze
        self._stateN = False  # True = Open | False = Wall
        self._stateE = False  # True = Open | False = Wall
        self._stateS = False  # True = Open | False = Wall
        self._stateW = False  # True = Open | False = Wall
        self.visit = False  # False = closed
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
        for i in range(self.width):
            for ii in range(self.height):
                new = CellGenerator(i, ii, self.width, self.height)
                self._all_cells.append(new)

    def print_maze(self):
        for obj in self._all_cells:
            if obj.coordinate[1] == 0:
                # obj._stateE = True
                # obj._color = color.BLACK
                pass
                print("\n", end="")
            if obj.coordinate[0] == 0:
                # obj._color = color.BLACK
                # obj._stateS = True
                pass
            if obj.coordinate[0] == obj.width - 1:
                # obj._stateN = True
                # obj._color = color.BLACK
                pass
            if obj.coordinate[1] == obj.width - 1:
                # obj._color = color.BLACK
                # obj._stateW = True
                pass
            # print(f"obj coordinate {type(obj.coordinate[0])} | obj entry {type(self.entry_maze[0])}")
            if obj.coordinate == self.entry_maze:
                obj._color = color.YELLOW
                obj.entry = True
                obj.visit = True
            if obj.coordinate == self.exit_maze:
                obj._color = color.YELLOW
                obj.exit = True
                obj.visit = True
            if obj.visit is True and obj.exit is False and obj.entry is False:
                obj._color = color.PURPLE
            print(obj._color, end="")

    def check_maze(self):
        print("\n")
        for obj in self._all_cells:
            try:
                cell_x = obj.coordinate[0]
                cell_y = obj.coordinate[1]
                et_droit = self.ret_state((cell_x, cell_y + 1))
                et_bas = self.ret_state((cell_x + 1, cell_y))
                et_haut = self.ret_state((cell_x - 1, cell_y))
                et_gauche = self.ret_state((cell_x, cell_y - 1))
                ce_droit = self.ret_cell((cell_x, cell_y + 1))
                ce_bas = self.ret_cell((cell_x + 1, cell_y))
                ce_haut = self.ret_cell((cell_x - 1, cell_y))
                ce_gauche = self.ret_cell((cell_x, cell_y - 1))
                # print(f"cell {cell_x}{cell_y} | et_droit {et_droit}, et_bas {et_bas}, et_gauche {et_gauche}, et_haut {et_haut}")
                if obj.visit is False:
                    print("cell is OPEN")
                    if et_haut is None and et_bas is False and et_droit is False and et_gauche is None:
                        print("start")
                        chg_state(self)
                        print("CHANGING STATE SELF")
                    if et_haut is None and et_bas is False and et_droit is False and et_gauche is True:
                        if self.ret_rdm() == 1:
                            print("CHANGING STATE SELF")
                            chg_state(self)
                        else:
                            print("CHANGING STATE DROIT")
                            chg_state(ce_droit)
                    if et_haut is None and et_bas is False and et_droit is False and et_gauche is False:
                        nb = self.ret_rdm()
                        if nb == 1:
                            print("CHANGING STATE BAS")
                            chg_state(ce_bas)
                        elif nb == 2:
                            print("CHANGING STATE DROIT")
                            chg_state(ce_droit)
                        elif nb == 3:
                            print("CHANGING STATE GAUCHE")
                            chg_state(ce_gauche)

                    if et_haut == False and et_bas == False and et_droit == False and et_gauche == False:
                        print("trying changing")
                        nb = self.ret_rdm()
                        if nb == 1:
                            print("CHANGING STATE BAS")
                            chg_state(ce_bas)
                        elif nb == 2:
                            print("CHANGING STATE DROIT")
                            chg_state(ce_droit)
                        elif nb == 3:
                            print("CHANGING STATE GAUCHE")
                            chg_state(ce_gauche)
                        elif nb == 4:
                            print("CHANGING STATE HAUT")
                            chg_state(ce_haut)
                        # choisir un des objet bas ou droite
                        # changer l'visit de cette obj a true 
#                print(f"IN OBJ cell ({cell_x},{cell_y}) ||"
#                    f"\nRIGHT cell({cell_x + 1},{cell_y}) - East: {self.ret_cell((cell_x + 1, cell_y))._stateE}, North: {self.ret_cell((cell_x + 1, cell_y))._stateN}, South: {self.ret_cell((cell_x + 1, cell_y))._stateS}, WEST: {self.ret_cell((cell_x + 1, cell_y))._stateW}"
#                    f"\nDOWN cell({cell_x},{cell_y + 1}) - East: {self.ret_cell((cell_x, cell_y + 1))._stateE}, North: {self.ret_cell((cell_x, cell_y + 1))._stateN}, South: {self.ret_cell((cell_x, cell_y + 1))._stateS}, WEST: {self.ret_cell((cell_x, cell_y + 1))._stateW}"
#                    f"\nLEFT cell({cell_x - 1},{cell_y}) - East: {self.ret_cell((cell_x - 1, cell_y))._stateE}, North: {self.ret_cell((cell_x - 1, cell_y))._stateN}, South: {self.ret_cell((cell_x - 1, cell_y))._stateS}, WEST: {self.ret_cell((cell_x - 1, cell_y))._stateW}"
#                    f"\nUP cell({cell_x},{cell_y - 1}) - East: {self.ret_cell((cell_x, cell_y - 1))._stateE}, North: {self.ret_cell((cell_x, cell_y - 1))._stateN}, South: {self.ret_cell((cell_x, cell_y - 1))._stateS}, WEST: {self.ret_cell((cell_x, cell_y - 1))._stateW}")
            except AttributeError as e:
                print(f"error when checking : ({cell_x},{cell_y}). {e}")
                continue

# 1 Départ : Choisissez une case au hasard. Marquez-la comme Visité.
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
        current_cell.visit = True
        # visited cell in list
        visited_stack = [current_cell]
        while len(visited_stack) > 0:
            try:
                cell_x = current_cell.coordinate[0]
                cell_y = current_cell.coordinate[0]
                # get info on cell next to current cell 
                lst_et = [
                    self.ret_cell((cell_x, cell_y + 1)),  # Right
                    self.ret_cell((cell_x + 1, cell_y)),  # Down
                    self.ret_cell((cell_x - 1, cell_y)),  # Up
                    self.ret_cell((cell_x, cell_y - 1))   # Left
                ]
                # filtered None return from next to current cell
                unvisited_ok_cell = [obj for obj in lst_et if obj is not None and not obj.visit]
                if unvisited_ok_cell:
                    # 5. Choose a random unvisited neighbor to move to
                    next_cell = random.choice(unvisited_ok_cell)
                    # --- Breaking the Wall ---
                    # define diff between x,y of current/next cell
                    d_x = next_cell.coordinate[0] - current_cell.coordinate[0]
                    d_y = next_cell.coordinate[1] - current_cell.coordinate[1]
                    if d_y == 1:  # This means moving East / Right
                        current_cell.stateE = True
                        next_cell.stateE = True
                    elif d_y == -1:  # This means moving West / Left
                        current_cell.stateW = True
                        next_cell.stateW = True
                    elif d_x == 1:  # This means moving South / Down
                        current_cell.stateS = True
                        next_cell.stateS = True
                    elif d_x == -1:  # This means moving North / Up
                        current_cell.stateN = True
                        next_cell.stateN = True
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
        nbr = (1, 2, 3)
        return random.choice(nbr)
