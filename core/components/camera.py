from ..math import Vector2, utils
from ..component import Component
from ..components import Transform

class Camera(Component):

    def __init__(self, v_width: int, v_height: int, bg_color: tuple[int, int, int] = (0,0,0)):
        super().__init__()
        self.viewport_size = Vector2(v_width, v_height)
        self.bg_color = bg_color
        self.min_zoom = 1
        self.max_zoom = 2
        self.zoom = 1
        self.base_zoom_multiplier = 1

    def start(self):
        super().start()
        self.transform: Transform = self.owner.get_component(Transform) or Transform()

    def world_to_screen(self, position):
        return (position - self.transform.get_global_position()) * self.zoom + (self.viewport_size / 2)

    def screen_to_world(self, position):
        return (position - (self.viewport_size / 2)) / self.zoom + self.transform.get_global_position()

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