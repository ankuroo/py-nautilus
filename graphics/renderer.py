import pygame, math
from ..core.math import Vector2, utils
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
        camera.viewport.fill(camera.bg_color)

        self.draw_calls.sort(key=lambda c: (c.layer.value, -c.position.y, c.order_in_layer))

        for call in self.draw_calls:
            _position = camera.world_to_screen(call.position) if call.space == DrawSpace.WORLD else call.position
            if call.type == DrawType.SPRITE:
                self._draw_sprite(call, _position, camera)

            elif call.type == DrawType.LINE:
                self._draw_line(call, _position, camera)

            elif call.type == DrawType.POLYGON:
                self._draw_polygon(call, _position, camera)

            elif call.type == DrawType.CURVE:
                self._draw_curve(call, _position, camera)

        absolute_bounds = (
            (camera.viewport_bounds[0] * Vector2(*self.engine.resolution)),
            (camera.viewport_bounds[1] * Vector2(*self.engine.resolution))
        )

        surface = pygame.transform.scale(camera.viewport, (absolute_bounds[1] - absolute_bounds[0]).to_tuple())

        self.screen.blit(surface, absolute_bounds[0].to_tuple())

        pygame.display.flip()

    def _draw_sprite(self, call: DrawCall, position: Vector2, camera):

        surface: pygame.Surface = call.data
        zoom = camera.get_zoom() * (camera.viewport_size.x / self.engine.resolution[0])

        if zoom * call.scale != Vector2(1,1) or call.rotation != 0:
            (scaled_x, scaled_y) = (zoom * call.scale * Vector2(*surface.get_size())).to_tuple()
            surface = pygame.transform.scale(call.data, (int(scaled_x), int(scaled_y)))
            angle = -call.rotation
            surface = pygame.transform.rotate(surface, angle)

        rect = surface.get_rect(center=(int(position.x), int(position.y)))

        camera.viewport.blit(surface, rect.topleft)

    def _draw_line(self, call, position, camera):
        zoom = camera.get_zoom() * (camera.viewport_size.x / self.engine.resolution[0])
        angle_rad = math.radians(call.rotation)

        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        _points = []
        for point in call.data:
            # Rotate point
            rotated_x = point.x * cos_a - point.y * sin_a
            rotated_y = point.x * sin_a + point.y * cos_a

            # Apply zoom and position offset
            screen_x = int(rotated_x * zoom + position.x)
            screen_y = int(rotated_y * zoom + position.y)

            _points.append((screen_x, screen_y))

        line_width = max(1, int(1 * zoom))
        pygame.draw.lines(camera.viewport, (255, 255, 255), False, _points, line_width)

    def _draw_polygon(self, call, position, camera):
        zoom = camera.get_zoom() * (camera.viewport_size.x / self.engine.resolution[0])
        angle_rad = math.radians(call.rotation)

        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        _points = []
        for point in call.data["points"]:
            rotated_x = point.x * cos_a - point.y * sin_a
            rotated_y = point.x * sin_a + point.y * cos_a

            screen_x = int(rotated_x * zoom + position.x)
            screen_y = int(rotated_y * zoom + position.y)

            _points.append((screen_x, screen_y))

        pygame.draw.polygon(camera.viewport, call.data['color'], _points)

    def _draw_curve(self, call, position, camera):
        points = call.data['points']
        color = call.data['color']
        segments = call.data['segments']
        zoom = camera.get_zoom() * (camera.viewport_size.x / self.engine.resolution[0])
        angle_rad = math.radians(call.rotation)

        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        curve_points = []
        n = len(points)

        if n < 2:
            return

        if n == 2:
            self._draw_line(call, position, camera)
            return

        padded_points = [points[0], points[0]] + points + [points[-1], points[-1]]
        n = len(padded_points)

        for i in range(n-3):
            p0, p1, p2, p3 = padded_points[i:i+4]

            for step in range(segments + 1):
                t = step / segments
                pt = utils.catmull_rom(p0, p1, p2, p3, t)

                rotated_x = pt.x * cos_a - pt.y * sin_a
                rotated_y = pt.x * sin_a + pt.y * cos_a
                screen_x = int(rotated_x * zoom + position.x)
                screen_y = int(rotated_y * zoom + position.y)

                curve_points.append((screen_x, screen_y))
        
        if len(curve_points) > 1:
            line_width = max(1, int(1 * zoom))
            pygame.draw.lines(camera.viewport, color, False, curve_points, line_width)

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        if not self.screen:
            raise ValueError("No screen found.")

        self.screen.fill((0,0,0))

        self.dispatch_draw_calls()

        self.draw_calls.clear()