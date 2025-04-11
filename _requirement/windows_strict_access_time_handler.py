# Standard library imports.
import os
import subprocess

# Project-specific module imports.
from _autostart.windows_autostarter import WindowsAutostarter
from _constant.integer import Integer
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _path.path_utils import PathUtils


class WindowsStrictAccessTimeHandler:
    """
    
    WindowsStrictAccessTimeHandler provides the necessary methods to enable strict access time on Windows.
    Strict access time is a requirement that must be enabled in order to enable accurate access and modification detection.

    WindowsStrictAccessTimeHandler enables both the enablement and disablement of strict access time,
    by executing the respective PowerShell command on a subprocess.

    Be noted, the enablement and disablement of strict access time requires admin privileges, which the script attempts to seek.

    """


    # Constant for the storage of the command for the disablement of strict access time on Windows.
    _COMMAND_DISABLE_STRICT_ACCESS_TIME_ON_WINDOWS: str = String.COMMAND_DISABLE_STRICT_ACCESS_TIME_ON_WINDOWS

    # Constant for the storage of the command for the enablement of strict access time on Windows.
    _COMMAND_ENABLE_STRICT_ACCESS_TIME_ON_WINDOWS: str = String.COMMAND_ENABLE_STRICT_ACCESS_TIME_ON_WINDOWS


    @staticmethod
    def disable() -> None:
        """
        
        Description:
            Based on various conditions,
            disables the strict access time on the platform.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Initialize various label constants.
        COMMAND = String.LITERAL_COMMAND
        NOT_OK = String.LITERAL_NOT_OK
        OK = String.LITERAL_OK
        POWERSHELL = String.LITERAL_POWERSHELL
        
        # If the requirements status attribute is not set and the strict access time lock exists:
        if not PropertiesJsonHandler.is_requirements_status_set() and WindowsStrictAccessTimeHandler._is_strict_access_time_lock_exist():
            # Execute the command on a subprocess; Store the output.
            output = subprocess.run(
                    [POWERSHELL, COMMAND, WindowsStrictAccessTimeHandler._COMMAND_DISABLE_STRICT_ACCESS_TIME_ON_WINDOWS], 
                    capture_output=True, 
                    text=True
                )
            
            # If return code is equal to 0:
            if output.returncode == Integer.RETURN_CODE_SUCCESS:
                # Set the requirements status attribute to not ok.
                PropertiesJsonHandler.set_requirements_status(NOT_OK)
                
                # Delete the strict access time lock.
                WindowsStrictAccessTimeHandler._delete_strict_access_time_lock()
            
            # If return code is not equal to 0:
            else:
                # Set the requirements status attribute to ok.
                PropertiesJsonHandler.set_requirements_status(OK)
        
        # If the requirements status is set and the strict access time lock does not exist:
        else:
            # Set the requirements status attribute to not ok.
            PropertiesJsonHandler.set_requirements_status(NOT_OK)


    @staticmethod
    def enable() -> None:
        """
        
        Description:
            Based on various conditions,
            enables the strict access time on the platform.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Initialize various label constants.
        COMMAND = String.LITERAL_COMMAND
        NOT_OK = String.LITERAL_NOT_OK
        OK = String.LITERAL_OK
        POWERSHELL = String.LITERAL_POWERSHELL

        # If the requirements status attribute is not set and the strict access time lock does not exist:
        if not PropertiesJsonHandler.is_requirements_status_set() and not WindowsStrictAccessTimeHandler._is_strict_access_time_lock_exist():
            # Execute the command on a subprocess; Store the output.
            output = subprocess.run(
                    [POWERSHELL, COMMAND, WindowsStrictAccessTimeHandler._COMMAND_ENABLE_STRICT_ACCESS_TIME_ON_WINDOWS],
                    capture_output=True,
                    text=True
                )
            
            # If the return code is not equal to 0:
            if output.returncode == Integer.RETURN_CODE_SUCCESS:
                # Set the requirements status attribute to ok.
                PropertiesJsonHandler.set_requirements_status(OK)
                
                # Create the strict access time lock.
                WindowsStrictAccessTimeHandler._create_strict_access_time_lock()
            
            # If the return code is not equal to 0:
            else:
                # Set the requirements status attribute to not ok.
                PropertiesJsonHandler.set_requirements_status(NOT_OK)
                
                # Delete the strict access time lock.
                WindowsStrictAccessTimeHandler._delete_strict_access_time_lock()
        
        # If the requirements status attribute is set and the strict access time lock exist:
        else:
            # Set the requirements status attribute to ok.
            PropertiesJsonHandler.set_requirements_status(OK)


    @staticmethod
    def _create_strict_access_time_lock() -> None:
        """
        
        Description:
            Creates the strict access time lock at the project root directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the file mode create.
        FILE_MODE_CREATE = String.FILE_MODE_CREATE

        # Constant for the storage of the strict access time lock file path.
        STRICT_ACCESS_TIME_LOCK_FILEPATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.STRICT_ACCESS_TIME_LOCK_FILENAME

        # Open the strict access time lock with file mode create.
        with open(STRICT_ACCESS_TIME_LOCK_FILEPATH, FILE_MODE_CREATE) as file:
            # Close the file.
            file.close()
        
        # Hide the strict access time lock.
        PathUtils.hide_file_on_windows(STRICT_ACCESS_TIME_LOCK_FILEPATH)


    @staticmethod
    def _delete_strict_access_time_lock() -> None:
        """
        
        Description:
            Deletes the strict access time lock from the project root directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of the strict access time lock file path.
        STRICT_ACCESS_TIME_LOCK_FILEPATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.STRICT_ACCESS_TIME_LOCK_FILENAME

        # Delete the strict access time lock.
        PathUtils.delete_file(STRICT_ACCESS_TIME_LOCK_FILEPATH)


    @staticmethod
    def _is_strict_access_time_lock_exist() -> bool:
        """
        
        Description:
            Checks if the strict access time lock exists at the project root directory.

            Note: This method is not meant to be accessed from outside this class.
            
        Args:
            None
        
        Returns:
            bool: Whether the strict access time lock exists.

        Raises:
            None
                
        """

        # Constant for the storage of the strict access time lock file path.
        STRICT_ACCESS_TIME_LOCK_FILEPATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.STRICT_ACCESS_TIME_LOCK_FILENAME      
        
        # Assert if the strict access time lock exists.
        return PathUtils.is_path_exist(STRICT_ACCESS_TIME_LOCK_FILEPATH)


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass