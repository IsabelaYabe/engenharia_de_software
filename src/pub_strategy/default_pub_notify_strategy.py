import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from pub_strategy.pub_notify_strategy_interface import PubNotifyStrategy
from custom_logger import setup_logger

logger = setup_logger()

class DefaultPubNotifyStrategy(PubNotifyStrategy):
    def notify(self, event_type, data, subscribers, *args, **kwargs):
        logger.info(f"Notifying subscribers for event {event_type} with data: {data}")
        for subscriber in subscribers:
            subscriber.update(event_type, data)