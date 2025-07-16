from .component import Component

class GameObject:

    def __init__(self, name="GameObject", tags: set[str] = None):
        self.name = name
        self.components: dict[Component] = {}
        self.active: bool = True
        self.parent: GameObject = None
        self.children: list[GameObject] = []
        self.started: bool = False
        self.scene = None
        self.tags = tags or set()

    def _is_ancestor_of(self, obj):
        current = obj
        while current is not None:
            if current == self:
                return True
            current = current.parent
        return False

    def set_active(self, active):
        self.active = active

    def start(self):
        if self.started:
            return

        for components in self.components.values():
            for component in components:
                if not component.started:
                    component.start()

        for child in self.children:
            child.start()

        self.started = True

    def add_child(self, child):
        if child is self:
            raise ValueError(f'GameObject {self.name} cannot be its own child.')

        if child._is_ancestor_of(self):
            raise ValueError(f"GameObject {self.name} cannot be its own ancestor. Cycle detected.")

        child.set_parent(self)

        if self.started:
            child.start()

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def add_component(self, component):
        comp_class = type(component)
        if comp_class not in self.components:
            self.components[comp_class] = []
        self.components[comp_class].append(component)
        component.set_owner(self)

        if self.started:
            component.start()

    def get_component(self, comp_class):
        components = self.components.get(comp_class, None)
        if components:
            return components[0]
        
        return None

    def get_components(self, comp_class):
        return self.components.get(comp_class, [])

    def remove_component(self, component_or_class):

        if isinstance(component_or_class, Component):
            _type = type(component_or_class)
            if _type in self.components and component_or_class in self.components[_type]:
                self.components[_type].remove(component_or_class)
                component_or_class.set_owner(None)
                if not self.components[_type]:
                    del self.components[_type]

                component_or_class.stop()

        elif isinstance(component_or_class, type):
            if component_or_class in self.components:
                for component in self.components[component_or_class]:
                    component.stop()
                    component.set_owner(None)
                del self.components[component_or_class]

    def add_tag(self, tag: str):
        self.tags.add(tag)

        if self.scene:
            self.scene.register_tagged_object(tag, self)

    def remove_tag(self, tag: str):
        self.tags.discard(tag)

        if self.scene:
            self.scene.unregister_tagged_object(tag, self)

    def set_parent(self, parent):
        if self.parent == parent:
            return

        if parent is self:
            raise ValueError(f"GameObject {self.name} cannot be its own parent.")

        if self._is_ancestor_of(parent):
            raise ValueError(f"GameObject {parent.name} cannot be its own ancestor. Cycle detected.")


        if self.parent is not None:
            self.parent.remove_child(self)

        self.parent = parent

        if parent is not None and self not in parent.children:
            parent.children.append(self)

    def update(self, dt):
        if not self.active:
            return
        
        for components in self.components.values():
            for component in components:
                component.update(dt)

        for child in self.children:
            child.update(dt)

    def render(self):
        if not self.active:
            return

        for components in self.components.values():
            for component in components:
                component.render()

        for child in self.children:
            child.render()

    def stop(self):
        if not self.started:
            return

        for components in self.components.values():
            for component in components:
                component.stop()

        for child in self.children:
            child.stop()

        self.started = False
        self.active = False
        self.scene = None