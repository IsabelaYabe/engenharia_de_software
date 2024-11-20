from transaction_validation_strategy.transaction_validation_strategy_interface import TransactionValidationStrategy
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_file import relationship_manager_central

class ForeignKeyExistsStrategy(TransactionValidationStrategy):
    def transaction_validation(self, transaction_instance, *args, **kwargs):
        for table_name, record_id in transaction_instance.foreing_keys.items():
            table = relationship_manager_central.dict_relationships[table_name]
            if record_id and not table.get_by_id(record_id):
                return f"{table.get_column_id()} `{record_id}` does not exist."
        return None