
import uuid
from database_manager import DatabaseManager

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators import immutable_fields

class CreateVM(DatabaseManager):

    def __init__(self, host, user, password, database):

        super().__init__(host, user, password, database, "create vending machine")
        self.columns = ["id", "owner id", "vending machine id", "timestamp"]
        self._create_table()

    def _create_table(self):

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS ´create vending machine´ (
            id VARCHAR(36) PRIMARY KEY,
            FOREIGN KEY (´owner id´) VARCHAR(36) UNIQUE NOT NULL,
            FOREIGN KEY (´vending machine id´) VARCHAR(36) UNIQUE NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, owner_id, vending_machine_id):
        transaction_id = str(uuid.uuid4())
        self._insert_row(
            id=transaction_id, owner_id=owner_id, vending_machine_id=vending_machine_id)
        return transaction_id
    
    @immutable_fields(['id', 'timestamp'])
    def update_row(self, record_id, **kwargs):
        
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, id):
        
        record = self._get_by_id(id, "id")

        if record is None:
            return None
        
        row = {}
        count = 0
        for value in record:
            row[self.columns[count]] = value
            count+=1
        return row