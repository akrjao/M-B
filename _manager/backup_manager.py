# Standard library imports.
import json
import os

# Standard library from imports.
from typing import Union

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _jsonx.backup_json_handler import BackupJsonHandler
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color


class BackupManager:
    """
    
    BackupManager provides core methods for,
    the operation of the backup service,
    the handling of backup targets,
    and the display of properties related to monitoring targets.

    """


    # Constant for the retrieval of screen text.
    _LOCALE: dict[str, str] = None


    @staticmethod
    def delete_backup_json_entry(target_id_to_delete: Union[int, str]) -> None:
        """
        
        Description:
            Deletes the json entry of the target from the backup json file,
            therefore, the backup service no longer tracks its modification attempts.

        Args:
            target_id_to_delete(Union[int, str]): Id of the target item whose json entry is desired to be deleted.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        FILE_MODE_WRITE = String.FILE_MODE_WRITE
        
        # Constant for the storage of integer literal.
        JSON_INDENT = Integer.JSON_INDENT

        # Constant for the storage of the backup json file path.
        BACKUP_JSON_FILE_PATH = PropertiesJsonHandler.get_backup_directory() + os.path.sep + BackupJsonHandler.BACKUP_FILENAME

        # Variable for the storage of the backup json data.
        data = {}

        # Variable for the storage of the modified backup json data.
        updated_dict = {}

        # Open the backup json file with file mode read.
        with open(BACKUP_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            
            # For every key and value in the backup json data:
            for key, value in data.items():
                # If the key is not equal to the target id to delete:
                if key != str(target_id_to_delete):
                    # Append the data of the non-concerned target to the modified backup json dictionary.
                    updated_dict[key] = value

            # Close the file.
            file.close()
    
        # Open the backup json file with file mode write.
        with open(BACKUP_JSON_FILE_PATH, FILE_MODE_WRITE) as file:
            # Write the modified backup json data to the backup json file.
            json.dump(updated_dict, file, indent=JSON_INDENT)

            # Close the file.
            file.close()


    @staticmethod
    def display_backedup_directories() -> None:
        """
        
        Description:
            Iterates through the dictionary of backed up directories.
            Formats and displays their attributes and their attribute values to the user.
            Notifies the user if there are no backed up directories to display.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Refresh the locale dictionary.
        BackupManager._refresh_locale()
        
        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME
        ADDED_BY = String.LITERAL_ADDED_BY
        ADDED_AT = String.LITERAL_ADDED_AT

        # Constants for the storage of string literals based on the selected locale.
        NOTIFY_EMPTINESS_BACKUP_REMOVER_FOR_DIRECTORY = BackupManager._LOCALE[String.LANGUAGE_KEY_NOTIFY_EMPTINESS_BACKUP_REMOVER_FOR_DIRECTORY]
        ID = BackupManager._LOCALE[String.LANGUAGE_KEY_ID]
        __PATH = BackupManager._LOCALE[String.LANGUAGE_KEY_PATH]
        __BACKUP_DIRNAME = BackupManager._LOCALE[String.LANGUAGE_KEY_BACKUP_DIRNAME]
        __ADDED_BY = BackupManager._LOCALE[String.LANGUAGE_KEY_ADDED_BY]
        __ADDED_AT = BackupManager._LOCALE[String.LANGUAGE_KEY_ADDED_AT]

        # Constants for the storage of colors.
        COLOR_GREEN = Color.GREEN
        COLOR_ENC = Color.ENC
        COLOR_YELLOW = Color.YELLOW

        # Variable for the storage of all directories that are tracked by the backup service.
        directory_dict = BackupManager._get_backedup_directories()

        # If the directory dictionary is not empty:
        if len(directory_dict.items()) > 0:
            # For every key and value in the directory dictionary:
            for key, value in directory_dict.items():
                # Retrieve the added at attribute value.
                added_at = value[ADDED_AT]

                # Modify the added at attribute value for better display.
                added_at = added_at.replace('-', ':').replace('_', ' ')

                # Print the first row; Id.
                print(f'{COLOR_GREEN}{ID}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{key}{COLOR_ENC}', end='\n')
                # Print the second row; Path.
                print(f'{COLOR_GREEN}{__PATH}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[PATH]}{COLOR_ENC}', end='\n')
                # Print the third row; Backup directory name.
                print(f'{COLOR_GREEN}{__BACKUP_DIRNAME}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[BACKUP_DIRNAME]}{COLOR_ENC}', end='\n')
                # Print the fourth row; Added by.
                print(f'{COLOR_GREEN}{__ADDED_BY}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[ADDED_BY]}{COLOR_ENC}', end='\n')
                # Print the fifth row; Added at.
                print(f'{COLOR_GREEN}{__ADDED_AT}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{added_at}{COLOR_ENC}', end='\n\n')

        # If the directory dictionary is empty:
        else:
            # Print the notification for empty directory dictionary.
            print(f'{COLOR_YELLOW}{NOTIFY_EMPTINESS_BACKUP_REMOVER_FOR_DIRECTORY}{COLOR_ENC}', end='\n\n')


    @staticmethod
    def display_backedup_files() -> None:
        """
        
        Description:
            Iterates through the dictionary of backed up files.
            Formats and displays their attributes and their attribute values to the user.
            Notifies the user if there are no backed up files to display.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Refresh the locale dictionary.
        BackupManager._refresh_locale()
        
        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        BACKUP_DIRNAME = String.LITERAL_BACKUP_DIRNAME
        ADDED_BY = String.LITERAL_ADDED_BY
        ADDED_AT = String.LITERAL_ADDED_AT

        # Constants for the storage of string literals based on the selected locale.
        NOTIFY_EMPTINESS_BACKUP_REMOVER_FOR_SINGLE_FILE = BackupManager._LOCALE[String.LANGUAGE_KEY_NOTIFY_EMPTINESS_BACKUP_REMOVER_FOR_SINGLE_FILE]
        ID = BackupManager._LOCALE[String.LANGUAGE_KEY_ID]
        __PATH = BackupManager._LOCALE[String.LANGUAGE_KEY_PATH]
        __BACKUP_DIRNAME = BackupManager._LOCALE[String.LANGUAGE_KEY_BACKUP_DIRNAME]
        __ADDED_BY = BackupManager._LOCALE[String.LANGUAGE_KEY_ADDED_BY]
        __ADDED_AT = BackupManager._LOCALE[String.LANGUAGE_KEY_ADDED_AT]

        # Constants for the storage of colors.
        COLOR_GREEN = Color.GREEN
        COLOR_ENC = Color.ENC
        COLOR_YELLOW = Color.YELLOW

        # Variable for the storage of all files that are tracked by the backup service.
        file_dict = BackupManager._get_backedup_files()

        # If the file dictionary is not empty:
        if len(file_dict.items()) > 0:
            # For every key and value in the file dictionary:
            for key, value in file_dict.items():
                # Retrieve the added at attribute value.
                added_at = value[ADDED_AT]

                # Modify the added at attribute value for better display.
                added_at = added_at.replace('-', ':').replace('_', ' ')

                # Print the first row; Id.
                print(f'{COLOR_GREEN}{ID}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{key}{COLOR_ENC}', end='\n')
                # Print the second row; Path.
                print(f'{COLOR_GREEN}{__PATH}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[PATH]}{COLOR_ENC}', end='\n')
                # Print the third row; Backup directory name.
                print(f'{COLOR_GREEN}{__BACKUP_DIRNAME}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[BACKUP_DIRNAME]}{COLOR_ENC}', end='\n')
                # Print the fourth row; Added by.
                print(f'{COLOR_GREEN}{__ADDED_BY}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[ADDED_BY]}{COLOR_ENC}', end='\n')
                # Print the fifth row; Added at.
                print(f'{COLOR_GREEN}{__ADDED_AT}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{added_at}{COLOR_ENC}', end='\n\n')
        
        # If the file dictionary is empty:
        else:
            # Print the notification for empty file dictionary.
            print(f'{COLOR_YELLOW}{NOTIFY_EMPTINESS_BACKUP_REMOVER_FOR_SINGLE_FILE}{COLOR_ENC}', end='\n\n')


    @staticmethod
    def get_ids_of_backedup_directories() -> list[int]:
        """
        
        Description:
            Iterates through the dictionary of the ids of backed up directories.
            Casts every id to an integer and appends it to the list of ids.
            Returns the list of ids of backed up directories.

        Args:
            None
        
        Returns:
            list[int]: List of ids of backed up directories in the integer format.

        Raises:
            None
                
        """
        
        # Return the ids of all backup json entries that represent directories and that are tracked by the backup service.
        return [int(key) for key in BackupManager._get_backedup_directories().keys()]


    @staticmethod
    def get_ids_of_backedup_files() -> list[int]:
        """
        
        Description:
            Iterates through the dictionary of the ids of backed up files.
            Casts every id to an integer and appends it to the list of ids.
            Returns the list of ids of backed up files.

        Args:
            None
        
        Returns:
            list[int]: List of ids of backed up files in the integer format.

        Raises:
            None
                
        """
        
        # Return the ids of all backup json entries that represent files and that are tracked by the backup service.
        return [int(key) for key in BackupManager._get_backedup_files().keys()]


    @staticmethod
    def _get_backedup_directories() -> dict:
        """
        
        Description:
            Iterates the backup json data.
            Searches for backup targets of type directory.
            Returns a dictionary of all target directories and their attribute values.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            dict: Dictionary of all target directories and their attribute values.

        Raises:
            None
                
        """
        
        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        IS_DIRECTORY = String.LITERAL_IS_DIRECTORY

        # Constant for the storage of the backup json file path.
        BACKUP_JSON_FILE_PATH = PropertiesJsonHandler.get_backup_directory() + os.path.sep + BackupJsonHandler.BACKUP_FILENAME

        # Variable for the storage of the backed up directories with their attributes.
        directory_dict = {}

        # Open the backup json file using the file mode read.
        with open(BACKUP_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            
            # For key and value in the backup json file data:
            for key, value in data.items():
                # If the target is a directory:
                if value[IS_DIRECTORY]:
                    # Append the data of the target to the directory dictionary.
                    directory_dict[key] = value
            
            # Close the file.
            file.close()

        # Return the dictionary of tracked directories.
        return directory_dict


    @staticmethod
    def _get_backedup_files() -> dict:
        """
        
        Description:
            Iterates the backup json data.
            Searches for backup targets of type file.
            Returns a dictionary of all target files and their attribute values.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            dict: Dictionary of all target files and their attribute values.

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        IS_DIRECTORY = String.LITERAL_IS_DIRECTORY

        # Constant for the storage of the backup json file path.
        BACKUP_JSON_FILE_PATH = PropertiesJsonHandler.get_backup_directory() + os.path.sep + BackupJsonHandler.BACKUP_FILENAME

        # Variable for the storage of backed up files with their attributes.
        file_dict = {}

        # Open the backup json file using the file mode read.
        with open(BACKUP_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
        
            # For key and value in the backup json file data:
            for key, value in data.items():
                # If the target is not a directory:
                if not value[IS_DIRECTORY]:
                    # Append the data of the target to the file dictionary.
                    file_dict[key] = value

            # Close the file.
            file.close()

        # Return the dictionary of tracked files.
        return file_dict


    @staticmethod
    def _refresh_locale() -> None:
        """
        
        Description:
            Updates the _LOCALE class constant to reflect language change.
            
            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Re-initialize the locale constant.
        BackupManager._LOCALE = LanguageSelector.get_language_dict()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass