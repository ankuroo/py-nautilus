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