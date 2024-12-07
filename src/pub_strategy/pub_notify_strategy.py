from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger

logger = setup_logger()

class PubNotifyStrategy(ABC):
    @abstractmethod
    def notify(self, event_type, data, subscribers, *args, **kwargs): ...

class DefaultPubNotifyStrategy(PubNotifyStrategy):
    def notify(self, event_type, data, subscribers, *args, **kwargs):
        logger.info(f"Notifying subscribers for event {event_type} with data: {data}")
        for subscriber in subscribers:
            try:
                subscriber.update(event_type, **data)
                logger.info(f"Subscriber {subscriber.table_name} updated for event {event_type}")
            except Exception as e:
                logger.error(f"Failed to notify subscriber {subscriber} for event {event_type}: {e}")