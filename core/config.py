# ######### comments ##########

# Configuration file of the A-Maze-Ing project

# ######### import  ##########

from utils import error as err

# ######### class   ##########


class Configuration():
    def __init__(self):
        self.__file_name: str = "config.txt"
        self._width: int = -1
        self._height: int = -1
        self._entry: tuple = ()
        self._exit: tuple = ()
        self._output_file: str = ""
        self._perfect = None
        self._seed: int = -1
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
                self.placing_data(truc, line.rstrip())

    def placing_data(self, truc, line):
        if truc == "WIDTH=":
            x = self.split_int(line)
            self._width = x
        elif truc == "HEIGHT=":
            y = self.split_int(line)
            self._height = y
        elif truc == "ENTRY=":
            z = self.split_tuple(line)
            self._entry = z
        elif truc == "EXIT=":
            a = self.split_tuple(line)
            self._exit = a
        elif truc == "OUTPUT_FILE=":
            b = self.split_str(line)
            self._output_file = b
        elif truc == "PERFECT=":
            c = self.split_bool(line)
            self._perfect = c

    # return 'True' or 'False' on success | 'None' on failed
    def split_bool(self, line) -> bool:
        accept = {"True", "True\n"}
        false = {"False", "False\n"}
        rslt = line.split("=")
        try:
            if rslt[1] in accept:
                self._data_check += 1
                return True
            elif rslt[1] in false:
                self._data_check += 1
                return False
            else:
                raise err.BooleanError("Perfect config issue. Must be True or False")
        except err.BooleanError:
            raise err.BooleanError

    # return a positive INT on success | neg on failed
    def split_int(self, line) -> int:
        rslt = line.split("=")
        # verifier que line [1] est bien un integer
        # return l'intenger si positive
        try:
            ret = int(rslt[1])
            if ret < 0:
                raise err.NegativeError("Integer cannot be negative.")
            self._data_check += 1
            return ret
        except TypeError as e:
            print(f"WRONG DATA : {e}")
        return -1

    # return an STR on success | empty on fail
    def split_str(self, line) -> str:
        rslt = line.split("=")
        try:
            ret = str(rslt[1])
            self._data_check += 1
            return ret
        except TypeError as e:
            print(f"WRONG DATA : {e}")
        return ""

        # return a TUPLE on success | (-1, -1) on fail
    def split_tuple(self, line) -> tuple:
        rslt = line.split("=")
        try:
            dt = rslt[1]
            dt_split = tuple(dt.split(","))
            if len(dt_split) != 2:
                raise err.TupleError
            for d in dt_split:
                int(d)
            self._data_check += 1
            return dt_split
        except TypeError as e:
            print(f"WRONG DATA : {e}")
        return (-1, -1)

    def validation(self):
        # checking entry/exit
        # issue on the first check - should be ok
        if self._entry[0] > self._exit[0] or self._entry[1] > self._exit[1]:
            self._data_check -= 1
            raise err.EntryExitError("Entry point outside of the maze.")
        if self._entry == self._exit:
            self._data_check -= 1
            raise err.EntryExitError("Entry can not be the same point as the Exit.")
        if int(self._entry[0]) > self._width or int(self._entry[1]) > self._height:
            self._data_check -= 1
            raise err.EntryExitError("Entry point cannot be outside the maze boundaries.")
        if int(self._exit[0]) > self._width or int(self._exit[1]) > self._height:
            self._data_check -= 1
            raise err.EntryExitError("Exit point cannot be outside the maze boundaries.")

# ######### methods ##########

def main_config():
    default = Configuration()
    try:
        default.extract()
        default.validation()
    except ValueError as error:
        print(f"Error in config file : {error}")
    except err.TupleError as e:
        print(f"Error in Tuple validation. {e}")
    except err.NegativeError as e:
        print(f"The config value cannot be negative. {e}")
    except FileNotFoundError as e:
        print(f"Error in the file name or location. {e}")
    except err.BooleanError as e:
        print(f"Error in the boolean part of config file. {e}")
    except err.EntryExitError as e:
        print(f"Error in the entry/exit parameters. {e}")
    return default

# ######### main    ##########


if __name__ == "__main__":
    main_config()
