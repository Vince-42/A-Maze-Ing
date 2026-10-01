# ######### comments ##########

# Main file of the A-Maze-Ing project

# ######### import  ##########

import sys
from config import main_config

# ######### class   ##########


class MazeGenerator():
    def __init__(self):
        if main():
            self.start_config = main_config()
            print(f"result: {self.start_config._data}")

# ######### methods ##########


def start() -> bool:
    arg = sys.argv
    l_arg = len(arg)
    if l_arg != 2:
        pass
    else:
        if parsing(arg):
            return True
    return False


def parsing(list_arg):
    chck = list_arg[1]
    if chck == "config.txt":
        return True
    return False


def main() -> bool:
    return start()


if __name__ == "__main__":
    start_maze = MazeGenerator()
