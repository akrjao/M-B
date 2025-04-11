# Standard library imports.
import json

# Project-specific module imports.
from _constant.integer import Integer
from _constant.string import String


class PropertiesJsonHandler():
    """
    
    PropertiesJsonHandler provides methods for the management of the properties json file under the project root directory.
    Operations include returning the values of individual attributes,
    the assignment of values to individual attributes,
    and the checking of whether individual attributes are set.

    """


    @staticmethod
    def get_backup_autostart_status() -> str:
        """
        
        Description:
            Returns the value of the backup autostart status attribute.

        Args:
            None

        Returns:
            str: Value of the backup autostart status attribute.

        Raises:
            None
                
        """
        
        # Return the value of the backup autostart status attribute.
        return PropertiesJsonHandler._get_attribute(String.PROPERTIES_KEY_BACKUP_AUTOSTART_STATUS)


    @staticmethod
    def get_backup_directory() -> str:
        """
        
        Description:
            Returns the value of the backup directory attribute.

        Args:
            None

        Returns:
            str: Value of the backup directory attribute.

        Raises:
            None
                
        """
        
        # Return the value of the backup directory attribute.
        return PropertiesJsonHandler._get_attribute(String.PROPERTIES_KEY_BACKUP_DIRECTORY)


    @staticmethod
    def get_language() -> str:
        """
        
        Description:
            Returns the value of the language attribute.

        Args:
            None

        Returns:
            str: Value of the language attribute.

        Raises:
            None
                
        """
        
        # Return the value of the language attribute.
        return PropertiesJsonHandler._get_attribute(String.PROPERTIES_KEY_LANGUAGE)


    @staticmethod
    def get_monitoring_autostart_status() -> str:
        """
        
        Description:
            Returns the value of the monitoring autostart status attribute.

        Args:
            None

        Returns:
            str: Value of the monitoring autostart status attribute.

        Raises:
            None
                
        """
        
        # Return the value of the monitoring autostart status attribute.
        return PropertiesJsonHandler._get_attribute(String.PROPERTIES_KEY_MONITORING_AUTOSTART_STATUS)


    @staticmethod
    def get_monitoring_directory() -> str:
        """
        
        Description:
            Returns the value of the monitoring directory attribute.

        Args:
            None

        Returns:
            str: Value of the monitoring directory attribute.

        Raises:
            None
                
        """
        
        # Return the value of the monitoring directory attribute.
        return PropertiesJsonHandler._get_attribute(String.PROPERTIES_KEY_MONITORING_DIRECTORY)


    @staticmethod
    def get_requirements_status() -> str:
        """
        
        Description:
            Returns the value of the requirements status attribute.

        Args:
            None

        Returns:
            str: Value of the requirements status attribute.

        Raises:
            None
                
        """
        
        # Return the value of the requirements status attribute.
        return PropertiesJsonHandler._get_attribute(String.PROPERTIES_KEY_REQUIREMENTS_STATUS)


    @staticmethod
    def is_backup_autostart_status_set() -> bool:
        """
        
        Description:
            Checks if the backup autostart status attribute has a value.

        Args:
            None

        Returns:
            bool: Whether the backup autostart status attribute has a value or not.

        Raises:
            None
                
        """
        
        # Assert if a value is set to the backup autostart status attribute.
        return PropertiesJsonHandler._is_attribute_set(String.PROPERTIES_KEY_BACKUP_AUTOSTART_STATUS)


    @staticmethod
    def is_backup_directory_set() -> bool:
        """
        
        Description:
            Checks if the backup directory attribute has a value.

        Args:
            None

        Returns:
            bool: Whether the backup directory attribute has a value or not.

        Raises:
            None
                
        """
        
        # Assert if a value is set to the backup directory attribute.
        return PropertiesJsonHandler._is_attribute_set(String.PROPERTIES_KEY_BACKUP_DIRECTORY)


    @staticmethod
    def is_language_set() -> bool:
        """
        
        Description:
            Checks if the language attribute has a value.

        Args:
            None

        Returns:
            bool: Whether the language attribute has a value or not.

        Raises:
            None
                
        """
        
        # Assert if a value is set to the language attribute.
        return PropertiesJsonHandler._is_attribute_set(String.PROPERTIES_KEY_LANGUAGE)


    @staticmethod
    def is_monitoring_autostart_status_set() -> bool:
        """
        
        Description:
            Checks if the monitoring autostart status attribute has a value.

        Args:
            None

        Returns:
            bool: Whether the monitoring autostart status attribute has a value or not.

        Raises:
            None
                
        """
        
        # Assert if a value is set to the monitoring autostart status attribute.
        return PropertiesJsonHandler._is_attribute_set(String.PROPERTIES_KEY_MONITORING_AUTOSTART_STATUS)


    @staticmethod
    def is_monitoring_directory_set() -> bool:
        """
        
        Description:
            Checks if the monitoring directory attribute has a value.

        Args:
            None

        Returns:
            bool: Whether the monitoring directory attribute has a value or not.

        Raises:
            None
                
        """
        
        # Assert if a value is set to the monitoring directory attribute.
        return PropertiesJsonHandler._is_attribute_set(String.PROPERTIES_KEY_MONITORING_DIRECTORY)


    @staticmethod
    def is_requirements_status_set() -> bool:
        """
        
        Description:
            Checks if the requirements status attribute has a value.

        Args:
            None

        Returns:
            bool: Whether the requirements status attribute has a value or not.

        Raises:
            None
                
        """
        
        # Assert if a value is set to the requirements status attribute.
        return PropertiesJsonHandler._is_attribute_set(String.PROPERTIES_KEY_REQUIREMENTS_STATUS)


    @staticmethod
    def set_backup_autostart_status(status: str) -> None:
        """
        
        Description:
            Assigns the status value to the backup autostart status attribute.

        Args:
            status(str): Value for the backup autostart status attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Set the value to the backup autostart status attribute.
        PropertiesJsonHandler._set_attribute(String.PROPERTIES_KEY_BACKUP_AUTOSTART_STATUS, status)


    @staticmethod
    def set_backup_directory(backup_directory: str) -> None:
        """
        
        Description:
            Assigns the backup directory value to the backup directory attribute.

        Args:
            backup_directory(str): Value for the backup directory attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Set the value to the backup directory attribute.
        PropertiesJsonHandler._set_attribute(String.PROPERTIES_KEY_BACKUP_DIRECTORY, backup_directory)


    @staticmethod
    def set_language(language: str) -> None:
        """
        
        Description:
            Assigns the language value to the language attribute.

        Args:
            language(str): Value for the language attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Set the value to the language attribute.
        PropertiesJsonHandler._set_attribute(String.PROPERTIES_KEY_LANGUAGE, language)


    @staticmethod
    def set_monitoring_autostart_status(status: str) -> None:
        """
        
        Description:
            Assigns the status value to the monitoring autostart status attribute.

        Args:
            status(str): Value for the monitoring autostart status attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Set the value to the monitoring autostart status attribute.
        PropertiesJsonHandler._set_attribute(String.PROPERTIES_KEY_MONITORING_AUTOSTART_STATUS, status)


    @staticmethod
    def set_monitoring_directory(monitoring_directory: str) -> None:
        """
        
        Description:
            Assigns the monitoring directory value to the monitoring directory attribute.

        Args:
            monitoring_directory(str): Value for the monitoring directory attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Set the value to the monitoring directory attribute.
        PropertiesJsonHandler._set_attribute(String.PROPERTIES_KEY_MONITORING_DIRECTORY, monitoring_directory)


    @staticmethod
    def set_requirements_status(status: str) -> None:
        """
        
        Description:
            Assigns the status value to the requirements status attribute.

        Args:
            status(str): Value for the requirements status attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Set the value to the requirements status attribute.
        PropertiesJsonHandler._set_attribute(String.PROPERTIES_KEY_REQUIREMENTS_STATUS, status)


    @staticmethod
    def unset_backup_autostart_status() -> None:
        """
        
        Description:
            Clears the value of the backup autostart status attribute.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Clear the value of the backup autostart status attribute.
        PropertiesJsonHandler._unset_attribute(String.PROPERTIES_KEY_BACKUP_AUTOSTART_STATUS)


    @staticmethod
    def unset_backup_directory() -> None:
        """
        
        Description:
            Clears the value of the backup directory attribute.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Clear the value of the backup directory attribute.
        PropertiesJsonHandler._unset_attribute(String.PROPERTIES_KEY_BACKUP_DIRECTORY)


    @staticmethod
    def unset_language() -> None:
        """
        
        Description:
            Clears the value of the language attribute.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Clear the value of the language attribute.
        PropertiesJsonHandler._unset_attribute(String.PROPERTIES_KEY_LANGUAGE)


    @staticmethod
    def unset_monitoring_autostart_status() -> None:
        """
        
        Description:
            Clears the value of the monitoring autostart status attribute.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Clear the value of the monitoring autostart status attribute.
        PropertiesJsonHandler._unset_attribute(String.PROPERTIES_KEY_MONITORING_AUTOSTART_STATUS)


    @staticmethod
    def unset_monitoring_directory() -> None:
        """
        
        Description:
            Clears the value of the monitoring directory attribute.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Clear the value of the monitoring directory attribute.
        PropertiesJsonHandler._unset_attribute(String.PROPERTIES_KEY_MONITORING_DIRECTORY)


    @staticmethod
    def unset_requirements_status() -> None:
        """
        
        Description:
            Clears the value of the requirements status attribute.

        Args:
            None

        Returns:
            None

        Raises:
            None
                
        """
        
        # Clear the value of the requirements status attribute.
        PropertiesJsonHandler._unset_attribute(String.PROPERTIES_KEY_REQUIREMENTS_STATUS)


    @staticmethod
    def _get_attribute(attribute: str) -> str:
        """
        
        Description:
            Reads the properties json data from the properties file.
            Returns the value of the specified attribute.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            attribute(str): Attribute whose value is to be returned.

        Returns:
            str: Value of the specified attribute.

        Raises:
            None
                
        """
        
        # Read and assign the json data from the properties file.
        properties_json = PropertiesJsonHandler._read()

        # Return the value of the attribute.
        return properties_json[attribute]


    @staticmethod
    def _is_attribute_set(attribute: str) -> bool:
        """
        
        Description:
            Reads the properties json data from the properties file.
            Checks if the specified attribute has a value.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            attribute(str): Attribute whose value is to be checked.

        Returns:
            bool: Whether the specified attribute has a value.

        Raises:
            None
                
        """
        
        # Read and assign the json data from the properties file.
        properties_json = PropertiesJsonHandler._read()

        # Assert if the value of the attribute is not set.
        return (properties_json[attribute]) != ''


    @staticmethod
    def _read() -> str:
        """
        
        Description:
            Reads the properties json data from the properties file.
            Serializes the properties json data.
            Returns the serialized properties json data.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None

        Returns:
            str: Properties json data in a serialized format.

        Raises:
            FileNotFoundError:
                If the properties json data is not found,
                then print the respective error message.

            json.JSONDecodeError:
                If the properties json data is malformed,
                then print the respective error message.
                
        """
        
        # Constants for the storage of string literals.
        FILE_MODE_READ = String.FILE_MODE_READ
        PROPERTIES_FILENAME = String.PROPERTIES_FILENAME
        EXCEPTION_MESSAGE_JSON_DECODE_ERROR = PROPERTIES_FILENAME + ': ' + String.EXCEPTION_MESSAGE_JSON_DECODE_ERROR
        EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR = PROPERTIES_FILENAME + ': ' + String.EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR

        # Variable for the storage of the properties json file data.
        json_data = None


        # Attempt to:
        try:
            # Open the properties file with the file mode read.
            with open(PROPERTIES_FILENAME, FILE_MODE_READ) as file:
                # Assign the json data.
                json_data = json.load(file)
                # Close the file.
                file.close()
            
            # Return the json data.
            return json_data
        
        # Handle: FileNotFoundError.
        except FileNotFoundError:
            # Print the file not found error message.
            print(EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR)
        
        # Handle: json.JSONDecodeError:
        except json.JSONDecodeError:
            # print the json decode error message.
            print(EXCEPTION_MESSAGE_JSON_DECODE_ERROR)


    @staticmethod
    def _set_attribute(attribute: str, value: str) -> None:
        """
        
        Description:
            Reads the properties json data from the properties file.
            Assigns the specified attribute the specified value.
            Writes back the modified properties json data to the properties file.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            attribute(str): Attribute whose value is desired to be set.
            value(str): Value for the attribute.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Read and assign the json data from the properties file.
        properties_json = PropertiesJsonHandler._read()
        
        # Assign the value to the attribute.
        properties_json[attribute] = value
        
        # Write the json data back to the properties file.
        PropertiesJsonHandler._write(properties_json)


    @staticmethod
    def _unset_attribute(attribute) -> None:
        """
        
        Description:
            Reads the properties json data from the properties file.
            Unsets the specified attribute by assigning an empty string.
            Writes back the modified properties json data to the properties file.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            attribute(str): Attribute whose value is desired to be unset.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Read and assign the json data from the properties file.
        properties_json = PropertiesJsonHandler._read()
        
        # Clear the value of the attribute.
        properties_json[attribute] = ''
        
        # Write the json data back to the properties file.
        PropertiesJsonHandler._write(properties_json)


    @staticmethod
    def _write(properties_json: str) -> None:
        """
        
        Description:
            Attempts to open the properties file,
            and write the specified properties json data to the properties file.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            properties_json(str): Properties json data to write to the properties file.
        
        Returns:
            None

        Raises:
            FileNotFoundError:
                If the properties file is not found,
                then print the respective error message.
                
        """
        
        # Constant for the storage of the properties file name.
        PROPERTIES_FILENAME = String.PROPERTIES_FILENAME

        # Constant for the storage of the file mode write.
        FILE_MODE_WRITE = String.FILE_MODE_WRITE
        
        # Constant for the storage of an integer literal.
        JSON_INDENT = Integer.JSON_INDENT

        # Constant for the storage of the file not found error message.
        EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR = PROPERTIES_FILENAME + ': ' + String.EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR

        # Attempt to:
        try:
            # Open the properties file with the file mode write.
            with open(PROPERTIES_FILENAME, FILE_MODE_WRITE) as file:
                # Write the properties json data to the file.
                json.dump(properties_json, file, indent=JSON_INDENT)
                # Close the file.
                file.close()

        # Handle: FileNotFoundError.
        except FileNotFoundError:
            # Print the file not found error message.
            print(EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR)


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass