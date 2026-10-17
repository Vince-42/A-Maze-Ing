from utils import color


CELL_SHAPES = {
    (0, 0, 0, 0): "━╋━",
    (1, 0, 0, 0): "━┳━",
    (0, 1, 0, 0): "━┫ ",
    (0, 0, 1, 0): "━┻━",
    (0, 0, 0, 1): " ┣━",
    (1, 1, 0, 0): "━┓ ",
    (1, 0, 1, 0): "━━━",
    (1, 0, 0, 1): " ┏━",
    (0, 1, 1, 0): "━┛ ",
    (0, 1, 0, 1): " ┃ ",
    (0, 0, 1, 1): " ┗━",
    (1, 1, 1, 0): "━╸ ",
    (1, 1, 0, 1): " ╻ ",
    (1, 0, 1, 1): " ╺━",
    (0, 1, 1, 1): " ╹ ",
    (1, 1, 1, 1): "   ",
}

MAZE = {
        "wall":  color.YELLOW + "██" + color.RESET,
        "path":  color.PURPLE + "  " + color.RESET,
        "start": color.GREEN  + "██" + color.RESET,
        "end":   color.RED  + "██" + color.RESET
    }
