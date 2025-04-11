# Standard library imports.
import json
import os

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _path.path_utils import PathUtils
from _timestamp.current_time_handler import CurrentTimeHandler
from _user.current_user_retriever import CurrentUserRetriever


class MonitoringJsonHandler:
    """

    MonitoringJsonHandler essentially serves to manage the monitoring json file found under the central monitoring directory.

    """


    # Constant for the storage of the monitoring json file name.
    MONITORING_FILENAME: str = String.MONITORING_FILENAME


    @staticmethod
    def add_monitoring_json_entry(path: str) -> None:
        """
        
        Description:
            Opens and serializes the monitoring json file.
            Invokes _create_monitoring_json_entry to create the monitoring json entry.
            Modifies the serialized monitoring json data to append the created monitoring json entry.
            Opens and writes the modified monitoring json data to the monitoring json file.
            Creates the respective monitoring log file at the central monitoring directory.

        Args:
            path(str): Path for the item to be tracked by the monitoring service.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the monitoring directory path.
        MONITORING_DIRECTORY_PATH = PropertiesJsonHandler.get_monitoring_directory() + os.path.sep
        
        # Constant for the storage of the monitoring json file path.
        MONITORING_JSON_FILEPATH = MONITORING_DIRECTORY_PATH + MonitoringJsonHandler.MONITORING_FILENAME
        
        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        FILE_MODE_WRITE = String.FILE_MODE_WRITE
        LOG_FILENAME = String.LITERAL_LOG_FILENAME

        # Constant for the storage of an integer literal.
        JSON_INDENT = Integer.JSON_INDENT

        # Variable for the storage of the monitoring json file data.
        data = {}

        # Open the backup json file path with file mode read.
        with open(MONITORING_JSON_FILEPATH, FILE_MODE_READ) as file:
            # Assign the json data.
            data = json.load(file)
            # Close the file.
            file.close()
           
        # Create the monitoring json entry.
        json_entry = MonitoringJsonHandler._create_monitoring_json_entry(path)
        # Add the json entry as the last element of the data dict.
        data[len(data) + 1] = json_entry

        # Open the monitoring json file path with file mode write.
        with open(MONITORING_JSON_FILEPATH, FILE_MODE_WRITE) as file:
            # Write the data dictionary to the file.
            json.dump(data, file, indent=JSON_INDENT)
            # Close the file.
            file.close()

        # Variable for the storage of the monitoring log file path.
        monitoring_log_file_path = MONITORING_DIRECTORY_PATH + json_entry[LOG_FILENAME]

        # Create the monitoring log file.
        MonitoringJsonHandler._create_monitoring_log_file(monitoring_log_file_path)


    @staticmethod
    def create_monitoring_json_file(directory_path: str) -> None:
        """
        
        Description:
            Constructs the monitoring json file path.
            Invokes _create_monitoring_json_file to create the monitoring json file.

        Args:
            directory_path(str): Path for the central monitoring directory.
        
        Returns:
            None

        Raises:
            None
                
        """
       
        # Variable for the storage of the monitoring json file path.
        target_file_path = directory_path + os.path.sep + MonitoringJsonHandler.MONITORING_FILENAME

        # Create the monitoring json file.
        MonitoringJsonHandler._create_monitoring_json_file(target_file_path)


    @staticmethod
    def create_monitoring_orphanage_directory() -> None:
        """
        
        Description:
            Creates the directory tree for the monitoring orphanage directory,
            including all non-existing parent directories.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Variable for the storage of the monitoring orphanage directory path.
        target_directory_path = PropertiesJsonHandler.get_monitoring_directory()  + os.path.sep + String.LITERAL_ORPHANAGE

        # Create the directory tree for the monitoring orphanage directory.
        PathUtils.create_directory_tree(target_directory_path)


    @staticmethod
    def _create_monitoring_json_entry(path: str) -> dict:
        """
        
        Description:
            Prepares various attribute values for the monitoring json entry.
            Constructs and populates a dictionary to represent the monitoring json entry.
            Returns the created dictionary.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(str): Path of the item to be tracked by the monitoring service.
        
        Returns:
            dict: Dictionary for the created monitoring json entry.

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        PATH = String.LITERAL_PATH
        LOG_FILENAME = String.LITERAL_LOG_FILENAME
        IS_DIRECTORY = String.LITERAL_IS_DIRECTORY
        ADDED_BY = String.LITERAL_ADDED_BY
        ADDED_AT =  String.LITERAL_ADDED_AT

        # Variables for the storage of attribute values.
        monitoring_log_filename = MonitoringJsonHandler._prepare_monitoring_log_filename(path)
        is_directory = PathUtils.is_directory(path)
        username = CurrentUserRetriever.get_username()
        current_time_formatted = CurrentTimeHandler.get_current_time_formatted()

        # Create the dictionary for the json entry.
        json_entry = {
                        PATH : path,
                        LOG_FILENAME : monitoring_log_filename,
                        IS_DIRECTORY : is_directory,
                        ADDED_BY : username,
                        ADDED_AT : current_time_formatted
                     }

        # Return the dictionary for the json entry.
        return json_entry


    @staticmethod
    def _create_monitoring_json_file(file_path: str) -> None:
        """
        
        Description:
            Creates the monitoring json file at the specified file path.
            Writes '{}' to the file to create the root object.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(str): Path of monitoring json file to create.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the file mode write.
        FILE_MODE_WRITE = String.FILE_MODE_WRITE

        # Open the file path with the file mode write.
        with open(file_path, FILE_MODE_WRITE) as file:
            # Write '{}' to the file.
            file.write(str({}))
            # Close the file.
            file.close()


    @staticmethod
    def _create_monitoring_log_file(file_path: str) -> None:
        """
        
        Description:
            Creates the monitoring log file at the specified file path.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            file_path(str): Path of monitoring log file to create.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the file mode create.
        FILE_MODE_CREATE = String.FILE_MODE_CREATE

        # Open the file path with the file mode create.
        with open(file_path, FILE_MODE_CREATE) as file:
            # Close the file.
            file.close()


    @staticmethod
    def _prepare_monitoring_log_filename(path: str) -> str:
        """
        
        Description:
            Formats and returns the monitoring log file name.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(str): Path of the item to be tracked by the monitoring service.
        
        Returns:
            str: Formatted monitoring log file name.

        Raises:
            None
                
        """
        
        # Return the monitoring log file name; Formatted.
        return PathUtils.get_filename(path) + '_' + String.generate_random_string() + String.MONITORING_LOG_FILE_EXTENSION


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass