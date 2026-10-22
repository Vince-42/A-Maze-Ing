from utils import color

MAZE = {
        "wall":  color.YELLOW + "██" + color.RESET,
        "path":  color.PURPLE + "  " + color.RESET,
        "start": color.GREEN  + "🐍" + color.RESET,
        "end":   color.RED  + "🍎" + color.RESET,
        "fortytwo":   color.BLUE  + "⁴²" + color.RESET
    }

MAZE_ONE = {
        "wall":  color.PURPLE + "██" + color.RESET,
        "path":  color.YELLOW + "  " + color.RESET,
        "start": color.GREEN  + "🐍" + color.RESET,
        "end":   color.RED  + "🍎" + color.RESET,
        "fortytwo":   color.BLUE  + "⁴²" + color.RESET
    }

MAZE_TWO = {
        "wall":  color.BLUE + "██" + color.RESET,
        "path":  color.PURPLE + "  " + color.RESET,
        "start": color.GREEN  + "🐍" + color.RESET,
        "end":   color.RED  + "🍎" + color.RESET,
        "fortytwo":   color.BLUE  + "⁴²" + color.RESET
    }