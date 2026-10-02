# ######### comments ##########

# Main file of the A-Maze-Ing project

# ######### import  ##########

from typing import IO

# ######### class   ##########

class TupleError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


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
        self._data_check: int = 0

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
                self.placing_data(truc, line.rstrip(), indicator)

    def placing_data(self, truc, line, indicator):
        if truc == "WIDTH=":
            x = self.split_int(line)
            self._width = x
        elif truc == "HEIGHT=":
            x = self.split_int(line)
            self._height = x
        elif truc == "ENTRY=":
            x = self.split_tuple(line)
            self._entry = x
        elif truc == "EXIT=":
            x = self.split_tuple(line)
            self._exit = x
        elif truc == "OUTPUT_FILE=":
            x = self.split_str(line)
            self._output_file = x
        elif truc == "PERFECT=":
            x = self.split_bool(line)
            self._perfect = x
            
            
    # return a True/False on success, None on fail
    def split_bool(self, line) -> bool:
        accept = {"True", "True\n", "False", "False\n"}
        rslt = line.split("=")
        try:
            if rslt[1] in accept:
                ret = bool(rslt[1])
                self._data_check += 1
                return ret
        except Exception as e:
            print(f"WRONG DATA : {e}")
            return None

    # return an INT on success
    def split_int(self, line) -> int:
        rslt = line.split("=")
        # verifier que line [1] est bien un integer
        # return l'intenger si OK
        try:
            ret = int(rslt[1])
            self._data_check += 1
            return ret
        except TypeError as e:
            print(f"WRONG DATA : {e}")

    # return an STR on success
    def split_str(self, line) -> str:
        rslt = line.split("=")
        try:
            ret = str(rslt[1])
            self._data_check += 1
            return ret
        except TypeError as e:
            print(f"WRONG DATA : {e}")
        pass

        # return a TUPLE on success
    def split_tuple(self, line) -> tuple:
        rslt = line.split("=")
        try:
            dt = rslt[1]
            dt_split = tuple(dt.split(","))
            if len(dt_split) < 2:
                raise TupleError
            for d in dt_split:
                int(d)
            self._data_check += 1
            return dt_split
        except TypeError as e:
            print(f"WRONG DATA : {e}")
        pass
# ######### methods ##########

def main_config():
    default = Configuration()
    try:
        default.extract()
    except ValueError as error:
        print(f"Error in config file : {error}")
    except TupleError as e:
        print(f"Error in Tuple validation. {e}")
    return default

# ######### main    ##########


if __name__ == "__main__":
    main_config()
