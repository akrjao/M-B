# Standard library imports.
import json
import os
import time

# Standard library from imports.
from pathlib import Path
from typing import Union

# Project-specific module imports.
from _autostart.linux_autostarter import LinuxAutostarter
from _autostart.windows_autostarter import WindowsAutostarter
from _constant.integer import Integer
from _constant.string import String
from _jsonx.monitoring_json_handler import MonitoringJsonHandler
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _manager.monitoring_manager import MonitoringManager
from _miscellaneous.platform_identifier import PlatformIdentifier
from _path.path_utils import PathUtils
from _timestamp.current_time_handler import CurrentTimeHandler
from _timestamp.meta_time_handler import MetaTimeHandler
from _user.logged_on_users_retriever import LoggedOnUsersRetriever


class MonitoringService:
    """
    
    MonitoringService is the core class for enabling the monitoring function.
    
    In a timely fashion, it:
        Creates or updates a preliminary dictionary for the storage of relevant metadata about target files and directories,
        Checks the historic last access time with the newly queried to detect access attempts.
        Checks the historic last modified time with the newly queried to detect modification attempts.

    Upon access detection, it seeks to update the respective log file for the target with an access entry.
    Upon modification detection, it seeks to update the respective log file for the target with a modified entry.
    
    MonitoringService employs exception handling to address the scenario when targets are not found,
    which ensures that the background process executing the MonitoringService does not terminate. 

    Additionally, it routinely checks the central monitoring directory for orphan files (previous log files of targets that are no longer tracked and non-log files).
    Upon the detection of orphan files, It moves them to the orphanage directory for safekeeping and for keeping the central monitoring directory clean and tidy.

    """
    

    # Constants for the storage of the wait time between monitoring iterations.
    _ITERATION_WAIT_TIME: str = Integer.MONITORING_SERVICE_ITERATION_WAIT_TIME

    # Variable for the storage of the metadata dictionary for all monitoring targets.
    _metadata_dict: dict = {}
    
    # Variable for the storage of the currently logged on users.
    _user_list: list[str] = []


    @staticmethod
    def _add_access_entry_to_monitoring_log_file(file_path: Union[str, Path]) -> None:
        """
        
        Description:
            Retrieves the formatted current timestamp.
            Retrieves the list of currently logged-on users.
            Opens the monitoring log file based on the specified file path.
            Appends an access entry to the respective monitoring log file.
            Flushes the buffer to reflect changes to the monitoring log file immediately.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path of the file that is tracked by the monitoring service.

        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        ACCESSED_AT = String.LITERAL_ACCESSED_AT
        DELIMITER = String.DELIMITER_MONITORING_LOG_FILE
        FILE_MODE_APPEND = String.FILE_MODE_APPEND
        LOG_FILEPATH = String.LITERAL_LOG_FILEPATH
        POTENTIALLY_BY = String.LITERAL_POTENTIALLY_BY
        TARGET = String.LITERAL_TARGET
        
        # Assign the current time; Formatted.
        current_time_formatted = CurrentTimeHandler.get_current_time_formatted()
        
        # Update the formatted current time for better display.
        current_time_formatted = current_time_formatted.replace('-', ':').replace('_', ' ')

        # Assign the formatted string of logged on users.
        logged_on_users_list = MonitoringService._format_logged_on_users_list()
        
        # Assign the target file name.
        target_file_name = Path(file_path).name
        
        # Open the log file path with the file mode append and assign its file descriptor.
        file = open(MonitoringService._metadata_dict[file_path][LOG_FILEPATH], FILE_MODE_APPEND)
        
        # Write the access entry to the monitoring log file.
        file.write('\n' + TARGET + target_file_name + DELIMITER + ACCESSED_AT + current_time_formatted + DELIMITER + POTENTIALLY_BY + logged_on_users_list)
        
        # Flush the buffer to reflect changes immediately.
        file.flush()
        
        # Close the file.
        file.close()


    @staticmethod
    def _add_modified_entry_to_monitoring_log_file(file_path: Union[str, Path]) -> None:
        """
        
        Description:
            Retrieves the formatted current timestampt.
            Retrieves the list of currently logged on users.
            Opens the monitoring log file based on the specified file path.
            Appends a modified entry to the respective monitoring log file.
            Flushes the buffer to reflect changes to the monitoring log file immediately.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path of the file that is tracked by the monitoring service.

        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        DELIMITER = String.DELIMITER_MONITORING_LOG_FILE
        FILE_MODE_APPEND = String.FILE_MODE_APPEND
        LOG_FILEPATH = String.LITERAL_LOG_FILEPATH
        MODIFIED_AT = String.LITERAL_MODIFIED_AT
        POTENTIALLY_BY = String.LITERAL_POTENTIALLY_BY
        TARGET = String.LITERAL_TARGET
        
        # Assign the current time; Formatted.
        current_time_formatted = CurrentTimeHandler.get_current_time_formatted()
        
        # Update the formatted current time for better display.
        current_time_formatted = current_time_formatted.replace('-', ':').replace('_', ' ')

        # Assign the formatted string of logged on users.
        logged_on_users_list = MonitoringService._format_logged_on_users_list()
        
        # Assign the target file name.
        target_file_name = Path(file_path).name
        
        # Open the log file path with the file mode append and assign its file descriptor.
        file = open(MonitoringService._metadata_dict[file_path][LOG_FILEPATH], FILE_MODE_APPEND)
        
        # Write the modified entry to the monitoring log file.
        file.write('\n' + TARGET + target_file_name + DELIMITER + MODIFIED_AT + current_time_formatted + DELIMITER + POTENTIALLY_BY + logged_on_users_list)
        
        # Flush the buffer to reflect changes immediately.
        file.flush()
        
        # Close the file.
        file.close()


    @staticmethod
    def _cleanup_monitoring_directory() -> None:
        """
        
        Description:
            Retrieves file paths of all files within the monitoring directory.
            Retrieves file paths of all monitoring log files within the monitoring directory.
            Identifies file paths of all orphan files within the monitoring directory.
            Moves orphan files to the orphanage directory located at the monitoring directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Assign the list with file paths of all files within the monitoring directory.
        file_path_list = MonitoringService._get_file_paths_for_all_files_within_monitoring_directory()

        # Assign the list with file paths of all monitoring log files.
        monitoring_log_file_path_list = MonitoringService._get_file_paths_of_all_monitoring_log_files()

        # Assign the list with file paths of orphan files.
        orphan_file_path_list = MonitoringService._get_file_paths_of_orphan_files(file_path_list, monitoring_log_file_path_list)

        # Move the orphan files to the orphanage directory.
        MonitoringService._move_orphan_files_to_orphanage(orphan_file_path_list)


    @staticmethod
    def _execute() -> None:
        """
        
        Description:
            Tracks all target files and files of target directories for access and modification attempts in a timely fashion.
            Logs the access and modification entries to the respective monitoring log files in the monitoring directory.
            
            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            None

        Raises:
            FileNotFoundError:
                If a target file is not found,
                then delegate handling to other methods.
                
        """
        
        # Constants for the storage of the string literals.
        ENABLED = String.LITERAL_ENABLED
        LOG_FILEPATH = String.LITERAL_LOG_FILEPATH
        ORPHANAGE = String.LITERAL_ORPHANAGE
        PARENT_DIRPATH = String.LITERAL_PARENT_DIRPATH
        
        # Prepare the metadata dict.
        MonitoringService._prepare_metadata()
        
        # Loop indefinitely.
        while True:
            # If the monitoring lock exists and the monitoring autostart status attribute is set to enabled:
            if MonitoringService._is_lock_exist() and PropertiesJsonHandler.get_monitoring_autostart_status() == ENABLED:
                # Assign the currently logged-on users to the user list.
                MonitoringService._user_list = LoggedOnUsersRetriever.get_logged_on_users()
                
                # For every key in the metadata dict:
                for key in MonitoringService._metadata_dict:
                    # Attempt to:
                    try:
                        # Monitor every target.
                        MonitoringService._monitor_single_file(key)
                    
                    # Handle: FileNotFoundError.
                    except FileNotFoundError:
                        # Assign the log file path of the target.
                        log_file_path = MonitoringService._metadata_dict[key][LOG_FILEPATH]
                        # Assign the parent directory path of the target.
                        parent_directory_path = MonitoringService._metadata_dict[key][PARENT_DIRPATH]
                        # Construct the orphanage directory path.
                        orphanage_directory_path = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + ORPHANAGE

                        # Handle the file not found error for the monitored file.
                        MonitoringService._handle_file_not_found_exception_for_file(key, log_file_path, orphanage_directory_path)
                        
                        # Handle the file not found error for a single file within the monitored directory.
                        MonitoringService._handle_file_not_found_exception_for_file_within_target_directory(key, log_file_path, parent_directory_path, orphanage_directory_path)
                
                # Re-prepare the metadata dict.
                MonitoringService._prepare_metadata()
            
            # If the monitoring lock does not exist or the monitoring autostart status attribute is set to disabled:
            else:
                # Re-prepare the metadata dict.
                MonitoringService._prepare_metadata()
            
            # Cleanup the monitoring directory for orphan files.
            MonitoringService._cleanup_monitoring_directory()
            
            # Wait for a few seconds.
            time.sleep(MonitoringService._ITERATION_WAIT_TIME)


    @staticmethod
    def _format_logged_on_users_list() -> str:
        """
        
        Description:
            Converts and returns the list of logged-on users as a string format.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            str: List of currently logged-on users in a string format.

        Raises:
            None
                
        """
        
        # Construct and return the string of the currently logged on users.
        return '[' + ', '.join(MonitoringService._user_list) + ']'


    @staticmethod
    def _get_file_paths_for_all_files_within_monitoring_directory() -> list[Path]:
        """
        
        Description:
            Retrieves and appends file paths of all files within the monitoring directory.
            Returns the list of file paths.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            list[Path]: List of file paths of all files within the monitoring directory.

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        MONITORING_FILENAME = String.MONITORING_FILENAME

        # Constant for the storage of the monitoring directory path.
        MONITORING_DIRECTORY_PATH = PropertiesJsonHandler.get_monitoring_directory()
    
        # Variable for the storage of a list of file paths.
        file_path_list = []

        # For every item in the monitoring directory path:
        for item in Path(MONITORING_DIRECTORY_PATH).iterdir():
            # If the item is a file and the name of the item is not equal to the monitoring file name:
            if item.is_file() and Path(item).name != MONITORING_FILENAME:
                # Resolve and append the file path to the list of the file paths.
                file_path_list.append(item.resolve())

        # Return the list of file paths.
        return file_path_list


    @staticmethod
    def _get_file_paths_of_all_monitoring_log_files() -> list[Path]:
        """
        
        Description:
            Retrieves and appends file paths of all monitoring log files within the monitoring directory.
            Returns the list of file paths.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            list[Path]: List of file paths of all monitoring log files within the monitoring directory.

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        LOG_FILEPATH = String.LITERAL_LOG_FILEPATH

        # Variable for the storage of a list of monitoring log file paths.
        monitoring_log_file_path_list = []

        # For every item in the metadata dict values:
        for item in MonitoringService._metadata_dict.values():
            # Append the log file path of the item to the monitoring log file path list.
            monitoring_log_file_path_list.append(Path(item[LOG_FILEPATH]))

        # Return the list of monitoring log file paths.
        return monitoring_log_file_path_list


    @staticmethod
    def _get_file_paths_of_orphan_files(file_path_list: list[Path], monitoring_log_file_path_list: list[Path]) -> list[Path]:
        """
        
        Description:
            Retrieves and appends file paths of all orphan files within the monitoring directory.
            Returns the list of file paths.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path_list(list[Path]): List of all file paths within the monitoring directory.
            monitoring_log_file_path_list(list[Path]): List of all file paths for monitoring log files.

        Returns:
            list[Path]: List of file paths of all orphan files within the monitoring directory.

        Raises:
            None
                
        """

        # Create and return a list of orphan files that are not being monitored.
        return [file_path for file_path in file_path_list if file_path not in monitoring_log_file_path_list]


    @staticmethod
    def _handle_file_not_found_exception_for_file(file_path: Union[str, Path], log_file_path: Union[str, Path], orphanage_directory_path: Union[str, Path]) -> None:
        """
        
        Description:
            Handles the scenario when a monitored file is not found.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path for the file that is tracked by the monitoring service.
            log_file_path(Union[str, Path]): Path for the log file respective to the file that is monitored.
            orphanage_directory_path(Union[str, Path]): Path for the orphanage directory in the monitoring directory.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of a string literal.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY

        # If the file is not monitored as part of a directory:
        if not MonitoringService._metadata_dict[file_path][AS_DIRECTORY]:
            # Copy the log file to the orphanage directory.
            PathUtils.copy_file(log_file_path, orphanage_directory_path)
            
            # Delete the log file.
            PathUtils.delete_file(log_file_path)


    @staticmethod
    def _handle_file_not_found_exception_for_file_within_target_directory(file_path: Union[str, Path], 
                                                                          log_file_path: Union[str, Path], 
                                                                          parent_directory_path: Union[str, Path], 
                                                                          orphanage_directory_path: Union[str, Path]) -> None:
        """
        
        Description:
            Handles the scenario when a file within a monitored directory is not found.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path for the file that is tracked by the monitoring service.
            log_file_path(Union[str, Path]): Path for the log file respective to the directory that is monitored.
            parent_directory_path(Union[str, Path]): Path for the parent directory of the file that is monitored.
            orphanage_directory_path(Union[str, Path]): Path for the orphanage directory in the monitoring directory.

        Returns:
            None

        Raises:
            FileNotFoundError:
                if the log file is not found,
                then ignore.
                
        """
        
        # Constant for the storage of a string literal.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY

        # If the file is monitored as part of a directory:
        if MonitoringService._metadata_dict[file_path][AS_DIRECTORY]:
            # If the parent directory path does not exist.
            if not PathUtils.is_path_exist(parent_directory_path):
                # Attempt to:
                try:
                    # Copy the log file to the orphanage directory.
                    PathUtils.copy_file(log_file_path, orphanage_directory_path)
                    
                    # Delete the log file.
                    PathUtils.delete_file(log_file_path)
                    
                    # Delete the monitoring json entry from the monitoring json file.
                    MonitoringManager.delete_monitoring_json_entry(file_path)
                
                # Handle: FileNotFoundError.
                except FileNotFoundError:
                    # Ignore.
                    pass


    @staticmethod
    def _is_file_accessed(file_path: Union[str, Path]) -> bool:
        """
        
        Description:
            Determines if a file is accessed by comparing the last access timestamp with the newly queried.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path for the file for which access attempts must be determined.

        Returns:
            bool: Whether the file specified by the file path is accessed or not.

        Raises:
            None
                
        """
        
        # Constant for the storage of string literal.
        ACCESSED_AT = String.LITERAL_ACCESSED_AT
        
        # Variable for the storage of the new last access time; Raw.
        last_access_time_new = MetaTimeHandler.get_last_access_time_raw(file_path)

        # If the last access time within the metadata dict is lower than the new last access time:
        if MonitoringService._metadata_dict[file_path][ACCESSED_AT] < last_access_time_new:
            # Update the last access time within the metadata dict to the new last access time.
            MonitoringService._metadata_dict[file_path][ACCESSED_AT] = last_access_time_new

            # Assert file as accessed.
            return True
    
        # If the last access time within the metadata dict is not lower than the new last access time:
        else:
            # Assert file as unaccessed.
            return False


    @staticmethod
    def _is_file_modified(file_path: Union[str, Path]) -> bool:
        """
        
        Description:
            Determines if a file is modified by comparing the last modified timestamp with the newly queried.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path for the file for which modification attempts must be determined.

        Returns:
            bool: Whether the file specified by the file path is modified or not.

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        ACCESSED_AT = String.LITERAL_ACCESSED_AT
        MODIFIED_AT = String.LITERAL_MODIFIED_AT

        # Variable for the storage of the new last modified time; Raw.
        last_modified_time_new = MetaTimeHandler.get_last_modified_time_raw(file_path)

        # If the last modified time within the metadata dict is lower than the new last modified time:
        if MonitoringService._metadata_dict[file_path][MODIFIED_AT] < last_modified_time_new:
            # Assign the new last access time; Raw.
            last_access_time_new = MetaTimeHandler.get_last_access_time_raw(file_path)
            
            # Update the last modified time within the metadata dict to the new last modified time.
            MonitoringService._metadata_dict[file_path][MODIFIED_AT] = last_modified_time_new
            
            # Update the last access time within the metadata dict to the new last access time.
            MonitoringService._metadata_dict[file_path][ACCESSED_AT] = last_access_time_new
        
            # Assert file as modified.
            return True
        
        # If the last modified time within the metadata dict is not lower than the new last modified time:
        else:
            # Assert file as unmodified.
            return False


    @staticmethod
    def _is_lock_exist() -> bool:
        """
        
        Description:
            Based on the current platform,
            Checks if the monitoring lock file exists.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            bool: Whether the monitoring lock exists or not.

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Assert if the monitoring lock exists for Windows.
            return WindowsAutostarter.is_monitoring_lock_exist()
        
        # If the current platform is not Windows:
        else:
            # Assert if the monitoring lock exists for Linux.
            return LinuxAutostarter.is_monitoring_lock_exist()


    @staticmethod
    def _monitor_single_file(file_path: Union[str, Path]) -> None:
        """
        
        Description:
            Checks if the file specified by the file path is modified.
            Modifies the corresponding monitoring log file to include the modified entry.
            Checks if the file specified by the file path is accessed.
            Modifies the corresponding monitoring log file to include the access entry.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path for the file to monitor by the monitoring service.

        Returns:
            None

        Raises:
            None
                
        """
            
        # If the file is modified:
        if MonitoringService._is_file_modified(file_path):
            # Add the modified entry to the monitoring log file.
            MonitoringService._add_modified_entry_to_monitoring_log_file(file_path)

        # If the file is accessed:
        elif MonitoringService._is_file_accessed(file_path):
            # Add the access entry to the monitoring log file.
            MonitoringService._add_access_entry_to_monitoring_log_file(file_path)


    @staticmethod
    def _move_orphan_files_to_orphanage(orphan_file_path_list: list[Path]) -> None:
        """
        
        Description:
            For every orphan file in the monitoring directory:
                Copies the orphan file to the orphanage directory.
                Deletes the orphan file from the monitoring directory.

            Note: This method is not meant to be accessed from outside this class.    

        Args:
            orphan_file_path_list(list[Path]): List of file paths for all orphan files.

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        ORPHANAGE = String.LITERAL_ORPHANAGE

        # Constant for the storage of the orphanage directory path.
        ORPHANAGE_DIRECTORY_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + ORPHANAGE

        # For every orphan file in the orphan file path list:
        for file_path in orphan_file_path_list:
            # Copy the orphan file to the orphanage directory.
            PathUtils.copy_file(file_path, ORPHANAGE_DIRECTORY_PATH)
            
            # Delete the orphan file.
            PathUtils.delete_file(file_path)


    @staticmethod
    def _prepare_metadata() -> None:
        """
        
        Description:
            Clears the _metadata_dict dictionary.
            Opens the monitoring json file and serializes its monitoring json data.
            For every item in the monitoring json data:
                Checks if the item path exists, otherwise deletes the corresponding monitoring json entry.
                Checks if the item is a directory to prepare and append metadata dictionary entries for its files to _metadata_dict.
                Checks if the item is a file to prepare and append its metadata dictionary entry to _metadata_dict.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        IS_DIRECTORY = String.LITERAL_IS_DIRECTORY
        PATH = String.LITERAL_PATH

        # Constant for the storage of the monitoring json file path.
        MONITORING_JSON_FILE_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + MonitoringJsonHandler.MONITORING_FILENAME

        # Clear the metadata dictionary.
        MonitoringService._metadata_dict.clear()
        
        # Variable for the storage of the monitoring json file data.
        data = {}
        
        # Open the monitoring json file path with the file mode read.
        with open(MONITORING_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            # Close the file.
            file.close()
        
        # For every key and value in the data dictionary:
        for key, value in data.items():
            # If the path exists:
            if PathUtils.is_path_exist(value[PATH]):
                # If the path represents a directory:
                if value[IS_DIRECTORY]:
                    # Prepare the metadata dict entry for the directory.
                    MonitoringService._prepare_metadata_for_directories(value)
                
                # If the path does not represent a directory:
                else:
                    # Prepare the metadata dict entry for the file.
                    MonitoringService._prepare_metadata_for_file(value)
            
            # If the path does not exist:
            else:
                # Delete the monitoring json entry from the monitoring json file.
                MonitoringManager.delete_monitoring_json_entry(key)


    @staticmethod
    def _prepare_metadata_for_directories(directory_json_entry_dict: dict) -> None:
        """
        
        Description:
            For every file within the target directory:
                Prepares attribute values for the file.
                Constructs the metadata dictionary entry by assigning values to attributes.
                Updates the _metadata_dict to include the constructed metadata dictionary entry.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            directory_json_entry_dict(dict): Properties json entry for the target directory.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        ACCESSED_AT = String.LITERAL_ACCESSED_AT
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY
        LOG_FILENAME = String.LITERAL_LOG_FILENAME
        LOG_FILEPATH = String.LITERAL_LOG_FILEPATH
        MODIFIED_AT = String.LITERAL_MODIFIED_AT
        PARENT_DIRPATH = String.LITERAL_PARENT_DIRPATH
        PATH = String.LITERAL_PATH

        # For every item in the directory path:
        for item in Path(directory_json_entry_dict[PATH]).iterdir():
            # If the item is a file:
            if item.is_file():
                # Resolve and assign the file path.
                path = item.resolve()
                # Assign the last modified time; Raw.
                modified_at = MetaTimeHandler.get_last_modified_time_raw(path)
                # Assign the last access time; Raw.
                accessed_at = MetaTimeHandler.get_last_access_time_raw(path)
                # Construct the log file path for the directory.
                log_file_path = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + directory_json_entry_dict[LOG_FILENAME]
                # Assign the directory path to be the parent directory path for the file.
                parent_directory_path = directory_json_entry_dict[PATH]

                # Construct and assign the metadata dictionary entry for the file.
                MonitoringService._metadata_dict[path] = {
                    MODIFIED_AT : modified_at,
                    ACCESSED_AT : accessed_at,
                    LOG_FILEPATH : log_file_path,
                    PARENT_DIRPATH : parent_directory_path,
                    AS_DIRECTORY : True
                }


    @staticmethod
    def _prepare_metadata_for_file(file_json_entry_dict: dict) -> None:
        """
        
        Description:
            Prepares attribute values for the file.
            Constructs the metadata dictionary entry by assigning values to attributes.
            Updates the _metadata_dict to include the constructed metadata dictionary entry.

            Note: This method is not meant to be accessed from outside this class.
            
        Args:
            file_json_entry_dict(dict): Properties json entry for the target file.

        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        ACCESSED_AT = String.LITERAL_ACCESSED_AT
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY
        LOG_FILENAME = String.LITERAL_LOG_FILENAME
        LOG_FILEPATH = String.LITERAL_LOG_FILEPATH
        MODIFIED_AT = String.LITERAL_MODIFIED_AT
        PARENT_DIRPATH = String.LITERAL_PARENT_DIRPATH
        PATH = String.LITERAL_PATH

        # Variable for the storage of the path value.
        path = file_json_entry_dict[PATH]
        # Variable for the storage of the last modified time; Raw.
        modified_at = MetaTimeHandler.get_last_modified_time_raw(path)
        # Variable for the storage of the last access time; Raw.
        accessed_at = MetaTimeHandler.get_last_access_time_raw(path)
        # Variable for the storage of the log file path.
        log_file_path = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + file_json_entry_dict[LOG_FILENAME]

        # Construct and assign the metadata dictionary entry for the file.
        MonitoringService._metadata_dict[path] = {
                MODIFIED_AT : modified_at,
                ACCESSED_AT : accessed_at,
                LOG_FILEPATH : log_file_path,
                PARENT_DIRPATH : None,
                AS_DIRECTORY : False
            }


# If this module is executed as the main program:
if __name__ == "__main__":
    # Start the monitoring service.
    MonitoringService._execute()