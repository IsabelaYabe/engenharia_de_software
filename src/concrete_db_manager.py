import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager import DatabaseManager
from decorators import immutable_fields

class TestDatabaseManagerConcrete(DatabaseManager):
    def _create_table(self):
        pass
    
    def insert_row(self, *args):
        pass
    
    def update_row(self, record_id, **kwargs):
        pass

    def delete_row(self, record_id):
        pass

    def get_by_id(self, record_id):
        pass