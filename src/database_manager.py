"""
Module for DatabaseManager Class.

This module provides a `DatabaseManager` class for managing database tables, including functionality for table creation,
modification, row operations (insert, update, delete), and integration with an event-driven architecture via pub-sub mechanisms.

Author: Isabela Yabe
Last Modified: 05/12/2024
Status: Complete

Dependencies:
    - mysql.connector
    - custom_logger
    - decorators_method (immutable_fields)
    - event_manager (EventManager)
    - utils (tuple_rows_to_dict)

Classes:
    - Config: Configuration for database table management.
    - ConfigPub: Configuration for publishing events.
    - ConfigSub: Configuration for subscribing to events.
    - DatabaseManager: Main class for managing database tables, including pub-sub functionality.

"""

from dataclasses import dataclass, field
from custom_logger import setup_logger
import mysql.connector
import re
from copy import deepcopy

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators_method import immutable_fields
from event_manager.event_manager import EventManager
from sub_strategy.sub_update_strategy import DefaultSubUpdateStrategy
from utils.utils import tuple_rows_to_dict

logger = setup_logger()

@dataclass
class Config:
    """
    Configuration class for managing database table settings.

    Attributes:
        host (str): Database host.
        user (str): Database user.
        password (str): Database password.
        database (str): Database name.
        table_name (str): Table name to manage.
        columns (list[str]): List of table column names.
        column_id (str): Primary key column. Default is "id".
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
    ConfigPub class for event publishing.

    Attributes:
        event_manager (EventManager): Event manager instance.
        events_type_pub (list[str]): List of event types to publish.
    """
    event_manager: EventManager
    events_type_pub: list[str] = field(default_factory=list)

@dataclass
class ConfigSub:
    """
    ConfigSub class for event subscribing.

    Attributes:
        event_manager (EventManager): Event manager instance.
        events_type_sub (list[str]): List of event types to subscribe to.
    """
    event_manager: EventManager
    events_type_sub: list[str] = field(default_factory=list)

