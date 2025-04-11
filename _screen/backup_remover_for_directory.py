# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _language.language_selector import LanguageSelector
from _manager.backup_manager import BackupManager
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class BackupRemoverForDirectory(RootScreen):
    """

    BackupRemoverForDirectory is a screen that enables the user to remove a target directory from the backup service.
    When done, the backup service no longer backs up files within the target directory upon their modification detection.
    
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
        BackupRemoverForDirectory._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        BackupRemoverForDirectory._take_input()


    @staticmethod
    def _display_screen(phase: str) -> None:
        """
        
        Description:
            Resets the console window.
            Based on phase, formats the screen text,
            and displays the screen text to the user.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            phase(str): The phase dictating which execution flow to carry out.
        
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
        SCREEN_MAIN_MENU = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_BACKUP_CONFIGURATOR = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_SCREEN_BACKUP_CONFIGURATOR]
        SCREEN_BACKUP_REMOVER_FOR_DIRECTORY = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_SCREEN_BACKUP_REMOVER_FOR_DIRECTORY]
        DESCRIBE_BACKUP_REMOVER_FOR_DIRECTORY_ONE = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_DESCRIBE_BACKUP_REMOVER_FOR_DIRECTORY_ONE]
        DESCRIBE_BACKUP_REMOVER_FOR_DIRECTORY_TWO = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_DESCRIBE_BACKUP_REMOVER_FOR_DIRECTORY_TWO]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*]{COLOR_END} {COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[2]{COLOR_END} {COLOR_YELLOW}{SCREEN_BACKUP_CONFIGURATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[3]{COLOR_END} {COLOR_YELLOW}{SCREEN_BACKUP_REMOVER_FOR_DIRECTORY}{COLOR_END}', end='\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n')

        # If phase is equal to phase one:
        if phase == String.LITERAL_PHASE_ONE:
            # Print the description for the backup remover for directory; for phase one.
            print(f'\n{COLOR_YELLOW}{DESCRIBE_BACKUP_REMOVER_FOR_DIRECTORY_ONE}{COLOR_END}', end='\n\n')
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
            
            # Display the list of backed up directories with their attributes.
            BackupManager.display_backedup_directories()
            
            # Print the bottom separator.
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        
        # If phase is not equal to phase one:
        else:
            # Print the description for the backup remover for directory; for phase two.
            print(f'\n{COLOR_YELLOW}{DESCRIBE_BACKUP_REMOVER_FOR_DIRECTORY_TWO}{COLOR_END}', end='\n\n')
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')


    @staticmethod
    def _is_input_valid(phase: str, user_input: str) -> bool:
        """
        
        Description:
            Checks the value of user_input to verify its validity with respect to the phase of this screen.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            phase(str): The phase dictating which execution flow to carry out.
            user_input(int): Input provided by the user.
        
        Returns:
            bool: Whether user_input is valid or invalid.

        Raises:
            None
                
        """
        
        # If phase is equal to phase one:
        if phase == String.LITERAL_PHASE_ONE:
            # Assert if user input is equal to '0' or if user input is in the list of ids of backed up directories.
            return user_input == String.LITERAL_ZERO or int(user_input) in BackupManager.get_ids_of_backedup_directories()
        
        # If phase is not equal to phase one:
        else:
            # Assert if user input is equal to yes or no.
            return user_input.lower() == String.LITERAL_YES or user_input.lower() == String.LITERAL_NO


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
        from _screen.backup_configurator import BackupConfigurator
        
        # Execute it.
        BackupConfigurator.execute()


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
    def _process_input(phase: str, user_input: str) -> None:
        """
        
        Description:
            Checks the value of phase and user_input to invoke other methods.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            phase(str): The phase dictating which execution flow to carry out.
            user_input(str): Input provided by the user.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If phase is equal to phase one:
        if phase == String.LITERAL_PHASE_ONE:
            # If user input is equal to '0':
            if user_input == String.LITERAL_ZERO:
                # Navigate to the previous screen.
                BackupRemoverForDirectory._navigate_backward()
            
            # If user input is not equal to '0':
            else:
                # Delete the respective backup json entry based on user input.
                BackupManager.delete_backup_json_entry(user_input)
        
        # If phase is not equal to phase one:
        else:
            # If user input is equal to yes:
            if user_input.lower() == String.LITERAL_YES:
               # Restart the current screen.
               BackupRemoverForDirectory.execute()
            
            # If user input is equal to no:
            if user_input.lower() == String.LITERAL_NO:
                # Import the respective screen module.
                from _screen.main_menu import MainMenu
                
                # Execute it.
                MainMenu.execute()


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

        # Initialize various label constants based on the selected language.
        PROMPT_BACKUP_REMOVER_FOR_DIRECTORY_ONE = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_PROMPT_BACKUP_REMOVER_FOR_DIRECTORY_ONE]
        PROMPT_BACKUP_REMOVER_FOR_DIRECTORY_TWO = BackupRemoverForDirectory._LOCALE[String.LANGUAGE_KEY_PROMPT_BACKUP_REMOVER_FOR_DIRECTORY_TWO]
        
        # Loop indefinitely; for phase one.
        while True:
            # Attempt to:
            try:
                # Display the screen; for phase one.
                BackupRemoverForDirectory._display_screen(String.LITERAL_PHASE_ONE)
                
                # Read user input from the console window; for phase one.
                user_input = input(f'{COLOR_BLUE}{PROMPT_BACKUP_REMOVER_FOR_DIRECTORY_ONE}{COLOR_END}')
                
                # If user input is valid; for phase one:
                if BackupRemoverForDirectory._is_input_valid(String.LITERAL_PHASE_ONE, user_input):
                    # Process user input; for phase one.
                    BackupRemoverForDirectory._process_input(String.LITERAL_PHASE_ONE, user_input)
                    
                    # Loop indefinitely; for phase two.
                    while True:
                        # Display the screen; for phase two.
                        BackupRemoverForDirectory._display_screen(String.LITERAL_PHASE_TWO)
                        
                        # Read user input from the console window; for phase two.
                        user_input = input(f'{COLOR_BLUE}{PROMPT_BACKUP_REMOVER_FOR_DIRECTORY_TWO}{COLOR_END}')
                        
                        # If user input is valid; for phase two:
                        if BackupRemoverForDirectory._is_input_valid(String.LITERAL_PHASE_TWO, user_input):
                            # Process user input; for phase two.
                            BackupRemoverForDirectory._process_input(String.LITERAL_PHASE_TWO, user_input)
                            # Break the infinite loop; for phase two.
                            break
                    
                    # Break the infinite loop; for phase one.
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