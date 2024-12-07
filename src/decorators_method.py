"""
Module for Project Decorators.

This module provides a set of decorators designed to enhance functionality in the project.
The decorators include features for request validation, enforcing immutability on database fields,
and more, ensuring robust input handling and safe data operations.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Incomplete; 
    request_validations completed (tests OK); 
    immutable_fields completed (tests OK).

Dependencies:
    - mysql.connector
    - functools.wraps
    - flask.jsonify
    - flask.request
    - utils.utils (tuple_to_dict)
    - validation_endpoints_strategy.banned_words_strategy.BannedWordsStrategy
    - validation_endpoints_strategy.sql_injection_strategy.SQLInjectionStrategy
    - custom_logger.setup_logger

Decorators:
    - request_validations: Validates request data using specified validation strategies.
    - immutable_fields: Prevents updates to specified immutable fields in a database table.
"""
import mysql.connector
from mysql.connector import Error
from functools import wraps
from flask import jsonify, request
from utils.utils import tuple_to_dict

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from validation_endpoints_strategy.banned_words_strategy import BannedWordsStrategy
from validation_endpoints_strategy.sql_injection_strategy import SQLInjectionStrategy
from custom_logger import setup_logger

logger = setup_logger()

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
                            logger.error(f"Validation error: {error}, strategy applied: {strategy}")
                            return jsonify({"error": error}), 400
                        logger.info(f"Request passed validation, strategy applied: {strategy}")    
                    logger.info("Request passed validation")
            return funcao(*args, **kwargs)
        return wrapped
    return decorator

def immutable_fields(attribute_name):
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
    def decorator(update_method):
        @wraps(update_method)
        def wrapper(self, record_id, **kwargs):
            immutable_fields = getattr(self, attribute_name, [])
    
            current_record = self.get_by_id(record_id)
            if current_record is None:
                logger.error(f"Record with ID {record_id} not found")
                raise ValueError(f"Record with ID {record_id} not found")
            logger.info(f"Record with ID {record_id} found")

            current_record_dict = tuple_to_dict(current_record, self.columns)
            
            for field in immutable_fields:
                if field in kwargs and kwargs[field] != current_record_dict.get(field):
                    logger.error(f"Attempt to update immutable field {field}")
                    raise ValueError(f"The {field} field is immutable and cannot be updated")
            logger.info("Update allowed fields")

            return update_method(self, record_id, **kwargs)

        return wrapper
    return decorator

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