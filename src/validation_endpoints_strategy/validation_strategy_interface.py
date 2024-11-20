"""
Module for ValidationStrategy Abstract Class.

This module provides a base class for creating custom validation strategies. The `ValidationStrategy` class defines an interface that requires subclasses to implement a `validate` method, allowing for flexible validation mechanisms based on different rules.

Author: Isabela Yabe
Last Modified: 09/11/2024
Status: Put logs

Dependencies:
    - ABC
    - abstractmethod

Classes:
    - ValidationStrategy: Abstract base class for creating validation strategies.
"""
from abc import ABC, abstractmethod

class ValidationStrategy(ABC):
    """
    ValidationStrategy class.

    This abstract class defines an interface for validation strategies. Any class inheriting from `ValidationStrategy`
    must implement the `validate` method, which accepts a string as input and performs validation based on the specific
    strategy defined in the subclass.

    Methods:
        - validate(data: str): Abstract method to validate input data based on specific rules.

    Example:
        class NumericValidationStrategy(ValidationStrategy):
            def validate(self, data: str):
                if not data.isdigit():
                    raise ValueError("Data must be numeric.")
        
        validator = NumericValidationStrategy()
        validator.validate("123")  # Valid
        validator.validate("abc")  # Raises ValueError
    """
    @abstractmethod
    def validate(self, data: str): ...