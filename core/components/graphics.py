from . import Transform
from ..math import Vector2
from .. import Component
from ...graphics import DrawCall, DrawType, RenderLayer

class SpriteRenderer(Component):

    def __init__(self, sprite):
        super().__init__()
        self.sprite = sprite
        self.layer = RenderLayer.WORLD

    def set_layer(self, layer):
        self.layer = layer

    def render(self):
        _transform: Transform = self.owner.get_component(Transform) if self.owner else None
        return [DrawCall(
            self.sprite,
            _transform.get_global_position() if _transform else Vector2(0,0),
            DrawType.SPRITE,
            self.layer
        )]