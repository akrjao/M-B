# Standard library imports.
import os

# Standard library from imports.
from typing import Union

# Project-specific module imports.
from _constant.string import String
from _language.language_selector import LanguageSelector
from _manager.monitoring_manager import MonitoringManager
from _miscellaneous.color import Color
from _miscellaneous.separator import Separator
from _screen.root_screen import RootScreen


class MonitoringLogViewerForSingleFile(RootScreen):
    """
    
    MonitoringLogViewerForSingleFile is a screen that lists all single files that are tracked by the monitoring service.
    Upon selection, It formats and displays the monitoring log entries for the target file. 

    """


    # Constant for the retrieval of screen text.
    _LOCALE = None

    # Variable for the storage of the target id to view.
    target_id_to_view = None


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
        MonitoringLogViewerForSingleFile._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        MonitoringLogViewerForSingleFile._take_input()


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
        SCREEN_MAIN_MENU = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_MONITORING_LOG_VIEWER = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_SCREEN_MONITORING_LOG_VIEWER]
        SCREEN_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_SCREEN_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE]
        DESCRIBE_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_ONE = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_DESCRIBE_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_ONE]
        DESCRIBE_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_TWO = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_DESCRIBE_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_TWO]

        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*] {COLOR_END}{COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[3] {COLOR_END}{COLOR_YELLOW}{SCREEN_MONITORING_LOG_VIEWER}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[2] {COLOR_END}{COLOR_YELLOW}{SCREEN_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE}{COLOR_END}', end='\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n')
        
        # If phase is equal to phase one:
        if phase == String.LITERAL_PHASE_ONE:
            # Print the description for the monitoring log viewer for single file; for phase one.
            print(f'\n{COLOR_YELLOW}{DESCRIBE_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_ONE}{COLOR_END}', end='\n\n')
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')
            
            # Display the list of monitored files with their attributes.
            MonitoringManager.display_monitored_files()
            
            # Print the bottom separator.
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        
        # If phase is not equal to phase one:
        else:
            # Print the description for the monitoring log viewer for single file; for phase two.
            print(f'\n{COLOR_YELLOW}{DESCRIBE_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_TWO}{COLOR_END}', end='\n\n')
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
            
            # Format and display the log file based on the selected target id.
            MonitoringManager.format_and_display_log_file(MonitoringLogViewerForSingleFile.target_id_to_view)
            
            # Print the bottom separator.
            print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')


    @staticmethod
    def _is_input_valid(phase: str, user_input: Union[int, str]) -> bool:
        """
        
        Description:
            Checks the value of user_input to verify its validity with respect to the phase of this screen.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            phase(str): The phase dictating which execution flow to carry out.
            user_input(Union[int, str]): Input provided by the user.
        
        Returns:
            bool: Whether user_input is valid or invalid.

        Raises:
            None
                
        """
        
        # If phase is equal to phase one:
        if phase == String.LITERAL_PHASE_ONE:
            # Assert if user input is equal to 0 or if user input is in the list of ids of monitored files.
            return user_input == 0 or user_input in MonitoringManager.get_ids_of_monitored_files()
        
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
        from _screen.monitoring_log_viewer import MonitoringLogViewer

        # Execute it.
        MonitoringLogViewer.execute()


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
    def _process_input(phase: str, user_input: Union[int, str]) -> None:
        """
        
        Description:
            Checks the value of phase and user_input to invoke other methods.
        
            Note: This method is not meant to be accessed from outside this class.

        Args:
            phase(str): The phase dictating which execution flow to carry out.
            user_input(Union[int, str]): Input provided by the user.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If phase is equal to phase one:
        if phase == String.LITERAL_PHASE_ONE:
            # If user input is equal to 0:
            if user_input == 0:
                # Navigate to the previous screen.
                MonitoringLogViewerForSingleFile._navigate_backward()
            
            # If user input is not equal to 0:
            else:
                # Assign user input to the target id to view.
                MonitoringLogViewerForSingleFile.target_id_to_view = user_input
        
        # If phase is not equal to phase one:
        else:
            # If user input is equal to yes:
            if user_input.lower() == String.LITERAL_YES:
               # Restart the current screen.
               MonitoringLogViewerForSingleFile.execute()
            
            # If user input is not equal to yes:
            else:
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
        PROMPT_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_ONE = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_PROMPT_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_ONE]
        PROMPT_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_TWO = MonitoringLogViewerForSingleFile._LOCALE[String.LANGUAGE_KEY_PROMPT_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_TWO]

        # Loop indefinitely; for phase one.
        while True:
            # Attempt to:
            try:
                # Display the screen; for phase one.
                MonitoringLogViewerForSingleFile._display_screen(String.LITERAL_PHASE_ONE)
                
                # Read user input from the console window; for phase one.
                user_input = int(input(f'{COLOR_BLUE}{PROMPT_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_ONE}{COLOR_END}'))
                
                # If user input is valid; for phase one:
                if MonitoringLogViewerForSingleFile._is_input_valid(String.LITERAL_PHASE_ONE, user_input):
                    # Process user input; for phase one.
                    MonitoringLogViewerForSingleFile._process_input(String.LITERAL_PHASE_ONE, user_input)
                    
                    # Loop indefinitely; for phase two.
                    while True:
                        # Display the screen; for phase two.
                        MonitoringLogViewerForSingleFile._display_screen(String.LITERAL_PHASE_TWO)
                        
                        # Read user input from the console window; for phase two.
                        user_input = input(f'{COLOR_BLUE}{PROMPT_MONITORING_LOG_VIEWER_FOR_SINGLE_FILE_TWO}{COLOR_END}')
                        
                        # If user input is valid; for phase two:
                        if MonitoringLogViewerForSingleFile._is_input_valid(String.LITERAL_PHASE_TWO, user_input):
                            # Process user input; for phase two.
                            MonitoringLogViewerForSingleFile._process_input(String.LITERAL_PHASE_TWO, user_input)
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