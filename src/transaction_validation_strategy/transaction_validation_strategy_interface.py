from abc import ABC, abstractmethod

class TransactionValidationStrategy(ABC):
    @abstractmethod
    def transaction_validation(self, transaction_instance, *args, **kwargs): ...