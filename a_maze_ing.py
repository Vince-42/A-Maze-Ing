# ######### comments ##########
# I can use Field to validate config file
# Main file of the A-Maze-Ing project

# ######### import  ##########

import sys
from core.config import main_config
from core.maze_generator import MazeGenerator
from core.maze_generator import CellGenerator
from utils import error as err
from utils import design
from utils import color

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
    print("\n\n**********\n1 - REGENERATE\n2 - CHANGE WALL COLOR\n3 - SHOW SOLUTION\n4 - OUTPUT MAZE DATA (Bonus)\n5 - CHANGE 42 COLOR &... (Bonus)\n6 - CHANGE PERFECT MAZE (Bonus)\nAny - QUIT\n**********\n\n")


if __name__ == "__main__":
    count = 0
    # could be the main menu on LOOP
    if main():
        while(1):
            try:
                conf = main_config()
                if conf._data_check >= 6:
                    maze_o = MazeGenerator(conf)
                    gen_obj = maze_o.cell_gen()
                else:
                    print("Error on config - No Maze to be generated")
                    break
            except err.FortyTwoError as e:
                print("Error. You can't have the entry/exit within the 42 logo.")
                break
            except IndexError as e:
                print(f"Error in the configuration. {e}")
                break
            while(1):
                sys.stdout.flush()
                user_input = sys.stdin.readline().rstrip()
                print_menu()
                if user_input == "1":
                    print("GENERATE NEW MAZE")
                    break
                elif user_input == "2":
                    choice = [
                        color.PURPLE + "██" + color.RESET,
                        color.YELLOW + "██" + color.RESET,
                        color.ORANGE + "██" + color.RESET,
                        color.GREEN + "██" + color.RESET
                    ]
                    design.MAZE["wall"] =  choice[count]
                    count += 1
                    if count == 4:
                        count = 0
                    gen_obj.print_maze(True)
                elif user_input == "3":
                    print("SHOW THE SOLUTION PATH")
                elif user_input == "4":
                    print(maze_o.output_txt)
                elif user_input == "5":
                    choice = [
                        color.PURPLE + "42" + color.RESET,
                        color.YELLOW + "🔥" + color.RESET,
                        color.ORANGE + "👾" + color.RESET,
                        color.GREEN + "██" + color.RESET
                    ]
                    design.MAZE["fortytwo"] =  choice[count]
                    count += 1
                    if count == 4:
                        count = 0
                    gen_obj.print_maze(True)
                elif user_input == "6":
                    if maze_o.perfect:
                        maze_o.perfect = False
                    else:
                        maze_o.perfect = True
                    maze_bis = MazeGenerator(conf)
                    gen_obj = maze_o.cell_gen()
                else :
                    exit(0)
        
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
