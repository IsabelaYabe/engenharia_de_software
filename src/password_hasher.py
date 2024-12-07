"""
Module for password hashing and encryption.

This module provides the `PasswordHasher` class, which is responsible for 
hashing passwords using SHA-256. This class can be used as a standalone utility 
or as part of a decorator for user profile creation.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - hashlib.sha256 (for password hashing)
    - custom_logger.setup_logger (for logging)
"""

from hashlib import sha256
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from custom_logger import setup_logger
from singleton_decorator import singleton

logger = setup_logger()

@singleton
class PasswordHasher:
    """
    Class responsible for password hashing and encryption.

    The `PasswordHasher` class provides a method to hash passwords using SHA-256. 
    It can be used as a utility or integrated into a decorator to ensure password 
    security during user profile creation.
    """
    
    def __init__(self):
        """
        Initializes the PasswordHasher instance.

        No parameters are required, as this class only provides hashing 
        functionality.
        """
        logger.info("PasswordHasher initialized.")

    def hash_password(self, password):
        """
        Hashes the given password using SHA-256.

        Args:
            password (str): The password in plain text.

        Returns:
            str: The SHA-256 hashed version of the password.

        Logs:
            - Logs an info message indicating that password hashing is taking place.
            - Logs an error message if an exception occurs.

        Raises:
            ValueError: If the provided password is not a string.
            Exception: If an error occurs during the hashing process.
        """
        logger.info("Hashing password using SHA-256.")

        if not isinstance(password, str):
            logger.error("Invalid password type. Expected a string.")
            raise ValueError("Password must be a string.")

        try:
            hashed_password = sha256(password.encode()).hexdigest()
            logger.debug(f"Password successfully hashed: {hashed_password}")
            return hashed_password
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise Exception("Error hashing password.") from e

def hash_password_decorator(func):
    """
    Decorator to hash the 'password' argument before calling the target function.
    
    It assumes that the function being decorated has a 'self' as the first argument 
    (i.e., it is a method of a class) and that 'password' is present in the arguments.
    """
    def wrapper(self, *args, **kwargs):
        """
        Wraps the target function, hashes the 'password' in kwargs, and calls the function.
        """
        if "password" in kwargs:
            logger.info("Hashing password before calling the original function.")
            logger.debug(f"Original password: {kwargs['password']}")
            kwargs["password"] = self.password_hasher.hash_password(kwargs["password"])
            logger.debug(f"Hashed password: {kwargs['password']}")
        return func(self, *args, **kwargs)
    return wrapper