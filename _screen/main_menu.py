# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class MainMenu(RootScreen):
    """
    
    MainMenu is a screen that enables the user to either select to:
        Enter the monitoring configurator.
        Enter the backup configurator.
        Enter the monitoring log viewer.
        Enter the setting screen.

    MainMenu also provides the option to gracefully exit the application.

    """


    # Constant for the retrieval of screen text.
    _LOCALE = None


    @staticmethod
    def execute() -> None:
        """
        
        Description:
            Updates the locale to be used for the retrieval of screen text.
            Invokes _take_input to prompt the user into entering input

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Initialize the locale constant.
        MainMenu._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        MainMenu._take_input()


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
        MONITORING_SERVICE_STATUS = MainMenu._LOCALE[String.LANGUAGE_KEY_MONITORING_SERVICE_STATUS]
        BACKUP_SERVICE_STATUS = MainMenu._LOCALE[String.LANGUAGE_KEY_BACKUP_SERVICE_STATUS]
        REQUIREMENTS_STATUS = MainMenu._LOCALE[String.LANGUAGE_KEY_REQUIREMENTS_STATUS]
        SCREEN_MAIN_MENU = MainMenu._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        OPEN_MONITORING_CONFIGURATOR = MainMenu._LOCALE[String.LANGUAGE_KEY_OPEN_MONITORING_CONFIGURATOR]
        OPEN_BACKUP_CONFIGURATOR = MainMenu._LOCALE[String.LANGUAGE_KEY_OPEN_BACKUP_CONFIGURATOR]
        OPEN_MONITORING_LOG_VIEWER = MainMenu._LOCALE[String.LANGUAGE_KEY_OPEN_MONITORING_LOG_VIEWER]
        OPEN_SETTINGS = MainMenu._LOCALE[String.LANGUAGE_KEY_OPEN_SETTINGS]
        EXIT = MainMenu._LOCALE[String.LANGUAGE_KEY_EXIT]
        ENABLED = MainMenu._LOCALE[String.LANGUAGE_KEY_ENABLED]
        DISABLED = MainMenu._LOCALE[String.LANGUAGE_KEY_DISABLED]
        OK = MainMenu._LOCALE[String.LANGUAGE_KEY_OK]
        NOT_OK = MainMenu._LOCALE[String.LANGUAGE_KEY_NOT_OK]

        # Initialize the monitoring service status label based on the monitoring autostart status attribute.
        __MONITORING_SERVICE_STATUS = (
            f'{MONITORING_SERVICE_STATUS}: {COLOR_GREEN}{ENABLED}{COLOR_END}'
            if PropertiesJsonHandler.get_monitoring_autostart_status() == String.LITERAL_ENABLED else
            f'{MONITORING_SERVICE_STATUS}: {COLOR_RED}{DISABLED}{COLOR_END}'
        )

        # Initialize the backup service status label based on the backup autostart status attribute.
        __BACKUP_SERVICE_STATUS = (
            f'{BACKUP_SERVICE_STATUS}: {COLOR_GREEN}{ENABLED}{COLOR_END}'
            if PropertiesJsonHandler.get_backup_autostart_status() == String.LITERAL_ENABLED else
            f'{BACKUP_SERVICE_STATUS}: {COLOR_RED}{DISABLED}{COLOR_END}'
        )

        # Initialize the requirements status label based on the requirements status attribute.
        __REQUIREMENTS_STATUS = (
            f'{REQUIREMENTS_STATUS}: {COLOR_GREEN}{OK}{COLOR_END}'
            if PropertiesJsonHandler.get_requirements_status() == String.LITERAL_OK else
            f'{REQUIREMENTS_STATUS}: {COLOR_RED}{NOT_OK}{COLOR_END}'
        )

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the status bar at the top.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[+] {COLOR_END}{COLOR_YELLOW}{__MONITORING_SERVICE_STATUS}{COLOR_END}', end=' ')
        print(f'{COLOR_PURPLE}[+] {COLOR_END}{COLOR_YELLOW}{__BACKUP_SERVICE_STATUS}{COLOR_END}', end=' ')
        print(f'{COLOR_PURPLE}[+] {COLOR_END}{COLOR_YELLOW}{__REQUIREMENTS_STATUS}{COLOR_END}', end='\n')

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*] {COLOR_END}{COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='\n')

        # Print the screen main content.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[1] {COLOR_END}{COLOR_YELLOW}{OPEN_MONITORING_CONFIGURATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[2] {COLOR_END}{COLOR_YELLOW}{OPEN_BACKUP_CONFIGURATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[3] {COLOR_END}{COLOR_YELLOW}{OPEN_MONITORING_LOG_VIEWER}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[4] {COLOR_END}{COLOR_YELLOW}{OPEN_SETTINGS}{COLOR_END}', end='\n\n\n\n')
        print(f'{COLOR_RED}[0] {COLOR_END}{COLOR_YELLOW}{EXIT}{COLOR_END}', end='\n\n')
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

        # If user input is not in [0, 5[ :
        if user_input not in range(0,5):
            # Assert user input as invalid.
            return False
        
        # If user input is in [0, 5[ :
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
                # Import the respective screen module.
                from _screen.monitoring_configurator import MonitoringConfigurator
                
                # Execute it.
                MonitoringConfigurator.execute()
            
            # user input is equal to 2:
            case 2:
                # Import the respective screen module.
                from _screen.backup_configurator import BackupConfigurator
                
                # Execute it.
                BackupConfigurator.execute()
            
            # user input is equal to 3:
            case 3:
                # Import the respective screen module.
                from _screen.monitoring_log_viewer import MonitoringLogViewer
                
                # Execute it.
                MonitoringLogViewer.execute()
            
            # user input is equal to 4:
            case 4:
                # Import the respective screen module.
                from _screen.settings import Settings
                
                # Execute it.
                Settings.execute()


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

        # If user input is equal to 0:
        if user_input == 0:
            # Exit the application.
            exit()

        # If user input is not equal to 0:
        else:
            # Navigate to the next screen based on user input.
            MainMenu._navigate_forward(user_input)


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
        PROMPT_MAIN_MENU = MainMenu._LOCALE[String.LANGUAGE_KEY_PROMPT_MAIN_MENU]

        # Loop indefinitely.
        while True:
            # Attempt to:
            try:
                # Display the screen.
                MainMenu._display_screen()
                
                # Read user input from the console window.
                user_input = int(input(f'{COLOR_BLUE}{PROMPT_MAIN_MENU}{COLOR_END}'))
                
                # If user input is valid:
                if MainMenu._is_input_valid(user_input):
                    # Process user input.
                    MainMenu._process_input(user_input)
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