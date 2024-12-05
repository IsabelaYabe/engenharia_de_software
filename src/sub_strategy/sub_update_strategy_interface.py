from abc import ABC, abstractmethod

class SubUpdateStrategy(ABC):
    @abstractmethod
    def Update(self, data): ...