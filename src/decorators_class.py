
"""
Module for PubSub Decorator.

This module provides a decorator function `pubsub` that dynamically adds publisher and subscriber functionalities 
to classes for event-driven architectures. Classes decorated with `pubsub` can publish and/or subscribe to specific 
event types using designated event managers. The decorator also integrates logging capabilities to provide insights 
into the publishing and subscribing mechanisms.

Author: Isabela Yabe
Last Modified: 05/12/2024
Status: Complete

Dependencies:
    - custom_logger
    - sub_strategy.default_sub_update_strategy

Functions:
    - pubsub(cls): A decorator to add publisher and subscriber functionalities to a class.
"""
from functools import wraps
from sub_strategy.sub_update_strategy import DefaultSubUpdateStrategy
from custom_logger import setup_logger
logger = setup_logger()

def pubsub(cls):
    """
    PubSub Decorator.

    This decorator augments a class with functionalities for publishing and subscribing to events in an event-driven 
    architecture. It dynamically adds methods for publishing (`__publish_event`) and subscribing (`update`) to events, 
    and initializes event subscriptions during the object's instantiation.

    Attributes (Required in Decorated Class):
    - event_manager_pub: The event manager instance for publishing events.
    - event_manager_sub: The event manager instance for subscribing to events.
    - events_type_pub: List or set of event types that the instance can publish.
    - events_type_sub: List or set of event types that the instance can subscribe to.

    Parameters:
    cls : class
        The class to be decorated.

    Returns:
    class
        The decorated class with added functionalities for event publishing and subscription.
    """
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):

        original_init(self, *args, **kwargs)
        
        event_manager_pub = getattr(self, "event_manager_pub", None)
        event_manager_sub = getattr(self, "event_manager_sub", None)
        events_type_pub = getattr(self, "events_type_pub", None)
        events_type_sub = getattr(self, "events_type_sub", None)

        logger.debug(f"event_manager_pub: {event_manager_pub}, event_manager_sub: {event_manager_sub}, events_type_pub: {events_type_pub}, events_type_sub: {events_type_sub}")    
        
        if event_manager_pub != None:
            if events_type_pub != None:
                logger.info(f"The data was instantiated as a publisher of events: {events_type_pub}")
                
                def publish_event(self, event_type, **data):
                    if event_type in self.events_type_pub:
                        try:
                            self.event_manager_pub.notify(event_type, data)
                            logger.info(f"Event published: {event_type} with data: {data}")
                        except Exception as e:
                             logger.error(f"Failed to publish event {event_type}: {e}")
                    else:
                         logger.warning(f"Event {event_type} is not in the configured publish list: {events_type_pub}")
                logger.debug(f"publish_event: {publish_event}")
                private_method_name = f"_{cls.__name__}__publish_event"
                setattr(self, private_method_name, publish_event.__get__(self))
                logger.debug(f"__publish_event created: {getattr(self, private_method_name)}")
        
        if event_manager_sub != None:    
            if events_type_sub != None:
                logger.info(f"The data was instantiated as a subscriber of events: {events_type_sub}")
                
                def update(self, event_type, **data):
                    strategies = self.event_manager_sub.update_strategies
                    strategy = strategies.get(event_type, DefaultSubUpdateStrategy())
                    if event_type in self.events_type_sub:
                        try:
                            logger.info(f"Received event {event_type} with data: {data}")
                            logger.debug(f"Table name: {self.table_name}")
                            strategy.update(data, self.search_record, self.update_row)
                        except Exception as e:
                            logger.error(f"Failed to handle event '{event_type}': {e}")
                    else:
                         logger.warning(f"Event {event_type} is not in the configured subscribe list: {events_type_sub}")

                setattr(cls, "update", update.__get__(self))
                logger.debug(f"__update created: {getattr(self, 'update')}")

                try:
                    for event_type in self.events_type_sub:
                        if event_type not in self.event_manager_sub.update_strategies:
                            logger.warning(f"No update strategy registered for event '{event_type}'. Using default.")
                        self.event_manager_sub.subscribe(event_type, self)
                        logger.info(f"Subscribed to event {event_type}")
                except Exception as e:
                     logger.error(f"Failed to subscribe to event {events_type_sub}: {e}")
    
    cls.__init__ = new_init 
    return cls