from . import Transform
from ..math import Vector2
from .. import Component
from ...graphics import DrawCall, DrawType, RenderLayer

class SpriteRenderer(Component):

    def __init__(self, sprite):
        super().__init__()
        self.sprite = sprite
        self.layer = RenderLayer.WORLD
        self.order_in_layer = 0

    def set_layer(self, layer):
        self.layer = layer

    def set_order_in_layer(self, order):
        self.order_in_layer = order

    def render(self):
        _transform: Transform = self.owner.get_component(Transform) if self.owner else None
        return [DrawCall(
            data= self.sprite,
            position= _transform.get_global_position() if _transform else Vector2(0,0),
            scale= _transform.get_global_scale() if _transform else Vector2(1,1),
            rotation= _transform.get_global_rotation() if _transform else 0,
            order_in_layer= self.order_in_layer,
            type= DrawType.SPRITE,
            layer= self.layer
        )]

class LineRenderer(Component):

    def __init__(self, points: list[Vector2]):
        super().__init__()
        self.points = points
        self.layer = RenderLayer.WORLD
        self.order_in_layer = 0

    def set_layer(self, layer):
        self.layer = layer

    def set_order_in_layer(self, order):
        self.order_in_layer = order

    def render(self):
        _transform: Transform = self.owner.get_component(Transform) if self.owner else None

        return [DrawCall(
            data=self.points,
            position= _transform.get_global_position() if _transform else Vector2(0,0),
            scale= _transform.get_global_scale() if _transform else Vector2(1,1),
            rotation= _transform.get_global_rotation() if _transform else 0,
            order_in_layer=self.order_in_layer,
            type=DrawType.LINE,
            layer= self.layer
        )]