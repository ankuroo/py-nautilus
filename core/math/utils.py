def lerp(a, b, t):
    return a + ((b - a) * t)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))