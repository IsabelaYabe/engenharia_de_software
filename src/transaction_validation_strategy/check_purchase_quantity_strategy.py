"""
Rever isso
"""

from transaction_validation_strategy.transaction_validation_strategy_interface import TransactionValidationStrategy

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main_file import database_manager_central
 
class CheckPurchaseQuantityStrategy(TransactionValidationStrategy):
    def transaction_validation(self, transaction_instance, *args, **kwargs):
        product_id = args[1]
        required_quantity = args[3]
        product = database_manager_central.get_table("products").get_by_id(product_id)
        quantity = product["quantity"]

        if required_quantity > quantity:
            return "Insufficient quantity available."
        
        return None