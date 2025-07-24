import os
from networksecurity.logging  import logger
import sys

class NetworkSecurityException(Exception):
    """Base class for all network security exceptions."""
    def __init__(self, error_message : str, error_details: sys):
        
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        if exc_tb is not None:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_number = exc_tb.tb_lineno
        else:
            self.file_name = "Unknown"
            self.line_number = "Unknown"
       
    def __str__(self):
        return f"Error occurred in script: {self.file_name} at line: {self.line_number} with message: {self.error_message}"

if __name__ == "__main__":
    try:
        logger.logging.info("Starting the network security exception demo.")
        1 / 0  # Force an exception for demonstration
       # raise NetworkSecurityException("This is a test exception")

    except Exception as e:
        try:
            raise NetworkSecurityException(str(e), sys)
        except NetworkSecurityException as e:
            logger.logging.info(f"Exception caught: {e}")
            logger.logging.info(f"Exception details: {e.file_name}, Line: {e.line_number}")