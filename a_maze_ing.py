# ######### comments ##########
# I can use Field to validate config file
# Main file of the A-Maze-Ing project

# ######### import  ##########

import sys
from core.config import main_config

# ######### class   ##########


class MazeGenerator():
    def __init__(self):
        if main():
            self.start_config = main_config()

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
    start_maze = MazeGenerator()
    # this below is just for checking purpose
    # print parameters to check config
    try:
        for param in start_maze.start_config.__dict__:
            print(param, end=": ")
            print(start_maze.start_config.__dict__[param])
        if start_maze.start_config._data_check >= 6:
            print("MAZE CAN BE GENERATED")
        else:
            print("Error on config - No Maze to be generated")
    except Exception as e:
        print(f"Error in checking printing parameters. {e}")
