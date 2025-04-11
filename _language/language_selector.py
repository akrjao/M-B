# Project-specific module imports.
from _constant.string import String
from _jsonx.properties_json_handler import PropertiesJsonHandler


class LanguageSelector:
    """
    
    LanguageSelector enables the selection of a language dictionary to utilize when displaying screen text.
    The language dictionary utilized is dependent on the user selection.

    """


    @staticmethod
    def get_language_dict() -> dict:
        """
        
        Description:
            Based on the chosen locale,
            returns the respective language dictionary from the chosen language module.

        Args:
            None
        
        Returns:
            dict: Language dictionary of the chosen locale.

        Raises:
            None
                
        """
        
        # Constants for the storage of locale codes.
        LOCALE_CODE_FRENCH = String.LITERAL_LOCALE_CODE_FRENCH
        
        # Assign the language.
        locale = PropertiesJsonHandler.get_language()
        
        
        # If the locale is equal to the French locale code:
        if locale == LOCALE_CODE_FRENCH:
            # Import the French language module.
            from _language.french import French as language
        
        # If the locale is not equal to French localecode:
        else:
            # Import the English language module.
            from _language.english import English as language

        # Return the dictionary of the selected language.
        return language.dict


# If this module is executed as the main program:
if __name__ == "__main__":
    # Ignore.
    pass