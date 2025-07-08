from enum import Enum
import time

class EventType(Enum):
    GENERIC="generic"

class Event:

    def __init__(self, type: EventType, data: dict = None, metadata: dict = None):
        self.type = type
        self.data = data or {}
        self.metadata = metadata or {}
        self.timestamp = time.time()

    def __repr__(self):
        return f"<Event type={self.type} data={self.data} metadata={self.metadata} timestamp={self.timestamp}>"