class DatabaseManager():
    """
    DatabaseManager class for table management and pub-sub integration.

    This class provides functionality for managing database tables, including table creation, modification,
    row insertion, updates, deletions, and searching. It integrates with an event-driven architecture
    via pub-sub mechanisms to publish and subscribe to events.

    Attributes:
        db_config (dict): Database connection configuration.
        table_name (str): Name of the database table.
        columns (list[str]): List of table columns.
        column_id (str): Primary key column.
        foreign_keys (dict): Dictionary of foreign keys and their references.
        foreign_keys_columns (list[str]): List of foreign key columns.
        event_manager_pub (EventManager): Event manager for publishing events.
        event_manager_sub (EventManager): Event manager for subscribing to events.
        events_type_pub (list[str]): List of event types to publish.
        events_type_sub (list[str]): List of event types to subscribe to.
        immutable_columns (list[str]): List of columns that cannot be updated.

    Methods:
        __connect: Establishes a database connection.
        modify_column: Renames a column in the table.
        add_column: Adds a new column to the table.
        delete_column: Deletes a column from the table.
        delete_rows: Deletes rows based on a column value.
        create_table: Creates a new table in the database.
        delete_table: Deletes the table.
        insert_row: Inserts a new row into the table.
        update_row: Updates specific columns in a row.
        get_by_id: Fetches a row by its primary key.
        search_record: Searches for rows matching specific criteria.
        execute_sql: Executes a raw SQL query.
    """

    def __init__(self, config, config_pub=None, config_sub=None, immutable_columns=None, foreign_keys=None):
        """
        Initializes the DatabaseManager.

        Args:
            config (Config): Configuration object for the database table.
            config_pub (ConfigPub, optional): Configuration for event publishing.
            config_sub (ConfigSub, optional): Configuration for event subscription.
            immutable_columns (list[str], optional): List of immutable columns.
            foreign_keys (dict, optional): Foreign key constraints for the table.
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
        self.__columns_parameters = []
        for column in self.__columns:
            if column != "id" or column != "timestamp":
                self.__columns_parameters.append(column)
                
        self.__column_id = config.column_id
        self.__foreign_keys = foreign_keys
        self.__foreign_keys_columns =  list(deepcopy(self.__foreign_keys).keys()) if self.__foreign_keys else None
        self.__event_manager_pub = config_pub.event_manager if config_pub else None
        self.__event_manager_sub = config_sub.event_manager if config_sub else None
        self.__events_type_pub = config_pub.events_type_pub if config_pub else None
        self.__events_type_sub = config_sub.events_type_sub if config_sub else None
        self.__immutable_columns = [self.__column_id, "timestamp"]
        if self.foreign_keys:  
            for foreign_key in list(self.__foreign_keys.values()):
                self.__immutable_columns.append(foreign_key)
        if immutable_columns:
            for col in immutable_columns:
                self.__immutable_columns.append(col)
        
        try:
            for event_type in self.events_type_sub:
                if event_type not in self.event_manager_sub.update_strategies.keys():
                    logger.warning(f"No update strategy registered for event '{event_type}'. Using default.")
                self.event_manager_sub.subscribe(event_type, self)
                logger.info(f"Subscribed to event {event_type}")
        except Exception as e:
             logger.error(f"Failed to subscribe to event: {e}")
        
    def __connect(self):
        """
        Establishes a connection to the MySQL database.

        Returns:
            mysql.connector.connection_cext.CMySQLConnection: The database connection.
        """
        try:
            conn = mysql.connector.connect(**self.__db_config)
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
            conn.commit()
        self.__columns.append(column_name) 
        logger.info(f"Column {column_name} was added to {self.__table_name} as {type} and not_null {not_null}")       

    def delete_column(self, column_name):
        """
        Deletes a column from the database table.

        Args:
            column_name (str): The name of the column to delete.
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
        tuple_rows_dict = tuple_rows_to_dict(list_tuples_row, self.columns)

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
        """
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
                logger.info(f"Table created {table_name}")
                raise ValueError("This table exist")
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
        """
        columns = []
        values = []
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
            conn.commit()
            id = cursor.lastrowid
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
            conn.commit()
            new_row = self.get_by_id(record_id)      
            logger.info(f"Row {record_id} id from table {self.table_name} updated columns: {columns} (from {old_row} (old row) to {new_row} (new row))")
      
    def get_by_id(self, record_id):
        """
        Fetches a row from the table by its primary key.

        Args:
            record_id (str): The ID of the row to fetch.

        Returns:
            tuple or None: The row data if found, or None if no matching row is found.
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
        
    def show_table(self):
        """
        Shows the table in the database.

        Returns:
            list[tuple]: A list of rows that match the search criteria.
        """
        head_query = f'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s;'
        query = f'SELECT * FROM `{self.__table_name}`;'
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(head_query, (self.__table_name,))
            head = [column[0] for column in cursor.fetchall()]
            cursor.execute(query)
            return_execute = cursor.fetchall()
            if not return_execute:
                logger.warning(f"No instance found in table: {self.__table_name}")
            else:
                logger.info(f"Got all instances in table: {self.__table_name}")
            return head, return_execute
        
    def execute_sql(self, query, params=None, fetch_one=False, fetch_all=False, error_message="", commit=False):
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
        """
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetch_all:
                return cursor.fetchall()
            elif fetch_one:
                return cursor.fetchone()
    
    def get_info(self):
        """
        Get information about the table.

        Returns:
            dict: Information about the table.
        """
        head, rows = self.show_table()

        return {
            "table_name": self.__table_name,
            "columns": self.__columns,
            "column_id": self.__column_id,
            "foreign_keys": self.__foreign_keys,
            "foreign_keys_columns": self.__foreign_keys_columns,
            "immutable_columns": self.__immutable_columns,
            "head": head,
            "rows": rows
        }
    
    def publish_event(self, event_type, **data):
        """
        Publishes an event to the event manager.

        Args:
            event_type (_type_): _description_
            **data: _description_
        """
        if self.event_manager_pub == None or self.events_type_pub == None:
            logger.error("Event manager or events type not set")
        if event_type in self.events_type_pub:
            try:
                self.event_manager_pub.notify(event_type, data)
                logger.info(f"Event published: {event_type} with data: {data}")
            except Exception as e:
                 logger.error(f"Failed to publish event {event_type}: {e}")
        else:
             logger.warning(f"Event {event_type} is not in the configured publish list: {self.evets_type_pub}")
            
    def update(self, event_type, **data):
        if self.event_manager_sub == None or self.events_type_sub == None:
            logger.error("Event manager or events type not set")
        strategies = self.event_manager_sub.update_strategies
        strategy = strategies.get(event_type, DefaultSubUpdateStrategy())
        if event_type in self.events_type_sub:
            try:
                logger.info(f"Received event {event_type} with data: {data}")
                strategy.update(data, self.table_name, self.search_record, self.update_row)
            except Exception as e:
                logger.error(f"Failed to handle event '{event_type}': {e}")
        else:
             logger.warning(f"Event {event_type} is not in the configured subscribe list: {self.events_type_sub}")

    def get_last_id(self):
        """
        Get the last inserted ID.

        Returns:
            int: The last inserted ID.
        """
        query = f"SELECT LAST_INSERT_ID();"
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]
    
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
    def foreign_keys_columns(self): 
        return self.__foreign_keys_columns

    @property
    def event_manager_pub(self):
        return self.__event_manager_pub

    @property
    def event_manager_sub(self):
        return self.__event_manager_sub

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
        logger.info(f"Database configuration updated: {new_config}")
        self.__db_config = new_config

    @table_name.setter
    def table_name(self, new_table_name):
        logger.info(f"Table name updated: {new_table_name}")
        self.__table_name = new_table_name

    @columns.setter
    def columns(self, new_columns):
        logger.info(f"Columns updated: {new_columns}")
        self.__columns = new_columns

    @column_id.setter
    def column_id(self, new_column_id):
        logger.info(f"Primary key column updated: {new_column_id}")
        self.__column_id = new_column_id
    
    @foreign_keys.setter
    def foreign_keys(self, new_foreign_keys): 
        logger.info(f"Foreign keys updated: {new_foreign_keys}")
        self.__foreign_keys = new_foreign_keys 

    @foreign_keys_columns.setter
    def foreign_keys_columns(self, new_foreign_keys_columns): 
        logger.info(f"Foreign keys columns updated: {new_foreign_keys_columns}")
        self.__foreign_keys_columns = new_foreign_keys_columns

    @event_manager_pub.setter
    def event_manager_pub(self, new_event_manager_pub):
        logger.info(f"Event manager updated: {new_event_manager_pub}")
        self.__event_manager_pub = new_event_manager_pub
    
    @event_manager_sub.setter
    def event_manager_sub(self, new_event_manager_sub):
        logger.info(f"Event manager updated: {new_event_manager_sub}")
        self.__event_manager_sub = new_event_manager_sub

    @events_type_pub.setter
    def events_type_pub(self, new_events_type_pub):
        logger.info(f"Events type published updated: {new_events_type_pub}")
        self.__events_type_pub = new_events_type_pub

    @events_type_sub.setter
    def events_type_sub(self, new_events_type_sub):
        logger.info(f"Events type subscribed updated: {new_events_type_sub}")
        self.__events_type_sub = new_events_type_sub

    @immutable_columns.setter
    def immutable_columns(self, new_immutable_columns):
        logger.info(f"Immutable columns updated: {new_immutable_columns}")
        self.__immutable_columns = new_immutable_columns 