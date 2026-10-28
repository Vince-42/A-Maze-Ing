# ######### comments ##########
# I can use Field to validate config file
# Main file of the A-Maze-Ing project

# ######### import  ##########

import sys
from core.config import main_config
from core.maze_generator import MazeGenerator
from utils import error as err
from utils import design
from utils import color
from core.maz_solver import MazSolver

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


def print_menu():
    print("\n\n**********\n"
          "1 - Generate Maze (cf. config.txt)\n"
          "2 - Rotate wall color\n3 - Show/Hide the solution\n"
          "4 - Output maze coordinate on terminal (Bonus)\n"
          "5 - Rotate color & design 42 (Bonus)\n"
          "6 - Generate a Perfect/Imperfect Maze (Bonus)\nAny - QUIT\n"
          "**********\n\n")


if __name__ == "__main__":
    solution = False
    count = 0
    # could be the main menu on LOOP
    if main():
        while (1):
            try:
                conf = main_config()
                if conf._data_check >= 6:
                    maze_o = MazeGenerator(conf)
                    gen_obj = maze_o.cell_gen()
                else:
                    print("Error on config - No Maze to be generated")
                    break
            except err.FortyTwoError as e:
                print(f"Error. The entry/exit can't be within the 42 logo.{e}")
                break
            except IndexError as e:
                print(f"Error in the configuration. {e}")
                break
            while (1):
                try:
                    print_menu()
                    sys.stdout.flush()
                    user_input = sys.stdin.readline().rstrip()
                    if user_input == "1":
                        print("GENERATE NEW MAZE")
                        solution = False
                        break
                    elif user_input == "2":
                        choice = [
                            color.PURPLE + "██" + color.RESET,
                            color.YELLOW + "██" + color.RESET,
                            color.ORANGE + "██" + color.RESET,
                            color.GREEN + "██" + color.RESET
                        ]
                        design.MAZE["wall"] = choice[count]
                        count += 1
                        if count == 4:
                            count = 0
                        gen_obj.print_maze(True, solution)
                    elif user_input == "3":
                        if solution:
                            solution = False
                        else:
                            solution = True
                        # init the display with the solution
                        gen_obj.print_maze(False, False)
                        # display the maze
                        gen_obj.print_maze(True, solution)
                    elif user_input == "4":
                        print(f"\n\n{maze_o.output_txt}")
                    elif user_input == "5":
                        choice = [
                            color.PURPLE + "42" + color.RESET,
                            color.YELLOW + "🔥" + color.RESET,
                            color.ORANGE + "👾" + color.RESET,
                            color.GREEN + "██" + color.RESET
                        ]
                        design.MAZE["fortytwo"] = choice[count]
                        count += 1
                        if count == 4:
                            count = 0
                        gen_obj.print_maze(True, solution)
                    elif user_input == "6":
                        if maze_o.perfect:
                            maze_o.perfect = False
                        else:
                            maze_o.perfect = True
                        maze_bis = MazeGenerator(conf)
                        gen_obj = maze_o.cell_gen()
                        solution = False
                    else:
                        exit(0)
                except KeyboardInterrupt:
                    print("  Not quit properly. Press any key .. --'")

    # this below is just for checking purpose
    # print parameters to check config
    '''
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
    '''
