import uuid
from database_manager import DatabaseManager

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators import immutable_fields

class FavoriteVM(DatabaseManager):

    def __init__(self, host, user, password, database):

        super().__init__(host, user, password, database, "favorite vending machine")
        self.columns = ["id", "user id", "vending machine id", "timestamp"]
        self.foreign_keys = ["users", "vending machines"]
    
    def get_column_id(self): 
        return "id"
    
    def _create_table(self):

        favorite_table_sql = """
        CREATE TABLE IF NOT EXISTS `favorite vending machine` (
            id VARCHAR(36) PRIMARY KEY,
            `user id` VARCHAR(36) UNIQUE NOT NULL,
            `vending machine id` VARCHAR(36) UNIQUE NOT NULL,
            FOREIGN KEY (`user id`) REFERENCES users(id),
            FOREIGN KEY (`vending machine id`) REFERENCES `vending machines`(id),
        );
        """
        self._create_table_(favorite_table_sql)

    def insert_row(self, user_id, vending_machine_id):
        transaction_id = str(uuid.uuid4())
        self._insert_row(
            id=transaction_id, user_id=user_id, vending_machine_id=vending_machine_id)
        return transaction_id
    
    @immutable_fields(['id'])
    def update_row(self, record_id, **kwargs):
        
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, record_id):
        
        record = self._get_by_id(record_id, "id")

        if record is None:
            return None
        
        row = {}
        count = 0
        for value in record:
            row[self.columns[count]] = value
            count+=1
        return row