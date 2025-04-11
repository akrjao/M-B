# Standard library imports.
import json
import os

# Standard library from imports.
from pathlib import Path

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _path.path_utils import PathUtils
from _timestamp.current_time_handler import CurrentTimeHandler
from _user.current_user_retriever import CurrentUserRetriever


class BackupJsonHandler:
    """

    BackupJsonHandler essentially serves to manage the backup json file found under the central backup directory.

    """


    # Constant for the storage of the backup json file name.
    BACKUP_FILENAME: str = String.BACKUP_FILENAME


    @staticmethod
    def add_backup_json_entry(path: str) -> None:
        """
        
        Description:
            Opens and serializes the backup json file.
            Invokes _create_backup_json_entry to create the backup json entry.
            Modifies the serialized backup json data to append the created backup json entry.
            Opens and writes the modified backup json data to the backup json file.
            Creates the respective backup at the central backup directory.

        Args:
            path(str): Path for the item to be tracked by the backup service.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the backup directory path. 
        BACKUP_DIRECTORY_PATH = PropertiesJsonHandler.get_backup_directory() + os.path.sep
        
        # Constant for the storage of the backup json file path.
        BACKUP_JSON_FILEPATH = BACKUP_DIRECTORY_PATH + BackupJsonHandler.BACKUP_FILENAME

        # Constants for the storage of string literals.
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME
        IS_DIRECTORY = String.LITERAL_IS_DIRECTORY
        FILE_MODE_READ = String.FILE_MODE_READ
        FILE_MODE_WRITE = String.FILE_MODE_WRITE

        # Constant for the storage of an integer literal.
        JSON_INDENT = Integer.JSON_INDENT

        # Variable for the storage of the backup json file data.
        data = {}
        
        # Open the backup json file path with file mode read.
        with open(BACKUP_JSON_FILEPATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            # Close the file.
            file.close()
        
        # Create the backup json entry.
        json_entry = BackupJsonHandler._create_backup_json_entry(path)
        # Create a random string suffix.
        suffix = String.generate_random_string()

        # Modify the backup directory name attribute to include the suffix.
        json_entry[BACKUP_DIRNAME] = json_entry[BACKUP_DIRNAME] + '_' + suffix
        # Add the json entry as the last element of the data dict.
        data[len(data) + 1] = json_entry

        # Open the backup json file path with file mode write.
        with open(BACKUP_JSON_FILEPATH, FILE_MODE_WRITE) as file:
            # Write the data dictionary to the file.
            json.dump(data, file, indent=JSON_INDENT)
            # Close the file.
            file.close()

        # If the json entry is for a file:
        if not json_entry[IS_DIRECTORY]:
            # Add a backup json entry for a file.
            BackupJsonHandler._add_backup_json_entry_for_file(json_entry, path)
        
        # If the json entry is for a directory:
        else:
            # Add a backup json entry for a directory.
            BackupJsonHandler._add_backup_json_entry_for_directory(json_entry, suffix)


    @staticmethod
    def create_backup_file(target_file_path: str, backup_file_path: str) -> None:
        """
        
        Description:
            Creates the backup file specified by the backup file path.
            Copies the content of the target file to the backup file.

        Args:
            target_file_path(str): Path for the target file (source).
            backup_file_path(str): Path for the backup file (destination).

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the file mode create.
        FILE_MODE_CREATE = String.FILE_MODE_CREATE
        
        try:

            # Open the backup file path with file mode create.
            with open(backup_file_path, FILE_MODE_CREATE) as file:
                # Close the file.
                file.close()
        except FileExistsError:
            pass

        # Copy the target file to the backup file.
        PathUtils.copy_file(target_file_path, backup_file_path)


    @staticmethod
    def create_backup_json_file(directory_path: str) -> None:
        """
        
        Description:
            Constructs the backup json file path.
            Invokes _create_backup_json_file to create the backup json file.

        Args:
            directory_path(str): Path for the central backup directory.
        
        Returns:
            None

        Raises:
            None
                
        """
       
        # Variable for the storage of the backup json file path.
        target_file_path = directory_path + os.path.sep + BackupJsonHandler.BACKUP_FILENAME
        
        # Create the backup json file.
        BackupJsonHandler._create_backup_json_file(target_file_path)


    @staticmethod
    def create_backup_orphanage_directory() -> None:
        """
        
        Description:
            Creates the directory tree for the backup orphanage directory,
            including all non-existing parent directories.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Variable for the storage of backup orphanage directory path.
        target_directory_path = PropertiesJsonHandler.get_backup_directory()  + os.path.sep + String.LITERAL_ORPHANAGE
        
        # Create the directory tree for the backup orphanage directory path.
        PathUtils.create_directory_tree(target_directory_path)


    @staticmethod
    def prepare_backup_dirname(path: str, random_string: str) -> str:
        """
        
        Description:
            Formats and returns the backup directory name.

        Args:
            path(str): Path of the item to be tracked by the backup service.
            random_string(str): Random string to be used as a suffix.
        
        Returns:
            str: Formatted backup directory name.

        Raises:
            None
                
        """
        
        # Return the backup directory name; Formatted.
        return PathUtils.get_filename(path) + '_' + random_string


    @staticmethod
    def prepare_backup_filename(file_path: str, current_time_formatted: str) -> str:
        """
        
        Description:
            Formats and returns the backup file name.

        Args:
            file_path(str): Path of the file to be tracked by the backup service.
            current_time_formatted(str): Formatted current timestamp on the platform.
        
        Returns:
            str: Formatted backup file name.

        Raises:
            None
                
        """
        
        # Return the backup filename; Formatted.
        return PathUtils.get_filename(file_path) + '_' + current_time_formatted + String.BACKUP_FILE_EXTENSION


    @staticmethod
    def _add_backup_json_entry_for_directory(json_entry: dict, suffix: str) -> None:
        """
        
        Description:
            For every file within the target directory:
                Retrieves the formatted current timestamp.
                Retrieves the source file path.
                Constructs the top level backup directory path.
                Constructs the backup directory.
                Constructs the backup file path.
                Creates the directory tree for the backup directory path.
                Creates the backup file.

            Note: This method is not meant to be accessed from outside this class.    
            
        Args:
            json_entry(dict): Dictionary for the json data representing the target directory.
            suffix(str): String to be used as a suffix for the backup directory path.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME

        # For every item in the path:
        for item in Path(json_entry[PATH]).iterdir():
            # Assign the current time; Formatted.
            current_time_formatted = CurrentTimeHandler.get_current_time_formatted()
            
            # If the item is a file:
            if PathUtils.is_file(item):
                # Resolve and assign the source file path.
                source_file_path = str(item.resolve())
                # Construct the top-level backup directory path.
                top_level_backup_directory_path = PropertiesJsonHandler.get_backup_directory() + os.path.sep + json_entry[BACKUP_DIRNAME] + os.path.sep
                # Construct the backup directory path.
                backup_directory_path = top_level_backup_directory_path + BackupJsonHandler.prepare_backup_dirname(source_file_path, suffix)
                # Construct the backup file path.
                backup_file_path = backup_directory_path + os.path.sep + BackupJsonHandler.prepare_backup_filename(source_file_path, current_time_formatted)
                
                # Create the directory tree for the backup directory path.
                PathUtils.create_directory_tree(backup_directory_path)

                # Create the backup file.
                BackupJsonHandler.create_backup_file(source_file_path, backup_file_path) 


    @staticmethod
    def _add_backup_json_entry_for_file(json_entry: dict, path: str) -> None:
        """
        
        Description:
            Constructs the backup directory path.
            Constructs the backup file path.
            Creates the directory tree for the backup directory path.
            Creates the backup file.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            json_entry(dict): Dictionary for the json data representing the target file.
            path(str): Path for the file to be tracked by the backup service.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of a string literal.
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME

        # Variable for the storage of the backup directory path.
        backup_directory_path = PropertiesJsonHandler.get_backup_directory() + os.path.sep + json_entry[BACKUP_DIRNAME] + os.path.sep
        
        # Variable for the storage of the backup file path.
        backup_file_path = backup_directory_path + BackupJsonHandler.prepare_backup_filename(path, CurrentTimeHandler.get_current_time_formatted())

        # Create the directory tree for the backup directory path.
        PathUtils.create_directory_tree(backup_directory_path)

        # Create the backup file.
        BackupJsonHandler.create_backup_file(path, backup_file_path) 


    @staticmethod
    def _create_backup_json_entry(path: str) -> dict:
        """
        
        Description:
            Prepares various attribute values for the backup json entry.
            Constructs and populates a dictionary to represent the backup json entry.
            Returns the created dictionary.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(str): Path of the item to be tracked by the backup service.
        
        Returns:
            dict: Dictionary for the created backup json entry.

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME
        IS_DIRECTORY = String.LITERAL_IS_DIRECTORY
        ADDED_BY = String.LITERAL_ADDED_BY
        ADDED_AT =  String.LITERAL_ADDED_AT

        # Variables for the storage of attribute values.
        backup_dirname = PathUtils.get_filename(path)
        is_directory = PathUtils.is_directory(path)
        username = CurrentUserRetriever.get_username()
        current_time_formatted = CurrentTimeHandler.get_current_time_formatted()

        # Create the dictionary for the json entry.
        json_entry = {
                        PATH : path,
                        BACKUP_DIRNAME : backup_dirname,
                        IS_DIRECTORY : is_directory,
                        ADDED_BY : username,
                        ADDED_AT : current_time_formatted
                     }
        
        # Return the dictionary for the json entry.
        return json_entry


    @staticmethod
    def _create_backup_json_file(file_path: str) -> None:
        """
        
        Description:
            Creates the backup json file at the specified file path.
            Writes '{}' to the file to create the root object.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(str): Path of backup json file to create.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the file mode write. 
        FILE_MODE_WRITE = String.FILE_MODE_WRITE

        # Open the file path with file mode write.
        with open(file_path, FILE_MODE_WRITE) as file:
            # Write '{}' to the file.
            file.write(str({}))
            # Close the file.
            file.close()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass