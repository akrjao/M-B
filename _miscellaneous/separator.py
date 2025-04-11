# Standard library imports.
import shutil


class Separator():
    """
    
    Separator serves to create a dashed separator based on the size of the terminal.

    """


    @staticmethod
    def draw() -> str:
        """
        
        Description:
            Based on the terminal window,
            draws a separator using dashes and returns it.

        Args:
            None
        
        Returns:
            str: Separator, drawn using dashes.

        Raises:
            None
                
        """
        
        # Assign the number of columns within the terminal window.
        terminal_size = shutil.get_terminal_size().columns
        
        # Specify 0 as the start index.
        k=0
        
        # Variable for the storage of the separator.
        separator = ''

        # for every column in the terminal window:
        for k in range(terminal_size):
            # Append '-' to the separator.
            separator = separator + '-'

        # Return the separator.
        return separator


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass