# Project-specific module imports.
from _constant.string import String


class Color():
    """
    
    Color is a simple class that holds class constants representing ASCII colors,
    for the colorization of console text.

    """
    
    
    # Constants for the storage of colors.
    GREEN: str = String.ASCII_GREEN
    PURPLE: str = String.ASCII_PURPLE
    RED: str = String.ASCII_RED
    BLUE: str = String.ASCII_BLUE
    YELLOW: str = String.ASCII_YELLOW

    # Constants for the storage of end-color.
    ENC: str = String.ASCII_ENC


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass