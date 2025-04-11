# Standard library imports.
import os

# Project-specific module imports.
from _autostart.autostarter import Autostarter
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.platform_identifier import PlatformIdentifier
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class AutostartBackup(RootScreen):
    """
    
    AutostartBackup is a screen that enables the user to:
        Start or stop the backup service.
        Schedule or de-schedule the backup service from autostarting upon system boot.

    """


    # Constant for the retrieval of screen text.
    _LOCALE = None


    @staticmethod
    def execute() -> None:
        """
        
        Description:
            Updates the locale to be used for the retrieval of screen text.
            Invokes _take_input to prompt the user into entering input.
            Starts the process of enabling or disabling the backup service.
            Invokes _navigate_forward to navigate to the next screen.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Initialize the locale constant.
        AutostartBackup._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        AutostartBackup._take_input()
        
        # Handle the process of enabling or disabling the backup service.
        Autostarter.handle_backup()
        
        # Navigate to the next screen.
        AutostartBackup._navigate_forward()


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
        SCREEN_MAIN_MENU = AutostartBackup._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_SETTINGS = AutostartBackup._LOCALE[String.LANGUAGE_KEY_SCREEN_SETTINGS]
        SCREEN_AUTOSTART_BACKUP = AutostartBackup._LOCALE[String.LANGUAGE_KEY_SCREEN_AUTOSTART_BACKUP]
        DESCRIBE_AUTOSTART_BACKUP_FOR_WINDOWS = AutostartBackup._LOCALE[String.LANGUAGE_KEY_DESCRIBE_AUTOSTART_BACKUP_FOR_WINDOWS]
        DESCRIBE_AUTOSTART_BACKUP_FOR_LINUX = AutostartBackup._LOCALE[String.LANGUAGE_KEY_DESCRIBE_AUTOSTART_BACKUP_FOR_LINUX]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*]{COLOR_END} {COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[4]{COLOR_END} {COLOR_YELLOW}{SCREEN_SETTINGS}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[5]{COLOR_END} {COLOR_YELLOW}{SCREEN_AUTOSTART_BACKUP}{COLOR_END}', end='\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Print the description for autostart backup for Windows.
            print(f'{COLOR_YELLOW}{DESCRIBE_AUTOSTART_BACKUP_FOR_WINDOWS}{COLOR_END}', end='')
        
        # If the current platform is not Windows:
        else:
            # Print the description for autostart backup for Linux.
            print(f'{COLOR_YELLOW}{DESCRIBE_AUTOSTART_BACKUP_FOR_LINUX}{COLOR_END}', end='')
        
        # Print the bottom separator.
        print(f'\n\n{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')


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
        
        # Assert if user input is equal to yes or no.
        return user_input.lower() == String.LITERAL_YES or user_input.lower() == String.LITERAL_NO


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
        from _screen.main_menu import MainMenu
        
        # Execute it.
        MainMenu.execute()


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
        
        # If user input is equal to yes:
        if user_input.lower() == String.LITERAL_YES:
            # Set the backup autostart status attribute to enabled.
            PropertiesJsonHandler.set_backup_autostart_status(String.LITERAL_ENABLED)
        
        # If user input is equal to no:
        elif user_input.lower() == String.LITERAL_NO:
            # Set the backup autostart status attribute to disabled.
            PropertiesJsonHandler.set_backup_autostart_status(String.LITERAL_DISABLED)


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
        PROMPT_AUTOSTART_BACKUP = AutostartBackup._LOCALE[String.LANGUAGE_KEY_PROMPT_AUTOSTART_BACKUP]

        # If the backup autostart status attribute is not set:
        if not PropertiesJsonHandler.is_backup_autostart_status_set():
            # Loop indefinitely.
            while True:
                # Attempt to:
                try:
                    # Display the screen.
                    AutostartBackup._display_screen()

                    # Read user input from the console window.
                    user_input = input(f'{COLOR_BLUE}{PROMPT_AUTOSTART_BACKUP}{COLOR_END}')
                    
                    # If user input is valid:
                    if AutostartBackup._is_input_valid(user_input):
                        # Process user input.
                        AutostartBackup._process_input(user_input)
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