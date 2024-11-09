"""
    Module for creating decorators for the project.

    Author: Isabela Yabe

    Last Modified: 07/11/2024

"""
import mysql.connector
from mysql.connector import Error

from functools import wraps
from flask import jsonify, request
#import json
#import os
#json_path = os.path.join(os.path.dirname(__file__), '..', 'data\json', 'banned_words.json')
#with open(json_path, 'r', encoding='utf-8') as file:
#    banned_words = set(json.load(file)["banned_words"])

def request_validations(strategies, *request_methods):
    def decorator(funcao):
        @wraps(funcao)
        def wrapped(*args, **kwargs):
            if request.method in request_methods:
                data = request.get_json()
                if data:
                    for strategy in strategies:
                        error = strategy.validate(data)
                        if error: 
                            return jsonify({"error": error}), 400
            return funcao(*args, **kwargs)
        return wrapped
    return decorator
                     

# Decorator for singleton classes
def singleton(class_):
    """
    Singleton decorator for classes.

    Args:
        class_ (_type_): _description_

    Returns:
        _type_: _description_
    """
    instances = {}

    def get_class(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    
    return get_class

## Decorator for check database existence
#def check_database(func): 
#    """
#    Decorator to check if the database exists before executing a function.
#
#    Args:
#        func (_type_): _description_
#
#    Returns:
#        _type_: _description_
#    """
#    def database_exists(self, host, user, password, database):
#        """
#        Checks if a database exists.
#
#        Args:
#            host (_type_): _description_
#            user (_type_): _description_
#            password (_type_): _description_
#            database (_type_): _description_
#
#        Returns:
#            _type_: _description_
#        """ 
#        try:
#            connection = mysql.connector.connect(
#                host=host,
#                user=user,
#                password=password
#            )
#            cursor = connection.cursor()
#            cursor.execute(f"SHOW DATABASES LIKE {database}")
#            result = cursor.fetchone()
#            return result is not None
#        except Error as e:
#            print(f"Error connection to MySQL: {e}")
#            return False
#        finally:
#            if "connection" in locals() and connection.is_connected():
#                cursor.close()
#                connection.close()
#        
#    def wrapper(self, host, user, password, database, *args, **kwargs):        