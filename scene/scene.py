from ..core import GameObject

class Scene:

    def __init__(self):
        self.screen = None
        self.scene_manager = None
        self.root = GameObject('root')

    def add_to_scene(self, g_object: GameObject, parent: GameObject = None):
        _parent = parent if parent is not None else self.root
        _parent.add_child(g_object)

    def remove_from_scene(self, g_object: GameObject):
        if g_object == self.root:
            raise ValueError("Cannot remove scene root from scene")

        if g_object.parent:
            g_object.parent.remove_child(g_object)
        g_object.stop()

    def set_screen(self, screen):
        self.screen = screen

    def set_scene_manager(self, manager):
        self.scene_manager = manager

    def start(self):
        self.root.start()

    def update(self, dt):
        self.root.update(dt)

    def render(self):
        self.root.render()

    def stop(self):
        self.root.stop()
