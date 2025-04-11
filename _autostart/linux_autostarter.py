# Standard library imports.
import getpass
import os
import subprocess
import sys

# Standard library from imports.
from pathlib import Path

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color
from _path.path_utils import PathUtils


class LinuxAutostarter:
    """
    
    LinuxAutostarter serves to start and schedule or stop and deschedule both the monitoring or backup service on the Linux platform.
    To achieve that, LinuxAutostarter executes bash commands on subprocesses, which require root privileges that the script attempts to seek.
    LinuxAutostarter utilizes a locking mechanism to ensure that duplicate background processes are not executing.
    Besides, the locking mechanism serves to ensure that duplicate cronjobs are not scheduled on the root crontab.
    """
    
    # Constant for the storage of the root directory of the script.
    ROOT_DIRECTORY: str = os.path.split(os.path.split(__file__)[0])[0]

    # Constant for the storage of the command to disable a cronjob via shell on Linux.
    _COMMAND_DISABLE_CRONJOB_VIA_SHELL_ON_LINUX: str = String.COMMAND_DISABLE_CRONJOB_VIA_SHELL_ON_LINUX

    # Constant for the storage of the command to enable a cronjob via shell on Linux.
    _COMMAND_ENABLE_CRONJOB_VIA_SHELL_ON_LINUX: str = String.COMMAND_ENABLE_CRONJOB_VIA_SHELL_ON_LINUX

    # Constant for the storage of the command to be executed.
    _COMMAND: str = None

    # Constant for the retrieval of screen text.
    _LOCALE: dict[str, str] = LanguageSelector.get_language_dict()
    
    # Constant for the storage of the Python executable path.
    _PYTHON_EXECUTABLE_PATH: str = sys.executable

    # Constant for the storage of the Python script path.
    _PYTHON_SCRIPT_PATH: str = None
    
    # Constant for the storage of the root password.
    _ROOT_PASSWORD: str = None


    @staticmethod
    def disable_backup() -> None:
        """
        
        Description:
            Deletes the backup lock.
            Disables and stops the backup service.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        BACKUP = String.LITERAL_BACKUP
        
        # If the backup lock does exist:
        if LinuxAutostarter.is_backup_lock_exist():
            # Delete the backup lock.
            LinuxAutostarter._delete_backup_lock()
            
            # De-schedule the backup service from autostarting; Stop it.
            LinuxAutostarter._execute(service=BACKUP, enable=False)


    @staticmethod
    def disable_monitoring() -> None:
        """
        
        Description:
            Deletes the monitoring lock.
            Disables and stops the monitoring service.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        MONITORING = String.LITERAL_MONITORING

        # If the monitoring lock does exist:
        if LinuxAutostarter.is_monitoring_lock_exist():
            # Delete the monitoring lock.
            LinuxAutostarter._delete_monitoring_lock()
            
            # De-schedule the monitoring service from autostarting; Stop it.
            LinuxAutostarter._execute(service=MONITORING, enable=False)


    @staticmethod
    def enable_backup() -> None:
        """
        
        Description:
            Creates the backup lock.
            Enables and starts the backup service.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        BACKUP = String.LITERAL_BACKUP

        # If the backup lock does not exist:
        if not LinuxAutostarter.is_backup_lock_exist():
            # Create the backup lock.
            LinuxAutostarter._create_backup_lock()
            
            # Schedule the backup service to start on system boot; Start it.
            LinuxAutostarter._execute(service=BACKUP, enable=True)


    @staticmethod
    def enable_monitoring() -> None:
        """
        
        Description:
            Creates the monitoring lock.
            Enables and starts the monitoring service.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
    
        # Constant for the storage of a string literal.
        MONITORING = String.LITERAL_MONITORING

        # If the monitoring lock does not exist:
        if not LinuxAutostarter.is_monitoring_lock_exist():
            # Create the monitoring lock.
            LinuxAutostarter._create_monitoring_lock()
            
            # Schedule the monitoring service to start on system boot; Start it.
            LinuxAutostarter._execute(service=MONITORING, enable=True)


    @staticmethod
    def is_backup_lock_exist() -> bool:
        """
        
        Description:
            Checks if the backup lock file for the backup service exists in the project root directory.

        Args:
            None

        Returns:
            bool: Whether the backup lock file exists.

        Raises:
            None
                
        """

        # Constant for the storage of the backup lock file path.
        BACKUP_LOCK_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_LOCK_FILENAME_LINUX

        # Assert if the backup lock exists.
        return PathUtils.is_path_exist(BACKUP_LOCK_FILE_PATH)


    @staticmethod
    def is_monitoring_lock_exist() -> bool:
        """
        
        Description:
            Checks if the monitoring lock file for the monitoring service exists in the project root directory.

        Args:
            None

        Returns:
            bool: Whether the monitoring lock file exists.

        Raises:
            None
                
        """
        
        # Constant for the storage of the monitoring lock file path.
        MONITORING_LOCK_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_LOCK_FILENAME_LINUX
        
        # Assert if the monitoring lock exists.
        return PathUtils.is_path_exist(MONITORING_LOCK_FILE_PATH)


    @staticmethod
    def _create_backup_lock() -> None:
        """
        
        Description:
            Creates and hides the backup lock file for the backup service in the project root directory.

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

        # Constant for the storage of the backup lock file path.
        BACKUP_LOCK_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_LOCK_FILENAME_LINUX
        
        # Open the backup lock file path with file mode create.
        with open(BACKUP_LOCK_FILE_PATH, FILE_MODE_CREATE) as file:
            # Close the file.
            file.close()


    @staticmethod
    def _create_monitoring_lock() -> None:
        """
        
        Description:
            Creates and hides the monitoring lock file for the monitoring service in the project root directory.

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

        # Constant for the storage of the monitoring lock file path.
        MONITORING_LOCK_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_LOCK_FILENAME_LINUX
        
        # Open the monitoring lock file path with file mode create.
        with open(MONITORING_LOCK_FILE_PATH, FILE_MODE_CREATE) as file:
            # Close the file.
            file.close()


    @staticmethod
    def _delete_backup_lock() -> None:
        """
        
        Description:
            Deletes the backup lock file for the backup service from the project root directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of the backup lock file path.
        BACKUP_LOCK_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_LOCK_FILENAME_LINUX

        # Delete the backup lock.
        PathUtils.delete_file(BACKUP_LOCK_FILE_PATH)


    @staticmethod
    def _delete_monitoring_lock() -> None:
        """
        
        Description:
            Deletes the monitoring lock file for the monitoring service from the project root directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of the monitoring lock file path.
        MONITORING_LOCK_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_LOCK_FILENAME_LINUX

        # Delete the monitoring lock.
        PathUtils.delete_file(MONITORING_LOCK_FILE_PATH)


    @staticmethod
    def _execute(service: str, enable: bool) -> None:
        """
        
        Description:
            Enables and starts or disables and stops the monitoring and backup service.
            Updates properties attributes and creates or deletes locks accordingly to reflect the status of services.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            service(str): Service name to enable and start or disable and stop.
            enable(bool): Whether the desired action is to enable and start or disable and stop.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        ENABLED = String.LITERAL_ENABLED
        DISABLED = String.LITERAL_DISABLED
        MONITORING = String.LITERAL_MONITORING
        BACKUP = String.LITERAL_BACKUP

        # Constant for the storage of the monitoring service file path.
        MONITORING_SERVICE_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_SERVICE_FILENAME

        # Constant for the storage of the backup service file path.
        BACKUP_SERVICE_FILE_PATH = LinuxAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_SERVICE_FILENAME

        # Prompt the user into entering the root password.
        LinuxAutostarter._prompt_for_root_password()

        # If the root password is correct:
        if LinuxAutostarter._is_root_password_correct():
            # If the desired service is the monitoring service:
            if service == String.LITERAL_MONITORING:
                    # Resolve and assign the monitoring service file path.
                    LinuxAutostarter._PYTHON_SCRIPT_PATH = str(Path(MONITORING_SERVICE_FILE_PATH).resolve())

            # If the desired service is the backup service.
            if service == String.LITERAL_BACKUP:
                    # Resolve and assign the backup service file path.
                    LinuxAutostarter._PYTHON_SCRIPT_PATH = str(Path(BACKUP_SERVICE_FILE_PATH).resolve())

            # Formulate the command based on the desired action.
            LinuxAutostarter._formulate_command(enable)
            
            # Execute the command on a subprocess.
            subprocess.run(
                        LinuxAutostarter._COMMAND, 
                        capture_output=True, 
                        text=True, 
                        shell=True
                    )
            
            # If the desired service is the monitoring service:
            if service == MONITORING:
                # If the desired action is to enable:
                if enable:
                    # Set the monitoring autostart status attribute to enabled.
                    PropertiesJsonHandler.set_monitoring_autostart_status(ENABLED)
                
                # If the desired action is to disable:
                else:
                    # Set the monitoring autostart status attribute to disabled.
                    PropertiesJsonHandler.set_monitoring_autostart_status(DISABLED)
            
            # If the desired service is the backup service:
            if service == BACKUP:
                # If the desired action is to enable:
                if enable:
                    # Set the backup autostart status attribute to enabled.
                    PropertiesJsonHandler.set_backup_autostart_status(ENABLED)
                
                # If the desired action is to disable:
                else:
                    # Set the backup autostart status attribute to disabled.
                    PropertiesJsonHandler.set_backup_autostart_status(DISABLED)
        
        # If the root password is incorrect:
        else:
            # If the desired service is the monitoring service:
            if service == MONITORING:
                # If the desired action is to disable:
                if not enable:
                    # Set the monitoring autostart status attribute to enabled.
                    PropertiesJsonHandler.set_monitoring_autostart_status(ENABLED)
                    
                    # Create the monitoring lock.
                    LinuxAutostarter._create_monitoring_lock()
                
                # If the desired action is to enable:
                else:
                    # Set the monitoring autostart service attribute to disabled.
                    PropertiesJsonHandler.set_monitoring_autostart_status(DISABLED)
                    
                    # Delete the monitoring lock.
                    LinuxAutostarter._delete_monitoring_lock()
            
            # If the desired service is the backup service:
            if service == BACKUP:
                # If the desired action is to disable:
                if not enable:
                    # Set the backup autostart status attribute to enabled.
                    PropertiesJsonHandler.set_backup_autostart_status(ENABLED)
                    
                    # Create the backup lock.
                    LinuxAutostarter._create_backup_lock()
                
                # If the desired action is to enable:
                else:
                    # Set the backup autostart status attribute to disabled.
                    PropertiesJsonHandler.set_backup_autostart_status(DISABLED)
                    
                    # Delete the backup lock.
                    LinuxAutostarter._delete_backup_lock()


    @staticmethod
    def _formulate_command(enable: bool) -> None:
        """
        
        Description:
            Based on enable,
            formats the appropriate command by replacing placeholders with actual values,
            and updates the _COMMAND class variable to reflect the formulated command.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            enable(bool): Whether the desired action is to enable and start or disable and stop.
        
        Returns:
            None

        Raises:
            None
                
        """

        # If the desired action is to enable:
        if enable:
            # Format and assign the command to enable a cronjob via shell on linux.
            LinuxAutostarter._COMMAND = LinuxAutostarter._COMMAND_ENABLE_CRONJOB_VIA_SHELL_ON_LINUX % (
                                                                                                    LinuxAutostarter._ROOT_PASSWORD,
                                                                                            "'" + LinuxAutostarter.ROOT_DIRECTORY + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_EXECUTABLE_PATH + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_SCRIPT_PATH + "'",
                                                                                            "'" + LinuxAutostarter.ROOT_DIRECTORY + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_EXECUTABLE_PATH + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_SCRIPT_PATH + "'",
                                                                                            "'" + LinuxAutostarter.ROOT_DIRECTORY + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_EXECUTABLE_PATH + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_SCRIPT_PATH + "'",
                                                                                        )
        # If the desired action is to disable:
        else:
            # Format and assign the command to disable a cronjob via shell on linux.
            LinuxAutostarter._COMMAND = LinuxAutostarter._COMMAND_DISABLE_CRONJOB_VIA_SHELL_ON_LINUX % (
                                                                                                    LinuxAutostarter._ROOT_PASSWORD,
                                                                                            "'" + LinuxAutostarter.ROOT_DIRECTORY + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_EXECUTABLE_PATH + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_SCRIPT_PATH + "'",
                                                                                            "'" + LinuxAutostarter.ROOT_DIRECTORY + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_EXECUTABLE_PATH + "'",
                                                                                            "'" + LinuxAutostarter._PYTHON_SCRIPT_PATH + "'",
                                                                                                    LinuxAutostarter._PYTHON_EXECUTABLE_PATH,
                                                                                                    LinuxAutostarter._PYTHON_SCRIPT_PATH,
                                                                                                    LinuxAutostarter._PYTHON_EXECUTABLE_PATH,
                                                                                                    LinuxAutostarter._PYTHON_SCRIPT_PATH,
                                                                                        )


    @staticmethod
    def _is_root_password_correct() -> bool:
        """
        
        Description:
            Executes the superuser command on a subprocess.
            Checks if the provided root password is correct or not.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            bool: Whether the root password is correct or incorrect.

        Raises:
            None
                
        """
        
        # Constant for the storage of the superuser command on Linux.
        COMMAND_SUPERUSER_ON_LINUX = String.COMMAND_SUPERUSER_ON_LINUX

        # Constant for the storage of the superuser command input.
        COMMAND_INPUT = LinuxAutostarter._ROOT_PASSWORD + '\n'

        # Execute the command on a subprocess; Store the output.
        result = subprocess.run(
            [COMMAND_SUPERUSER_ON_LINUX],
            input=COMMAND_INPUT,
            capture_output=True,
            text=True
        )

        # If the return code is equal to 0:
        if result.returncode == Integer.RETURN_CODE_SUCCESS:
            # Assert the root password as correct.
            return True
        
        # If the return code is not equal to 0:
        else:
            # Assert the root password as incorrect.
            return False


    @staticmethod
    def _prompt_for_root_password() -> None:
        """
        
        Description:
            Prompts the user to input the root password.
            Assigns the user input to the _ROOT_PASSWORD class constant.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of colors.
        COLOR_BLUE = Color.BLUE
        COLOR_ENC = Color.ENC

        # Constant for the storage of string literal.
        PROMPT_ROOT_PASSWORD_FOR_LINUX = COLOR_BLUE + LinuxAutostarter._LOCALE[String.LANGUAGE_KEY_PROMPT_ROOT_PASSWORD_FOR_LINUX] + COLOR_ENC

        # Attempt to:
        try:

            # Prompt the user to enter the root password; Assign it.
            LinuxAutostarter._ROOT_PASSWORD = getpass.getpass(PROMPT_ROOT_PASSWORD_FOR_LINUX)

        # Handle: KeyboardInterrupt.
        except KeyboardInterrupt:
            # Move the cursor back to the start of the line.
            print('\r', end='')

            # Re-prompt the user to enter the root password;
            LinuxAutostarter._prompt_for_root_password()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass