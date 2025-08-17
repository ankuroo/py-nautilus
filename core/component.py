class Component:
    def __init__(self):
        self.owner = None
        self.started = False
        self.active = False

    def set_active(self, active):
        self.active = active

    def set_owner(self, owner):
        self.owner = owner

    def start(self):
        self.started = True
        self.active = True

    def update(self, dt):
        if not self.active:
            return
        pass

    def render(self):
        return []

    def stop(self):
        self.started = False
        self.active = False