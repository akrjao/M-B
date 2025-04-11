# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.english import English
from _language.french import French
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class LanguageSelection(RootScreen):
    """
    
    LanguageSelection is a screen that enables the user to pick their desired screen language.

    """


    # Constant for the retrieval of screen text.
    _LOCALE = None


    @staticmethod
    def execute() -> None:
        """
        
        Description:
            Updates the locale to be used for the retrieval of screen text.
            Invokes _take_input to prompt the user into entering input.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Initialize the locale constant.
        LanguageSelection._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        LanguageSelection._take_input()
        
        # Navigate to the next screen.
        LanguageSelection._navigate_forward()


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
            None
                
        """
        
        # Initialize color constants.
        COLOR_END = Color.ENC
        COLOR_PURPLE = Color.PURPLE
        COLOR_YELLOW = Color.YELLOW
        COLOR_GREEN = Color.GREEN

        # Initialize the separator.
        SEPARATOR = Separator.draw()

        # Initialize various label constants based on the selected language.
        SCREEN_MAIN_MENU = LanguageSelection._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_SETTINGS = LanguageSelection._LOCALE[String.LANGUAGE_KEY_SCREEN_SETTINGS]
        SCREEN_LANGUAGE_SELECTION = LanguageSelection._LOCALE[String.LANGUAGE_KEY_SCREEN_LANGUAGE_SELECTION]
        ENGLISH = English.dict[String.LANGUAGE_KEY_LANGUAGE]
        FRENCH = French.dict[String.LANGUAGE_KEY_LANGUAGE]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*]{COLOR_END} {COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[4]{COLOR_END} {COLOR_YELLOW}{SCREEN_SETTINGS}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[1]{COLOR_END} {COLOR_YELLOW}{SCREEN_LANGUAGE_SELECTION}{COLOR_END}', end='\n')

        # Print the screen main content.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[1]{COLOR_END} {COLOR_YELLOW}{ENGLISH}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[2]{COLOR_END} {COLOR_YELLOW}{FRENCH}{COLOR_END}', end='\n\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')


    @staticmethod
    def _is_input_valid(user_input: int) -> bool:
        """
        
        Description:
            Checks the value of user_input to verify its validity with respect to this screen.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            user_input(int): Input provided by the user.
        
        Returns:
            bool: Whether user_input is valid or invalid.

        Raises:
            None
                
        """
        
        # If user input is not in [1, 3[ :
        if user_input not in range(1,3):
            # Assert user input as invalid.
            return False
        
        # If user input is in [1, 3[ :
        else:
            # Assert user input as valid.
            return True

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
        from _screen.requirements import Requirements
        
        # Execute it.
        Requirements.execute()


    @staticmethod
    def _process_input(user_input: int) -> None:
        """
        
        Description:
            Checks the value of user_input to invoke other methods based on user_input.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            user_input(int): Input provided by the user.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If:
        match user_input:
            # user input is equal to 1:
            case 1:
               # Set English as the selected language.
               PropertiesJsonHandler.set_language(String.LITERAL_LOCALE_CODE_ENGLISH)
            
            # user input is equal to 2:
            case 2:
                # Set French as the selected language.
                PropertiesJsonHandler.set_language(String.LITERAL_LOCALE_CODE_FRENCH)


    @staticmethod
    def _take_input() -> None:
        """

        Description:
            Repeatedly, invokes _display_screen for the display of the respective screen,
            reads user input from the console window,
            invokes _is_input_valid to verify the validity of user input,
            and invokes _process_input to process validated user input.

            Note: This method is not meant to be accessed from outside this class.
        
        Args:
            None
        
        Returns:
            None

        Raises:
            ValueError: 
                If user input is of incompatible data type,
                then the current iteration is skipped,
                and the user is re-prompted.

            KeyboardInterrupt:
                If the user attempts to press (Ctrl+C),
                then the signal is ignored.
                
        """

        # Initialize color constants.
        COLOR_BLUE = Color.BLUE
        COLOR_END = Color.ENC

        # Initialize label constant based on the selected language.
        PROMPT_LANGUAGE_SELECTION = LanguageSelection._LOCALE[String.LANGUAGE_KEY_PROMPT_LANGUAGE_SELECTION]

        # If language attribute is not set:
        if not PropertiesJsonHandler.is_language_set():
            # Loop indefinitely.
            while True:
                # Attempt to:
                try:
                    # Display the screen.
                    LanguageSelection._display_screen()
                    
                    # Read user input from the console window.
                    user_input = int(input(f'{COLOR_BLUE}{PROMPT_LANGUAGE_SELECTION}{COLOR_END}'))
                    
                    # If user input is valid:
                    if LanguageSelection._is_input_valid(user_input):
                        # Process user input.
                        LanguageSelection._process_input(user_input)
                        # Break the infinite loop.
                        break
                
                # Handle: ValueError.
                except ValueError:
                    # Skip iteration.
                    continue
                
                # Handle: KeyboardInterrupt.
                except KeyboardInterrupt:
                    # Ignore.
                    pass


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass