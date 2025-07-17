import pygame
from ..core.math import Vector2
from .graphics import DrawCall, DrawSpace, DrawType

class Renderer:

    def __init__(self, engine):
        self.engine = engine
        self.screen = None
        self.draw_calls: list[DrawCall] = []

    def add_draw_call(self, call: DrawCall):
        self.draw_calls.append(call)

    def add_draw_calls(self, calls: list[DrawCall]):
        self.draw_calls.extend(calls)

    def dispatch_draw_calls(self):
        if len(self.draw_calls) == 0:
            return

        if not self.engine.scene_manager.active_scene or not self.engine.scene_manager.active_scene.active_camera:
            return

        camera = self.engine.scene_manager.active_scene.active_camera

        self.draw_calls.sort(key=lambda c: (c.layer.value, c.position.y))

        for call in self.draw_calls:
            _position = camera.world_to_screen(call.position) if call.space == DrawSpace.WORLD else call.position
            if call.type == DrawType.SPRITE:
                self._draw_sprite(call.data, _position, camera.get_zoom())

            elif call.type == DrawType.LINE:
                self._draw_line(call.data, _position, camera.get_zoom())

            elif call.type in [DrawType.CURVE, DrawType.POLYGON]:
                raise NotImplementedError(f"Draw type '{call.type.value}' not yet implemented.")

        pygame.display.flip()

    def _draw_sprite(self, surface: pygame.Surface, position: Vector2, zoom: float|int = 1.0):
        if zoom != 1:
            surface = pygame.transform.scale_by(surface, zoom)
        self.screen.blit(surface, position.to_tuple())

    def _draw_line(self, points: list[Vector2], position: Vector2, zoom: float|int = 1.0):

        _points = [((point * zoom) + position).to_tuple() for point in points]

        pygame.draw.lines(self.screen, (255, 255, 255), False, _points, int(1 * zoom))

    def set_screen(self, screen):
        self.screen = screen


    def draw(self):
        if not self.screen:
            raise ValueError("No screen found.")

        self.screen.fill((0,0,0))

        self.dispatch_draw_calls()

        self.draw_calls.clear()