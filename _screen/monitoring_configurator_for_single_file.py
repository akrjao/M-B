# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _jsonx.monitoring_json_handler import MonitoringJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _path.path_utils import PathUtils
from _path.path_validator import PathValidator
from _screen.root_screen import RootScreen


class MonitoringConfiguratorForSingleFile(RootScreen):
    """
    
    MonitoringConfiguratorForSingleFile is a screen that prompts the user into entering the absolute path for the target file.
    When done, the target file is monitored by the monitoring service.

    """


    # Constant for the retrieval of screen text.
    _LOCALE = None


    @staticmethod
    def execute() -> None:
        """
        
        Description:
            Updates the locale to be used for the retrieval of screen text.
            Invokes _take_input to prompt the user into entering input.
            Invokes _navigate_backward to navigate to the previous screen.
        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Initialize the locale constant.
        MonitoringConfiguratorForSingleFile._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        MonitoringConfiguratorForSingleFile._take_input()
        
        # Navigate to the previous screen.
        MonitoringConfiguratorForSingleFile._navigate_backward()


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

        # Initialize the separator.
        SEPARATOR = Separator.draw()

        # Initialize various label constants based on the selected language.
        SCREEN_MAIN_MENU = MonitoringConfiguratorForSingleFile._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_MONITORING_CONFIGURATOR = MonitoringConfiguratorForSingleFile._LOCALE[String.LANGUAGE_KEY_SCREEN_MONITORING_CONFIGURATOR]
        SCREEN_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE = MonitoringConfiguratorForSingleFile._LOCALE[String.LANGUAGE_KEY_SCREEN_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE]
        DESCRIBE_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE = MonitoringConfiguratorForSingleFile._LOCALE[String.LANGUAGE_KEY_DESCRIBE_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*] {COLOR_END}{COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[1] {COLOR_END}{COLOR_YELLOW}{SCREEN_MONITORING_CONFIGURATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[2] {COLOR_END}{COLOR_YELLOW}{SCREEN_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE}{COLOR_END}', end='\n')

        # Print the screen main content.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_YELLOW}{DESCRIBE_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE}{COLOR_END}', end='\n\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')


    @staticmethod
    def _is_input_valid(user_input: str) -> bool:
        """
        
        Description:
            Checks the value of user_input to verify its validity with respect to this screen.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            user_input(str): Input provided by the user.
        
        Returns:
            bool: Whether user_input is valid or invalid.

        Raises:
            None
                
        """
        
        # Assert if user input is equal to '0' or if user input is a valid path of a file.
        return user_input == String.LITERAL_ZERO or (PathUtils.is_file(user_input) and PathValidator.is_path_valid(user_input))


    @staticmethod
    def _navigate_backward() -> None:
        """
        
        Description:
            Imports the required screen module.
            Navigates to the previous screen.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Import the respective screen module.
        from _screen.monitoring_configurator import MonitoringConfigurator
        
        # Execute it.
        MonitoringConfigurator.execute()


    @staticmethod
    def _navigate_forward() -> None:
        """

        Note:
        
        Given that this screen extends RootScreen, and to abide by (OOP) fundamentals, all abstract methods must be implemented.
        This method is not required for this screen. Therefore, It is implemented but is given an empty body.
        
        """
        
        # Ignore.
        pass


    @staticmethod
    def _process_input(user_input: str) -> None:
        """
        
        Description:
            Checks the value of user_input to invoke other methods based on user_input.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            user_input(str): Input provided by the user.
        
        Returns:
            None

        Raises:
            None
                
        """

        # If user input is equal to '0':
        if user_input == String.LITERAL_ZERO:
            # Navigate to the previous screen.
            MonitoringConfiguratorForSingleFile._navigate_backward()
        
        # If user input is not equal to '0':
        else:
            # Add a monitoring json entry based on user input.
            MonitoringJsonHandler.add_monitoring_json_entry(user_input)


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
        PROMPT_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE = MonitoringConfiguratorForSingleFile._LOCALE[String.LANGUAGE_KEY_PROMPT_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE]

        # Loop indefinitely.
        while True:
            # Attempt to:
            try:
                # Display the screen.
                MonitoringConfiguratorForSingleFile._display_screen()
                
                # Read user input from the console window.
                user_input = input(f'{COLOR_BLUE}{PROMPT_MONITORING_CONFIGURATOR_FOR_SINGLE_FILE}{COLOR_END}')
                
                # Update user input after removing the trailing slash.
                user_input = PathUtils.remove_trailing_slash_from_path(user_input)

                # If user input is valid:
                if MonitoringConfiguratorForSingleFile._is_input_valid(user_input):
                    # Process user input.
                    MonitoringConfiguratorForSingleFile._process_input(user_input)
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