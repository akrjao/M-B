# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _miscellaneous.platform_identifier import PlatformIdentifier
from _miscellaneous.separator import Separator
from _requirement.windows_strict_access_time_handler import WindowsStrictAccessTimeHandler
from _screen.root_screen import RootScreen


class Requirements(RootScreen):
    """
    
    Requirements is a screen that allows the user to enable or disable requirements for the proper functioning of M&B.
    Weather on Windows or Linux, requirements pertain to the activation of strict access time. 

    """


    # Constant for the retrieval of screen text.
    _LOCALE = LanguageSelector.get_language_dict()


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
        Requirements._LOCALE = LanguageSelector.get_language_dict()
        
        # Take input from the user.
        Requirements._take_input()
        
        # Navigate to the next screen.
        Requirements._navigate_forward()


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
        COLOR_GREEN = Color.GREEN

        # Initialize the separator.
        SEPARATOR = Separator.draw()

        # Initialize various label constants based on the selected language.
        SCREEN_MAIN_MENU = Requirements._LOCALE[String.LANGUAGE_KEY_SCREEN_MAIN_MENU]
        SCREEN_SETTINGS = Requirements._LOCALE[String.LANGUAGE_KEY_SCREEN_SETTINGS]
        SCREEN_REQUIREMENTS = Requirements._LOCALE[String.LANGUAGE_KEY_SCREEN_REQUIREMENTS]

        # Initialize the operating system label based on the current platform.
        OPERATING_SYSTEM = (
            f'{COLOR_PURPLE}[+] {COLOR_END}'
            f'{COLOR_YELLOW}{Requirements._LOCALE[String.LANGUAGE_KEY_OPERATING_SYSTEM]}{COLOR_END}'
            f'{COLOR_GREEN}{String.LITERAL_WINDOWS}{COLOR_END}' if PlatformIdentifier.is_windows() 
            else 
            f'{COLOR_PURPLE}[+] {COLOR_END}'
            f'{COLOR_YELLOW}{Requirements._LOCALE[String.LANGUAGE_KEY_OPERATING_SYSTEM]}{COLOR_END}'
            f'{COLOR_GREEN}{String.LITERAL_LINUX}{COLOR_END}'
        )
        
        # Reset the console window.
        os.system(String.COMMAND_RESET_CONSOLE)

        # Print the screen header.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[*]{COLOR_END} {COLOR_YELLOW}{SCREEN_MAIN_MENU}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[4]{COLOR_END} {COLOR_YELLOW}{SCREEN_SETTINGS}{COLOR_END}', end='')
        print(f'{COLOR_PURPLE} > {COLOR_END}', end='')
        print(f'{COLOR_PURPLE}[6]{COLOR_END} {COLOR_YELLOW}{SCREEN_REQUIREMENTS}{COLOR_END}', end='\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')

        # Print the screen header.
        print(f'{COLOR_YELLOW}{OPERATING_SYSTEM}{COLOR_END}', end='\n\n')
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}', end='\n\n')

        # If phase is equal to phase one:
        if (phase == String.LITERAL_PHASE_ONE):
            # Print requirements description for Windows.
            print(Requirements._LOCALE[String.LANGUAGE_KEY_DESCRIBE_REQUIREMENTS_FOR_WINDOWS])

        # If phase is not equal to phase one:
        else:
            # Print requirements description for Linux.
            print(Requirements._LOCALE[String.LANGUAGE_KEY_DESCRIBE_REQUIREMENTS_FOR_LINUX])

        # Print the bottom separator.
        print(f'{COLOR_PURPLE}{SEPARATOR}{COLOR_END}')


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
        from _screen.monitoring_directory_selection import MonitoringDirectorySelection

        # Execute it.
        MonitoringDirectorySelection.execute()


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
            # If user input is equal to yes:
            if user_input.lower() == String.LITERAL_YES:
                # Enable strict access time on Windows.
                WindowsStrictAccessTimeHandler.enable()
            
            # If user input is equal to no:
            elif user_input.lower() == String.LITERAL_NO:
                # Disable strict access time on Windows.
                WindowsStrictAccessTimeHandler.disable()

        # If phase is not equal to phase one:
        else:
            # If user input is equal to yes:
            if user_input.lower() == String.LITERAL_YES:
                # Set requirements status attribute to ok.
                PropertiesJsonHandler.set_requirements_status(String.LITERAL_OK)
            
            # If user input is equal to no:
            elif user_input.lower() == String.LITERAL_NO:
                # Set requirements status attribute to not ok.
                PropertiesJsonHandler.set_requirements_status(String.LITERAL_NOT_OK)


    @staticmethod
    def _take_input() -> None:
        """

        Description:
            Based on the current platform,
            repeatedly invokes _display_screen for the display of the respective screen,
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
        PROMPT_REQUIREMENTS_FOR_WINDOWS = Requirements._LOCALE[String.LANGUAGE_KEY_PROMPT_REQUIREMENTS_FOR_WINDOWS]
        PROMPT_REQUIREMENTS_FOR_LINUX = Requirements._LOCALE[String.LANGUAGE_KEY_PROMPT_REQUIREMENTS_FOR_LINUX]

        # If the requirements status attribute is set:
        if not PropertiesJsonHandler.is_requirements_status_set():
            # If the current platform is Windows:
            if PlatformIdentifier.is_windows():
                # Loop indefinitely.
                while True:
                    # Display the screen.
                    Requirements._display_screen(String.LITERAL_PHASE_ONE)

                    # Attempt to:
                    try:
                        # Read user input from the console window.
                        user_input = input(f'{COLOR_BLUE}{PROMPT_REQUIREMENTS_FOR_WINDOWS}{COLOR_END}')
                        
                        # If user input is valid:
                        if Requirements._is_input_valid(user_input):
                            # Process user input.
                            Requirements._process_input(String.LITERAL_PHASE_ONE, user_input)
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

            # If the current platform is not Windows:
            else:
                # Loop indefinitely.
                while True:
                    # Attempt to:
                    try:
                        # Display the screen.
                        Requirements._display_screen(String.LITERAL_PHASE_TWO)

                        # Read user_input from the console window.
                        user_input = input(f'{COLOR_BLUE}{PROMPT_REQUIREMENTS_FOR_LINUX}{COLOR_END}')
                        
                        # If user input is valid:
                        if Requirements._is_input_valid(user_input):
                            # Process user input.
                            Requirements._process_input(String.LITERAL_PHASE_TWO, user_input)
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