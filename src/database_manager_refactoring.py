from dataclasses import dataclass, field
from custom_logger import setup_logger
import mysql.connector
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators import immutable_fields

logger = setup_logger()
@dataclass
class ConfigClass:
    host: str
    user: str
    password: str 
    database: str
    table_name: str
    columns: list[str] = field(default_factory=list)
    column_id: str="id"

class DatabaseManager():
    
    def __init__(self, config, columns_foreign_keys_table=None, immutable_columns=None):

        logger.info("Initializing DatabaseManager for table: %s", config.table_name)
        self._db_config = {
            "host": config.host,
            "user": config.user,
            "password": config.password,
            "database": config.database
        }
        self.table_name = config.table_name
        self.columns = config.columns
        self.column_id = config.column_id
        self.columns_foreing_keys_table = columns_foreign_keys_table
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
        conn = self.__connect()
        cursor = conn.cursor()
        alter_table_sql = f"ALTER TABLE `{self._table_name}` RENAME COLUMN `{old_column_name}` TO `{new_column_name}`;"

        try: 
            cursor.execute(alter_table_sql)
            conn.commit()
            indice = self.columns.index(old_column_name)
            self.columns[indice] = "new_column_name"
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

    def _delete_row(self, record_id):
        conn = self.__connect()
        cursor = conn.cursor()
        delete_sql = f"DELETE FROM `{self._table_name}` WHERE `{self.column_id}` = %s;"

        try:
            cursor.execute(delete_sql, (record_id,))
            conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to delete row into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn) 
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
        conn = self.__connect()
        cursor = conn.cursor()
        drop_table_sql = f"DROP TABLE IF EXISTS `{self._table_name}`;"
        cursor.execute(drop_table_sql)
        conn.commit()
        cursor.close()
        conn.close()

    def _insert_row(self, **kwargs):
        id = str(uuid.uuid4())
        column_id = f"`{self.column_id}`"
        columns = [column_id]
        values = [id]
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

    @immutable_fields("immutable_columns")
    def _update_row(self, record_id, **kwargs):
        conn = self.__connect()
        cursor = conn.cursor()

        arguments = []
        values = []
        for key, value in kwargs.items():
            arguments.append(f"`{key}` = %s")
            values.append(value)
        arguments =  ", ".join(arguments)
        values.append(record_id)
        query = f"UPDATE `{self._table_name}` SET {arguments} WHERE `{self.column_id}` = %s;"
        try:
            cursor.execute(query, tuple(values))
            conn.commit()
        except mysql.connector.Error as e:
            logger.error(f"Failed to update row to `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1054:
                raise ValueError(f"Column `{self.column_id}` not found: {e.msg}")
            elif e.errno == 1048:
                raise ValueError(f"Missing required value for column: {e.msg}")
            elif e.errno == 1366:
                raise ValueError(f"Incorrect value type for column: {e.msg}")
            else:
                raise
        finally:
            cursor.close()
            conn.close()        
      
    def _get_by_id(self, record_id):
        conn = self.__connect()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM `{self._table_name}` WHERE `{self.column_id}` = %s;"

        try: 
            cursor.execute(query, (record_id,))
            record = cursor.fetchone()
        except mysql.connector.Error as e: 
            logger.error(f"Failed to get instance by id into `{self._table_name}`: {e.msg} (errno={e.errno})")
            self._rollback(conn)
            if e.errno == 1054: 
                raise ValueError(f"Column `{self.column_id}` not found: {e.msg}")
            else: 
                raise
        finally:     
            cursor.close()
            conn.close()
    
        if record:
            return record
        return None
    
    def _rollback(self, conn):
        try:
            conn.rollback()
            print("Transaction rolled back.")
        except mysql.connector.Error as e: 
            logger.error(f"Failed to rollback into `{self._table_name}`: {e.msg} (errno={e.errno})")
            print(f"Error rolling back transaction: {e}")

    def _execute_sql(self, query, params=None, fetch_one=False, error_message=""):
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