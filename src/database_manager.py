"""
    Module for DatabaseManager class.

    This module provides a class for managing a single MySQL table in a database.

    Author: Isabela Yabe

    Date: 15/10/2024
"""
import uuid
import mysql.connector


class DatabaseManager:
    """
    DatabaseManager class.
    
    This class provides basic database operations and manages a single table in a MySQL database.
    
    Attributes:
    - db_config (dict): A dictionary containing the MySQL database configuration.
    - table_name (str): The name of the table managed by this instance.
    
    Methods:
    - _connect(self): Establishes a connection to the MySQL database.
    - _create_table(self, create_table_sql): Creates the managed table with the provided SQL statement.
    - modify_column(self, old_column_name, new_column_name): Modifies a column name.
    - delete_row(self, row_id): Deletes a row from the table.
    - delete_table(self): Deletes the entire table.
    - insert_row(self, columns, values): Inserts a new row into the table.
    - update_row(self, column_values, condition): Updates specific columns based on a condition.
    - get_by_id(self, record_id): Retrieves a record by its ID from the table.
    - delete_column(self, column_name): Deletes a column from the table.
    """
    
    def __init__(self, host, user, password, database, table_name = None):
        """
        Constructor for the DatabaseManager class.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user"s password.
            database (str): The name of the MySQL database.
            table_name (str): The name of the table to be managed by this instance.
        """
        self._db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.table_name = table_name
        self._create_database_if_not_exists(database)
        self._connect()
    
    def _connect(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            conn: A MySQL database connection object.
        """
        return mysql.connector.connect(**self._db_config)
    
    def _create_database_if_not_exists(self, database):
        """
        Creates the database if it does not exist.

        Parameters:
            database (str): The name of the database to be created.
        """
        conn = mysql.connector.connect(
            host=self._db_config["host"],
            user=self._db_config["user"],
            password=self._db_config["password"]
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        cursor.close()
        conn.close()

    def create_table(self, create_table_sql):
        """
        Creates the table in the MySQL database with the provided SQL statement.

        Parameters:
            create_table_sql (str): The SQL query to create the table.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def modify_column(self, old_column_name, new_column_name):
        """
        Modifies a column name in the managed table.
        
        Parameters:
            old_column_name (str): The current name of the column.
            new_column_name (str): The new name of the column.
        """
        conn = self._connect()
        cursor = conn.cursor()
        alter_table_sql = f"ALTER TABLE {self.table_name} CHANGE {old_column_name} {new_column_name};"
        cursor.execute(alter_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def delete_row(self, row_id):
        """
        Deletes a row from the managed table based on row_id.

        Parameters:
            row_id (str): The row_id to match for deleting rows.
        """
        conn = self._connect()
        cursor = conn.cursor()
        delete_sql = f"DELETE FROM {self.table_name} WHERE id = %s;"
        cursor.execute(delete_sql, (row_id,))
        conn.commit()
        cursor.close()
        conn.close()


    def delete_table(self, table_name):
        """
        Deletes the managed table from the database.
        """
        conn = self._connect()
        cursor = conn.cursor()
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name};"
        cursor.execute(drop_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_row(self, table, columns, values):
        """
        Inserts a new row into the managed table.
        
        Parameters:
            columns (list): A list of column names to insert values into.
            values (tuple): A tuple of values corresponding to the columns.
        """
        conn = self._connect()
        cursor = conn.cursor()
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders});"
        cursor.execute(insert_sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    def update_row(self, column_values, condition):
        """
        Updates specific columns with the provided values based on a condition.

        Parameters:
            column_values (dict): A dictionary with column names as keys and the updated values as values.
            condition (str): The condition to select the row(s) to be updated (e.g., "id = %s").

        Returns:
            None
        """
        conn = self._connect()
        cursor = conn.cursor()

        # Formata os pares "coluna = valor"
        updates = ", ".join([f"{column} = %s" for column in column_values.keys()])
        values = tuple(column_values.values())

        update_sql = f"UPDATE {self.table_name} SET {updates} WHERE {condition};"
        
        # Executa a query com os valores
        cursor.execute(update_sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    def get_by_id(self, record_id, id_column="id"):
        """
        Retrieves a record by its ID from the database.
    
        Parameters:
            record_id (str): The ID of the record to be fetched.
            id_column (str): The name of the ID column in the table (default is "id").
    
        Returns:
            dict: A dictionary with the record details, or None if not found.
        """
        conn = self._connect()
        cursor = conn.cursor()
        
        # Query usando a coluna de ID explícita
        query = f'SELECT * FROM {self.table_name} WHERE {id_column} = %s'
        cursor.execute(query, (record_id,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
    
        if record:
            return {f"{id_column}": record[0], "name": record[1], "description": record[2], "price": record[3]}
        return None
    
    def get_all(self, table):
        """
        Retrieves all records from the managed table.
        
        Returns:
            list: A list of dictionaries containing all records in the table.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table};")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return records
    
    def get_cols(self, table):
        """
        Retrieves all columns from the managed table.
        
        Returns:
            list: A list of column names.
        """
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM {table};")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return records