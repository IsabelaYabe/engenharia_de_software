def pubsub(cls):
    original_init = cls.__init__
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        event_manager = getattr(cls, "event_manager", False)     
        event_type_pub = getattr(cls, "event_type_pub", False)
        event_type_sub = getattr(cls, "event_type_sub", False)
        if event_type_pub and event_manager:
            def publish_event(data):
                event_manager.notify(self.event_type_pub, data)
            self.publish_event = publish_event.__get__(self)
        if event_type_sub:
            def update(self, data):
                print (f"Something happened! {event_type_sub}: {data}")
            self.update = update.__get__(self)
    cls.__init__ = new_init 
    return cls