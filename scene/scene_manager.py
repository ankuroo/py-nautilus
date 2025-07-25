from .scene import Scene

class SceneManager:

    def __init__(self, engine):
        self.engine = engine
        self.scenes : dict[str, Scene] = {}
        self.stack : list[Scene] = []
        self.active_scene : Scene = None

    def _ensure_scene_exists(self, name):
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found.")

    def _ensure_scene_not_exists(self, name):
        if name in self.scenes:
            raise ValueError(f"Scene '{name}' already in scene manager.")

    def _is_scene_active(self, name):
        return self.active_scene == self.scenes[name]

    def add_scene(self, name: str, scene: Scene):
        self._ensure_scene_not_exists(name)

        scene.set_screen(self.engine.screen)
        scene.set_scene_manager(self)
        self.scenes[name] = scene

    def push_scene(self, name):
        self._ensure_scene_exists(name)

        if not self._is_scene_active(name) and self.scenes[name] not in self.stack:
            if self.active_scene and self.active_scene not in self.stack:
                self.stack.append(self.active_scene)
            self.set_active_scene(name)

    def pop_scene(self):
        if len(self.stack) == 0:
            raise ValueError("No scenes stacked.")

        if self.active_scene:
            self.active_scene.stop()

        self.active_scene = self.stack.pop()

    def set_active_scene(self, name):
        self._ensure_scene_exists(name)

        if not self._is_scene_active(name):
            self.active_scene = self.scenes[name]
            self.active_scene.start()

    def switch_scene(self, name: str, reset_stack: bool= True):
        self._ensure_scene_exists(name)

        if not self._is_scene_active(name):
            if self.active_scene:
                self.active_scene.stop()

            if reset_stack:
                self.stack.clear()

            self.set_active_scene(name)

    def exit(self):
        if self.active_scene:
            self.active_scene.stop()
            self.active_scene = None

        self.scenes.clear()
        self.stack.clear()