import pygame
from ..math import Vector2, utils
from ..component import Component
from ..components import Transform

PIXELS_PER_WORLD_UNIT = 100

class Camera(Component):

    def __init__(self, viewport_size: Vector2, viewport_bounds: tuple[Vector2, Vector2]= None, bg_color: tuple[int, int, int]= (0, 0, 0)):
        super().__init__()

        self.render_tags = set(["all"])

        # Viewport Settings
        self.viewport_size = viewport_size
        self.render_target = pygame.Surface(viewport_size.to_tuple(), pygame.SRCALPHA)
        self.viewport_bounds = viewport_bounds if viewport_bounds else (Vector2(0,0), Vector2(1,1))

        self.bg_color = bg_color

        # Zoom settings
        self.min_zoom = 1
        self.max_zoom = 2
        self.zoom = 1
        self.base_zoom_multiplier = PIXELS_PER_WORLD_UNIT

    def start(self):
        super().start()
        self.transform: Transform = self.owner.get_component(Transform) or Transform()

    def add_render_tags(self, tags: list[str]):
        for tag in tags:
            self.render_tags.add(tag)

    def remove_render_tags(self, tags: list[str]):
        for tag in tags:
            self.render_tags.discard(tag)

    def toggle_render_tag(self, tag: str):
        if tag in self.render_tags:
            self.render_tags.remove(tag)
        else:
            self.render_tags.add(tag)

    def clear_render_tags(self):
        self.render_tags.clear()

    def world_to_screen(self, position):
        return (position - self.transform.get_global_position()) * self.get_zoom() + (self.viewport_size / 2)

    def screen_to_world(self, position):
        return (position - (self.viewport_size / 2)) / self.get_zoom() + self.transform.get_global_position()

    def get_zoom(self):
        return self.zoom * self.base_zoom_multiplier

    def set_bg_color(self, color: tuple[int, int, int]):
        self.bg_color = color

    def set_zoom(self, zoom: float | int):
        if not isinstance(zoom, (float, int)):
            raise TypeError(f"Cannot zoom camera with type: {type(zoom)}")

        self.zoom = utils.clamp(zoom, self.min_zoom, self.max_zoom)

    def set_zoom_limits(self, min_zoom: float, max_zoom: float):
        if min_zoom <= 0 or max_zoom <= 0:
            raise ValueError("Zoom limits must be positive numbers")
        if min_zoom > max_zoom:
            min_zoom, max_zoom = max_zoom, min_zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.set_zoom(self.zoom)

    def zoom_by(self, zoom: float | int):
        if not isinstance(zoom, (float, int)):
            raise TypeError(f"Cannot zoom camera with type: {type(zoom)}")
        self.set_zoom(self.zoom * zoom)