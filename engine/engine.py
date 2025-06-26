import pygame
from nautilus.input import InputManager

class Engine:

    def __init__(self, title='Game', resolution=(1920, 1080)):
        pygame.display.init()
        pygame.display.set_caption(title)
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)  # test small size
        self.clock = pygame.time.Clock()

        self.dt = 0
        self.tickrate = 60

        self.input_manager = InputManager()

        self.running = False

    def render(self):
        self.screen.fill((0,0,0))
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
        self.input_manager.update()

        if self.input_manager.is_input_exit():
            self.end()

    def update(self):
        pass

    def end(self):
        self.running = False