"""
Module for managing event subscriptions, notifications, and strategies.

This module provides the `EventManager` class, which facilitates the subscription 
and notification of events, as well as handling custom strategies for publishing 
and updating subscribers.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - custom_logger.setup_logger
    - pub_strategy.PubNotifyStrategy, DefaultPubNotifyStrategy
    - sub_strategy.SubUpdateStrategy, DefaultSubUpdateStrategy, PurchaseProductSubUpdateStrategy
"""

from custom_logger import setup_logger
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from pub_strategy.pub_notify_strategy import PubNotifyStrategy, DefaultPubNotifyStrategy
from sub_strategy.sub_update_strategy import SubUpdateStrategy

logger = setup_logger()

class EventManager():
    """
    Manages event subscriptions and notifications.

    The `EventManager` class allows you to manage subscribers for different event types, 
    notify them when events occur, and apply custom strategies for publishing and updating.

    Attributes:
        __subscribers (dict): Stores event types as keys and lists of subscribers as values.
        __notify_strategies (dict): Stores custom notification strategies for each event type.
        __update_strategies (dict): Stores custom update strategies for each event type.
    """
    def __init__(self):
        """
        Initializes an `EventManager` instance.

        Sets up empty dictionaries for managing subscribers, notification strategies, 
        and update strategies.
        """
        self.__subscribers = {} 
        self.__notify_strategies = {}  
        self.__update_strategies = {}  
    
    def subscribe(self, event_type, subscriber):
        """
        Subscribes a new subscriber to a specific event type.

        Args:
            event_type (str): The type of event to subscribe to.
            subscriber (object): The subscriber to add to the event.

        Logs:
            - Logs info when a new subscriber list is created for an event type.
            - Logs info when a subscriber is added.
            - Logs info if a subscriber is already subscribed.

        Raises:
            None
        """
        if event_type not in self.__subscribers:
            self.__subscribers[event_type] = []
            logger.info(f"Created new subscriber list for event {event_type}")

        if subscriber not in self.__subscribers[event_type]:
            self.__subscribers[event_type].append(subscriber)
            logger.info(f"Subscriber added to event {event_type}")
        else:
            logger.info(f"Subscriber already subscribed to event {event_type}")

    def unsubscribe(self, event_type, subscriber):
        """
        Unsubscribes a subscriber from a specific event type.

        Args:
            event_type (str): The type of event to unsubscribe from.
            subscriber (object): The subscriber to remove.

        Logs:
            - Logs info when a subscriber is successfully removed.
            - Logs a warning if the event type has no subscribers.
            - Logs an error if the subscriber is not found.

        Raises:
            None
        """
        if event_type in self.__subscribers:
            try:
                self.__subscribers[event_type].remove(subscriber)
                logger.info(f"Subscriber removed from event {event_type}")
            except ValueError:
                logger.error(f"Subscriber not found for event {event_type}")
        else:
            logger.warning(f"Event type {event_type} has no subscribers.")
    
    def notify(self, event_type, data, *args, **kwargs):
        """
        Notifies all subscribers of a specific event type.

        Args:
            event_type (str): The type of event to notify subscribers about.
            data (dict): The data to send to the subscribers.
            *args: Additional positional arguments for the notify strategy.
            **kwargs: Additional keyword arguments for the notify strategy.

        Logs:
            - Logs a warning if no subscribers exist for the event type.
            - Logs an error if the notification fails.
            - Logs info when the notification is successful.

        Raises:
            None
        """
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