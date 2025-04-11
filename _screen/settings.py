# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class Settings(RootScreen):
    """

    Settings is a screen that enables the user to customize their M&B experience.
    It enables the user to access other screens for:
        The modification of language, central monitoring directory, and central backup directory.
        The starting or stopping and scheduling or de-scheduling of the monitoring service, and backup service.
        The enablement or disablement of requirements for the proper functioning of M&B.

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
        Settings._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        Settings._take_input()


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
        COLOR_RED = Color.RED

        # Initialize the separator.
        SEPARATOR = Separator.draw()

        # Initialize various label constants based on the selected language.
        SCREEN_MAIN_MENU = Settings._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_SETTINGS = Settings._LOCALE[String.LANGUAGE_KEY_SCREEN_SETTINGS]
        OPEN_LANGUAGE_SELECTION = Settings._LOCALE[String.LANGUAGE_KEY_OPEN_LANGUAGE_SELECTION]
        OPEN_MONITORING_DIRECTORY_SELECTION = Settings._LOCALE[String.LANGUAGE_KEY_OPEN_MONITORING_DIRECTORY_SELECTION]
        OPEN_BACKUP_DIRECTORY_SELECTION = Settings._LOCALE[String.LANGUAGE_KEY_OPEN_BACKUP_DIRECTORY_SELECTION]
        OPEN_AUTOSTART_MONITORING = Settings._LOCALE[String.LANGUAGE_KEY_OPEN_AUTOSTART_MONITORING]
        OPEN_AUTOSTART_BACKUP = Settings._LOCALE[String.LANGUAGE_KEY_OPEN_AUTOSTART_BACKUP]
        OPEN_REQUIREMENTS = Settings._LOCALE[String.LANGUAGE_KEY_OPEN_REQUIREMENTS]
        GO_BACKWARDS = Settings._LOCALE[String.LANGUAGE_KEY_GO_BACKWARD]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*] {COLOR_END}{COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[4] {COLOR_END}{COLOR_YELLOW}{SCREEN_SETTINGS}{COLOR_END}', end='\n')

        # Print the screen main content.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[1] {COLOR_END}{COLOR_YELLOW}{OPEN_LANGUAGE_SELECTION}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[2] {COLOR_END}{COLOR_YELLOW}{OPEN_MONITORING_DIRECTORY_SELECTION}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[3] {COLOR_END}{COLOR_YELLOW}{OPEN_BACKUP_DIRECTORY_SELECTION}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[4] {COLOR_END}{COLOR_YELLOW}{OPEN_AUTOSTART_MONITORING}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[5] {COLOR_END}{COLOR_YELLOW}{OPEN_AUTOSTART_BACKUP}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[6] {COLOR_END}{COLOR_YELLOW}{OPEN_REQUIREMENTS}{COLOR_END}', end='\n\n\n\n')
        print(f'{COLOR_RED}[0] {COLOR_END}{COLOR_YELLOW}{GO_BACKWARDS}{COLOR_END}', end='\n\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}')


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

        # If user input is not in [0, 7[ :
        if user_input not in range(0, 7):
            # Assert user input as invalid.
            return False
        
        # If user input is in [0, 7[ :
        else:
            # Assert user input as valid.
            return True


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
        from _screen.main_menu import MainMenu

        # Execute it.
        MainMenu.execute()


    @staticmethod
    def _navigate_forward(user_input: int) -> None:
        """
        
        Description:
            Checks the value of user_input to import the required screen module.
            Navigates to the next screen.
        
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
                # Unset language attribute.
                PropertiesJsonHandler.unset_language()

                # Import the respective screen module.
                from _screen.language_selection import LanguageSelection
                
                # Execute it.
                LanguageSelection.execute()
            
            # user input is equal to 2:
            case 2:
                # Unset monitoring directory attribute.
                PropertiesJsonHandler.unset_monitoring_directory()

                # Import the respective screen module.
                from _screen.monitoring_directory_selection import MonitoringDirectorySelection
                
                # Execute it.
                MonitoringDirectorySelection.execute()

            # user input is equal to 3:
            case 3:
                # Unset backup directory attribute.
                PropertiesJsonHandler.unset_backup_directory()

                # Import the respective screen module.
                from _screen.backup_directory_selection import BackupDirectorySelection
                
                # Execute it.
                BackupDirectorySelection.execute()

            # user input is equal to 4:
            case 4:
                # Unset monitoring autostart status attribute.
                PropertiesJsonHandler.unset_monitoring_autostart_status()
                
                # Import the respective screen module.
                from _screen.autostart_monitoring import AutostartMonitoring

                # Execute it.
                AutostartMonitoring.execute()

            # user input is equal to 5:
            case 5:
                # Unset backup autostart status attribute.
                PropertiesJsonHandler.unset_backup_autostart_status()
                
                # Import the respective screen module.
                from _screen.autostart_backup import AutostartBackup

                # Execute it.
                AutostartBackup.execute()
            
            # user input is equal to 6:
            case 6:
                # Unset requirements status attribute.
                PropertiesJsonHandler.unset_requirements_status()
                
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
        
        # If user_input equals 0:
        if user_input == 0:
            # Navigate to the previous screen.
            Settings._navigate_backward()

        # If user input is not equal to 0: 
        else:
            # Navigate to the next screen based on user input.
            Settings._navigate_forward(user_input)


    @staticmethod
    def _take_input() -> None:
        """

        Description:
            Repeatedly invokes _display_screen for the display of the respective screen,
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
        PROMPT_SETTINGS = Settings._LOCALE[String.LANGUAGE_KEY_PROMPT_SETTINGS]

        # Loop indefinitely.
        while True:
            # Attempt to:
            try:
                # Display the screen.
                Settings._display_screen()
                
                # Read user input from the console window.
                user_input = int(input(f'{COLOR_BLUE}{PROMPT_SETTINGS}{COLOR_END}'))
                
                # If user input is valid:
                if Settings._is_input_valid(user_input):
                    # Process user input.
                    Settings._process_input(user_input)
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