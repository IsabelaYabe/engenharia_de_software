from abc import ABC, abstractmethod

class PubNotifyStrategy(ABC):
    @abstractmethod
    def notify(self, event_type, data, subscribers, *args, **kwargs): ...