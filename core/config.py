# ######### comments ##########

# Main file of the A-Maze-Ing project

# ######### import  ##########

from typing import IO

# ######### class   ##########


class Configuration():
    def __init__(self):
        self.__file_name = "config.txt"
        self._width: int = None
        self._height: int = None
        self._entry: tuple = ()
        self._exit: tuple = ()
        self._output_file: str = None
        self._perfect: bool = None
        self._seed: int = None
        self._algorythm = None
        self._display_mode = None
        self._data = None

    def extract(self):
        with open(self.__file_name, "r") as f:
            for line in f:
                if line[0] != '#' and line[0] != "\n":
                    self.parsing_file(line)

    def parsing_file(self, line: str):
        indicator = ["WIDTH=", "HEIGHT=", "ENTRY=", "EXIT=", "OUTPUT_FILE=",
                     "PERFECT=", "SEED="]
        for truc in indicator:
            if truc in line:
                self.placing_data(truc, line, indicator)
            #  print(f"var: {truc}")

    def placing_data(self, truc, line, indicator):
        if truc == "WIDTH=":
            x = self.split_return(line)
            self._width = x
        if truc == "HEIGHT=":
            y = self.split_return(line)
            self._height = y

    # ca marche pour les INTS
    def split_return(self, line) -> int:
        rslt = line.split("=")
        # verifier que line [1] est bien un integer
        # return l'intenger si OK
        try:
            return int(rslt[1])
        except TypeError as e:
            print(f"WRONG DATA : {e}")
        pass
# ######### methods ##########


def main_config():
    default = Configuration()
    default.extract()
    return default

# ######### main    ##########


if __name__ == "__main__":
    main_config()
