# Standard library imports.
import re

# Project-specific module imports.
from _constant.string import String
from _miscellaneous.platform_identifier import PlatformIdentifier


class PathValidator():
    """
    
    PathValidator is responsible for the validation of paths,
    based on the platform on which the script is executing.

    """


    @staticmethod
    def is_path_valid(path: str) -> bool:
        """
        
        Description:
            Based on the current platform,
            Checks if the specified path is a valid path.

        Args:
            path(str): Path to validate.
        
        Returns:
            bool: Whether the path is valid or invalid.

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Assert if the path is valid on Windows.
            return PathValidator._is_path_valid_on_windows(path)
        
        # If the current platform is not Windows:
        else:
            # Assert if the path is valid on Linux.
            return PathValidator._is_path_valid_on_linux(path) 


    @staticmethod
    def _is_path_valid_on_linux(path: str) -> bool:
        """
        
        Description:
            Checks if the specified path is a valid path on Linux.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(str): Path to validate.
        
        Returns:
            bool: Whether the path is valid or invalid.

        Raises:
            None
                
        """
        
        # Assign the regular expression for a valid path on Linux.
        path_pattern_for_linux = re.compile(String.REGEX_LINUX_VALID_PATH)
        
        # Assert if the path is a valid path on Linux.
        return bool(path_pattern_for_linux.match(path))


    @staticmethod
    def _is_path_valid_on_windows(path: str) -> bool:
        """
        
        Description:
            Checks if the specified path is a valid path on Windows.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            path(str): Path to validate.
        
        Returns:
            bool: Whether the path is valid or invalid.

        Raises:
            None
                
        """
        
        # Assign the regular expression for a valid path on Windows.
        path_pattern_for_windows = re.compile(String.REGEX_WINDOWS_VALID_PATH)

        # Assert if the path is a valid path on Windows.
        return bool(path_pattern_for_windows.match(path))


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass