########## comments ##########

# Main file of the A-Maze-Ing project

########## import  ##########

import sys

########## class   ##########


########## methods ##########
def start() -> bool:
    arg = sys.argv
    l_arg = len(arg)
    if l_arg != 2:
        pass
    else:
        if parsing(arg):
            print("file config.txt exist")
            return True
    return False

def parsing(list_arg):
    chck = list_arg[1]
    if chck == "config.txt":
        return True
    return False

def main():
    start()


if __name__ == "__main__":
    main()