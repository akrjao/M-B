# Standard library from imports.
from datetime import datetime
from pathlib import Path
from typing import Union

# Project-specific module imports.
from _constant.string import String


class MetaTimeHandler:
    """
    
    MetaTimeHandler provides methods to handle the time metadata of files.
    It enables the retrieval of the last access timestamp, and the last modified timestamp of files.
    Additionally, It enables the conversion of the timestamps into a human-readable format. 

    """


    @staticmethod
    def get_last_access_time_formatted(file_path: Union[str, Path]) -> str:
        """
        
        Description:
            Formats and returns the last access timestamp of the file specified by file path.

        Args:
            file_path(Union[str, Path]): File path of the target file.
        
        Returns:
            str: Formatted last access timestamp of the target file.

        Raises:
            None
                
        """
        
        # Constant for the storage of the last access time format.
        FORMAT_LAST_ACCESS_TIME = String.FORMAT_LAST_ACCESS_TIME

        # Variable for the storage of the last access time; Raw.
        last_access_time_raw = MetaTimeHandler.get_last_access_time_raw(file_path)

        # Return the last access time; Formatted.
        return datetime.fromtimestamp(last_access_time_raw).strftime(FORMAT_LAST_ACCESS_TIME)


    @staticmethod
    def get_last_access_time_raw(file_path: Union[str, Path]) -> float:
        """
        
        Description:
            Retrieves the last access timestamp of the file specified by file path.

        Args:
            file_path(Union[str, Path]): File path of the target file.
        
        Returns:
            float: Last access timestamp of the target file.

        Raises:
            None
                
        """
        
        # Return the last access time for the file; Raw.
        return Path(file_path).stat().st_atime


    @staticmethod
    def get_last_modified_time_formatted(file_path: Union[str, Path]) -> str:
        """
        
        Description:
            Formats and returns the last modified timestamp of the file specified by file path.

        Args:
            file_path(Union[str, Path]): File path of the target file.
        
        Returns:
            str: Formatted last modified timestamp of the target file.

        Raises:
            None
                
        """
        
        # Constant for the storage of the format of the last modified time.
        FORMAT_LAST_MODIFIED_TIME = String.FORMAT_LAST_MODIFIED_TIME

        # Variable for the storage of the last modified time; Raw.
        last_modified_time_raw = MetaTimeHandler.get_last_modified_time_raw(file_path)

        # Return the last modified time; Formatted.
        return datetime.fromtimestamp(last_modified_time_raw).strftime(FORMAT_LAST_MODIFIED_TIME)


    @staticmethod
    def get_last_modified_time_raw(file_path: Union[str, Path]) -> float:
        """
        
        Description:
            Retrieves the last modified timestamp of the file specified by file path.

        Args:
            file_path(Union[str, Path]): File path of the target file.
        
        Returns:
            float: Last modified timestamp of the target file.

        Raises:
            None
                
        """
        
        # Return the last modified time for the file; Raw.
        return Path(file_path).stat().st_mtime


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass