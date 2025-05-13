import sys
from typing import TypeVar

ExceptionType = TypeVar('ExceptionType', bound=Exception)


class AppException(Exception):
    """Custom exception class to capture detailed error information.
    
    This exception provides contextual information about errors including:
    - The filename where the error occurred
    - The line number where the error occurred
    - The original error message
    
    Args:
        error_message: The original exception or error message
        error_detail: System execution information (from sys module)
    
    Example:
        >>> try:
        ...     raise ValueError("Example error")
        ... except Exception as e:
        ...     raise AppException(e, sys) from e
    """

    def __init__(self, error_message: ExceptionType | str, error_detail: sys) -> None:
        """Initialize the exception with detailed error information."""
        super().__init__(str(error_message))
        self.error_message = self.get_error_message_detail(
            error=error_message,
            error_detail=error_detail
        )

    @staticmethod
    def get_error_message_detail(error: ExceptionType | str, error_detail: sys) -> str:
        """Construct a detailed error message including file and line number.
        
        Args:
            error: Original exception object or error message
            error_detail: System execution info from sys module
            
        Returns:
            Formatted error message string
            
        Raises:
            AttributeError: If traceback information is unavailable
        """
        exc_type, exc_value, exc_tb = error_detail.exc_info()
        
        if exc_tb is None:
            return str(error)
            
        try:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            error_message = str(error)
            
            return (
                f"Error occurred in Python script: [{file_name}] "
                f"at line [{line_number}] with message: [{error_message}]"
            )
        except AttributeError as attr_error:
            return f"Error processing exception details: {attr_error}. Original error: {error}"

    def __repr__(self) -> str:
        """Official string representation of the exception."""
        return f"{self.__class__.__name__}(message={self.error_message})"

    def __str__(self) -> str:
        """User-friendly string representation of the exception."""
        return self.error_message