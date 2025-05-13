import logging
import os
from datetime import datetime
from typing import Optional

class LoggingConfig:
    """Configure application logging with file and console handlers.
    
    Features:
    - Creates log directory if it doesn't exist
    - Generates timestamped log files
    - Configures both file and console logging
    - Allows customizable log formats and levels
    
    Args:
        log_dir: Directory to store log files (default: "logs")
        log_prefix: Prefix for log files (default: "log")
        file_log_level: File logging level (default: logging.NOTSET)
        console_log_level: Console logging level (default: logging.WARNING)
    """
    
    def __init__(
        self,
        log_dir: str = "logs",
        log_prefix: str = "log",
        file_log_level: int = logging.NOTSET,
        console_log_level: Optional[int] = logging.WARNING
    ) -> None:
        self.log_dir = os.path.abspath(log_dir)
        self.log_prefix = log_prefix
        self.file_log_level = file_log_level
        self.console_log_level = console_log_level
        self._setup_logging()

    def _get_log_file_path(self) -> str:
        """Generate timestamped log file path."""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        filename = f"{self.log_prefix}_{timestamp}.log"
        return os.path.join(self.log_dir, filename)

    def _create_log_dir(self) -> None:
        """Create log directory if it doesn't exist."""
        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create log directory {self.log_dir}: {e}")

    def _setup_logging(self) -> None:
        """Configure logging handlers and formatting."""
        self._create_log_dir()
        log_file_path = self._get_log_file_path()
        
        # Clear any existing handlers
        logging.root.handlers = []
        
        # Common formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler
        file_handler = logging.FileHandler(
            filename=log_file_path,
            mode='a'  # Append mode to preserve logs
        )
        file_handler.setLevel(self.file_log_level)
        file_handler.setFormatter(formatter)
        
        # Console handler
        if self.console_log_level is not None:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.console_log_level)
            console_handler.setFormatter(formatter)
            logging.root.addHandler(console_handler)
        
        logging.root.addHandler(file_handler)
        logging.root.setLevel(min(
            self.file_log_level,
            self.console_log_level if self.console_log_level is not None else self.file_log_level
        ))

# Example usage
if __name__ == "__main__":
    # Initialize logging configuration
    LoggingConfig(
        log_dir="logs",
        log_prefix="log",
        file_log_level=logging.INFO,
        console_log_level=logging.DEBUG
    )
    
    # Test logging
    logging.info("Application logging configured successfully")
    logging.debug("Debug message")
    logging.warning("Warning message")
    logging.error("Error message")