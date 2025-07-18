from ... import Component

class Collider(Component):

    def __init__(self, is_trigger=False):
        super().__init__()
        self.is_trigger = is_trigger

    def get_bounds(self):
        raise NotImplementedError()

    def overlaps(self, collider) -> bool:
        raise NotImplementedError()