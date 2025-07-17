from enum import Enum
from ..core.math import Vector2

class RenderLayer(Enum):
    BACKGROUND= 0
    WORLD= 100
    EFFECTS= 200
    UI= 300
    OVERLAY= 400
    DEBUG= 500

class DrawType(Enum):
    SPRITE= "SPRITE"
    POLYGON= "POLYGON"
    LINE= "LINE"
    CURVE= "CURVE"

class DrawSpace(Enum):
    WORLD= "WORLD"
    SCREEN= "SCREEN"

class DrawCall():

    def __init__(self, data, position: Vector2, type: DrawType, layer: RenderLayer, space: DrawSpace= DrawSpace.WORLD):
        self.data = data
        self.position = position
        self.type = type
        self.layer = layer
        self.space = space