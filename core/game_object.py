class GameObject:

    def __init__(self, name="GameObject"):
        self.name = name
        self.components = {}
        self.active = True
        self.parent = None
        self.children = []

    def _is_ancestor_of(self, obj):
        current = obj
        while current is not None:
            if current == self:
                return True
            current = current.parent
        return False

    def add_child(self, child):
        if child is self:
            raise ValueError(f'GameObject {self.name} cannot be its own child.')

        if child._is_ancestor_of(self):
            raise ValueError(f"GameObject {self.name} cannot be its own ancestor. Cycle detected.")

        child.set_parent(self)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def add_component(self, component):
        comp_class = type(component)
        self.components[comp_class] = component
        component.set_owner(self)

    def get_component(self, comp_class):
        return self.components.get(comp_class, None)

    def remove_component(self, comp_class):
        if comp_class in self.components:
            del self.components[comp_class]

    def set_parent(self, parent):
        if self.parent == parent:
            return

        if self.parent is not None:
            self.parent.remove_child(self)

        self.parent = parent

        if parent is not None and self not in parent.children:
            parent.children.append(self)


    def update(self, dt):
        if not self.active:
            return
        
        for component in self.components.values():
            component.update(dt)

        for child in self.children:
            child.update(dt)

    def render(self):
        if not self.active:
            return

        for component in self.components.values():
            component.render()

        for child in self.children:
            child.render()