def lerp(a, b, t):
    return a + ((b - a) * t)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def catmull_rom(p0, p1, p2, p3, t: float):
    t2 = t * t
    t3 = t2 * t

    return (
        (p1 * 2) +
        (p2 - p0) * t +
        (p0 * 2 - p1 * 5 + p2 * 4 - p3) * t2 +
        (-p0 + p1 * 3 - p2 * 3 + p3) * t3
    ) * 0.5

def point_in_aabb(point: tuple[float|int, float|int], a: tuple[int|float, int|float], b: tuple[int|float, int|float]):
    x_min = min(a[0], b[0])
    x_max = max(a[0], b[0])
    y_min = min(a[1], b[1])
    y_max = max(a[1], b[1])

    return x_min <= point[0] <= x_max and y_min <= point[1] <= y_max