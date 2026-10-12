# ######### comments ##########

# Maze Generator file of the A-Maze-Ing project

# ######### import  ##########

import utils.color as color
import random


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
        generator.check_maze()
        generator.print_maze()

    def get_entry(self) -> tuple:
        return self.entry

def chg_state(Cell):
        print("CHANGING STATE FT")
        Cell.etat = True
        print(Cell.etat)

class CellGenerator(MazeGenerator):
    entry_maze = ()
    exit_maze = ()

    def __init__(self, x: int, y: int, width: int, height: int):
        self._color = "██"  # The color of the cell on the maze
        self._stateN = False  # True = Open | False = Wall
        self._stateE = False  # True = Open | False = Wall
        self._stateS = False  # True = Open | False = Wall
        self._stateW = False  # True = Open | False = Wall
        self.etat = False # False = closed
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
                # obj._color = color.BLACK
                print("\n", end="")
            if obj.coordinate[0] == 0:
                # obj._color = color.BLACK
                obj._stateS = True
            if obj.coordinate[0] == obj.width - 1:
                obj._stateN = True
                # obj._color = color.BLACK
            if obj.coordinate[1] == obj.width - 1:
                # obj._color = color.BLACK
                obj._stateW = True
            # print(f"obj coordinate {type(obj.coordinate[0])} | obj entry {type(self.entry_maze[0])}")
            if obj.coordinate == self.entry_maze:
                obj._color = color.YELLOW
                obj.entry = True
                obj.etat = True
            if obj.coordinate == self.exit_maze:
                obj._color = color.YELLOW
                obj.exit = True
                obj.etat = True
            if obj.etat == True and obj.exit == False and obj.entry == False:
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
                print(f"cell {cell_x}{cell_y} | et_droit {et_droit}, et_bas {et_bas}, et_gauche {et_gauche}, et_haut {et_haut}")
                # print(f"cell {cell_x}{cell_y} | ce_droit {ce_droit}, ce_bas {ce_bas}, ce_gauche {ce_gauche}, ce_haut {ce_haut}")
                if obj.etat == False:
                    print("cell is OPEN")
                    if et_haut == None and et_bas == False and et_droit == False and et_gauche == None:
                        print("str - trying changing")
                        chg_state(self)
                        print("CHANGING STATE SELF")
                    if et_haut == None and et_bas == False and et_droit == False and et_gauche == True:
                        print("trying changing")
                        if self.ret_rdm() == 1:
                            print("CHANGING STATE SELF")
                            chg_state(self)
                        else:
                            print("CHANGING STATE DROIT")
                            chg_state(ce_droit)
                    if et_haut == None and et_bas == False and et_droit == False and et_gauche == False:
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
                        # changer l'etat de cette obj a true 
#                print(f"IN OBJ cell ({cell_x},{cell_y}) ||"
#                    f"\nRIGHT cell({cell_x + 1},{cell_y}) - East: {self.ret_cell((cell_x + 1, cell_y))._stateE}, North: {self.ret_cell((cell_x + 1, cell_y))._stateN}, South: {self.ret_cell((cell_x + 1, cell_y))._stateS}, WEST: {self.ret_cell((cell_x + 1, cell_y))._stateW}"
#                    f"\nDOWN cell({cell_x},{cell_y + 1}) - East: {self.ret_cell((cell_x, cell_y + 1))._stateE}, North: {self.ret_cell((cell_x, cell_y + 1))._stateN}, South: {self.ret_cell((cell_x, cell_y + 1))._stateS}, WEST: {self.ret_cell((cell_x, cell_y + 1))._stateW}"
#                    f"\nLEFT cell({cell_x - 1},{cell_y}) - East: {self.ret_cell((cell_x - 1, cell_y))._stateE}, North: {self.ret_cell((cell_x - 1, cell_y))._stateN}, South: {self.ret_cell((cell_x - 1, cell_y))._stateS}, WEST: {self.ret_cell((cell_x - 1, cell_y))._stateW}"
#                    f"\nUP cell({cell_x},{cell_y - 1}) - East: {self.ret_cell((cell_x, cell_y - 1))._stateE}, North: {self.ret_cell((cell_x, cell_y - 1))._stateN}, South: {self.ret_cell((cell_x, cell_y - 1))._stateS}, WEST: {self.ret_cell((cell_x, cell_y - 1))._stateW}")
            except AttributeError as e:
                print(f"error when checking : ({cell_x},{cell_y}) ")
                continue

    def ret_cell(self, coordinate: tuple):
        try:
            for obj in self._all_cells:
                if obj.coordinate == coordinate:
                    return obj
        except:
            return None

    def ret_state(self, coordinate: tuple):
        for obj in self._all_cells:
            if obj.coordinate == coordinate:
                return obj.etat
        return None

    def ret_rdm(self):
        nbr = (1, 2, 3)
        return random.choice(nbr)
