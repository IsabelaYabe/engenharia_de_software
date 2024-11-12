
import uuid
from database_manager import DatabaseManager

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators import immutable_fields

class AddProduct(DatabaseManager):

    def __init__(self, host, user, password, database):

        super().__init__(host, user, password, database, "add product")
        self.columns = ["id", "owner id", "product id", "vending machine id", "timestamp", "quantity", "price"]
        self.foreign_keys = ["vending machines", "products", "owners"]

    def get_column_id(self): 
        return "id"
    
    def _create_table(self):

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS `add product` (
            id VARCHAR(36) PRIMARY KEY,
            `owner id` VARCHAR(36) UNIQUE NOT NULL,
            `product id` VARCHAR(36) UNIQUE NOT NULL,
            `vending machine id` VARCHAR(36) UNIQUE NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            quantity INT NOT NULL,
            FOREIGN KEY (`vending machine id`) REFERENCES `vending machines`(id), 
            FOREIGN KEY (`product id`) REFENCES products(id)
            FOREIGN KEY (`owner id`) REFENCES owners(id)
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, owner_id, product_id, vending_machine_id, quantity):
        transaction_id = str(uuid.uuid4())
        self._insert_row(
            id=transaction_id, owner_id=owner_id, product_id=product_id, vending_machine_id=vending_machine_id, quantity=quantity)
        return transaction_id
    
    @immutable_fields(['id', 'timestamp'])
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