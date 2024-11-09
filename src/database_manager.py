"""
    Module for DatabaseManager abstractmethod class.

    This module provides a class for managing a single MySQL table in a database.

    Author: Isabela Yabe
    Last Modified: 06/11/2024
    Status: Complete, put logs

    Dependencies:
        - setup_logger
        - ABC
        - abstractmethod
        - mysql.connector
"""
from custom_logger import setup_logger
from abc import ABC, abstractmethod
import mysql.connector

logger = setup_logger()

class DatabaseManager(ABC):
    """
        DatabaseManager class.

        This abstract class provides basic database operations and manages a single table in a MySQL database.

        Attributes:
        - db_config (dict): A dictionary containing the MySQL database configuration.
        - table_name (str): The name of the table managed by this instance.

        Methods:
        - __connect(): Establishes a connection to the MySQL database.
        - _create_table_(create_table_sql): Creates the managed table with the provided SQL statement.
        - _modify_column(old_column_name, new_column_name): Modifies a column name.
        - _delete_row(row_id, column_id): Deletes a row from the table based on a column condition.
        - _delete_table(): Deletes the entire table.
        - _insert_row(**kwargs): Inserts a new row into the table with specified column-value pairs.
        - _update_row(record_id, column_id, **kwargs): Updates specific columns based on a record condition.
        - _get_by_id(record_id, column_id="id"): Retrieves a record by its ID from the table.
        - _delete_column(column_name): Deletes a column from the table.
        - _add_column(column_name, type, not_null=True): Adds a new column to the table.
        - _rollback(conn): Roll back a uncommitted transaction on the corrent connection.
    """
    
    def __init__(self, host, user, password, database, table_name):
        """
        Constructor for the DatabaseManager class.
        
        Args:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user"s password.
            database (str): The name of the MySQL database.
            table_name (str): The name of the table to be managed by this instance.
        """
        logger.info("Initializing DatabaseManager for table: %s", table_name)
        self._db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self._table_name = table_name
        
    @abstractmethod
    def _create_table(self): ...
    
    @abstractmethod
    def insert_row(self, *args) -> int : ... 

    @abstractmethod
    def update_row(self, record_id, **kwargs): ...

    @abstractmethod
    def delete_row(self, record_id): ...

    @abstractmethod
    def get_by_id(self, record_id) -> dict : ...
    
    def __connect(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            conn: A MySQL database connection object.
        """
        logger.info("Connecting to the database")
        try:
            conn = mysql.connector.connect(**self._db_config)
            logger.debug("Successful connection")
        except mysql.connector.Error as e:
            logger.error("Unsuccessful connection: %s (errno=%d)", e.msg, e.errno)
            raise
        return conn 

    def _create_table_(self, create_table_sql): 
        """
        Creates the table in the MySQL database with the provided SQL statement.

        Args:
            create_table_sql (str): The SQL query to create the table.
        """
        logger.info("Creating table with SQL: %s", create_table_sql)
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        cursor.close()
        conn.close()
 
    def _modify_column(self, old_column_name, new_column_name):
        """
        Modifies a column name in the managed table.
        
        Args:
            old_column_name (str): The current name of the column.
            new_column_name (str): The new name of the column.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        alter_table_sql = f"ALTER TABLE `{self._table_name}` RENAME COLUMN `{old_column_name}` TO `{new_column_name}`;"

        try: 
            cursor.execute(alter_table_sql)
            conn.commit()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to modify column `{old_column_name}` to `{new_column_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1060:
                raise ValueError(f"Existing column name (`{new_column_name}`): {e.msg}")
            
            else:
                raise
        finally:
            cursor.close()
            conn.close()

    def _add_column(self, column_name, type, not_null=True):
        """
        Add a column in the managed table.

        Args:
            column_name (str): The name of the new column.
            type (str): The type of the new column.
        """
        if not_null:
            null = " NOT NULL"
        else:
            null = ""
        conn = self.__connect()
        cursor = conn.cursor()

        alter_table_sql = f"ALTER TABLE `{self._table_name}` ADD `{column_name}` {type.upper()}{null};"

        try: 
            cursor.execute(alter_table_sql)
            conn.commit()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to insert column into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1060:
                raise ValueError(f"Existing column name (`{column_name}`): {e.msg}")
            
            else:
                raise
        finally:
            cursor.close()
            conn.close()

    def _delete_column(self, column_name):
        """
        Delete a column in the managed table.

        Args:
            column_name (str): The name of the new column.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        alter_table_sql = f"ALTER TABLE `{self._table_name}` DROP COLUMN `{column_name}`;"
        try: 
            cursor.execute(alter_table_sql)
            conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to deleted column into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1054:
                raise ValueError(f"Column `{column_name}` not found: {e.msg}")
            else: 
                raise
        finally:
            cursor.close()
            conn.close()

    def _delete_row(self, record_id, column_id):
        """
        Deletes a row from the managed table based on record_id.
        This method delete all rows with the conditional `column_id = record_id`.

        Args:
            record_id (str): The record_id to match for deleting rows.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        delete_sql = f"DELETE FROM `{self._table_name}` WHERE `{column_id}` = %s;"

        try:
            cursor.execute(delete_sql, (record_id,))
            conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to delete row into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn) 
            if e.errno == 1054:
                raise ValueError(f"Column `{column_id}` not found: {e.msg}")
            else:
                raise
        finally:
            if cursor.rowcount == 0:
                print("No rows are deleted; the key was not found.")
            cursor.close()
            conn.close()

    def _delete_table(self):
        """
        Deletes the managed table from the database.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        drop_table_sql = f"DROP TABLE IF EXISTS `{self._table_name}`;"
        cursor.execute(drop_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def _insert_row(self, **kwargs):
        """
        Inserts a new row into the managed table.
        
        Args:
            **kwargs (dict): A dict of column names and values.
        """
        columns = []
        values = []
        placeholders = []
        for key, value in kwargs.items():
            columns.append(f"`{key}`")
            values.append(value)
            placeholders.append("%s")
        conn = self.__connect()
        cursor = conn.cursor()
        columns_str = ", ".join(columns)
        placeholders = ", ".join(placeholders)
        insert_sql = f"INSERT INTO `{self._table_name}` ({columns_str}) VALUES ({placeholders});"
        
        try:
            cursor.execute(insert_sql, tuple(values))
            conn.commit()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to insert row into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1366:
                raise ValueError(f"Incorrect value type for column: {e.msg}")    
            elif e.errno == 1048:
                raise ValueError(f"Missing required value for column: {e.msg}")
            else:
                raise
        finally:
            cursor.close()
            conn.close()

    def _update_row(self, record_id, column_id, **kwargs):
        """
        Update row by its id.

        Args:
            record_id (str): The record_id to match for update.
            column_id (str): The name of id`s column.
            kwargs (dict): Column-value pairs to update.  
        """
        conn = self.__connect()
        cursor = conn.cursor()

        arguments = []
        values = []
        for key, value in kwargs.items():
            arguments.append(f"`{key}` = %s")
            values.append(value)
        arguments =  ", ".join(arguments)
        values.append(record_id)
        query = f"UPDATE `{self._table_name}` SET {arguments} WHERE `{column_id}` = %s;"
        try:
            cursor.execute(query, tuple(values))
            conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to update row to `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1054:
                raise ValueError(f"Column `{column_id}` not found: {e.msg}")
            elif e.errno == 1048:
                raise ValueError(f"Missing required value for column: {e.msg}")
            elif e.errno == 1366:
                raise ValueError(f"Incorrect value type for column: {e.msg}")
            else:
                raise
        finally:
            cursor.close()
            conn.close()        
      
    def _get_by_id(self, record_id, column_id ="id"):
        """
        Retrieves a record by its ID from the database.
    
        Args:
            record_id (str): The ID of the record to be fetched.
            id_column (str): The name of the ID column in the table (default is "id").
    
        Returns:
            dict: A dictionary with the record details, or None if not found.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM `{self._table_name}` WHERE `{column_id}` = %s;"

        try: 
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to get instance by id into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1054: 
                raise ValueError(f"Column `{column_id}` not found: {e.msg}")
            else: 
                raise
        finally:     
            cursor.close()
            conn.close()
    
        if record:
            return record
        return None
    
    def _rollback(self, conn):
        """
        This method roll back an uncommitted transaction on the corrent connection.
        """
        try:
            conn.rollback()
            print("Transaction rolled back.")
        except mysql.connector.Error as e: 
            logger.error(f"Failed to rollback into `{self._table_name}`: {e.msg} (errno={e.errno})")
            print(f"Error rolling back transaction: {e}")

    def _execute_sql(self, query, params=None, fetch_one=False, error_message=""):
        """
        Executes a SQL command and handles exceptions.

        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters for the SQL query (default is None).
            fetch_one (bool): Whether to fetch a single result (default is False).
            error_message (str): Custom error message for logging (default is "").

        Returns:
            The result of the query if fetch_one is True, or None otherwise.
        """

        conn = self.__connect()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)
            conn.commit()
            if fetch_one:
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                return result
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            logger.error(f"{error_message}: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            cursor.close()
            conn.close()
            raise ValueError(f"{error_message}: {e.msg} (errno={e.errno})")