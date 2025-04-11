# Standard library imports.
import subprocess

# Project-specific module imports.
from _constant.string import String
from _miscellaneous.platform_identifier import PlatformIdentifier


class LoggedOnUsersRetriever:
    """

    LoggedOnUsersRetriever is responsible for the retrieval of the logged-on users in real-time.
    Depending on the platform on which the script is running, it invokes the respective command in a subprocess.
    The output of the subprocess is captured and manipulated to retrieve the list of logged-on users.
    
    """


    @staticmethod
    def get_logged_on_users() -> list[str]:
        """

        Description:
            Based on the current platform,
            executes the respective command on a subprocess,
            and retrieves the list of logged-on users.

        Args:
            None
        
        Returns:
            list[str]: List of logged-on users.

        Raises:
            None
                
        """
        
        # Constant for the storage of the command to get logged on users.
        COMMAND_GET_LOGGED_ON_USERS = None

        # Initialize various label constants.
        COMMAND = String.LITERAL_COMMAND
        POWERSHELL = String.LITERAL_POWERSHELL
        
        # Variable for the storage of command execution output.
        output = None

        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Assign the command to get logged on users on Windows.
            COMMAND_GET_LOGGED_ON_USERS = String.COMMAND_GET_LOGGED_ON_USERS_ON_WINDOWS
            
            # Execute the command on a subprocess; Store the output.
            output = subprocess.run(
                    [POWERSHELL, COMMAND, COMMAND_GET_LOGGED_ON_USERS], 
                    capture_output=True, 
                    text=True
                )
        
        # If the current platform is not Windows:
        else:
            # Assign the command to get logged on users on Linux.
            COMMAND_GET_LOGGED_ON_USERS = String.COMMAND_GET_LOGGED_ON_USERS_ON_LINUX
            
            # Execute the command on a subprocess; Store the output.
            output = subprocess.run(
                    COMMAND_GET_LOGGED_ON_USERS,
                    shell=True,
                    capture_output=True,
                    text=True
                )
        
        # Split the output by line breaks.
        return output.stdout.splitlines()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass