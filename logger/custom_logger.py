# import os
# from datetime import datetime
# import logging

# class CustomLogger:
#     def __init__(self):
#         # Create a logs directory if it doesn't exist
#         self.logs_dir = os.path.join(os.getcwd(), "logs")
#         os.makedirs(self.logs_dir, exist_ok=True)

#         # Define the log file path
#         self.LOG_FILE_PATH = os.path.join(self.logs_dir, f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log")

#         # Configure the logging
#         logging.basicConfig(
#             filename=self.LOG_FILE_PATH,
#             level=logging.INFO,
#             format="[ %(asctime)s ]- %(name)s - %(levelname)s -%(lineno)d -%(message)s",
#             handlers=[
#                 logging.FileHandler(self.LOG_FILE_PATH),
#                 logging.StreamHandler()
#             ]
#         )

#     def get_logger(self, name=__file__):
#         return logging.getLogger(os.path.basename(name))

#     def info(self, message):
#         self.get_logger(__file__).info(message)

#     def warning(self, message):
#         self.get_logger(__file__).warning(message)

#     def error(self, message):
#         self.get_logger(__file__).error(message)

# if __name__ == "__main__":
#     # Example usage of the CustomLogger
#     logger = CustomLogger()
#     logger.info("This is an info message.")
#     logger.warning("This is a warning message.")
#     logger.error("This is an error message.")
    
    
# # This code defines a custom logger that writes logs to both a file and the console.
# # The log files are stored in a 'logs/' directory with timestamped filenames.
# # The logger supports different log levels and formats the log messages consistently.
# # It can be used to log messages at various levels (info, warning, error) and can be easily integrated into other modules.

# import logging
# import os
# import sys
# from datetime import datetime

# class DualLogger:
#     """
#     A logger that writes logs to both a file and the console.

#     - File logs include all levels (DEBUG and above).
#     - Console logs include INFO level and above.
#     - Log files are stored in a 'logs/' directory with timestamped filenames.
#     """

#     def __init__(self, logger_name="DualLogger"):
#         """
#         Initializes the logger with file and console handlers.

#         Args:
#             logger_name (str): Name of the logger instance.
#         """
#         self.logger = logging.getLogger(logger_name)
#         self.logger.setLevel(logging.DEBUG)

#         # Create logs directory if it doesn't exist
#         logs_dir = os.path.join(os.getcwd(), "logs")
#         os.makedirs(logs_dir, exist_ok=True)

#         # Generate a timestamped log file name
#         log_file = os.path.join(logs_dir, f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log")

#         # Define a consistent log format
#         formatter = logging.Formatter("[ %(asctime)s ] - %(name)s - %(levelname)s - %(lineno)d - %(message)s")

#         # File handler for writing logs to a file
#         file_handler = logging.FileHandler(log_file)
#         file_handler.setLevel(logging.DEBUG)
#         file_handler.setFormatter(formatter)

#         # Stream handler for outputting logs to the console
#         stream_handler = logging.StreamHandler(sys.stdout)
#         stream_handler.setLevel(logging.INFO)
#         stream_handler.setFormatter(formatter)

#         # Add handlers only if they haven't been added already
#         if not self.logger.hasHandlers():
#             self.logger.addHandler(file_handler)
#             self.logger.addHandler(stream_handler)

#     def get_logger(self):
#         """
#         Returns the configured logger instance.

#         Returns:
#             logging.Logger: The logger object.
#         """
#         return self.logger

#     def info(self, message):
#         """
#         Logs an info-level message.

#         Args:
#             message (str): The message to log.
#         """
#         self.logger.info(message)

#     def warning(self, message):
#         """
#         Logs a warning-level message.

#         Args:
#             message (str): The message to log.
#         """
#         self.logger.warning(message)

#     def error(self, message):
#         """
#         Logs an error-level message.

#         Args:
#             message (str): The message to log.
#         """
#         self.logger.error(message)

# if __name__ == "__main__":
#     # Example usage of DualLogger
#     logger = DualLogger().get_logger()
#     logger.info("This is an info message.")
#     logger.warning("This is a warning message.")
#     logger.error("This is an error message.")



## This code defines a custom logger using structlog that writes structured logs to both a file and the console.
# ## The log files are stored in a 'logs/' directory with timestamped filenames.
# ## The logger supports different log levels and formats the log messages consistently.
# ## It can be used to log messages at various levels (info, warning, error) and can be easily integrated into other modules.
import logging
import os
import sys
from datetime import datetime
import structlog

class DualStructLogger:
    """
    A logger using structlog that writes structured logs to both a file and the console.

    - File logs include all levels (DEBUG and above).
    - Console logs include INFO level and above.
    - Log files are stored in a 'logs/' directory with timestamped filenames.
    """

    def __init__(self, logger_name="DualStructLogger"):
        """
        Initializes the structlog logger with file and console handlers.

        Args:
            logger_name (str): Name of the logger instance.
        """
        # Create logs directory
        logs_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # Create log file path
        log_file = os.path.join(logs_dir, f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log")

        # Standard logging setup
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )

        # Structlog configuration
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        self.logger = structlog.get_logger(logger_name)

    def get_logger(self):
        """
        Returns the configured structlog logger.

        Returns:
            structlog.stdlib.BoundLogger: The structured logger object.
        """
        return self.logger

if __name__ == "__main__":
    # Example usage
    logger = DualStructLogger().get_logger()
    logger.info("Application started", user="admin", action="login")
    logger.warning("Low disk space", disk="C:", remaining="500MB")
    logger.error("Unhandled exception", error="FileNotFoundError", file="config.yaml")