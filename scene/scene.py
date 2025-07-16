from ..core import GameObject

class Scene:

    def __init__(self):
        self.screen = None
        self.scene_manager = None
        self.root = GameObject('root')
        self.tag_registry: dict[str, set[GameObject]] = {}

    def add_to_scene(self, g_object: GameObject, parent: GameObject = None):
        if g_object == self.root:
            raise ValueError("Cannot add scene root to itself")

        _parent = parent if parent is not None else self.root
        _parent.add_child(g_object)
        self._set_object_scene_recursive(g_object)

        for tag in g_object.tags:
            self.register_tagged_object(tag, g_object)

    def _set_object_scene_recursive(self, g_object: GameObject):
        g_object.scene = self

        for child in g_object.children:
            self._set_object_scene_recursive(child)

    def remove_from_scene(self, g_object: GameObject):
        if g_object == self.root:
            raise ValueError("Cannot remove scene root from scene")

        if g_object.parent:
            g_object.parent.remove_child(g_object)

        self._unregister_tagged_objects_recursive(g_object)

        g_object.stop()

    def find_by_name(self, name: str):
        return self._find_by_name_recursive(name, self.root)

    def _find_by_name_recursive(self, name: str, g_object: GameObject):
        if g_object.name == name:
            return g_object

        for child in g_object.children:
            found = self._find_by_name_recursive(name, child)
            if found:
                return found

        return None

    def find_by_tag(self, tag):
        if tag not in self.tag_registry:
            return set()
            
        return self.tag_registry[tag]

    def register_tagged_object(self, tag: str, g_object: GameObject):
        if tag not in self.tag_registry:
            self.tag_registry[tag] = set()

        self.tag_registry[tag].add(g_object)

    def unregister_tagged_object(self, tag: str, g_object: GameObject):
        if tag not in self.tag_registry:
            return

        self.tag_registry[tag].discard(g_object)

        if not self.tag_registry[tag]:
            del self.tag_registry[tag]

    def _unregister_tagged_objects_recursive(self, g_object: GameObject):
        for tag in g_object.tags:
            self.unregister_tagged_object(tag, g_object)

        g_object.scene = None

        for child in g_object.children:
            self._unregister_tagged_objects_recursive(child)

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