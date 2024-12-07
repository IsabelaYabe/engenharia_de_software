"""
    Preciso fazer testes, colocar logs

"""
from custom_logger import setup_logger
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from pub_strategy.pub_notify_strategy import PubNotifyStrategy, DefaultPubNotifyStrategy
from sub_strategy.sub_update_strategy import SubUpdateStrategy, DefaultSubUpdateStrategy, PurchaseProductSubUpdateStrategy

logger = setup_logger()

class EventManager():
    def __init__(self):
        self.__subscribers = {} # Key event, value list of subscribers
        self.__notify_strategies = {}  # Key: event_type, Value: NotifyStrategy
        self.__update_strategies = {}  # Key: event_type, Value: UpdateStrategy
    
    def subscribe(self, event_type, subscriber):
        if event_type not in self.__subscribers:
            self.__subscribers[event_type] = []
            logger.info(f"Created new subscriber list for event {event_type}")

        if subscriber not in self.__subscribers[event_type]:
            self.__subscribers[event_type].append(subscriber)
            logger.info(f"Subscriber added to event {event_type}")
        else:
            logger.info(f"Subscriber already subscribed to event {event_type}")

    def unsubscribe(self, event_type, subscriber):
        if event_type in self.__subscribers:
            try:
                self.__subscribers[event_type].remove(subscriber)
                logger.info(f"Subscriber removed from event {event_type}")
            except ValueError:
                logger.error(f"Subscriber not found for event {event_type}")
        else:
            logger.warning(f"Event type {event_type} has no subscribers.")
    
    def notify(self, event_type, data, *args, **kwargs):
        if not self.subscribers.get(event_type, []):
            logger.warning(f"No subscribers to notify for event {event_type}.")
            return
        
        strategy = self.notify_strategies.get(event_type, DefaultPubNotifyStrategy())
        try:
            strategy.notify(event_type, data, self.subscribers[event_type], *args, **kwargs)
            logger.info(f"Event {event_type} notified successfully")
        except Exception as e:
            logger.error(f"Failed to notify subscribers for event {event_type}: {e}")

    @property
    def subscribers(self):
        return self.__subscribers

    @property
    def notify_strategies(self):
        return self.__notify_strategies

    @property
    def update_strategies(self):
        return self.__update_strategies

    @notify_strategies.setter        
    def notify_strategies(self, event_type, strategy):
        """
        Sets a custom notification strategy for a specific event type.
        """
        if not isinstance(strategy, PubNotifyStrategy):
            logger.error(f"Invalid strategy provided for event {event_type}")
            return
        
        self.__notify_strategies[event_type] = strategy
        logger.info(f"Custom notification strategy set for event {event_type}")
    
    @update_strategies.setter        
    def update_strategies(self, event_type, strategy):
        if not isinstance(strategy, SubUpdateStrategy):
            logger.error(f"Invalid strategy provided for event {event_type}")
            return
        
        self.__update_strategies[event_type] = strategy
        logger.info(f"Custom updateing strategy set for event {event_type}")