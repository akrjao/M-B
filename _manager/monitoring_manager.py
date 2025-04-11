# Standard library imports.
import json
import os

# Standard library from imports.
from typing import Union

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _jsonx.monitoring_json_handler import MonitoringJsonHandler
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _language.language_selector import LanguageSelector
from _miscellaneous.color import Color


class MonitoringManager:
    """
    
    MonitoringManager provides core methods for,
    the operation of the monitoring service,
    the handling of monitoring targets,
    and the display of properties related to backup targets.

    """


    # Constant for the retrieval of screen text.
    _LOCALE: dict[str, str] = None


    @staticmethod
    def delete_monitoring_json_entry(target_id_to_delete: Union[int, str]) -> None:
        """
        
        Description:
            Deletes the json entry of the target from the monitoring json file,
            therefore, the monitoring service no longer tracks its access and modification attempts.

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

        # Constant for the storage of the monitoring json file path.
        MONITORING_JSON_FILE_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + MonitoringJsonHandler.MONITORING_FILENAME

        # Variable for the storage of the monitoring json data.
        data = {}

        # Variable for the storage of the modified monitoring json data.
        updated_dict = {}

        # Open the monitoring json file with file mode read.
        with open(MONITORING_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            
            # For every key and value in the monitoring json data:
            for key, value in data.items():
                # If the key is not equal to the target id to delete:
                if key != str(target_id_to_delete):
                    # Append data of the non-concerned target to the modified monitoring json dictionary.
                    updated_dict[key] = value

            # Close the file.
            file.close()
    
        # Open the monitoring json file with file mode write.
        with open(MONITORING_JSON_FILE_PATH, FILE_MODE_WRITE) as file:
            # Write the modified monitoring json data to the monitoring json file.
            json.dump(updated_dict, file, indent=JSON_INDENT)

            # Close the file.
            file.close()


    @staticmethod
    def display_monitored_directories() -> None:
        """
        
        Description:
            Iterates through the dictionary of monitored directories.
            Formats and displays their attributes and their attribute values to the user.
            Notifies the user if there are no monitored directories to display.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Refresh the locale dictionary.
        MonitoringManager._refresh_locale()
        
        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        LOG_FILENAME = String.LITERAL_LOG_FILENAME
        ADDED_BY = String.LITERAL_ADDED_BY
        ADDED_AT = String.LITERAL_ADDED_AT

        # Constants for the storage of string literals based on the selected locale.
        NOTIFY_EMPTINESS_MONITORING_REMOVER_AND_LOG_VIEWER_FOR_DIRECTORY = MonitoringManager._LOCALE[String.LANGUAGE_KEY_NOTIFY_EMPTINESS_MONITORING_REMOVER_AND_LOG_VIEWER_FOR_DIRECTORY]
        ID = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ID]
        __PATH = MonitoringManager._LOCALE[String.LANGUAGE_KEY_PATH]
        __LOG_FILENAME = MonitoringManager._LOCALE[String.LANGUAGE_KEY_LOG_FILENAME]
        __ADDED_BY = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ADDED_BY]
        __ADDED_AT = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ADDED_AT]

        # Constants for the storage of colors.
        COLOR_GREEN = Color.GREEN
        COLOR_ENC = Color.ENC
        COLOR_YELLOW = Color.YELLOW

        # Variable for the storage of all directories that are tracked by the monitoring service.
        directory_dict = MonitoringManager._get_monitored_directories()
        
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
                # Print the third row; Log file name.
                print(f'{COLOR_GREEN}{__LOG_FILENAME}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[LOG_FILENAME]}{COLOR_ENC}', end='\n')
                # Print the fourth row; Added by.
                print(f'{COLOR_GREEN}{__ADDED_BY}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[ADDED_BY]}{COLOR_ENC}', end='\n')
                # Print the fifth row; Added at.
                print(f'{COLOR_GREEN}{__ADDED_AT}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{added_at}{COLOR_ENC}', end='\n\n')

        # If the directory dictionary is empty:
        else:
            # Print the notification for empty directory dictionary.
            print(f'{COLOR_YELLOW}{NOTIFY_EMPTINESS_MONITORING_REMOVER_AND_LOG_VIEWER_FOR_DIRECTORY}{COLOR_ENC}', end='\n\n')


    @staticmethod
    def display_monitored_files() -> None:
        """
        
        Description:
            Iterates through the dictionary of monitored files.
            Formats and displays their attributes and their attribute values to the user.
            Notifies the user if there are no monitored files to display.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Refresh the locale dictionary.
        MonitoringManager._refresh_locale()
        
        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        LOG_FILENAME = String.LITERAL_LOG_FILENAME
        ADDED_BY = String.LITERAL_ADDED_BY
        ADDED_AT = String.LITERAL_ADDED_AT

        # Constants for the storage of string literals based on the selected locale.
        NOTIFY_EMPTINESS_MONITORING_REMOVER_AND_LOG_VIEWER_FOR_SINGLE_FILE = MonitoringManager._LOCALE[String.LANGUAGE_KEY_NOTIFY_EMPTINESS_MONITORING_REMOVER_AND_LOG_VIEWER_FOR_SINGLE_FILE]
        ID = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ID]
        __PATH = MonitoringManager._LOCALE[String.LANGUAGE_KEY_PATH]
        __LOG_FILENAME = MonitoringManager._LOCALE[String.LANGUAGE_KEY_LOG_FILENAME]
        __ADDED_BY = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ADDED_BY]
        __ADDED_AT = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ADDED_AT]

        # Constants for the storage of colors.
        COLOR_GREEN = Color.GREEN
        COLOR_ENC = Color.ENC
        COLOR_YELLOW = Color.YELLOW

        # Variable for the storage of all files that are tracked by the monitoring service.
        file_dict = MonitoringManager._get_monitored_files()

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
                # Print the third row; Log file name.
                print(f'{COLOR_GREEN}{__LOG_FILENAME}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[LOG_FILENAME]}{COLOR_ENC}', end='\n')
                # Print the fourth row; Added by.
                print(f'{COLOR_GREEN}{__ADDED_BY}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{value[ADDED_BY]}{COLOR_ENC}', end='\n')
                # Print the fifth row; Added at.
                print(f'{COLOR_GREEN}{__ADDED_AT}{COLOR_ENC}', end='')
                print(f'{COLOR_YELLOW}{added_at}{COLOR_ENC}', end='\n\n')

        # If the file dictionary is empty:
        else:
            # Print the notification for empty file dictionary.
            print(f'{COLOR_YELLOW}{NOTIFY_EMPTINESS_MONITORING_REMOVER_AND_LOG_VIEWER_FOR_SINGLE_FILE}{COLOR_ENC}', end='\n\n')


    @staticmethod
    def format_and_display_log_file(target_id_to_format_and_display: Union[int, str]) -> None:
        """
        
        Description:
            Opens the log file of the target item.
            Formats and displays entries of the log file to the user.
            Notifies the user if there are no monitoring log entries to display.

        Args:
            target_id_to_format_and_display(Union[int, str]): Id of the target item whose log file is to be formatted and displayed.
        
        Returns:
            None

        Raises:
            None
                
        """

        # Refresh the locale dictionary.
        MonitoringManager._refresh_locale()

        # Constants for the storage of string literals.
        TARGET = String.LITERAL_TARGET
        ACCESSED_AT = String.LITERAL_ACCESSED_AT
        MODIFIED_AT = String.LITERAL_MODIFIED_AT
        POTENTIALLY_BY = String.LITERAL_POTENTIALLY_BY
        FILE_MODE_READ = String.FILE_MODE_READ

        # Constants for the storage of string literals based on the selected locale.
        NOTIFY_EMPTINESS_MONITORING_LOG_VIEWER_TWO = MonitoringManager._LOCALE[String.LANGUAGE_KEY_NOTIFY_EMPTINESS_MONITORING_LOG_VIEWER_TWO]
        __TARGET = MonitoringManager._LOCALE[String.LANGUAGE_KEY_TARGET]
        __ACCESSED_AT = MonitoringManager._LOCALE[String.LANGUAGE_KEY_ACCESSED_AT]
        __MODIFIED_AT = MonitoringManager._LOCALE[String.LANGUAGE_KEY_MODIFIED_AT]
        __POTENTIALLY_BY = MonitoringManager._LOCALE[String.LANGUAGE_KEY_POTENTIALLY_BY]

        # Constants for the storage of colors.
        COLOR_GREEN = Color.GREEN
        COLOR_ENC = Color.ENC
        COLOR_YELLOW = Color.YELLOW

        # Constant dictionary for the storage of old string literals and their replacements.
        REMPLACEMENT_DICT = {
            TARGET : f'{COLOR_GREEN}{__TARGET}{COLOR_ENC}{COLOR_YELLOW}',
            ACCESSED_AT : f'{COLOR_ENC}{COLOR_GREEN}{__ACCESSED_AT}{COLOR_ENC}{COLOR_YELLOW}',
            MODIFIED_AT : f'{COLOR_ENC}{COLOR_GREEN}{__MODIFIED_AT}{COLOR_ENC}{COLOR_YELLOW}',
            POTENTIALLY_BY : f'{COLOR_ENC}{COLOR_GREEN}{__POTENTIALLY_BY}{COLOR_ENC}{COLOR_YELLOW}',
            '\n' : f'{COLOR_ENC}\n'
        }

        # Variable for the storage of the path of the log file to display.
        target_log_file_path = MonitoringManager._search_for_log_file_path(target_id_to_format_and_display)

        # Attempt to:
        try:
            # Open the target log file with file mode read.
            with open(target_log_file_path, FILE_MODE_READ) as file:
                # Read the content of the log file.
                file_content = file.read()
                
                # If the log file is not empty:
                if len(file_content) > 0:
                    # For every line in the list of lines of the log file:
                    for line in file_content.splitlines():
                        # For every old string literal and its replacement in the replacement dictionary:
                        for old_string, new_string in REMPLACEMENT_DICT.items():
                            # Replace the old string with its replacement and assign it.
                            line = line.replace(old_string, new_string)
                        
                        # Print the modified line.
                        print(line, end='\n\n')

                # If the log file is empty:
                else:
                    # Print the notification for an empty log file.
                    print(f'\n\n{COLOR_YELLOW}{NOTIFY_EMPTINESS_MONITORING_LOG_VIEWER_TWO}{COLOR_ENC}', end='\n\n')

                # Close the file.
                file.close()

        # Handle: FileNotFoundError.
        except FileNotFoundError:
            # Print the notification for an empty log file.
            print(f'\n\n{COLOR_YELLOW}{NOTIFY_EMPTINESS_MONITORING_LOG_VIEWER_TWO}{COLOR_ENC}', end='\n\n')


    @staticmethod
    def get_ids_of_monitored_directories() -> list[int]:
        """
        
        Description:
            Iterates through the dictionary of the ids of monitored directories.
            Casts every id to an integer and appends it to the list of ids.
            Returns the list of ids of monitored directories.

        Args:
            None
        
        Returns:
            list[int]: List of ids of monitored directories in the integer format.

        Raises:
            None
                
        """
        
        # Return the ids of all monitoring json entries that represent directories and that are tracked by the monitoring service.
        return [int(key) for key in MonitoringManager._get_monitored_directories().keys()]


    @staticmethod
    def get_ids_of_monitored_files() -> list[int]:
        """
        
        Description:
            Iterates through the dictionary of the ids of monitored files.
            Casts every id to an integer and appends it to the list of ids.
            Returns the list of ids of monitored files.

        Args:
            None
        
        Returns:
            list[int]: List of ids of monitored files in the integer format.

        Raises:
            None
                
        """
        
        # Return the ids of all monitoring json entries that represent files and that are tracked by the monitoring service.
        return [int(key) for key in MonitoringManager._get_monitored_files().keys()]


    @staticmethod
    def _get_monitored_directories() -> dict:
        """
        
        Description:
            Iterates the monitoring json data.
            Searches for monitoring targets of type directory.
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

        # Constant for the storage of the monitoring json file path.
        MONITORING_JSON_FILE_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + MonitoringJsonHandler.MONITORING_FILENAME

        # Variable for the storage of the monitored directories with their attributes.
        directory_dict = {}

        # Open the monitoring json file using the file mode read.
        with open(MONITORING_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            
            # For key and value in the monitoring json file data:
            for key, value in data.items():
                # If the target is a directory:
                if value[IS_DIRECTORY]:
                    # Append the data of the target to the directory dictionary.
                    directory_dict[key] = value

            # Close the file.
            file.close()

        # Return the dictionary of monitored directories.
        return directory_dict


    @staticmethod
    def _get_monitored_files() -> dict:
        """
        
        Description:
            Iterates the monitoring json data.
            Searches for monitoring targets of type file.
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

        # Constant for the storage of the monitoring json file path.
        MONITORING_JSON_FILE_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep + MonitoringJsonHandler.MONITORING_FILENAME

        # Variable for the storage of monitored files with their attributes.
        file_dict = {}

        # Open the monitoring json file using the file mode read.
        with open(MONITORING_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
        
            # For key and value in the monitoring json file data:
            for key, value in data.items():
                # If the target is not a directory:
                if not value[IS_DIRECTORY]:
                    # Append the data of the target to the file dictionary.
                    file_dict[key] = value
            
            # Close the file.
            file.close()

        # Return the dictionary of monitored files.
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
        MonitoringManager._LOCALE = LanguageSelector.get_language_dict()


    @staticmethod
    def _search_for_log_file_path(target_id_to_search_for: Union[int, str]) -> str:
        """
        
        Description:
            Searches for the log file path of the monitoring target in the monitoring directory.
            Returns the respective log file path.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            target_id_to_search_for(Union[int, str]): Id of the target whose log file path is to be searched for.
        
        Returns:
            str: Path of the respective log file.

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        LOG_FILENAME = String.LITERAL_LOG_FILENAME

        # Constant for the storage of the monitoring directory path.
        MONITORING_DIRECTORY_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep
        
        # Constant for the storage of the monitoring json file path.
        MONITORING_JSON_FILE_PATH = MONITORING_DIRECTORY_PATH + MonitoringJsonHandler.MONITORING_FILENAME

        # Open the monitoring json file with file mode read.
        with open(MONITORING_JSON_FILE_PATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            
            # For every key and value in the monitoring json data:
            for key, value in data.items():
                # If the key is equal to the target id to search for:
                if key == str(target_id_to_search_for):
                    # Return the log file path of the target.
                    return MONITORING_DIRECTORY_PATH + value[LOG_FILENAME]


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass