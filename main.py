# Project-specific module imports.
from _screen.welcome_message import WelcomeMessage


# If this module is executed as the main program:
if __name__ == "__main__":
    # Greet and welcome users into M&B.
    WelcomeMessage.execute()
