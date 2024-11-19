"""
Module: DatabaseManager

This module provides a `DatabaseManager` class for managing MySQL database tables with support for CRUD operations,
table creation, column modification, and event-driven communication using publish-subscribe mechanisms.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Complete, maybe adjust the logs

Dependencies:
    - mysql.connector
    - uuid
    - re
    - decorators_method
    - decorators_class
    - event_manager.event_manager
    - custom_logger.setup_logger
"""

from dataclasses import dataclass, field
from custom_logger import setup_logger
import mysql.connector
import uuid
import re

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators_method import immutable_fields
from decorators_class import pubsub
from event_manager.event_manager import EventManager
from utils.utils import tuple_rows_to_dict

logger = setup_logger()
@dataclass
class Config:
    """
    Configuration class for database connection and table setup.

    Attributes:
        host (str): The database server hostname.
        user (str): The username for the database.
        password (str): The password for the database.
        database (str): The name of the database.
        table_name (str): The name of the table.
        columns (list[str]): A list of column names in the table.
        column_id (str): The primary key column name. Default is "id".
    """
    host: str
    user: str
    password: str 
    database: str
    table_name: str
    columns: list[str] = field(default_factory=list)
    column_id: str="id"

@dataclass
class ConfigPub:
    """
    Configuration class for publishing events.

    Attributes:
        event_manager (EventManager): The event manager instance for handling events.
        event_type (list[str]): A list of type of event to publish.
    """
    event_manager: EventManager
    events_type_pub: list[str] = field(default_factory=list)

@dataclass
class ConfigSub:
    """
    Configuration class for subscribing to events.

    Attributes:
        event_type (list[str]): A list of event types to subscribe to.
    """
    events_type_sub: list[str] = field(default_factory=list)

