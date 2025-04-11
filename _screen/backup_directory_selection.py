# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _jsonx.backup_json_handler import BackupJsonHandler
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _path.path_utils import PathUtils
from _path.path_validator import PathValidator
from _screen.root_screen import RootScreen


class BackupDirectorySelection(RootScreen):
    """

    BackupDirectorySelection is a screen that enables the user to enter the absolute path to the central backup directory.
    The central backup directory includes the backup json file, the orphanage directory, and backup directories.    

    """


    # Constant for the retrieval of screen text.
    _LOCALE = None


    @staticmethod
    def execute() -> None:
        """
        
        Description:
            Updates the locale to be used for the retrieval of screen text.
            Invokes _take_input to prompt the user into entering input.
            Invokes _navigate_forward to navigate to the next screen.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Initialize the locale constant.
        BackupDirectorySelection._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        BackupDirectorySelection._take_input()
        
        # Navigate to the next screen.
        BackupDirectorySelection._navigate_forward()


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
        SCREEN_MAIN_MENU = BackupDirectorySelection._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_SETTINGS = BackupDirectorySelection._LOCALE[String.LANGUAGE_KEY_SCREEN_SETTINGS]
        SCREEN_BACKUP_DIRECTORY_SELECTION = BackupDirectorySelection._LOCALE[String.LANGUAGE_KEY_SCREEN_BACKUP_DIRECTORY_SELECTION]
        DESCRIBE_BACKUP_DIRECTORY = BackupDirectorySelection._LOCALE[String.LANGUAGE_KEY_DESCRIBE_BACKUP_DIRECTORY]
        
        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*]{COLOR_END} {COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[4]{COLOR_END} {COLOR_YELLOW}{SCREEN_SETTINGS}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[3]{COLOR_END} {COLOR_YELLOW}{SCREEN_BACKUP_DIRECTORY_SELECTION}{COLOR_END}', end='\n')
        
        # Print the screen main content.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_YELLOW}{DESCRIBE_BACKUP_DIRECTORY}{COLOR_END}', end='\n\n')
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
        
        # If user input is a valid path:
        if PathValidator.is_path_valid(user_input):
            # If user input is an existing path:
            if PathUtils.is_path_exist(user_input): 
                # If user input is not an empty directory:
                if not PathUtils.is_directory_empty(user_input):
                    # Assert user input as invalid.
                    return False
                
            # Assert user input as valid.
            return True
        
        # If user input is not a valid path:
        else:
            # Assert user input as invalid.
            return False


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
        from _screen.autostart_monitoring import AutostartMonitoring
        
        # Execute it.
        AutostartMonitoring.execute()


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
        
        # Set user input as the backup directory.
        PropertiesJsonHandler.set_backup_directory(user_input)
        
        # Create the directory tree based on user input.
        PathUtils.create_directory_tree(user_input)
        
        # Create the backup json file based on user input.
        BackupJsonHandler.create_backup_json_file(user_input)
        
        # Create the backup orphanage directory within the backup directory.
        BackupJsonHandler.create_backup_orphanage_directory()


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
        PROMPT_BACKUP_DIRECTORY_SELECTION = BackupDirectorySelection._LOCALE[String.LANGUAGE_KEY_PROMPT_BACKUP_DIRECTORY_SELECTION]
        
        # If the backup directory attribute is not set:
        if not PropertiesJsonHandler.is_backup_directory_set():
            # Loop indefinitely.
            while True:
                # Attempt to:
                try:
                    # Display the screen.
                    BackupDirectorySelection._display_screen()

                    # Read user input from the console window.
                    user_input = input(f'{COLOR_BLUE}{PROMPT_BACKUP_DIRECTORY_SELECTION}{COLOR_END}')

                    # Update user input after removing the trailing slash.
                    user_input = PathUtils.remove_trailing_slash_from_path(user_input)
                    
                    # If user input is valid:
                    if BackupDirectorySelection._is_input_valid(user_input):
                        # Process user input.
                        BackupDirectorySelection._process_input(user_input)
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