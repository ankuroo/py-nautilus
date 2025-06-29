import pygame
import platform
from nautilus.scene import SceneManager

class Engine:

    def __init__(self, title='Game', resolution=(1920, 1080)):
        self.os = self._detect_os()

        if self.os == "Unsupported":
            raise SystemExit("This OS is currently not supported by the engine.")

        pygame.display.init()
        pygame.display.set_caption(title)
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)  # test small size
        self.clock = pygame.time.Clock()

        self.dt = 0
        self.tickrate = 60

        self.scene_manager = SceneManager(self)

        self.running = False

    def _detect_os(self):
        _platform = platform.system()
        if _platform == "Windows":
            return "Windows"
        elif _platform == "Linux":
            return "Linux"
        elif _platform == "Darwin":
            return "Mac OS X"
        else:
            return "Unsupported"


    def render(self):
        self.screen.fill((0,0,0))
        if self.scene_manager.active_scene:
            self.scene_manager.active_scene.render()

        pygame.display.flip()

    def run(self):
        self.running = True

        while self.running:

            self.handle_events()
            self.update()
            self.render()

            self.dt = self.clock.tick(self.tickrate)/1000

        pygame.quit()


    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()


    def update(self):
        if self.scene_manager.active_scene:
            self.scene_manager.active_scene.update(self.dt)

    def end(self):
        self.running = False