@pubsub
class DatabaseManager():
    """
    A class for managing MySQL database tables with CRUD operations, column management, and event-driven features.

    This class allows operations such as adding, deleting, or modifying rows and columns, as well as creating
    or dropping tables. It also supports event-driven interactions using publish-subscribe mechanisms.

    Attributes:
        config (Config): The database configuration.
        config_pub (ConfigPub): The publish configuration.
        config_sub (ConfigSub): The subscribe configuration.
        immutable_columns (list[str]): A list of columns that cannot be modified.
        foreign_keys (list[str]): A list of foreign key's columns.
    """
    def __init__(self, config, config_pub=None, config_sub=None, immutable_columns=None, foreign_keys=None):
        """
        Initializes the DatabaseManager instance.

        Args:
            config (Config): The database configuration.
            config_pub (ConfigPub, optional): The publish configuration. Default is None.
            config_sub (ConfigSub, optional): The subscribe configuration. Default is None.
            immutable_columns (list[str], optional): A list of immutable columns. Default is None.
            foreign_keys (list[str], optional): A list of foreign_keys columns. Default is None.
        """
        logger.info("Initializing DatabaseManager for table: %s", config.table_name)
        self.__db_config = {
            "host": config.host,
            "user": config.user,
            "password": config.password,
            "database": config.database
        }
        self.__table_name = config.table_name
        self.__columns = config.columns
        self.__column_id = config.column_id
        self.__foreign_keys = foreign_keys
        self.__event_manager = config_pub.event_manager if config_pub else None
        self.__events_type_pub = config_pub.events_type_pub if config_pub else None
        self.__events_type_sub = config_sub.events_type_sub if config_sub else None
        self.__immutable_columns = [self.__column_id, "timestamp"]  + (self.__foreign_keys or []) + (immutable_columns or [])
        
    def __connect(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection: The database connection.

        Raises:
            mysql.connector.Error: If the connection fails.
        """
        try:
            conn = mysql.connector.connect(**self.__db_config)
            logger.debug("Successful connection")
        except mysql.connector.Error as e:
            logger.error("Unsuccessful connection: %s (errno=%d)", e.msg, e.errno)
            raise
        logger.info("Connected into database")
        return conn 

    def modify_column(self, old_column_name, new_column_name):
        """
        Renames a column in the database table.

        Args:
            old_column_name (str): The current name of the column.
            new_column_name (str): The new name for the column.

        Raises:
            ValueError: If attempting to rename the primary key column.
        """
        if old_column_name == self.__column_id:
            logger.error("An attempt was made to change the name of the id column")
            raise ValueError("You can't modify an id column!")
        
        alter_table_sql = f"ALTER TABLE `{self.__table_name}` RENAME COLUMN `{old_column_name}` TO `{new_column_name}`;"

        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(alter_table_sql)
        indice = self.__columns.index(old_column_name)
        self.__columns[indice] = new_column_name
        logger.info(f"Column {old_column_name} from {self.__table_name} was changed to {new_column_name}")

    def add_column(self, column_name, type, not_null=True):
        """
        Adds a new column to the database table.

        Args:
            column_name (str): The name of the column to add.
            type (str): The data type of the column.
            not_null (bool): Whether the column should be NOT NULL. Default is True.
        """
        if not_null:
            null = " NOT NULL"
        else:
            null = ""

        alter_table_sql = f"ALTER TABLE `{self.__table_name}` ADD `{column_name}` {type.upper()}{null};"
     
        with self.__connect() as conn, conn.cursor() as cursor:    
            cursor.execute(alter_table_sql)
        self.__columns.append(column_name) 
        logger.info(f"Column {column_name} was added to {self.__table_name} as {type} and not_null {not_null}")       

    def delete_column(self, column_name):
        """
        Deletes a column from the database table.

        Args:
            column_name (str): The name of the column to delete.

        Raises:
            ValueError: If the column to delete does not exist in the table.
        """
        alter_table_sql = f"ALTER TABLE `{self.__table_name}` DROP COLUMN `{column_name}`;"
        
        with self.__connect() as conn, conn.cursor() as cursor: 
            cursor.execute(alter_table_sql)
        self.__columns.remove(column_name)
        logger.info(f"Column {column_name} was deleted from {self.__table_name}")

    def delete_rows(self, record, column):
        """
        Deletes rows from the database table based on a column value.

        Args:
            record (any): The value to match for deletion.
            column (str): The column to match against.
        """
        delete_sql = f"DELETE FROM `{self.__table_name}` WHERE `{column}` = %s;"
        list_tuples_row = self.search_record(column=record)
        logger.debug(f"{list_tuples_row}")
        tuple_rows_dict = tuple_rows_to_dict(list_tuples_row, self.columns)   
        logger.debug(f"{tuple_rows_dict}") 
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(delete_sql, (record,))
            if cursor.rowcount == 0:
                logger.info(f"No rows are deleted; the value {record} in {column} was not found")

        logger.info(f"All rows with value {record} in {column} was delete from {self.__table_name}: {tuple_rows_dict}")        

    def create_table(self, sql_batabase):
        """
        Creates a new table in the database.

        Args:
            sql_statement (str): The SQL CREATE TABLE statement.

        Raises:
            ValueError: If the table already exists.
        """
        logger.debug("Create table teste")
        regex = r"CREATE TABLE\s`?+([a-zA-Z0-9_]+)`?\s*\("
        match = re.search(regex, sql_batabase, re.IGNORECASE)
        table_name = match.group(1)

        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME =  %s;
                    """,
                    ("test_db","test_table"))
            if cursor.fetchone()[0] == 1:
                raise ValueError("This table exist")
                logger.info(f"Table created {table_name}")
            else:
                cursor.execute(sql_batabase)

    def delete_table(self):
        """
        Deletes the table managed by this class from the database.

        If the table does not exist, this method will safely exit without throwing an error.
        """
        drop_table_sql = f"DROP TABLE IF EXISTS `{self.__table_name}`;"
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(drop_table_sql)
            logger.info(f"Table {self.__table_name} deleted")

    def insert_row(self, **kwargs):
        """
        Inserts a new row into the database table.

        Args:
            **kwargs: Column names and values as key-value pairs for the new row.

        Returns:
            str: The ID of the newly inserted row.

        Raises:
            ValueError: If insertion fails due to invalid data or constraints.
        """
        id = str(uuid.uuid4())
        column_id = self.__column_id
        columns = [column_id]
        values = [id]
        placeholders = []
        for key, value in kwargs.items():
            columns.append(f"`{key}`")
            values.append(value)
            placeholders.append("%s")
        columns_str = ", ".join(columns)
        placeholders = ", ".join(placeholders)
        insert_sql = f"INSERT INTO `{self.__table_name}` ({columns_str}) VALUES ({placeholders});"
        
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(insert_sql, tuple(values))
            logger.info(f"Row ({kwargs}) inserted in table {self.__table_name} with id {id}")
        return id

    @immutable_fields("immutable_columns")
    def update_row(self, record_id, **kwargs):
        """
        Updates specified fields in a row identified by its primary key in the database table.

        This method updates columns in a table while respecting immutability constraints enforced
        by the `immutable_fields` decorator. Only mutable fields can be updated, and attempts to 
        modify immutable fields will raise a `ValueError`.

        Args:
            record_id (str): The primary key of the row to update.
            **kwargs: Key-value pairs representing the columns to update and their new values.

        Raises:
            ValueError: If there is an attempt to update immutable fields.
            mysql.connector.Error: If the query execution fails.

        Notes:
            - The `immutable_fields` decorator ensures that certain fields cannot be updated.
        """
        old_row = self.get_by_id(record_id)
        columns = []
        arguments = []
        values = []
        for key, value in kwargs.items():
            columns.append(key)
            arguments.append(f"`{key}` = %s")
            values.append(value)
        columns = ", ".join(columns)
        arguments =  ", ".join(arguments)
        values.append(record_id)

        query = f"UPDATE `{self.__table_name}` SET {arguments} WHERE `{self.__column_id}` = %s;"

        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(query, tuple(values))
            new_row = self.get_by_id(record_id)      
            logger.info(f"Row {record_id} id from table {self.table_name} updated columns: {columns} (from {old_row} (old row) to {new_row} (new row))")
      
    def get_by_id(self, record_id):
        """
        Fetches a row from the table by its primary key.

        Args:
            record_id (str): The ID of the row to fetch.

        Returns:
            tuple or None: The row data if found, or None if no matching row is found.

        Raises:
            Exception: If the query fails for any reason.
        """
        query = f"SELECT * FROM `{self.__table_name}` WHERE `{self.__column_id}` = %s;"
        
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(query, (record_id,))
            return_execute = cursor.fetchall() 
            if return_execute == []:
                logger.warning(f"No instance found with id: {record_id}")
            else:
                logger.info(f"Got instance with id: {record_id}")
                return return_execute[0]
        
    def search_record(self, **kwargs):
        """
        Searches for rows in the table that match the given column-value pairs.

        Args:
            **kwargs: Column names and values as key-value pairs to filter the search.

        Returns:
            list[tuple]: A list of rows that match the search criteria.

        Raises:
            Exception: If the search query fails for any reason.
        """
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(f"`{key}` = %s")
            values.append(value)
        columns_query = " AND ".join(columns)
        query = f"SELECT * FROM `{self.__table_name}` WHERE {columns_query};"
         
        with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                return_ = cursor.fetchall()
                logger.info(f"Records founds: {return_}")
                return return_
        
    def execute_sql(self, query, params=None, fetch_one=False, fetch_all=False, error_message=""):
        """
        Executes a raw SQL query on the database.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to substitute into the query. Default is None.
            fetch_one (bool, optional): Whether to fetch a single row from the result. Default is False.
            fetch_all (bool, optional): Whether to fetch all rows from the result. Default is False.
            error_message (str, optional): A custom error message to log if the query fails.

        Returns:
            tuple or list[tuple] or None: The fetched row(s) if applicable, otherwise None.

        Raises:
            ValueError: If the query execution fails.
        """
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_all:
                return cursor.fetchall()
            elif fetch_one:
                return cursor.fetchone()
    
    @property
    def db_config(self):
        return self.__db_config

    @property
    def table_name(self):
        return self.__table_name

    @property
    def columns(self):
        return self.__columns

    @property
    def column_id(self):
        return self.__column_id
    
    @property
    def foreign_keys(self): 
        return self.__foreign_keys 

    @property
    def event_manager(self):
        return self.__event_manager

    @property
    def events_type_pub(self):
        return self.__events_type_pub

    @property
    def events_type_sub(self):
        return self.__events_type_sub

    @property
    def immutable_columns(self):
        return self.__immutable_columns

    @db_config.setter
    def db_config(self, new_config):
        self.__db_config = new_config

    @table_name.setter
    def table_name(self, new_table_name):
        self.__table_name = new_table_name

    @columns.setter
    def columns(self, new_columns):
        self.__columns = new_columns

    @column_id.setter
    def column_id(self, new_column_id):
        self.__column_id = new_column_id
    
    @foreign_keys.setter
    def foreign_keys(self, new_foreign_keys): 
        self.__foreign_keys = new_foreign_keys 

    @event_manager.setter
    def event_manager(self, new_event_manager):
        self.__event_manager = new_event_manager

    @events_type_pub.setter
    def events_type_pub(self, new_events_type_pub):
        self.__events_type_pub = new_events_type_pub

    @events_type_sub.setter
    def events_type_sub(self, new_events_type_sub):
        self.__events_type_sub = new_events_type_sub

    @immutable_columns.setter
    def immutable_columns(self, new_immutable_columns):
        self.__immutable_columns = new_immutable_columns