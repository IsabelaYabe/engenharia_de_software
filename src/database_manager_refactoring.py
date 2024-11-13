from dataclasses import dataclass, field
from custom_logger import setup_logger
import mysql.connector
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators_method import immutable_fields
from decorators_class import pubsub
from event_manager.event_manager import EventManager

logger = setup_logger()
@dataclass
class Config:
    host: str
    user: str
    password: str 
    database: str
    table_name: str
    columns: list[str] = field(default_factory=list)
    column_id: str="id"

@dataclass
class ConfigPub:
    event_manager: EventManager
    event_type: str

@dataclass
class ConfigSub:
    event_type: str

@pubsub
class DatabaseManager():
    def __init__(self, config, config_pub=None, config_sub=None, immutable_columns=None):

        logger.info("Initializing DatabaseManager for table: %s", config.table_name)
        self._db_config = {
            "host": config.host,
            "user": config.user,
            "password": config.password,
            "database": config.database
        }
        self._table_name = config.table_name
        self.columns = config.columns
        self.column_id = config.column_id
        self.event_manager = config_pub.event_manager if config_pub else None
        self.event_type_pub = config_pub.event_type if config_pub else None
        self.event_type_sub = config_sub.event_type if config_sub else None
        self.immutable_columns = [self.column_id, "timestamp"] + (immutable_columns or [])
        
    def __connect(self):
        logger.info("Connecting to the database")
        try:
            conn = mysql.connector.connect(**self._db_config)
            logger.debug("Successful connection")
        except mysql.connector.Error as e:
            logger.error("Unsuccessful connection: %s (errno=%d)", e.msg, e.errno)
            raise
        return conn 
 
    def _modify_column(self, old_column_name, new_column_name):
        if old_column_name == self.column_id:
            raise ValueError(f"You can't modify an id column!")
        alter_table_sql = f"ALTER TABLE `{self._table_name}` RENAME COLUMN `{old_column_name}` TO `{new_column_name}`;"
        try:
            with self.__connect() as conn, conn.cursor() as cursor: 
                cursor.execute(alter_table_sql)
                conn.commit()
            indice = self.columns.index(old_column_name)
            self.columns[indice] = new_column_name
        except mysql.connector.Error as e: 
            logger.error(f"Failed to modify column `{old_column_name}` to `{new_column_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1060:
                raise ValueError(f"Existing column name (`{new_column_name}`): {e.msg}")
            else:
                raise

    def _add_column(self, column_name, type, not_null=True):
        if not_null:
            null = " NOT NULL"
        else:
            null = ""

        alter_table_sql = f"ALTER TABLE `{self._table_name}` ADD `{column_name}` {type.upper()}{null};"
        try: 
            with self.__connect() as conn, conn.cursor() as cursor:    
                cursor.execute(alter_table_sql)
                conn.commit()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to insert column into `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1060:
                raise ValueError(f"Existing column name (`{column_name}`): {e.msg}")
            
            else:
                raise

    def _delete_column(self, column_name):
        alter_table_sql = f"ALTER TABLE `{self._table_name}` DROP COLUMN `{column_name}`;"
        try:
            with self.__connect() as conn, conn.cursor() as cursor: 
                cursor.execute(alter_table_sql)
                conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to deleted column into `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1054:
                raise ValueError(f"Column `{column_name}` not found: {e.msg}")
            else: 
                raise

    def _delete_row(self, record_id):
        delete_sql = f"DELETE FROM `{self._table_name}` WHERE `{self.column_id}` = %s;"
        try:
            with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(delete_sql, (record_id,))
                conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to delete row into `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1054:
                raise ValueError(f"Column `{self.column_id}` not found: {e.msg}")
            else:
                raise
        finally:
            if cursor.rowcount == 0:
                print("No rows are deleted; the key was not found.")
            cursor.close()
            conn.close()

    def _delete_table(self):
        drop_table_sql = f"DROP TABLE IF EXISTS `{self._table_name}`;"
        with self.__connect() as conn, conn.cursor() as cursor:
            cursor.execute(drop_table_sql)
            conn.commit()

    def _insert_row(self, **kwargs):
        id = str(uuid.uuid4())
        column_id = self.column_id
        columns = [column_id]
        values = [id]
        placeholders = []
        for key, value in kwargs.items():
            columns.append(f"`{key}`")
            values.append(value)
            placeholders.append("%s")
        columns_str = ", ".join(columns)
        placeholders = ", ".join(placeholders)
        insert_sql = f"INSERT INTO `{self._table_name}` ({columns_str}) VALUES ({placeholders});"
        try:
            with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(insert_sql, tuple(values))
                conn.commit()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to insert row into `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1366:
                raise ValueError(f"Incorrect value type for column: {e.msg}")    
            elif e.errno == 1048:
                raise ValueError(f"Missing required value for column: {e.msg}")
            else:
                raise

    @immutable_fields("immutable_columns")
    def _update_row(self, record_id, **kwargs):
        arguments = []
        values = []
        for key, value in kwargs.items():
            arguments.append(f"`{key}` = %s")
            values.append(value)
        arguments =  ", ".join(arguments)
        values.append(record_id)
        query = f"UPDATE `{self._table_name}` SET {arguments} WHERE `{self.column_id}` = %s;"
        try:
            with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to update row to `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1054:
                raise ValueError(f"Column `{self.column_id}` not found: {e.msg}")
            elif e.errno == 1048:
                raise ValueError(f"Missing required value for column: {e.msg}")
            elif e.errno == 1366:
                raise ValueError(f"Incorrect value type for column: {e.msg}")
            else:
                raise       
      
    def _get_by_id(self, record_id):
        query = f"SELECT * FROM `{self._table_name}` WHERE `{self.column_id}` = %s;"
        try: 
            with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(query, (record_id,))
                return cursor.fetchone()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to get instance by id into `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1054: 
                raise ValueError(f"Column `{self.column_id}` not found: {e.msg}")
            else: 
                raise
    
    def _search_record(self, **kwargs):
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(f"`{key}` = %s")
            values.append(value)
        columns_query = " AND ".join(columns)
        query = f"SELECT * FROM `{self._table_name}` WHERE {columns_query};"
        try: 
            with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(query, tuple(values))
                return cursor.fetchall()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to search records in `{self._table_name}`: {e.msg} (errno={e.errno})")
            if e.errno == 1054: 
                raise ValueError(f"Column not found: {e.msg}")
            else: 
                raise

    def _execute_sql(self, query, params=None, fetch_one=False, error_message=""):
        try:
            with self.__connect() as conn, conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
            if fetch_one:
                return cursor.fetchone()
            else:
                return cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"{error_message}: {e.msg} (errno={e.errno})")
            raise ValueError(f"{error_message}: {e.msg} (errno={e.errno})")