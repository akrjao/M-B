# Standard library imports.
import json
import os
import time

# Standard library from imports.
from datetime import datetime
from pathlib import Path
from typing import Union

# Project-specific module imports.
from _autostart.linux_autostarter import LinuxAutostarter
from _autostart.windows_autostarter import WindowsAutostarter
from _constant.integer import Integer
from _constant.string import String
from _jsonx.backup_json_handler import BackupJsonHandler
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _manager.backup_manager import BackupManager
from _miscellaneous.platform_identifier import PlatformIdentifier
from _path.path_utils import PathUtils
from _timestamp.current_time_handler import CurrentTimeHandler
from _timestamp.meta_time_handler import MetaTimeHandler


class BackupService:
    """

    BackupService is the core class for enabling the backup function.
    
    In a timely fashion, it:
        Creates or updates a preliminary dictionary for the storage of relevant metadata about target files and directories,
        Checks the historic last modified time with the newly queried to detect modification attempts.

    Upon modification detection, it seeks to create a backup file at the respective backup directory within the central backup directory.
    
    BackupService employs exception handling to address the scenario when targets are not found,
    which ensures that the background process executing the BackupService does not terminate. 

    Additionally, it routinely checks the central backup directory for orphan directories (previous backup directories of targets that are no longer tracked and non-backup directories).
    Upon the detection of orphan directories, It moves them to the orphanage directory for safekeeping and for keeping the central backup directory clean and tidy.

    """

    # Constants for the storage of the wait time between backup iterations.
    _ITERATION_WAIT_TIME: int = Integer.BACKUP_SERVICE_ITERATION_WAIT_TIME
    
    # Variable for the storage of the metadata dictionary for all backed up targets.
    _metadata_dict: dict = {}


    @staticmethod
    def _backup_single_file(file_path: Union[str, Path]) -> None:
        """
        
        Description:
            Checks if the file specified by the file path is modified.
            Creates the timestamped backup of the file at the target file path within the backup directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path for the file to track by the backup service.

        Returns:
            None

        Raises:
            None
                
        """

        # If the file is modified:
        if BackupService._is_file_modified(file_path):
            # Formulate and assign the file path for the backed up file.
            target_file_path_for_backedup_file = BackupService._formulate_target_file_path_for_backedup_file(file_path)

            # Attempt to:
            try:
                # Create the backup file at the target backup file path.
                BackupJsonHandler.create_backup_file(file_path, target_file_path_for_backedup_file)

            # Handle: FileNotFoundError.
            except FileNotFoundError:
                # Retrieve the directory path from the target file path for the backedup file.
                target_directory_path_for_backedup_file = os.path.dirname(target_file_path_for_backedup_file)

                # Create the directory for the backedup file.
                PathUtils.create_directory_tree(target_directory_path_for_backedup_file)

                # Create the backup file at the target backup file path.
                BackupJsonHandler.create_backup_file(file_path, target_file_path_for_backedup_file)


    @staticmethod
    def _cleanup_backup_directory() -> None:
        """
        
        Description:
            Retrieves the paths of all directories within the backup directory.
            Retrieves the paths of all backup directories within the backup directory.
            Identifies paths of all orphan directories within the backup directory.
            Moves orphan directories to the orphanage directory located at the backup directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """

        # Assign the list with directory paths of all directories within the backup directory.
        directory_path_list = BackupService._get_directory_paths_of_all_directories_within_backup_directory()
        
        # Assign the list with directory paths of all backups.
        backup_directory_path_list = BackupService._get_paths_of_all_backup_items()

        # Assign the list with directory paths of orphan directories.
        orphan_directory_path_list = BackupService._get_directory_paths_of_orphan_items(directory_path_list, backup_directory_path_list)
        
        # Move the orphan directories to the orphanage directory.
        BackupService._move_orphan_directories_to_orphanage(orphan_directory_path_list)


    @staticmethod
    def _establish_backup_directory_for_target_directory_files(path: str, backup_directory_path: Union[str, Path], backup_parent_directory_path: str) -> None:
        """
        
        Description:
            Creates the parent backup directory for files that are within the tracked directory.
            Creates the backup for the file specified by the path in its backup directory that is located in its backup parent directory.
            
            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(str): Path of the file that is being tracked by the backup service.
            backup_directory_path(Union[str, Path]): Path of the backup directory respective to the file being tracked.
            backup_parent_directory_path(str): Path of the backup parent directory respective to the file being tracked.

        Returns:
            None

        Raises:
            None
                
        """

        # If the backup directory does not exist:
        if not PathUtils.is_path_exist(backup_directory_path):
            # Assign the current time; Formatted.
            current_time_formatted = CurrentTimeHandler.get_current_time_formatted()

            # Construct the backup file path.
            #backup_file_path = backup_parent_directory_path + backup_directory_path + os.path.sep + BackupJsonHandler.prepare_backup_filename(path, current_time_formatted)

            backup_file_path = backup_directory_path + os.path.sep + BackupJsonHandler.prepare_backup_filename(path, current_time_formatted)


            # Create the parent directory tree for the backup directory.
            PathUtils.create_directory_tree(backup_directory_path)
            
            # Create the backup directory and the backup file; Timestamped.
            BackupJsonHandler.create_backup_file(path, backup_file_path)


    @staticmethod
    def _execute() -> None:
        """
        
        Description:
            Tracks all target files and files of target directories for modification attempts in a timely fashion.
            Backups all target files and files of target directories upon modification detection in the backup directory.

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
        BACKUP_DIRPATH = String.LITERAL_BACKUP_DIRPATH
        BACKUP_PARENT_DIRPATH = String.LITERAL_BACKUP_PARENT_DIRPATH
        ENABLED = String.LITERAL_ENABLED
        ORPHANAGE = String.LITERAL_ORPHANAGE
        PARENT_DIRPATH = String.LITERAL_PARENT_DIRPATH
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY

        # Prepare the metadata dict.
        BackupService._prepare_metadata()
        
        # Loop indefinitely.
        while True:
            # If the backup lock exists and the backup autostart status attribute is set to enabled:
            if BackupService._is_lock_exist() and PropertiesJsonHandler.get_backup_autostart_status() == ENABLED:
                # For every key in the metadata dict:
                for key in BackupService._metadata_dict:
                    # Attempt to:
                    try:
                        # Backup every target.
                        BackupService._backup_single_file(key)
                    
                    # Handle: FileNotFoundError.
                    except FileNotFoundError:
                        # Assign the backup directory of the target.
                        backup_directory_path = BackupService._metadata_dict[key][BACKUP_DIRPATH]
                        # Assign the backup parent directory of the target.
                        backup_parent_directory_path = BackupService._metadata_dict[key][BACKUP_PARENT_DIRPATH]
                        # Assign the parent directory of the target.
                        parent_directory_path = BackupService._metadata_dict[key][PARENT_DIRPATH]
                        # Construct the orphanage directory path.
                        orphanage_directory_path = PropertiesJsonHandler.get_backup_directory() + os.path.sep + ORPHANAGE

                        # If the target is part of a directory:
                        if BackupService._metadata_dict[key][AS_DIRECTORY]:
                            # Construct the backup directory path within the orphanage directory.
                            backup_directory_path_within_orphanage_directory = orphanage_directory_path + os.path.sep + os.path.split(BackupService._metadata_dict[key][BACKUP_PARENT_DIRPATH])[1]
                        
                        # If the target is not part of a directory: 
                        else:
                            # Ignore.
                            backup_directory_path_within_orphanage_directory = None

                        # Handle the file not found error for the backed up file.
                        BackupService._handle_file_not_found_exception_for_file(key, backup_directory_path, orphanage_directory_path)
                        
                        # Handle the file not found error for a single file within the backed up directory.
                        BackupService._handle_file_not_found_exception_for_file_within_target_directory(key, parent_directory_path, backup_directory_path, backup_directory_path_within_orphanage_directory)

                        # Handle the file not found error for a non-existing directory.
                        BackupService._handle_file_not_found_exception_for_non_existing_target_directory(key, parent_directory_path, backup_directory_path, backup_parent_directory_path, backup_directory_path_within_orphanage_directory)
                
                # Re-prepare the metadata dict.
                BackupService._prepare_metadata()
            
            # If the backup lock does not exist or the backup autostart status attribute is set to disabled:
            else:
                # Re-prepare the metadata dict.
                BackupService._prepare_metadata()
            
            # Cleanup the backup directory for orphan directories.
            BackupService._cleanup_backup_directory()
            
            # Wait for a few seconds.
            time.sleep(BackupService._ITERATION_WAIT_TIME)


    @staticmethod
    def _formulate_target_file_path_for_backedup_file(file_path: Union[str, Path]) -> str:
        """
        
        Description:
            Constructs the backup file path for the target file that is tracked by the backup service.
            Returns the backup file path.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(Union[str, Path]): Path of the file that is tracked by the backup service.

        Returns:
            str: Constructed backup file path for the target file.

        Raises:
            None
                
        """


        # Constants for the storage of string literals.
        BACKUP_DIRPATH = String.LITERAL_BACKUP_DIRPATH
        BACKUP_FILE_EXTENSION = String.BACKUP_FILE_EXTENSION
        FORMAT_LAST_MODIFIED_TIME = String.FORMAT_LAST_MODIFIED_TIME

        # Assign the current time; Raw.
        current_time_raw = CurrentTimeHandler.get_current_time_raw()

        # Calculate the actual modification time by subtracting the backup iteration wait time.
        modification_time = current_time_raw - BackupService._ITERATION_WAIT_TIME

        # Construct the backed up file path; Backup parent directory.
        target_file_path_for_backedup_file = BackupService._metadata_dict[file_path][BACKUP_DIRPATH] + os.path.sep + Path(file_path).name
        # Construct the backed up file path; Backup parent directory + Backup directory + Backup file name.
        target_file_path_for_backedup_file = target_file_path_for_backedup_file #+ os.path.sep + Path(file_path).name
        # Construct the backed up file path; Backup parent directory + Backup directory + Backup file name + Modification timestamp.
        target_file_path_for_backedup_file = target_file_path_for_backedup_file + "_" + datetime.fromtimestamp(modification_time).strftime(FORMAT_LAST_MODIFIED_TIME)
        # Construct the backed up file path; Backup parent directory + Backup directory + Backup file name + Modification timestamp + Backup file extension.
        target_file_path_for_backedup_file = target_file_path_for_backedup_file + BACKUP_FILE_EXTENSION

        # Return the constructed file path for the backed up file.
        return target_file_path_for_backedup_file


    @staticmethod
    def _get_directory_paths_of_all_directories_within_backup_directory() -> list[Path]:
        """
        
        Description:
            Retrieves and appends the paths of all directories within the backup directory.
            Returns the list of directory paths.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            list[Path]: List of paths of all directories within the backup directory.

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        ORPHANAGE = String.LITERAL_ORPHANAGE

        # Constant for the storage of the backup directory path.
        BACKUP_DIRECTORY_PATH = PropertiesJsonHandler.get_backup_directory()
       
        # Variable for the storage of a list of directory paths.
        directory_path_list = []
       
        # For every item in the backup directory path:
        for item in Path(BACKUP_DIRECTORY_PATH).iterdir():
            # If the item is not a file and the item name is not equal to the orphanage directory name:
            if not item.is_file() and Path(item).name != ORPHANAGE:
                # Resolve and append the directory path to the list of directory paths.
                directory_path_list.append(item.resolve())
        
        # Return the list of directory paths.
        return directory_path_list


    @staticmethod
    def _get_directory_paths_of_orphan_items(directory_path_list: list[Path], backedup_directory_path_list: list[Path]) -> list[Path]:
        """
        
        Description:
            Retrieves and appends file paths of all orphan directories within the backup directory.
            Returns the list of directory paths.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            directory_path_list(list[Path]): List of all directory paths within the backup directory.
            backedup_directory_path_list(list[Path]): List of all directory paths for backups.

        Returns:
            list[Path]: List of directory paths of all orphan items within the backup directory.

        Raises:
            None
                
        """
        
        # Create and return a list of orphan directories that are not being backed up.
        return [directory_path for directory_path in directory_path_list if directory_path not in backedup_directory_path_list]


    @staticmethod
    def _get_paths_of_all_backup_items() -> list[Path]:
        """
        
        Description:
            Retrieves and appends file paths of all backup directories within the backup directory.
            Returns the list of directory paths.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            list[Path]: List of directory paths of all backups within the backup directory.

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY
        BACKUP_DIRPATH = String.LITERAL_BACKUP_DIRPATH

        # Variable for the storage of a list of backed up directory paths.
        backedup_directory_path_list = []
        
        # For every item in the metadata dict:
        for item in BackupService._metadata_dict.values():
            # If the file is backed up as part of a directory:
            if item[AS_DIRECTORY]:
                # Append the path of the parent backup directory.
                backedup_directory_path_list.append(Path(os.path.dirname(item[BACKUP_DIRPATH])))
            
            # If the file is not backed up as part of a directory:
            else:
                # Append the path of the backup directory.
                backedup_directory_path_list.append(Path(item[BACKUP_DIRPATH]))

        # Return the list of backed up directory paths.
        return backedup_directory_path_list


    @staticmethod
    def _handle_file_not_found_exception_for_file(path: Union[str, Path], backup_directory_path: Union[str, Path], orphanage_directory_path: Union[str, Path]) -> None:
        """
        
        Description:
            Handles the scenario when a tracked file is not found.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(Union[str, Path]): Path for the file that is tracked by the backup service.
            backup_directory_path(Union[str, Path]): Path for the backup directory respective to the tracked file.
            orphanage_directory_path(Union[str, Path]): Path for the orphanage directory in the backup directory.

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY

        # If the file is not backed up as part of a directory:
        if not BackupService._metadata_dict[path][AS_DIRECTORY]:
            # Copy the backup directory to the orphanage directory.
            PathUtils.copy_directory(backup_directory_path, orphanage_directory_path)
            
            # Delete the backup directory.
            PathUtils.delete_directory_tree(backup_directory_path)


    @staticmethod
    def _handle_file_not_found_exception_for_file_within_target_directory(path: Union[str, Path], 
                                                                          parent_directory_path: Union[str, Path], 
                                                                          backup_directory_path: Union[str, Path], 
                                                                          backup_parent_directory_path_within_orphanage_directory: Union[str, Path]) -> None:
        """
        
        Description:
            Handles the scenario when a file within a tracked directory is not found, but the tracked directory exists.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(Union[str, Path]): Path for the file that is tracked by the backup service.
            parent_directory_path(Union[str, Path]): Path for the parent directory respective to the tracked file.
            backup_directory_path(Union[str, Path]): Path for the backup directory respective to the tracked file.
            backup_parent_directory_path_within_orphanage_directory(Union[str, Path]): Path for the backup parent directory,
                                                                                       located inside the orphanage directory respective to the tracked file.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of a string literal.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY
        
        # If the file is backed up as part of a directory:
        if BackupService._metadata_dict[path][AS_DIRECTORY]:
            # If the parent directory path exists:
            if PathUtils.is_path_exist(parent_directory_path):
                # Copy the backup directory to the backup parent directory within the orphanage directory.
                PathUtils.copy_directory(backup_directory_path, backup_parent_directory_path_within_orphanage_directory)
                
                # Delete the backup directory.
                PathUtils.delete_directory_tree(backup_directory_path)


    @staticmethod
    def _handle_file_not_found_exception_for_non_existing_target_directory(path: Union[str, Path],
                                                                           parent_directory_path: Union[str, Path],
                                                                           backup_directory_path: Union[str, Path],
                                                                           backup_parent_directory_path: Union[str, Path],
                                                                           backup_directory_path_within_orphanage_directory: Union[str, Path]) -> None:
        """
        
        Description:
            Handles the scenario when a file within a tracked directory is not found because the tracked directory is not found.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(Union[str, Path]): Path for the file that is tracked by the backup service.
            parent_directory_path(Union[str, Path]): Path for the parent directory respective to the tracked file.
            backup_directory_path(Union[str, Path]): Path for the backup directory respective to the tracked file.
            backup_parent_directory_path(Union[str, Path]): Path for the parent backup directory respective to the tracked file.
            backup_directory_path_within_orphanage_directory(Union[str, Path]): Path for the backup directory,
                                                                                located inside the orphanage directory respective to the tracked file.

        Returns:
            None

        Raises:
            None
                
        """

        # Constant for the storage of a string literal.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY

        # If the file is backed up as part of a directory:
        if BackupService._metadata_dict[path][AS_DIRECTORY]:
            # If the parent directory does not exist:
            if not PathUtils.is_path_exist(parent_directory_path):
                # Copy the backup directory to the backup directory within the orphanage directory.
                PathUtils.copy_directory(backup_directory_path, backup_directory_path_within_orphanage_directory)
                
                # Delete the backup json entry from the backup json file.
                BackupManager.delete_backup_json_entry(path)


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
        MODIFIED_AT = String.LITERAL_MODIFIED_AT

        # Variable for the storage of the new last modified time; Raw.
        last_modified_time_new = MetaTimeHandler.get_last_modified_time_raw(file_path)

        # If the last modified time within the metadata dict is lower than the new last modified time:
        if BackupService._metadata_dict[file_path][MODIFIED_AT] < last_modified_time_new:
            # Update the last modified time within the metadata dict to the new last modified time.
            BackupService._metadata_dict[file_path][MODIFIED_AT] = last_modified_time_new
        
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
            Checks if the backup lock file exists.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            bool: Whether the backup lock exists or not.

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Assert if the backup lock exists for Windows.
            return WindowsAutostarter.is_backup_lock_exist()
        
        # If the current platform is not Windows:
        else:
            # Assert if the backup lock exists for Linux.
            return LinuxAutostarter.is_backup_lock_exist()


    @staticmethod
    def _move_orphan_directories_to_orphanage(orphan_directory_path_list: list[Path]) -> None:
        """
        
        Description:
            For every orphan directory in the backup directory:
                Copies the orphan directory to the orphanage directory.
                Deletes the orphan directory from the backup directory.

            Note: This method is not meant to be accessed from outside this class.    

        Args:
            orphan_directory_path_list(list[Path]): List of paths for all orphan directories.

        Returns:
            None

        Raises:
            PermissionError:
                If the orphan directory path is inaccessible,
                then ignore.
                
        """

        # Constant for the storage of a string literal.
        ORPHANAGE = String.LITERAL_ORPHANAGE

        # Constant for the storage of the orphanage directory path.
        ORPHANAGE_DIRECTORY_PATH = PropertiesJsonHandler.get_backup_directory() + os.path.sep + ORPHANAGE

        # For every orphan directory in the orphan directory path list:
        for directory_path in orphan_directory_path_list:
            # If the orphan directory is not empty:
            if not PathUtils.is_directory_empty(directory_path):
                # Attempt to:
                try:
                    # For every item in the directory:
                    for item in directory_path.iterdir():
                        # If the item is a directory:
                        if item.is_dir():
                            # Construct the orphanage directory path for the sub directory.
                            ORPHANAGE_DIRECTORY_PATH_FOR_SUB_DIRECTORY = ORPHANAGE_DIRECTORY_PATH + os.path.sep + PathUtils.get_filename(str(directory_path))
                            # Copy the orphan sub directory to the orphanage directory.
                            PathUtils.copy_directory(item.resolve(), ORPHANAGE_DIRECTORY_PATH_FOR_SUB_DIRECTORY)
                        
                        # If the item is a file:
                        if item.is_file():
                            # Copy the orphan directory to the orphanage directory.
                            PathUtils.copy_directory(directory_path, ORPHANAGE_DIRECTORY_PATH)
                
                # Handle: PermissionError.
                except PermissionError:
                    # Ignore.
                    pass
            
            # Delete the directory tree of the orphan directory.
            PathUtils.delete_directory_tree(directory_path)


    @staticmethod
    def _prepare_metadata() -> None:
        """
        
        Description:
            Clears the _metadata_dict dictionary.
            Opens the backup json file and serializes its backup json data.
            For every item in the backup json data:
                Checks if the item path exists, otherwise deletes the corresponding backup json entry.
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

        # Constant for the storage of the backup json file path.
        BACKUP_JSON_FILE_PATH = PropertiesJsonHandler.get_backup_directory() + os.path.sep + BackupJsonHandler.BACKUP_FILENAME

        # Variable for the storage of the backup json file data.
        data = {}
        
        # Clear the metadata dictionary.
        BackupService._metadata_dict.clear()

        # Open the backup json file path with the file mode read.
        with open(BACKUP_JSON_FILE_PATH, FILE_MODE_READ) as file:
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
                    BackupService._prepare_metadata_for_directories(value)

                # If the path does not represent a directory:
                else:
                    # Prepare the metadata dict entry for the file.
                    BackupService._prepare_metadata_for_file(value)

            # If the path does not exist:
            else:
                # Delete the backup json entry from the backup json file.
                BackupManager.delete_backup_json_entry(key)


    @staticmethod
    def _prepare_metadata_for_directories(directory_json_entry_dict: dict) -> None:
        """
        
        Description:
            For every file within the target directory:
                Prepares attribute values for the file.
                Constructs the metadata dictionary entry by assigning values to attributes.
                Updates the _metadata_dict to include the constructed metadata dictionary entry.
                Creates the backup directory tree.
                Creates the backup for the file within the respective backup directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            directory_json_entry_dict(dict): Properties json entry for the target directory.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME
        BACKUP_DIRPATH = String.LITERAL_BACKUP_DIRPATH
        BACKUP_PARENT_DIRPATH = String.LITERAL_BACKUP_PARENT_DIRPATH
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
                # Construct the backup parent directory path for the directory.
                backup_parent_directory_path = PropertiesJsonHandler.get_backup_directory() + os.path.sep + directory_json_entry_dict[BACKUP_DIRNAME]
                # Construct the backup directory path for the file.
                backup_directory_path = backup_parent_directory_path + os.path.sep + PathUtils.get_filename(str(path)) + '_' + directory_json_entry_dict[BACKUP_DIRNAME].split('_')[-1]
                # Assign the directory path to be the parent directory path for the file.
                parent_directory_path = directory_json_entry_dict[PATH]
                
                # Construct and assign the metadata dictionary entry for the file.
                BackupService._metadata_dict[path] = {
                        MODIFIED_AT : modified_at,
                        BACKUP_PARENT_DIRPATH : backup_parent_directory_path,
                        BACKUP_DIRPATH : backup_directory_path,
                        PARENT_DIRPATH : parent_directory_path,
                        AS_DIRECTORY : True
                    } 

                # Create the backup directory tree and the backup file.
                BackupService._establish_backup_directory_for_target_directory_files(str(path), backup_directory_path, backup_parent_directory_path)


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
        AS_DIRECTORY = String.LITERAL_AS_DIRECTORY
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME
        BACKUP_DIRPATH = String.LITERAL_BACKUP_DIRPATH
        BACKUP_PARENT_DIRPATH = String.LITERAL_BACKUP_PARENT_DIRPATH
        MODIFIED_AT = String.LITERAL_MODIFIED_AT
        PARENT_DIRPATH = String.LITERAL_PARENT_DIRPATH
        PATH = String.LITERAL_PATH

        # Variable for the storage of the path value.
        path = file_json_entry_dict[PATH]
        # Variable for the storage of the last modified time; Raw.
        modified_at = MetaTimeHandler.get_last_modified_time_raw(path)
        # Variable for the storage of the backup directory path.
        backup_directory_path = PropertiesJsonHandler.get_backup_directory() + os.path.sep + file_json_entry_dict[BACKUP_DIRNAME]

        # Construct and assign the metadata dictionary entry for the file.
        BackupService._metadata_dict[path] = {
                MODIFIED_AT : modified_at,
                BACKUP_PARENT_DIRPATH : None,
                BACKUP_DIRPATH : backup_directory_path,
                PARENT_DIRPATH : None,
                AS_DIRECTORY : False
            }


# If this module is executed as the main program:
if __name__ == "__main__":
    # Start the backup service.
    BackupService._execute()