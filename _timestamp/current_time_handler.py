# Standard library from imports.
from datetime import datetime

# Project-specific module imports.
from _constant.string import String


class CurrentTimeHandler:
    """
    
    CurrentTimeHandler provides methods to handle the current time on the platform.
    It enables the retrieval of the current timestamp.
    Additionally, It enables the conversion of the timestamp into a human-readable format. 

    """


    @staticmethod
    def get_current_time_formatted() -> str:
        """
        
        Description:
            Formats and returns the current timestamp on the platform.

        Args:
            None
        
        Returns:
            float: Formatted current timestamp on the platform.

        Raises:
            None
                
        """
        
        # Constant for the storage of the format for the current time.
        FORMAT_CURRENT_TIME = String.FORMAT_CURRENT_TIME

        # Variable for the storage of the current time; Raw.
        current_time_raw = CurrentTimeHandler.get_current_time_raw()

        # Return the current time; Formatted.
        return datetime.fromtimestamp(current_time_raw).strftime(FORMAT_CURRENT_TIME)


    @staticmethod
    def get_current_time_raw() -> float:
        """
        
        Description:
            Retrieves the current timestamp on the platform.

        Args:
            None
        
        Returns:
            float: Current timestamp on the platform.

        Raises:
            None
                
        """
        
        # Return the current time; Raw.
        return datetime.now().timestamp()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass