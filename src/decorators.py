"""
Module for creating decorators for the project.

This module provides decorators to enhance functionality in the project. It includes:
- `request_validations`: A decorator to apply multiple validation strategies to API request data based on the HTTP method.
- `singleton`: A decorator to implement the singleton pattern for classes, ensuring only one instance of the class is created.
- `immutable_fields`: A decorator, which enforces immutability on specified fields within
a database table by raising an exception if there is an attempt to update those fields.

Author: Isabela Yabe
Last Modified: 10/11/2024
Status: Complete, put logs

Dependencies:
    - mysql.connector (optional for database connection)
    - functools.wraps
    - flask.jsonify
    - flask.request
    - BannedWordsStrategy
    - SQLInjectionStrategy

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
from validation_strategy.banned_words_strategy import BannedWordsStrategy
from validation_strategy.sql_injection_strategy import SQLInjectionStrategy


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

def immutable_fields(fields):
    """
    Decorator to enforce immutability on specified fields in a class method.

    This decorator restricts updates to the fields specified in the `fields` argument. If an update attempt
    includes any of these fields, a `ValueError` is raised.

    Args:
        fields (list): A list of field names (strings) that should be immutable and cannot be updated.

    Returns:
        function: The decorated function that enforces immutability for specified fields.

    Raises:
        ValueError: If there is an attempt to update any of the immutable fields.
    """
    def decorador(update_method):
        @wraps(update_method)
        def wrapper(self, record_id, **kwargs):
            current_record = self.get_by_id(record_id)

            for field in fields:
                if field in kwargs and kwargs[field] != current_record.get(field):
                    raise ValueError(f"The '{field}' field is immutable and cannot be updated.")
            
            return update_method(self, record_id, **kwargs)
        return wrapper
    return decorador

def foreign_key_validation(foreign_keys):
    def decorador(funcao):
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from main_file import relationship_manager_central
        @wraps(funcao)
        def wrapper(self, *args, **kwargs):    
            for table_name in foreign_keys:
                table_name_id = table_name[:-1].replace(" ","_")+"_id"
                record_id = kwargs.get(table_name_id)
                table = relationship_manager_central.dict_relationships[table_name]
                if record_id and not table.get_by_id(record_id):
                    return f"{table.get_column_id()} {record_id} does not exist."
            return funcao(self, record_id, **kwargs)
        return wrapper
    return decorador 

'''
def transaction_validations(strategies):
    def decorator(funcao):
        @wraps(funcao)
        def wrapped(self, *args, **kwargs):
            for strategy in strategies:
                error = strategy.transaction_validation(self, *args, **kwargs)
                if error:
                    return jsonify({"error": error}), 400
            return funcao(self, *args, **kwargs)
        return wrapped
    return decorator'''