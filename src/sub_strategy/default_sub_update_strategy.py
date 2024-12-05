import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from sub_strategy.sub_update_strategy_interface import SubUpdateStrategy
from custom_logger import setup_logger

logger = setup_logger()

class DefaultSubUpdateStrategy(SubUpdateStrategy):
    def update(self, data):
        logger.info(f"Executing update strategy with data: {data}")
        