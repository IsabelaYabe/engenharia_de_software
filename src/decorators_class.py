"""
Module for Pub/Sub Decorator.

This module provides the `pubsub` decorator, which extends a class with publish/subscribe capabilities for event-driven architectures. It dynamically adds methods for publishing and subscribing to events, allowing objects to interact with an event manager for efficient communication.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Complete

Dependencies:
    - sub_strategy.default_sub_update_strategy.DefaultSubUpdateStrategy
    - custom_logger.setup_logger

Decorator:
    - pubsub: Adds publish/subscribe behavior to a class.

Classes:
    - DefaultSubUpdateStrategy (imported): Provides a default strategy for handling subscription updates.

"""

from sub_strategy.default_sub_update_strategy import DefaultSubUpdateStrategy
from custom_logger import setup_logger
logger = setup_logger()

def pubsub(cls):
    """
    Decorator to add publish/subscribe behavior to a class.

    This decorator dynamically injects methods for publishing and subscribing to events into the decorated class.
    It interacts with an event manager, allowing instances of the class to notify and respond to events in an
    event-driven system.

    Args:
        cls (type): The class to be decorated.

    Attributes Added to the Class:
        - `__publish_event`: A method to publish events to the event manager.
        - `update`: A method to handle incoming events and execute associated strategies.

    Requirements:
        - The decorated class must have the following attributes:
            - `__event_manager`: An instance of the event manager handling notifications and subscriptions.
            - `__events_type_pub`: A list of event types the class can publish.
            - `__events_type_sub`: A list of event types the class can subscribe to.
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        event_manager = getattr(cls, "__event_manager", None)     
        events_type_pub = getattr(cls, "__events_type_pub", None)
        events_type_sub = getattr(cls, "__events_type_sub", None)
        logger.debug(f"event_manager: {event_manager}, events_type_pub: {events_type_pub}, events_type_sub: {events_type_sub}")    
        if event_manager != None:
                if events_type_pub != None:
                    def publish_event(self, event_type, **data):
                        if event_type in self.__events_type_pub:
                            try:
                                self.__event_manager.notify(event_type, data)
                                logger.info(f"Event published: {event_type} with data: {data}")
                            except Exception as e:
                                 logger.error(f"Failed to publish event {event_type}: {e}")
                        else:
                             logger.warning(f"Event {event_type} is not in the configured publish list: {events_type_pub}")
                    
                    self.__publish_event = publish_event.__get__(self)

                if events_type_sub != None:
                    def update(self, event_type, **data):
                        strategies = {}
                        strategy = strategies.get(event_type, DefaultSubUpdateStrategy())
                        if event_type in self.__events_type_sub:
                            try:
                                logger.info(f"Received event {event_type} with data: {data}")
                                strategy.update(data)
                            except Exception as e:
                                logger.error(f"Failed to handle event '{event_type}': {e}")
                        else:
                             logger.warning(f"Event {event_type} is not in the configured subscribe list: {events_type_sub}")
                    
                    self.update = update.__get__(self)
                    try:
                        for event_type in self.__events_type_sub:
                            event_manager.subscribe(event_type, self)
                            logger.info(f"Subscribed to event {event_type}")
                    except Exception as e:
                         logger.error(f"Failed to subscribe to event {events_type_sub}: {e}")
    cls.__init__ = new_init 
    return cls