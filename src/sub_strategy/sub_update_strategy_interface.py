from abc import ABC, abstractmethod

class SubUpdateStrategy(ABC):
    @abstractmethod
    def update(self, data): ...