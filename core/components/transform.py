from ..component import Component
from ..math import Vector2

class Transform(Component):

    def __init__(self, position: Vector2 = None, rotation: float = 0, scale: Vector2 = None):
        super().__init__()
        self.set_position(position or Vector2(0, 0))
        self.set_rotation(rotation)
        self.set_scale(scale or Vector2(1, 1))

    def get_local_position(self):
        return self.position

    def get_global_position(self):
        if self.owner and self.owner.parent:
            _transform: Transform = self.owner.parent.get_component(Transform)
            if _transform:
                _parent_scale = _transform.get_global_scale()
                _parent_rotation = _transform.rotation
                _offset = self.position.rotate(_parent_rotation) * _parent_scale
                return _transform.get_global_position() + _offset
            return self.position
        return self.position

    def get_local_scale(self):
        return self.scale

    def get_global_scale(self):
        if self.owner and self.owner.parent:
            _transform: Transform = self.owner.parent.get_component(Transform)
            if _transform:
                return _transform.get_global_scale() * self.scale

        return self.scale

    def get_local_rotation(self):
        return self.rotation
    
    def get_global_rotation(self):
        if self.owner and self.owner.parent:
            _transform: Transform = self.owner.parent.get_component(Transform)
            if _transform:
                return _transform.get_global_rotation() + self.rotation
        return self.rotation

    def move(self, vector: Vector2 = Vector2(0,0)):
        self.position += vector

    def rotate(self, rotation: float):
        self.rotation = (self.rotation + rotation) % 360

    def scale_by(self, scale: Vector2 | float | int):
        if not isinstance(scale, (Vector2, float, int)):
            raise TypeError(f"Cannot scale by type: {type(scale)}")
        self.scale *= scale

    def set_position(self, position: Vector2):
        if not isinstance(position, Vector2):
            raise TypeError("Position must be a Vector2.")
        self.position = position

    def set_rotation(self, rotation: float | int):
        if not isinstance(rotation, (float, int)):
            raise TypeError("Rotation must be a float or integer.")

        self.rotation = float(rotation)

    def set_scale(self, scale: Vector2 | float | int):
        if isinstance(scale, (float, int)):
            self.scale = Vector2(scale, scale)
        elif isinstance(scale, Vector2):
            self.scale = scale
        else:
            raise TypeError("Scale must be a Vector2, float, or integer.")
    
    def __repr__(self):
        return f"<Transform position={self.position}, rotation={self.rotation}, scale={self.scale}>"