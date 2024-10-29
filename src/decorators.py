"""
    Module for creating decorators for the project.

    Author: Isabela Yabe

    Last Modified: 28/10/2024

"""
import mysql.connector
from mysql.connector import Error

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