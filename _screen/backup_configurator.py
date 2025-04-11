# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class BackupConfigurator(RootScreen):
    """

    BackupConfigurator is a screen that enables the user to either select to:
        Add a directory to the backup service.
        Add a single file to the backup service.
        Remove a directory from the backup service.
        Remove a single file from the backup service.

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
        BackupConfigurator._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        BackupConfigurator._take_input()


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
        SCREEN_MAIN_MENU = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_BACKUP_CONFIGURATOR = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_SCREEN_BACKUP_CONFIGURATOR]
        OPEN_BACKUP_CONFIGURATOR_FOR_DIRECTORY = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_OPEN_BACKUP_CONFIGURATOR_FOR_DIRECTORY]
        OPEN_BACKUP_CONFIGURATOR_FOR_SINGLE_FILE = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_OPEN_BACKUP_CONFIGURATOR_FOR_SINGLE_FILE]
        OPEN_BACKUP_REMOVER_FOR_DIRECTORY = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_OPEN_BACKUP_REMOVER_FOR_DIRECTORY]
        OPEN_BACKUP_REMOVER_FOR_SINGLE_FILE = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_OPEN_BACKUP_REMOVER_FOR_SINGLE_FILE]
        GO_BACKWARD = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_GO_BACKWARD]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*]{COLOR_END} {COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[2]{COLOR_END} {COLOR_YELLOW}{SCREEN_BACKUP_CONFIGURATOR}{COLOR_END}', end='\n')

        # Print the screen main content.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[1]{COLOR_END} {COLOR_YELLOW}{OPEN_BACKUP_CONFIGURATOR_FOR_DIRECTORY}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[2]{COLOR_END} {COLOR_YELLOW}{OPEN_BACKUP_CONFIGURATOR_FOR_SINGLE_FILE}{COLOR_END}', end='\n\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[3]{COLOR_END} {COLOR_YELLOW}{OPEN_BACKUP_REMOVER_FOR_DIRECTORY}{COLOR_END}', end='\n\n')
        print(f'{COLOR_GREEN}[4]{COLOR_END} {COLOR_YELLOW}{OPEN_BACKUP_REMOVER_FOR_SINGLE_FILE}{COLOR_END}', end='\n\n\n\n')
        print(f'{COLOR_RED}[0]{COLOR_END} {COLOR_YELLOW}{GO_BACKWARD}{COLOR_END}', end='\n\n')
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
                # Import the respective screen module.
                from _screen.backup_configurator_for_directory import BackupConfiguratorForDirectory
                
                # Execute it.
                BackupConfiguratorForDirectory.execute()
            
            # user input is equal to 2:
            case 2:
                # Import the respective screen module.
                from _screen.backup_configurator_for_single_file import BackupConfiguratorForSingleFile
                
                # Execute it.
                BackupConfiguratorForSingleFile.execute()
            
            # user input is equal to 3:
            case 3:
                # Import the respective screen module.
                from _screen.backup_remover_for_directory import BackupRemoverForDirectory
                
                # Execute it.
                BackupRemoverForDirectory.execute()
            
            # user input is equal to 4:
            case 4:
                # Import the respective screen module.
                from _screen.backup_remover_for_single_file import BackupRemoverForSingleFile
                
                # Execute it.
                BackupRemoverForSingleFile.execute()


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
            # Navigate to the previous screen.
            BackupConfigurator._navigate_backward()
        
        # If user input is not equal to 0:
        else:
            # Navigate to the next screen based on user input.
            BackupConfigurator._navigate_forward(user_input)


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
        PROMPT_BACKUP_CONFIGURATOR = BackupConfigurator._LOCALE[String.LANGUAGE_KEY_PROMPT_BACKUP_CONFIGURATOR]

        # Loop indefinitely.
        while True:
            # Attempt to:
            try:
                # Display the screen.
                BackupConfigurator._display_screen()
                
                # Read user input from the console window.
                user_input = int(input(f'{COLOR_BLUE}{PROMPT_BACKUP_CONFIGURATOR}{COLOR_END}'))
                
                # If user input is valid:
                if BackupConfigurator._is_input_valid(user_input):
                    # Process user input.
                    BackupConfigurator._process_input(user_input)
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