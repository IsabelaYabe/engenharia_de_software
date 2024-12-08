"""
Module for defining publish notification strategies.

This module provides an abstract base class `PubNotifyStrategy` and a default 
implementation `DefaultPubNotifyStrategy` for notifying subscribers about events.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - abc.ABC
    - abc.abstractmethod
    - custom_logger.setup_logger
"""

from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger

logger = setup_logger()

class PubNotifyStrategy(ABC):
    """
    Abstract base class for publish notification strategies.

    This class defines the interface for notifying subscribers about events. 
    Any custom notification strategy should inherit from this class and implement the `notify` method.
    """
    @abstractmethod
    def notify(self, event_type, data, subscribers, *args, **kwargs): 
        """
        Notifies subscribers about a specific event.

        Args:
            event_type (str): The type of event being notified.
            data (dict): Data related to the event.
            subscribers (list): A list of subscribers to notify.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass


class DefaultPubNotifyStrategy(PubNotifyStrategy):
    """
    Default implementation of the `PubNotifyStrategy` interface.

    This class provides the default logic for notifying subscribers. It iterates over 
    all subscribers and calls their `update` method with the event type and associated data.
    """
    def notify(self, event_type, data, subscribers, *args, **kwargs):
        """
        Notifies all subscribers for a specific event.

        Args:
            event_type (str): The type of event being notified.
            data (dict): Data related to the event.
            subscribers (list): A list of subscribers to notify.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        for subscriber in subscribers:

            try:
                subscriber.update(event_type, **data)
                logger.info(f"Subscriber {subscriber.table_name} updated for event {event_type}")
            except Exception as e:
                logger.error(f"Failed to notify subscriber {subscriber} for event {event_type}: {e}")