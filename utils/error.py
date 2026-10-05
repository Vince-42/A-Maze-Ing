# ######### comments ##########

# Error file of the A-Maze-Ing project

# ######### import  ##########


# ######### Errorclass   ##########

class TupleError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NegativeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class BooleanError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
