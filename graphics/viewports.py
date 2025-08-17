import pygame
from ..core.math import Vector2
from ..core.math.utils import point_in_aabb

class Viewport():

    def __init__(self, name, bounds: tuple[Vector2, Vector2] = None, manager=None):
        self.manager = manager
        self.name = name
        self.bounds = bounds if bounds else (Vector2(0.0, 0.0), Vector2(1.0, 1.0))
        self.camera = None
        self.draw_order = 0

    def assign_camera(self, camera):
        if camera is None:
            raise ValueError("Cannot assign a null camera to viewport")

        self.camera = camera

    def is_mouse_over(self):
        pos = pygame.mouse.get_pos()
        real_bounds = (self.bounds[0] * Vector2(*self.manager.engine.resolution), self.bounds[1] * Vector2(*self.manager.engine.resolution))
        return point_in_aabb(pos, real_bounds[0].to_tuple(), real_bounds[1].to_tuple())

class ViewportManager():

    def __init__(self, engine):
        self.engine = engine
        self.viewports: dict[str, Viewport] = {}

    def create_viewport(self, name, bounds: tuple[Vector2, Vector2]= None):
        if name in self.viewports:
            raise ValueError(f"Viewport with name '{name}' already exists.")

        self.viewports[name] = Viewport(name, bounds, self)

    def clear_viewports(self):
        self.viewports.clear()

    def destroy_viewport(self, name):
        if name in self.viewports:
            del self.viewports[name]

    def get_hovered_viewport(self):

        for vp in sorted(self.viewports.values(), key=lambda v: -v.draw_order):
            if vp.is_mouse_over():
                return vp

        return None