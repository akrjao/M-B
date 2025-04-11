# Project-specific module imports.
from _autostart.linux_autostarter import LinuxAutostarter
from _autostart.windows_autostarter import WindowsAutostarter
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler
from _miscellaneous.platform_identifier import PlatformIdentifier


class Autostarter:
    """
    
    Autostarter serves to start and schedule or stop and deschedule both the monitoring and backup services.
    To achieve that, Autostarter determines the current platform on which the script is executing to invoke the proper methods.

    """


    @staticmethod
    def handle_backup() -> None:
        """
        
        Description:
            Based on the value of the backup autostart status attribute,
            enables and starts or disables and stops the backup service.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        ENABLED = String.LITERAL_ENABLED
        DISABLED = String.LITERAL_DISABLED
        
        # If the backup autostart status attribute is set to enabled:
        if PropertiesJsonHandler.get_backup_autostart_status() == ENABLED:
            # Enable the backup service.
            Autostarter._enable_backup()
        
        # If the backup autostart status attribute is set to disabled:
        elif PropertiesJsonHandler.get_backup_autostart_status() == DISABLED:
            # Disable the backup service.
            Autostarter._disable_backup()


    @staticmethod
    def handle_monitoring() -> None:
        """
        
        Description:
            Based on the value of the monitoring autostart status attribute,
            enables and starts or disables and stops the monitoring service.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """

        # Constants for the storage of string literals.
        ENABLED = String.LITERAL_ENABLED
        DISABLED = String.LITERAL_DISABLED

        # If the monitoring autostart status attribute is set to enabled:
        if PropertiesJsonHandler.get_monitoring_autostart_status() == ENABLED:
            # Enable the monitoring service.
            Autostarter._enable_monitoring()
        
        # If the monitoring autostart status attribute is set to disabled:
        elif PropertiesJsonHandler.get_monitoring_autostart_status() == DISABLED:
            # Disable the monitoring service.
            Autostarter._disable_monitoring()


    @staticmethod
    def _disable_backup() -> None:  
        """
        
        Description:
            Based on the current platform,
            invokes the proper method to disable and stop the backup service.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Disable the backup service on Windows.
            WindowsAutostarter.disable_backup()
        
        # If the current platform is not Windows:
        else:
            # Disable the backup service on Linux.
            LinuxAutostarter.disable_backup()


    @staticmethod
    def _disable_monitoring() -> None:
        """
        
        Description:
            Based on the current platform,
            invokes the proper method to disable and stop the monitoring service.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Disable the monitoring service on Windows.
            WindowsAutostarter.disable_monitoring()
        
        # If the current platform is not Windows:
        else:
            # Disable the monitoring service on Linux.
            LinuxAutostarter.disable_monitoring()


    @staticmethod
    def _enable_backup() -> None:    
        """
        
        Description:
            Based on the current platform,
            invokes the proper method to enable and start the backup service.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Enable the backup service on Windows.
            WindowsAutostarter.enable_backup()
        
        # If the current platform is not Windows:
        else:
            # Enable the backup service on Linux.
            LinuxAutostarter.enable_backup()


    @staticmethod
    def _enable_monitoring() -> None:    
        """
        
        Description:
            Based on the current platform,
            invokes the proper method to enable and start the monitoring service.

            Note: This method is not meant to be accessed from outside this class.

        Args:
            None
        
        Returns:
            None

        Raises:
            None
                
        """
        
        # If the current platform is Windows:
        if PlatformIdentifier.is_windows():
            # Enable the monitoring service on Windows.
            WindowsAutostarter.enable_monitoring()
        
        # If the current platform is not Windows:
        else:
            # Enable the monitoring service on Linux.
            LinuxAutostarter.enable_monitoring()


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass