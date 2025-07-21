import pygame
from ..core.math.utils import point_in_aabb

class Viewport():

    def __init__(self, name, bounds: tuple[tuple[float, float], tuple[float, float]] = None):
        self.name = name
        self.bounds = bounds if bounds else ((0.0, 0.0), (1.0, 1.0))
        self.camera = None
        self.draw_order = 0

    def assign_camera(self, camera):
        if camera is None:
            raise ValueError("Cannot assign a null camera to viewport")

        self.camera = camera

    def is_mouse_over(self):
        pos = pygame.mouse.get_pos()
        return point_in_aabb(pos, *self.bounds)

    def draw(self):
        pass

class ViewportManager():

    def __init__(self):
        self.viewports: dict[str, Viewport] = {}
        pass

    def create_viewport(self, name, bounds):
        self.viewports[name] = Viewport(name, bounds)

    def destroy_viewport(self, name):
        del self.viewports[name]

    def get_hovered_viewport(self):

        for vp in sorted(self.viewports.values(), key=lambda v: -v.draw_order):
            if vp.is_mouse_over():
                return vp

        return None