# Standard library imports.
import os
import shutil

# Standard library from imports.
from pathlib import Path
from typing import Union

# Project-specific module imports.
from _constant.string import String
from _miscellaneous.platform_identifier import PlatformIdentifier


class PathUtils:
    """
    
    PathUtils provides various methods for the manipulation of file and directory paths.
    Operations include copying, deletion, creation,
    checking of path representation, checking for emptiness, hiding, 
    and the retrieval of names.

    """


    @staticmethod
    def copy_directory(source_directory_path: Union[str, Path], target_directory_path: Union[str, Path]) -> None:
        """
        
        Description:
            Copies the content of source files from the source directory to target files of the target directory.

        Args:
            source_directory_path(Union[str, Path]): Path for the source directory.
            target_directory_path(Union[str, Path]): Path for the target directory.
            
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the target directory path.
        TARGET_DIRECTORY_PATH = target_directory_path + os.path.sep + Path(source_directory_path).name

        # Create the directory tree for the target directory.
        PathUtils.create_directory_tree(TARGET_DIRECTORY_PATH)
        
        # For every file within the source directory:
        for file in Path(source_directory_path).iterdir():
            # Resolve and assign the file path of the respective file.
            source_file_path = Path(file).resolve()

            # Copy the source file to the target directory.
            PathUtils.copy_file(source_file_path, TARGET_DIRECTORY_PATH)


    @staticmethod
    def copy_file(source_file_path: Union[str, Path], target_file_path: Union[str, Path]) -> None:
        """
        
        Description:
            Copies the content of the source file to the target file.

        Args:
            source_file_path(Union[str, Path]): File path of the source file.
            target_file_path(Union[str, Path]): File path of the target file.

        Returns:
            None

        Raises:
            None
                
        """
        
        # Copy the source file to the target file path.
        shutil.copy2(source_file_path, target_file_path)


    @staticmethod
    def create_directory_tree(directory_path: Union[str, Path]) -> None:
        """
        
        Description:
            Creates the directory specified by the directory path, including all non-existing parent directories.

        Args:
            directory_path(Union[str, Path]): Path of the directory whose creation is desired.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Create the entire directory tree.
        Path(directory_path).mkdir(parents=True, exist_ok=True)


    @staticmethod
    def delete_directory_tree(directory_path: Union[str, Path]) -> None:
        """
        
        Description:
            Deletes the directory tree whose top level is specified by the directory path.

        Args:
            directory_path(Union[str, Path]): Directory path of the top level in the directory tree.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If the directory path exists:
        if PathUtils.is_path_exist(directory_path):
            # Remove the entire directory tree.
            shutil.rmtree(directory_path)


    @staticmethod
    def delete_file(file_path: Union[str, Path]) -> None:
        """
        
        Description:
            Attempts to delete the file specified by its file path from the file system.

        Args:
            file_path(Union[str, Path]): File path of the file whose deletion is desired.
        
        Returns:
            None

        Raises:
            FileNotFoundError:
                If the file does not exist,
                then print an error message.
                
        """
        
        # Constant for the storage of the file not found error message.
        EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR = str(file_path) + ': ' + String.EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR

        # Attempt to:
        try:
            # Remove the file.
            Path(file_path).unlink()
        
        # Handle: FileNotFoundError.
        except FileNotFoundError:
            # Print the file not found error message.
            print(EXCEPTION_MESSAGE_FILE_NOT_FOUND_ERROR)


    @staticmethod
    def get_filename(file_path: str) -> str:
        """
        
        Description:
            Based on the current platform,
            returns the filename of the file specified by the file path.

        Args:
            file_path(str): File path for the file whose name is desired.
        
        Returns:
            str: Name of the file derived from its file path.

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Divide the path.
            split_path = file_path.split('\\')
            
            # If the last element of the list is empty:
            if split_path[-1] == '':
                # Return the pre-last element of the list.
                return split_path[-2]
            
            # If the last element is not empty.
            else:
                # Return the last element of the list.
                return split_path[-1]
        
        # If the current platform is not Windows.
        else:
            # Divide the path.
            split_path = file_path.split('/')

            # If the last element of the list is empty:
            if split_path[-1] == '':
                # Return the pre-last element of the list.
                return split_path[-2]
            
            # If the last element of the list is not empty:
            else:
                # Return the last element of the list.
                return split_path[-1]


    @staticmethod
    def hide_file_on_windows(file_path: str) -> None:
        """
        
        Description:
            Based on the current platform,
            executes a command to hide the file on the file system based on its file path.

        Args:
            file_path(str): File path for the file to hide.
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # Constant for the storage of the command to hide a file on Windows.
        COMMAND_HIDE_FILE_ON_WINDOWS = String.COMMAND_HIDE_FILE_ON_WINDOWS + ' ' + '"' + file_path + '"'

        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Execute the command to hide the file.
            os.system(COMMAND_HIDE_FILE_ON_WINDOWS)


    @staticmethod
    def is_directory(path: Union[str, Path]) -> bool:
        """
        
        Description:
            Checks if the specified path represents a directory or not.

        Args:
            path(Union[str, Path]): Path to check for its representation.
        
        Returns:
            bool: Whether the path represents a directory.

        Raises:
            None
                
        """
        
        # Assert if the path represents a directory.
        return Path(path).is_dir()


    @staticmethod
    def is_directory_empty(path: Union[str, Path]) -> bool:
        """
        
        Description:
            Checks if the specified path represents an empty directory.

        Args:
            path(Union[str, Path]): Path for which representation and emptiness are checked.
        
        Returns:
            bool: Whether the path represents an empty directory.

        Raises:
            None
                
        """
        
        # Assert if the path represents a non-empty directory.
        return PathUtils.is_directory(path) and PathUtils._is_directory_empty(path)


    @staticmethod
    def is_file(path: Union[str, Path]) -> bool:
        """
        
        Description:
            Checks if the specified path represents a file or not.

        Args:
            path(Union[str, Path]): Path to check for its representation.
        
        Returns:
            bool: Whether the path represents a file.

        Raises:
            None
                
        """

        # Assert if the path represents a file.
        return Path(path).is_file()


    @staticmethod
    def is_path_exist(path: Union[str, Path]) -> bool:
        """
        
        Description:
            Checks if the specified path exists on the file system.

        Args:
            path(Union[str, Path]): Path to check for existence.
        
        Returns:
            bool: Whether the path exists or is non-existing.

        Raises:
            None
                
        """

        # Assert if the path exists.
        return Path(path).exists()


    @staticmethod
    def remove_trailing_slash_from_path(path: str)  -> str:
        """
        
        Description:
            Based on the current platform,
            removes the trailing slash from the specified path and returns it.


        Args:
            path(str): Path whose trailing slash must be removed.
        
        Returns:
            str: Path without the trailing slash.

        Raises:
            None
                
        """

        # Variable for the storage of the path separator on Linux.
        path_separator = '/'

        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Update the path separator.
            path_separator = '\\'

        # If the path ends with a path separator:
        if path.endswith(path_separator):
            # Return the path without the path separator.
            return path[:-1]
        
        # IF the path does not end with a path separator:
        else:
            # Return the path intact.
            return path


    @staticmethod
    def _is_directory_empty(directory_path: Union[str, Path]) -> bool:
        """
        
        Description:
            Checks if the specified directory path represents an empty directory.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            directory_path(Union[str, Path]): Path of the directory for which emptiness is checked.
        
        Returns:
            bool: Whether the directory is empty or contains items.

        Raises:
            None
                
        """
        
        # Assert if the directory is empty.
        return len(list(Path(directory_path).iterdir())) == 0


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass