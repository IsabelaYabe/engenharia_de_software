class EventManager():
    def __init__(self):
        self.subscribers = {} # Key event, value list of subscribers
    
    def subscribe(self, event_type, subscriber): 
        if event_type not in self.subscribers:
            subscribers = self.subscribers[event_type] 
            subscribers = []
        if subscriber in subscribers:
            print("Já inscrito")

    def unsubscribe(self, event_type, subscriber):
        if event_type in self.subscribers:
            try: 
                self.subscribers[event_type].remove(subscriber)
            except:
                raise
    
    def notify(self, event_type, data):
        if event_type in self.subscribers:
            for subscriber in self.subscribers:
                subscriber.update(event_type, data)