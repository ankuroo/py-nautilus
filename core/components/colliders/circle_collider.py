from .base import Collider
from ...math import Vector2, utils
from ...components import Transform

class CircleCollider(Collider):

    def __init__(self, radius=100, is_trigger=False):
        super().__init__(is_trigger)
        self.radius = radius

    def start(self):
        super().start()
        self.transform: Transform = self.owner.get_component(Transform)

    def get_bounds(self):
        center = self.transform.get_global_position()
        aa = center - Vector2(self.radius, self.radius)
        bb = center + Vector2(self.radius, self.radius)

        return (aa, bb)

    def overlaps(self, collider):

        if not utils.aabb_overlap(self.get_bounds(), collider.get_bounds()):
            return False

        if isinstance(collider, CircleCollider):
            return self.transform.get_global_position().distance(collider.transform.get_global_position()) < (self.radius + collider.radius)

        return False