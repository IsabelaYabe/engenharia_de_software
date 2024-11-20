"""
Module: Utilities for Tuple to Dictionary Conversion

This module provides utility functions for converting rows from a database query (represented as tuples)
into dictionary format. These functions help format database query results into more readable and
structured data representations.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Complete

Dependencies:
    - os
    - sys
    - custom_logger

Functions:
    - tuple_rows_to_dict(list_of_tuples, columns): Converts a list of tuples into a list of dictionaries.
    - tuple_to_dict(tuple, columns): Converts a single tuple into a dictionary.
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))
from custom_logger import setup_logger

logger = setup_logger()

def tuple_rows_to_dict(list_of_tuples, columns):
    """
    Converts a list of tuples (rows from a database table) into a list of dictionaries.

    Each tuple represents a row from the database, and the `columns` parameter specifies the corresponding
    column names. The function maps each value in a tuple to its corresponding column name, creating a 
    dictionary for each row.

    Args:
        list_of_tuples (list[tuple]): A list of tuples representing rows from a database table.
        columns (list[str]): A list of column names corresponding to the values in each tuple.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a row in the format {column: value}.
    """
    n_cols = len(columns)
    list_ = []
    for tuple_ in list_of_tuples: 
        current_dict = {}
        for i in range(n_cols):
            current_dict[columns[i]] = tuple_[i]
        list_.append(current_dict)
    logger.info(f"List of dictionaries: {list_}")
    return list_

def tuple_to_dict(tuple, columns):
    """
    Converts a single tuple (a row from a database table) into a dictionary.

    The function maps each value in the tuple to its corresponding column name, creating a dictionary that
    represents the row.

    Args:
        tuple (tuple): A tuple representing a single row from a database table.
        columns (list[str]): A list of column names corresponding to the values in the tuple.

    Returns:
        dict: A dictionary representing the row in the format {column: value}.
    """
    n_cols = len(columns)
    _dict = {}
    for i in range(n_cols):
        _dict[columns[i]] = tuple[i]
    logger.info(f"Dictionary: {_dict}")
    return _dict