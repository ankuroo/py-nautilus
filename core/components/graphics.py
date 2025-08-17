from . import Transform
from ..math import Vector2
from .. import Component
from ...graphics import DrawCall, DrawType, RenderLayer

class SpriteRenderer(Component):

    def __init__(self, sprite, render_tags: set[str]=None):
        super().__init__()
        self.sprite = sprite
        self.layer = RenderLayer.WORLD
        self.order_in_layer = 0
        self.render_tags = render_tags if render_tags else set(["all"])

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
            layer= self.layer,
            render_tags= self.render_tags
        )]

class LineRenderer(Component):

    def __init__(self, points: list[Vector2], render_tags: set[str]= None):
        super().__init__()
        self.points = points
        self.layer = RenderLayer.WORLD
        self.order_in_layer = 0
        self.render_tags = render_tags if render_tags else set(["all"])

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
            layer= self.layer,
            render_tags= self.render_tags
        )]

class PolygonRenderer(Component):

    def __init__(self, points, color= (255,255,255), render_tags: set[str]= None):
        super().__init__()
        self.points = points
        self.color = color
        self.layer = RenderLayer.WORLD
        self.order_in_layer = 0
        self.render_tags = render_tags if render_tags else set(["all"])

    def set_layer(self, layer):
        self.layer = layer

    def set_order_in_layer(self, order):
        self.order_in_layer = order

    def render(self):
        _transform = self.owner.get_component(Transform) if self.owner else None
        return [
            DrawCall(
            data= {"points": self.points, "color": self.color},
            position= _transform.get_global_position() if _transform else Vector2(0,0),
            scale= _transform.get_global_scale() if _transform else Vector2(1,1),
            rotation= _transform.get_global_rotation() if _transform else 0,
            order_in_layer=self.order_in_layer,
            type=DrawType.POLYGON,
            layer= self.layer,
            render_tags= self.render_tags
            )
        ]

class CurveRenderer(Component):

    def __init__(self, points, color= (255,255,255), resolution: int= 10, render_tags: set[str]= None):
        super().__init__()
        self.points = points
        self.color = color
        self.resolution = max(1, min(20, resolution))
        self.layer = RenderLayer.WORLD
        self.order_in_layer = 0
        self.render_tags = render_tags if render_tags else set(["all"])

    def set_layer(self, layer):
        self.layer = layer

    def set_order_in_layer(self, order):
        self.order_in_layer = order

    def render(self):
        _transform = self.owner.get_component(Transform) if self.owner else None
        return [
            DrawCall(
            data= {"points": self.points, "color": self.color, "segments": self.resolution},
            position= _transform.get_global_position() if _transform else Vector2(0,0),
            scale= _transform.get_global_scale() if _transform else Vector2(1,1),
            rotation= _transform.get_global_rotation() if _transform else 0,
            order_in_layer=self.order_in_layer,
            type=DrawType.CURVE,
            layer= self.layer,
            render_tags= self.render_tags
            )
        ]
