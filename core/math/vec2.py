import math

class Vector2:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        if isinstance(other, Vector2):
             return Vector2(self.x + other.x, self.y + other.y)
        raise TypeError("Unsupported operand type(s) for +: 'Vector2' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        raise TypeError(f"Unsupported operand type(s) for -: 'Vector2' and '{type(other).__name__}'")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        elif isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        raise TypeError(f"Unsupported operand type(s) for *: 'Vector2' and '{type(other).__name__}'")

    def __rmul__(self, other):
        return self.__mul__(other)  # Uses existing multiplication logic

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return Vector2(self.x / other, self.y / other)
        raise TypeError(f"Unsupported operand type(s) for /: 'Vector2' and '{type(other).__name__}'")

    def clean(self, epsilon: float = 1e-10):
        x = 0 if abs(self.x) < epsilon else self.x
        y = 0 if abs(self.y) < epsilon else self.y
        return Vector2(x, y)

    def distance(self, other):
        if isinstance(other, Vector2):
            return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        raise TypeError(f"Unsupported operand type(s) for distance: 'Vector2' and '{type(other).__name__}'")

    def dot(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        raise TypeError(f"Unsupported operand type(s) for dot product: 'Vector2' and '{type(other).__name__}'")

    def length(self):
        return (self.x**2 + self.y**2) ** 0.5

    def normalized(self):
        magnitude = self.length()
        return Vector2(self.x / magnitude, self.y / magnitude) if magnitude != 0 else Vector2(0, 0)

    def rotate(self, degrees: int | float):
        _rads = math.radians(degrees)
        sin_a = math.sin(_rads)
        cos_a = math.cos(_rads)
        _x = (self.x * cos_a) - (self.y * sin_a)
        _y = (self.x * sin_a) + (self.y * cos_a)
        return Vector2(_x, _y)

    def round(self, ndigits: int = 0):
        return Vector2(round(self.x, ndigits), round(self.y, ndigits))

    def to_tuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
