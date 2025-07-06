import pygame
from ..core.math import Vector2
from .graphics import DrawCall, DrawSpace, DrawType

class Renderer:

    def __init__(self):
        self.screen = None
        self.draw_calls: list[DrawCall] = []

    def add_draw_call(self, call: DrawCall):
        self.draw_calls.append(call)

    def add_draw_calls(self, calls: list[DrawCall]):
        self.draw_calls.extend(calls)

    def dispatch_draw_calls(self):
        self.draw_calls.sort(key=lambda c: (c.layer.value, c.position.y))

        for call in self.draw_calls:
            _position = call.position if call.space == DrawSpace.WORLD else call.position # TODO implement offset translation 
            if call.type == DrawType.SPRITE:
                self._draw_sprite(call.surface, _position)
            elif call.type in [DrawType.CURVE, DrawType.LINE, DrawType.POLYGON]:
                raise NotImplementedError(f"Draw type '{call.type.value}' not yet implemented.")

        pygame.display.flip()

    def _draw_sprite(self, surface, position: Vector2):
        self.screen.blit(surface, position.to_tuple())

    def set_screen(self, screen):
        self.screen = screen


    def draw(self):
        if not self.screen:
            raise ValueError("No screen found.")

        self.screen.fill((0,0,0))

        self.dispatch_draw_calls()

        self.draw_calls.clear()