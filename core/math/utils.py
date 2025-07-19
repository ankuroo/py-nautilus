from . import Vector2

def aabb_overlap(a: tuple[Vector2, Vector2], b: tuple[Vector2, Vector2]):
    a_min, a_max = a
    b_min, b_max = b

    return a_min.x < b_max.x and a_max.x > b_min.x and a_min.y < b_max.y and a_max.y > b_min.y

def lerp(a, b, t):
    return a + ((b - a) * t)