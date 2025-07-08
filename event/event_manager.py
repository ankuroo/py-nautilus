from collections import deque
from .event import Event, EventType

class EventManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EventManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.subscriptions: dict[EventType, list[callable]] = {}
        self.event_queue = deque()
        self.MAX_EVENTS_PER_FRAME = 1000

        self._initialized = True

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def dispatch(self, event: Event):
        self.event_queue.append(event)

    def handle_events(self):
        processed = 0

        while len(self.event_queue) > 0 and processed < self.MAX_EVENTS_PER_FRAME:
            event = self.event_queue.popleft()
            if event.type in self.subscriptions:
                for callback in self.subscriptions[event.type]:
                    callback(event)
            processed += 1

    def subscribe(self, event_type: EventType, callback: callable):
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []

        self.subscriptions[event_type].append(callback)


