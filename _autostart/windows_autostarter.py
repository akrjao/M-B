# Standard library imports.
import os
import subprocess
import sys

# Standard library from imports.
from pathlib import Path

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _path.path_utils import PathUtils


class WindowsAutostarter:
    """
    
    WindowsAutostarter serves to start and schedule or stop and de-schedule both the monitoring and backup services on the Windows platform.
    To achieve that, WindowsAutostarter executes PowerShell commands on subprocesses, which require admin privileges that the script attempts to seek.
    WindowsAutostarter utilizes a locking mechanism to ensure that duplicate background processes are not executing.
    Besides, the locking mechanism serves to ensure that duplicate tasks are not scheduled on the task manager.

    """


    # Constant for the storage of the root directory of the script.
    ROOT_DIRECTORY: str = os.path.split(os.path.split(__file__)[0])[0]

    # Constant for the storage of the command to disable a task via PowerShell on Windows.
    _COMMAND_DISABLE_TASK_VIA_POWERSHELL_ON_WINDOWS: str = String.COMMAND_DISABLE_TASK_VIA_POWERSHELL_ON_WINDOWS

    # Constant for the storage of the command to enable a task via PowerShell on Windows.
    _COMMAND_ENABLE_TASK_VIA_POWERSHELL_ON_WINDOWS: str = String.COMMAND_ENABLE_TASK_VIA_POWERSHELL_ON_WINDOWS

    # Constant for the storage of the command to be executed.
    _COMMAND: str = None

    # Constant for the storage of the Python executable path.
    _PYTHON_EXECUTABLE_PATH: str = sys.executable
    
    # Constant for the storage of the Python script path.
    _PYTHON_SCRIPT_PATH: str = None

    # Constant for the storage of the task name.
    _TASK_NAME: str = None
    
    # Constant for the storage of the task description.
    _TASK_DESCRIPTION: str = None


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
        if WindowsAutostarter.is_backup_lock_exist():
            # Delete the backup lock.
            WindowsAutostarter._delete_backup_lock()
            
            # De-schedule the backup service from autostarting; Stop it.
            WindowsAutostarter._execute(service=BACKUP, enable=False)


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
        if WindowsAutostarter.is_monitoring_lock_exist():
            # Delete the monitoring lock.
            WindowsAutostarter._delete_monitoring_lock()
            
            # De-schedule the monitoring service from autostarting; Stop it.
            WindowsAutostarter._execute(service=MONITORING, enable=False)


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
        if not WindowsAutostarter.is_backup_lock_exist():
            # Create the backup lock.
            WindowsAutostarter._create_backup_lock()
            
            # Schedule the backup service to start on system boot; Start it.
            WindowsAutostarter._execute(service=BACKUP, enable=True)


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
        if not WindowsAutostarter.is_monitoring_lock_exist():
            # Create the monitoring lock.
            WindowsAutostarter._create_monitoring_lock()
            
            # Schedule the monitoring service to start on system boot; Start it.
            WindowsAutostarter._execute(service=MONITORING, enable=True)


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
        BACKUP_LOCK_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_LOCK_FILENAME_WINDOWS
        
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
        MONITORING_LOCK_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_LOCK_FILENAME_WINDOWS

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
        BACKUP_LOCK_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_LOCK_FILENAME_WINDOWS

        # Open the backup lock file path with the file mode create.
        with open(BACKUP_LOCK_FILE_PATH, FILE_MODE_CREATE) as file:
            # Close the file.
            file.close()
        
        # Hide the backup lock.
        PathUtils.hide_file_on_windows(BACKUP_LOCK_FILE_PATH)


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
        MONITORING_LOCK_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_LOCK_FILENAME_WINDOWS

        # Open the monitoring lock file path with file mode create.
        with open(MONITORING_LOCK_FILE_PATH, FILE_MODE_CREATE) as file:
            # Close the file.
            file.close()
        
        # Hide the monitoring lock.
        PathUtils.hide_file_on_windows(MONITORING_LOCK_FILE_PATH)


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
        BACKUP_LOCK_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_LOCK_FILENAME_WINDOWS
        
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
        MONITORING_LOCK_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_LOCK_FILENAME_WINDOWS

        # Delete the monitoring lock.
        PathUtils.delete_file(MONITORING_LOCK_FILE_PATH)


    @staticmethod
    def _execute(service: str, enable: bool) -> None:
        """
        
        Description:
            Enables and starts or disables and stops the monitoring and backup service.
            Updates properties json attributes and creates or deletes locks accordingly to reflect the status of services.

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
        POWERSHELL = String.LITERAL_POWERSHELL
        COMMAND = String.LITERAL_COMMAND
        ENABLED = String.LITERAL_ENABLED
        DISABLED = String.LITERAL_DISABLED
        MONITORING = String.LITERAL_MONITORING
        BACKUP = String.LITERAL_BACKUP

        # Constants for the storage of monitoring task parameters.
        MONITORING_TASK_NAME = String.TASK_NAME_MONITORING
        MONITORING_TASK_DESCRIPTION = String.TASK_DESCRIPTION_MONITORING

        # Constant for the storage of the monitoring service file path.
        MONITORING_SERVICE_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.MONITORING_SERVICE_FILENAME

        # Constants for the storage of backup task parameters.
        BACKUP_TASK_NAME = String.TASK_NAME_BACKUP
        BACKUP_TASK_DESCRIPTION = String.TASK_DESCRIPTION_BACKUP

        # Constants for the storage of the backup service file path.
        BACKUP_SERVICE_FILE_PATH = WindowsAutostarter.ROOT_DIRECTORY + os.path.sep + String.BACKUP_SERVICE_FILENAME

        # If the desired service is the monitoring service:
        if service == MONITORING:
            # Assign the monitoring task name.
            WindowsAutostarter._TASK_NAME = MONITORING_TASK_NAME

            # If the desired action is to enable:
            if enable:
                # Assign the monitoring task description.
                WindowsAutostarter._TASK_DESCRIPTION = MONITORING_TASK_DESCRIPTION
                # Resolve and assign the monitoring service file path.
                WindowsAutostarter._PYTHON_SCRIPT_PATH = str(Path(MONITORING_SERVICE_FILE_PATH).resolve())

        # If the desired service is the backup service:
        if service == BACKUP:
            # Assign the backup task name.
            WindowsAutostarter._TASK_NAME = BACKUP_TASK_NAME
            
            # If the desired action is to enable:
            if enable:
                # Assign the backup task description.
                WindowsAutostarter._TASK_DESCRIPTION = BACKUP_TASK_DESCRIPTION
                # Resolve and assign the backup service file path.
                WindowsAutostarter._PYTHON_SCRIPT_PATH = str(Path(BACKUP_SERVICE_FILE_PATH).resolve())

        # Formulate the command based on the desired action.
        WindowsAutostarter._formulate_command(enable)

        # Execute the command on a subprocess; Store the output.
        output = subprocess.run(
                                [POWERSHELL, COMMAND, WindowsAutostarter._COMMAND], 
                                capture_output=True, 
                                text=True
                            )

        # If the return code is equal to 0:
        if output.returncode == Integer.RETURN_CODE_SUCCESS:
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
        
        # If the return code is not equal to 0:
        else:
            # If the desired service is the monitoring service:
            if service == MONITORING:
                # If the desired action is to disable:
                if not enable:
                    # Set the monitoring autostart status attribute to enabled.
                    PropertiesJsonHandler.set_monitoring_autostart_status(ENABLED)
                    
                    # Create the monitoring lock.
                    WindowsAutostarter._create_monitoring_lock()
                
                # If the desired action is to enable:
                else:
                    # Set the monitoring autostart status attribute to disabled.
                    PropertiesJsonHandler.set_monitoring_autostart_status(DISABLED)
                    
                    # Delete the monitoring lock.
                    WindowsAutostarter._delete_monitoring_lock()
            
            # If the desired service is the backup service:
            if service == BACKUP:
                # If the desired action is to disable:
                if not enable:
                    # Set the backup autostart status attribute to enabled.
                    PropertiesJsonHandler.set_backup_autostart_status(ENABLED)
                    
                    # Create the backup lock.
                    WindowsAutostarter._create_backup_lock()
                
                # If the desired action is to enable:
                else:
                    # Set the backup autostart status attribute to disabled.
                    PropertiesJsonHandler.set_backup_autostart_status(DISABLED)
                    
                    # Delete the backup lock.
                    WindowsAutostarter._delete_backup_lock()


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
            # Format and assign the command to enable a task via PowerShell on Windows.
            WindowsAutostarter._COMMAND = WindowsAutostarter._COMMAND_ENABLE_TASK_VIA_POWERSHELL_ON_WINDOWS % (
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._PYTHON_EXECUTABLE_PATH,
                                                                                            WindowsAutostarter._PYTHON_SCRIPT_PATH,
                                                                                            WindowsAutostarter.ROOT_DIRECTORY,
                                                                                            WindowsAutostarter._TASK_DESCRIPTION,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._PYTHON_EXECUTABLE_PATH,
                                                                                            WindowsAutostarter._PYTHON_SCRIPT_PATH,
                                                                                            WindowsAutostarter.ROOT_DIRECTORY,
                                                                                            WindowsAutostarter._TASK_DESCRIPTION,
                                                                                            WindowsAutostarter._TASK_NAME
                                                                                        )
            
        # If the desired action is to disable:
        else:
            # Format and assign the command to disable a task via PowerShell on Windows.
            WindowsAutostarter._COMMAND = WindowsAutostarter._COMMAND_DISABLE_TASK_VIA_POWERSHELL_ON_WINDOWS % (
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME,
                                                                                            WindowsAutostarter._TASK_NAME
                                                                                        )


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass