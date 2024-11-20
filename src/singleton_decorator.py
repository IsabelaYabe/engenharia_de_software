"""
Singleton Decorator Module.

This module provides a `singleton` decorator that can be used to ensure a class has only one instance.
The decorator is useful for cases where maintaining a single instance of a class throughout the application
lifecycle is necessary, such as in configuration managers, database connections, or logging utilities.

Author: Isabela Yabe
Last Modified: 20/11/2024
Status: Complete

Functions:
    - singleton(class_): Decorates a class to ensure it behaves as a singleton.
"""

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