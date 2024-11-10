"""
Module for creating decorators for the project.

This module provides decorators to enhance functionality in the project. It includes:
- `request_validations`: A decorator to apply multiple validation strategies to API request data based on the HTTP method.
- `singleton`: A decorator to implement the singleton pattern for classes, ensuring only one instance of the class is created.

Author: Isabela Yabe
Last Modified: 09/11/2024
Status: In Development, put logs

Dependencies:
    - mysql.connector (optional for database connection)
    - functools.wraps
    - flask.jsonify
    - flask.request

Functions:
    - request_validations(strategies, *request_methods): Applies validation strategies to requests for specified HTTP methods.
    - singleton(class_): Implements the singleton pattern for a class.
"""

import mysql.connector
from mysql.connector import Error
from functools import wraps
from flask import jsonify, request

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from banned_words_strategy import BannedWordsStrategy
from sql_injection_strategy import SQLInjectionStrategy

banned_words_strategy = BannedWordsStrategy()
sql_injection_strategy = SQLInjectionStrategy()

def request_validations(strategies=[banned_words_strategy, sql_injection_strategy], *request_methods):
    """
    Decorator to apply validation strategies to API request data based on HTTP methods.

    This decorator checks the HTTP method of incoming requests and applies specified validation strategies to the request data if the method matches one of the allowed methods (e.g., POST, PUT). If any validation strategy returns an error, the decorator interrupts the request, returning an error response.

    Args:
        strategies (list): A list of validation strategy instances implementing a `validate` method.
        *request_methods (str): Variable number of HTTP methods to restrict validation (e.g., "POST", "PUT").

    Returns:
        function: The decorated function that performs validation before proceeding.
    """
    def decorator(funcao):
        @wraps(funcao)
        def wrapped(*args, **kwargs):
            data = request.get_json()
            if request.method in request_methods:
                if data:
                    for strategy in strategies:
                        error = strategy.validate(data)
                        if error: 
                            return jsonify({"error": error}), 400
            return funcao(*args, **kwargs)
        return wrapped
    return decorator
                     
def singleton(class_):
    """
    Singleton decorator for classes.

    Ensures only one instance of the decorated class is created. Subsequent calls to create an instance of the class will return the same instance.

    Args:
        class_ (type): The class to be decorated as a singleton.

    Returns:
        function: A function that returns the singleton instance of the class.
    """
    instances = {}

    def get_class(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_class      