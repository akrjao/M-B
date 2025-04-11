# Standard library imports.
import os


class CurrentUserRetriever:
    """

    CurrentUserRetriever enables the retrieval of the username of the user,
    that is executing the script.
    
    """
    
    
    @staticmethod
    def get_username() -> str:
        """
        
        Description:
            Retrieves the username of the user executing the script.

        Args:
            None
        
        Returns:
            str: Username of the user executing the script.

        Raises:
            None
                
        """
        
        # Return the username of the user executing the script.
        return os.getlogin()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass