from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger

logger = setup_logger()

class SubUpdateStrategy(ABC):
    @abstractmethod
    def update(self, data): ...

class DefaultSubUpdateStrategy(SubUpdateStrategy):
    def update(self, data):
        logger.info(f"Executing update strategy with data: {data}")

# Event: PurchaseProductEvent
class PurchaseProductSubUpdateStrategy(SubUpdateStrategy):
    def update(self, data):
        logger.info(f"Executing update strategy with data: {data}")
        name = data["name"]
        vending_machine_id = data["vending_machine_id"]
        quantity = data["quantity"]
        try:
            existing_records = self.search_record(name=name, vending_machine_id=vending_machine_id)
            
            if not existing_records:
                logger.warning(f"Product '{name}' not found in vending machine '{vending_machine_id}'. Purchase aborted.")
                return
            
            existing_product = existing_records[0]
            existing_id = existing_product[0]
            existing_quantity = existing_product[4]
            if quantity > existing_quantity:
                logger.warning(f"Insufficient stock for product '{name}' in vending machine '{vending_machine_id}'. Available: {existing_quantity}, Requested: {quantity}")
                return       

            new_quantity = existing_quantity - quantity
            self.update_row(existing_id, quantity=new_quantity)

            logger.info(f"Purchase successful. Updated product '{name}' in vending machine '{vending_machine_id}' to new quantity: {new_quantity}")
        
        except Exception as e:
            logger.error(f"Failed to update product '{name}' in vending machine '{vending_machine_id}': {e}")
            raise