from functools import wraps
from sub_strategy.sub_update_strategy import DefaultSubUpdateStrategy
from custom_logger import setup_logger

logger = setup_logger()

def pubsub(instance):
    """
    PubSub Decorator for instances.

    This decorator augments an **instance** of a class with functionalities for publishing and subscribing to events.
    It dynamically adds methods for publishing (`__publish_event`) and subscribing (`update`) to events, and initializes 
    event subscriptions during the object's instantiation.

    Attributes (Required in Instance):
    - event_manager_pub: The event manager instance for publishing events.
    - event_manager_sub: The event manager instance for subscribing to events.
    - events_type_pub: List or set of event types that the instance can publish.
    - events_type_sub: List or set of event types that the instance can subscribe to.

    Parameters:
    instance : object
        The instance to be decorated.

    Returns:
    object
        The same instance with added functionalities for event publishing and subscription.
    """
    event_manager_pub = getattr(instance, "event_manager_pub", None)
    event_manager_sub = getattr(instance, "event_manager_sub", None)
    events_type_pub = getattr(instance, "events_type_pub", None)
    events_type_sub = getattr(instance, "events_type_sub", None)

    logger.debug(f"event_manager_pub: {event_manager_pub}, event_manager_sub: {event_manager_sub}, events_type_pub: {events_type_pub}, events_type_sub: {events_type_sub}")    

    if event_manager_pub and events_type_pub:
        logger.info(f"The instance was instantiated as a publisher of events: {events_type_pub}")
        
        def publish_event(self, event_type, **data):
            if event_type in self.events_type_pub:
                try:
                    self.event_manager_pub.notify(event_type, data)
                    logger.info(f"Event published: {event_type} with data: {data}")
                except Exception as e:
                    logger.error(f"Failed to publish event {event_type}: {e}")
            else:
                logger.warning(f"Event {event_type} is not in the configured publish list: {events_type_pub}")
        
        private_method_name = f"_{type(instance).__name__}__publish_event"
        setattr(instance, private_method_name, publish_event.__get__(instance))
        logger.debug(f"__publish_event created for instance: {getattr(instance, private_method_name)}")
    
    if event_manager_sub and events_type_sub:
        logger.info(f"The instance was instantiated as a subscriber of events: {events_type_sub}")
        
        def update(self, event_type, **data):
            strategies = self.event_manager_sub.update_strategies
            strategy = strategies.get(event_type, DefaultSubUpdateStrategy())
            if event_type in self.events_type_sub:
                try:
                    logger.info(f"Received event {event_type} with data: {data}")
                    strategy.update(data)
                except Exception as e:
                    logger.error(f"Failed to handle event '{event_type}': {e}")
            else:
                logger.warning(f"Event {event_type} is not in the configured subscribe list: {events_type_sub}")

        setattr(instance, 'update', update.__get__(instance))
        logger.debug(f"update method set on instance: {instance}")

        try:
            for event_type in events_type_sub:
                if event_type not in event_manager_sub.update_strategies:
                    logger.warning(f"No update strategy registered for event '{event_type}'. Using default.")
                event_manager_sub.subscribe(event_type, instance)
                logger.info(f"Subscribed to event {event_type}")
        except Exception as e:
            logger.error(f"Failed to subscribe to event {events_type_sub}: {e}")
    
    return instance
