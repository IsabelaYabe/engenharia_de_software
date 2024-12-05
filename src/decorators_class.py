from sub_strategy.default_sub_update_strategy import DefaultSubUpdateStrategy
from custom_logger import setup_logger
logger = setup_logger()

def pubsub(cls):
    original_init = cls.__init__

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
                logger.debug("Após definição de publish event")
                private_method_name = f"_{cls.__name__}__publish_event"
                setattr(self, private_method_name, publish_event.__get__(self))
                logger.debug(f"publish_event criado: {getattr(self, private_method_name)}")
        
        if event_manager_sub != None:    
            if events_type_sub != None:
                logger.info(f"The data was instantiated as a subscriber of events: {events_type_sub}")
                
                def update(self, event_type, **data):
                    strategies = {}
                    strategy = strategies.get(event_type, DefaultSubUpdateStrategy())
                    if event_type in self.events_type_sub:
                        try:
                            logger.info(f"Received event {event_type} with data: {data}")
                            strategy.update(data)
                        except Exception as e:
                            logger.error(f"Failed to handle event '{event_type}': {e}")
                    else:
                         logger.warning(f"Event {event_type} is not in the configured subscribe list: {events_type_sub}")

                setattr(cls, "update", update.__get__(self))
                logger.debug(f"__update criado: {getattr(self, 'update')}")

                try:
                    for event_type in self.events_type_sub:
                        self.event_manager_sub.subscribe(event_type, self)
                        logger.info(f"Subscribed to event {event_type}")
                except Exception as e:
                     logger.error(f"Failed to subscribe to event {events_type_sub}: {e}")
    logger.debug("Após adicionar novo init")
    if hasattr(cls, "_DatabaseManager__publish_event"):
        logger.debug("Método criado com sucesso")
    else:
        logger.debug("Método não criado com sucesso")
    logger.debug("Após teste de add métodos")
    
    cls.__init__ = new_init 
    return cls