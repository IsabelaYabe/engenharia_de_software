"""
Module for CustomLogger Class.

This module provides a configurable and flexible logging solution using Python's `logging` module. 
The `CustomLogger` class allows for the creation of a logger instance with customized file and console handlers, 
applying specific formatting and filtering to log messages. A `LogFilter` is also provided to exclude log messages 
that start with sensitive keywords, such as "password".

Author: Isabela Yabe
Last Modified: 09/11/2024
Status: Complete

Dependencies:
    - logging
    - decorators.singleton

Classes:
    - LogFilter: A logging filter class that excludes sensitive information from logs.
    - CustomLogger: A singleton class for creating a flexible logger with customizable handlers and filters.

Functions:
    - setup_logger(): Returns an instance of `CustomLogger` for convenient access to a pre-configured logger.
"""

import logging
from logging import Filter
from logging import FileHandler, StreamHandler, Formatter
from decorators_method import singleton

class LogFilter(Filter):
    """
    LogFilter class.

    This class defines a filter for log messages that excludes messages starting with the word "password".
    It helps to avoid logging sensitive information.

    Methods:
        - filter(record): Returns True if the message does not start with "password", False otherwise.
    """
    def filter(self, record):
        return not record.msg.lower().startswith("password")

@singleton
class CustomLogger:
    """
        CustomLogger Class

        This class provides a flexible and configurable logging solution using Python's built-in logging module.
        It allows the creation of a logger instance with customized file and console handlers, each configured 
        with specific formatting and logging levels.

        The CustomLogger class supports:
        - Configurable log level and log file name.
        - Separate console and file handlers to manage logging outputs.
        - A LogFilter to exclude messages that start with sensitive information like "password".
        - The ability to add additional handlers and filters as needed.

        Attributes:
            log_file (str): The path to the file where log messages are saved.
            level (int): The default logging level for console output.
            logger (Logger): The main logger instance created for logging messages.
            handlers (list): A list of logging handlers, such as file and console handlers.
            filters (list): A list of filters to apply to logging messages.

        Methods:
            _create_file_handler: Sets up the file handler with specific formatting and logging level.
            _create_console_handler: Sets up the console handler with specific formatting and logging level.
            add_handler: Adds an external logging handler to the logger.
            add_filter: Adds an external filter to the logger.
            _setup_logger: Initializes the logger with all specified handlers and filters.
            get_logger: Returns the logger instance for use in other modules.

        Helper Function:
            setup_logger(): Returns an instance of CustomLogger's logger for convenient access to a pre-configured logger.
    """
    def __init__(self, log_file="app.log", level=logging.DEBUG, handlers=None, filters=None):
        """
        Initializes the CustomLogger instance with specified file path, log level, handlers, and filters.

        Args:
            log_file (str): The path to the file where log messages are saved. Default is "app.log".
            level (int): The default logging level for console output. Default is logging.DEBUG.
            handlers (list, optional): Custom handlers for the logger. If None, default file and console handlers are used.
            filters (list, optional): Custom filters for the logger. If None, a default LogFilter is applied.
        """
        self.log_file = log_file
        self.level = level
        self.logger = logging.getLogger(__name__)
        self.handlers = handlers or [self._create_file_handler(), self._create_console_handler()]
        self.filters = filters or [LogFilter()]
        self._setup_logger()

    def _create_file_handler(self):
        """
        Creates a file handler for logging with a specific formatter and level. 

        The file handler is configured to append to the existing log file if it exists, ensuring that previous logs
        are preserved.

        Returns:
            FileHandler: A configured file handler for logging to a file.
        """
        file_log_formatter = Formatter("%(asctime)s | %(levelname)s | %(module)s:%(funcName)s - %(message)s")
        file_handler = FileHandler(self.log_file, mode="a", encoding="utf-8")

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_log_formatter)

        return file_handler
    
    def _create_console_handler(self):
        """
        Creates and configures a console handler for logging with specific formatting and level.

        Returns:
            StreamHandler: A configured console handler for displaying logs in the console.
        """
        console_log_formatter = Formatter(
            "%(asctime)s | %(levelname)s | %(module)s:%(funcName)s:line%(lineno)d - %(message)s")
        console_handler = StreamHandler()
        
        console_handler.setLevel(self.level)
        console_handler.setFormatter(console_log_formatter)
        
        return console_handler
    
    def add_handler(self, handler):
        """
        Adds an external logging handler to the logger.

        Args:
            handler (logging.Handler): The handler to be added to the logger.
        """
        self.logger.addHandler(handler)

    def add_filter(self, filter):
        """
        Adds an external filter to the logger.

        Args:
            filter (logging.Filter): The filter to be added to the logger.
        """
        self.logger.addFilter(filter)

    def _setup_logger(self):
        """
        Sets up the logger by adding all specified handlers and filters, and setting the logging level.
        """
        for handler in self.handlers:
            self.add_handler(handler)
        for filter in self.filters:
            self.add_filter(filter)
        self.logger.setLevel(self.level)

    def get_logger(self):
        """
        Returns the logger instance for use in other modules.

        Returns:
            Logger: The main logger instance configured with file and console handlers.
        """
        return self.logger
    
def setup_logger():
    """
    Helper function to retrieve a pre-configured logger instance.

    This function returns an instance of `CustomLogger`'s logger, simplifying access to a pre-configured
    logging setup for applications that need consistent logging behavior.

    Returns:
        Logger: An instance of the logger with pre-configured handlers and filters.
    """
    return CustomLogger().get_logger()

if __name__ == "__main__":
    logger = setup_logger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
