"""
    Module for DatabaseManager abstractmethod class.

    This module provides a class for managing a single MySQL table in a database.

    Author: Isabela Yabe

    Dependencies:
        - mysql.connector
        - flask
        - jsonify

    Last Modified: 28/10/2024

"""

from flask import Flask, jsonify, request
from abc import ABC, abstractmethod
import mysql.connector


class DatabaseManager(ABC):
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
    
    def __init__(self, host, user, password, database, table_name):
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
        self._table_name = table_name
        self._app = Flask(__name__)

        @self.app.route(f"/api/{self.table_name}/<record_id>", methods=["GET"])
        def get_record(record_id):
                return self.get_record_api(record_id)
    
    def _connect(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            conn: A MySQL database connection object.
        """
        # Aqui estamos nos conectando a base de dados com as configurações passadas no inicializador
        return mysql.connector.connect(**self._db_config) 

    @abstractmethod
    def _create_table(self, create_table_sql): # create_table_sql (aqui passamos a query que queremos executar)
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
 
    def _modify_column(self, old_column_name, new_column_name):
        """
        Modifies a column name in the managed table.
        
        Parameters:
            old_column_name (str): The current name of the column.
            new_column_name (str): The new name of the column.
        """
        conn = self._connect()
        cursor = conn.cursor()
        alter_table_sql = f"ALTER TABLE {self.table_name} RENAME COLUMN {old_column_name} TO {new_column_name};"
        cursor.execute(alter_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def _delete_row(self, row_id):
        """
        Deletes a row from the managed table based on row_id.

        Parameters:
            row_id (str): The row_id to match for deleting rows.
        """
        conn = self._connect()
        cursor = conn.cursor()
        delete_sql = f"DELETE FROM {self.table_name} WHERE id = %s;"
        cursor.execute(delete_sql, (row_id))
        conn.commit()
        cursor.close()
        conn.close()

    def _delete_table(self):
        """
        Deletes the managed table from the database.
        """
        conn = self._connect()
        cursor = conn.cursor()
        drop_table_sql = f"DROP TABLE IF EXISTS {self.table_name};"
        cursor.execute(drop_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def _insert_row(self, columns, values):
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
        insert_sql = f"INSERT INTO {self.table_name} ({columns_str}) VALUES ({placeholders});"
        cursor.execute(insert_sql, values)
        conn.commit()
        cursor.close()
        conn.close()

    @abstractmethod
    def _update_row(self, dict_update, id_row):
        conn = self.__connect()
        cursor = conn.cursor()

        arguments = []
        for value, key in dict_update.items():
            arguments.append(f"{value} =  '{key}', ")
        arguments =  str(arguments[:-1])
        query = f"UPDATE {self.table_name} SET {dict_update.key} WHERE {self._table_name[:-1]}ID = {id_row};"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()        
      

    @abstractmethod
    def _get_by_id(self, record_id, id_column="id"):
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
        
        query = f"SELECT * FROM {self.table_name} WHERE {id_column} = %s"
        cursor.execute(query, (record_id))
        record = cursor.fetchone()
        cursor.close()
        conn.close()
    
        if record:
            return {f"{id_column}": record[0]}
        return None
    
    def get_record_api(self, record_id):
        """
        API endpoint to get record details by record_id.
        """
        record = self._get_by_id(record_id)
        
        if record:
            return jsonify(record), 200 
        else:
            return jsonify({"error": "Record not found"}), 404 
    
    def run(self):
        """
        Run the Flask app.
        """
        self.app.run(debug=True)