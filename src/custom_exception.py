import sys
import traceback

class CustomException(Exception):
    def __init__(self, error_message, error_details=None):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_details)

    @staticmethod
    def get_detailed_error_message(error_message, error_details):
        # Extract traceback from sys.exc_info(), not from error object
        exc_type, exc_obj, exc_tb = traceback.extract_tb(sys.exc_info())

        # If traceback is not available
        if exc_tb is None:
            return f"{error_message}"

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return f"Error occurred in script: {file_name} at line number: {line_number} with message: {error_message}"

    def __str__(self):
        return self.error_message
