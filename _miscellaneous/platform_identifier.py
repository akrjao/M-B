# Standard library imports.
import os

# Project-specific module imports.
from _constant.string import String


class PlatformIdentifier():
    """
    
    PlatformIdentifier serves to identify the platform on which the script is executing.

    """


    @staticmethod
    def is_windows() -> bool:
        """
        
        Description:
            Based on the operating system name,
            returns whether the current platform on which the script is running is Windows.

        Args:
            None
        
        Returns:
            bool: Whether the current platform is Windows.

        Raises:
            None
                
        """
        
        # If the operating system name is equal to 'nt':
        if os.name == String.LITERAL_WINDOWS_OS_NAME:
            # Assert the current platform as Windows.
            return True
        
        # If the operating system name is not equal to 'nt':
        else:
            # Assert the current platform as Linux.
            return False


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass