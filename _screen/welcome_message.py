# Standard library imports.
import os
import time

# Standard library from imports.
from typing import Union

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _language.english import English
from _language.french import French
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class WelcomeMessage(RootScreen):
    """

    WelcomeMessage is the gateway screen for M&B. It serves to greet and welcome users.
    
    """


    @staticmethod
    def execute() -> None:
        """
        
        Description:
            Updates the locale to be used for the retrieval of screen text.
            Invokes _navigate_forward to navigate to the next screen.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Display the screen.
        WelcomeMessage._display_screen()

        # Navigate to the next screen.
        WelcomeMessage._navigate_forward()


    @staticmethod
    def _display_screen() -> None:
        """
        
        Description:
            Resets the console window.
            Formats the screen text.
            Displays the screen text to the user.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            KeyboardInterrupt:
                If the user attempts to press (Ctrl+C),
                then the signal is ignored.
                
        """

        # Initialize color constants.
        COLOR_END = Color.ENC
        COLOR_PURPLE = Color.PURPLE
        COLOR_YELLOW = Color.YELLOW

        # Initialize the separator.
        SEPERATOR = Separator.draw()

        # Initialize welcome message label constants in different languages.
        WELCOME_MESSAGE_ENGLISH = English.dict[String.LANGUAGE_KEY_WELCOME_MESSAGE]
        WELCOME_MESSAGE_FRENCH = French.dict[String.LANGUAGE_KEY_WELCOME_MESSAGE]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Attempt to:
        try:
            # Print the screen main content.
            print(f'{COLOR_PURPLE}{SEPERATOR}{COLOR_END}', end='\n\n')
            print(f'{COLOR_YELLOW}{WELCOME_MESSAGE_ENGLISH}{COLOR_END}', end='\n\n')
            print(f'{COLOR_YELLOW}{WELCOME_MESSAGE_FRENCH}{COLOR_END}', end='\n\n')
            print(f'{COLOR_PURPLE}{SEPERATOR}{COLOR_END}')

            # Wait for few seconds.
            time.sleep(Integer.WELCOME_MESSAGE_WAIT_TIME)

        # Handle: KeyboardInterrupt.
        except KeyboardInterrupt:
            # Ignore.
            pass


    @staticmethod
    def _is_input_valid(user_input: Union[int, str]) -> bool:
        """

        Note:
        
        Given that this screen extends RootScreen, and to abide by (OOP) fundamentals, all abstract methods must be implemented.
        This method is not required for this screen. Therefore, It is implemented but is given an empty body.
        
        """

        # Ignore.
        pass


    @staticmethod
    def _navigate_backward() -> None:
        """

        Note:
        
        Given that this screen extends RootScreen, and to abide by (OOP) fundamentals, all abstract methods must be implemented.
        This method is not required for this screen. Therefore, It is implemented but is given an empty body.
        
        """

        # Ignore.
        pass


    @staticmethod
    def _navigate_forward() -> None:
        """
        
        Description:
            Imports the required screen module.
            Navigates to the next screen.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Import the respective screen module.
        from _screen.language_selection import LanguageSelection

        # Execute it.
        LanguageSelection.execute()


    @staticmethod
    def _process_input(user_input: Union[int, str]) -> None:
        """

        Note:
        
        Given that this screen extends RootScreen, and to abide by (OOP) fundamentals, all abstract methods must be implemented.
        This method is not required for this screen. Therefore, It is implemented but is given an empty body.
        
        """

        # Ignore.
        pass


    @staticmethod
    def _take_input() -> None:
        """

        Note:
        
        Given that this screen extends RootScreen, and to abide by (OOP) fundamentals, all abstract methods must be implemented.
        This method is not required for this screen. Therefore, It is implemented but is given an empty body.
        
        """

        # Ignore.
        pass


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass