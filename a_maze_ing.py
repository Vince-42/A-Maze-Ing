# ######### comments ##########
# I can use Field to validate config file
# Main file of the A-Maze-Ing project

# ######### import  ##########

import sys
from core.config import main_config
from core.maze_generator import MazeGenerator
from core.maze_generator import CellGenerator

# ######### class   ##########


# ######### methods ##########


def start() -> bool:
    arg = sys.argv
    l_arg = len(arg)
    if l_arg != 2:
        pass
    else:
        if parsing(arg):
            # print("start = true")
            return True
    # print("start = false")
    return False


def parsing(list_arg) -> bool:
    chck = list_arg[1]
    if chck == "config.txt":
        return True
    return False


def main() -> bool:
    return start()


if __name__ == "__main__":
    # could be the main menu on LOOP
    if main():
        conf = main_config()
        if conf._data_check >= 6:
            maze_o = MazeGenerator(conf)
            maze_o.cell_gen()
        
    # this below is just for checking purpose
    # print parameters to check config
    print("\n")
    try:
        print("*"*45)
        for param in maze_o.maze.__dict__:
            print(param, end=": ")
            print(maze_o.maze.__dict__[param])
        if maze_o.maze._data_check >= 6:
            print("*"*45)
            print("MAZE CAN BE GENERATED")
        else:
            print("*"*45)
            print("Error on config - No Maze to be generated")
    except Exception as e:
        print(f"Error in checking printing parameters. {e}")
