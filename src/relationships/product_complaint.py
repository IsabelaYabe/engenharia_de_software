
import uuid

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from database_manager import DatabaseManager
from decorators import immutable_fields

class ProductComplaint(DatabaseManager):

    def __init__(self, host, user, password, database):

        super().__init__(host, user, password, database, "product complaints")
        self.columns = ["id", "complaint id", "product id", "user id", "timestamp"]
        self._create_table()

    def _create_table(self):

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS ´product complaints´ (
            id VARCHAR(36) PRIMARY KEY,
            FOREIGN KEY (´complaint id´) VARCHAR(36) UNIQUE NOT NULL,
            FOREIGN KEY (´product id´) VARCHAR(36) UNIQUE NOT NULL,
            FOREIGN KEY (´user id´) VARCHAR(36) UNIQUE NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, complaint_id, product_id, user_id):
        transaction_id = str(uuid.uuid4())
        self._insert_row(
            id=transaction_id, complaint_id=complaint_id, product_id=product_id, user_id=user_id)
        return transaction_id
    
    @immutable_fields(['id'])
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