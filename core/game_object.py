class GameObject:

    def __init__(self, name="GameObject"):
        self.name = name
        self.components = {}
        self.active = True

    def add_component(self, component):
        comp_class = type(component)
        self.components[comp_class] = component
        component.set_owner(self)

    def get_component(self, comp_class):
        return self.components.get(comp_class, None)

    def remove_component(self, comp_class):
        if comp_class in self.components:
            del self.components[comp_class]

    def update(self, dt):
        if not self.active:
            return
        
        for component in self.components.values():
            component.update(dt)

    def render(self):
        if not self.active:
            return

        for component in self.components.values():
            component.render()