class Scene:

    def __init__(self):
        self.screen = None
        self.scene_manager = None

    def set_screen(self, screen):
        self.screen = screen

    def set_scene_manager(self, manager):
        self.scene_manager = manager

    def start(self):
        pass

    def update(self, dt):
        pass

    def render(self):
        pass

    def stop(self):
        pass
