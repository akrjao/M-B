class Integer():
    """
    
    Integer is a class that provides integer constants to be utilized all over the project.
    It provides a central place for the management of all integer literals.

    """
    
    # Constant for the storage of the wait time on the welcome message screen (in seconds).
    WELCOME_MESSAGE_WAIT_TIME = 3
    
    # Constant for the storage of the number of spaces to use for indentation in json files.
    JSON_INDENT = 4
    
    # Constant for the storage of the return code denoting command execution success on subprocesses.
    RETURN_CODE_SUCCESS = 0
    
    # Constant for the storage of the wait time between iterations of the backup service (in seconds).
    BACKUP_SERVICE_ITERATION_WAIT_TIME = 5
    
    # Constant for the storage of the wait time between iterations of the monitoring service (in seconds).
    MONITORING_SERVICE_ITERATION_WAIT_TIME = 5
    
    # Constant for the storage of the number of letters the random string must comprise.
    RANDOM_STRING_LENGTH = 8


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass