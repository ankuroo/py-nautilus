import pygame

from enum import Enum

class HatDirection(Enum):
    NEUTRAL = (0, 0)
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP_LEFT = (-1, 1)
    UP_RIGHT = (1, 1)
    DOWN_LEFT = (-1, -1)
    DOWN_RIGHT = (1, -1)

def detect_layout(guid: str, name: str):
    if "PlayStation" in name or "DualSense" in name or "Sony" in name:
        return "PlayStation"
    elif "Xbox" in name or guid.startswith("030000005e04"):
        return "Xbox"
    elif "Switch" in name or "Nintendo" in name:
        return "Nintendo"
    elif "8BitDo" in name:
        return "8BitDo"
    else:
        return "Unknown"

class Controller:

    def __init__(self, joystick: pygame.joystick.Joystick):
        joystick.init()
        self.joystick = joystick
        self.instance_id = joystick.get_instance_id()
        self.name = joystick.get_name()
        self.guid = joystick.get_guid()
        self.layout = detect_layout(self.guid, self.name)

        self.hat_count = self.joystick.get_numhats()
        self.current_frame_hats = {}
        self.last_frame_hats = {}

        self.current_frame_buttons = set()
        self.last_frame_buttons = set()

    def get_hat_direction(self, hat_idx=0):
        return self.current_frame_hats.get(hat_idx, (0,0))

    def hat_changed(self, hat_idx=0):
        return hat_idx in self.current_frame_hats and hat_idx in self.last_frame_hats and self.current_frame_hats[hat_idx] != self.last_frame_hats[hat_idx]

    def was_hat_pressed(self, hat_idx=0, direction=HatDirection.UP):
        dir_value = direction.value if isinstance(direction, HatDirection) else direction
        return (
            self.current_frame_hats.get(hat_idx) == dir_value and
            self.last_frame_hats.get(hat_idx) != dir_value
        )

    def was_hat_released(self, hat_idx=0, direction=HatDirection.UP):
        dir_value = direction.value if isinstance(direction, HatDirection) else direction
        return (
            self.current_frame_hats.get(hat_idx) != dir_value and
            self.last_frame_hats.get(hat_idx) == dir_value
        )

    def is_hat_held(self, hat_idx=0, direction=HatDirection.UP):
        dir_value = direction.value if isinstance(direction, HatDirection) else direction
        return (
            self.current_frame_hats.get(hat_idx) == dir_value and
            self.last_frame_hats.get(hat_idx) == dir_value
        )


    def button_down(self, button):
        self.current_frame_buttons.add(button)

    def button_up(self, button):
        self.current_frame_buttons.discard(button)

    def was_button_pressed(self, button):
        return button in self.current_frame_buttons and button not in self.last_frame_buttons

    def was_button_released(self, button):
        return button not in self.current_frame_buttons and button in self.last_frame_buttons

    def is_button_held(self, button):
        return button in self.current_frame_buttons and button in self.last_frame_buttons
        
    def update(self):
        self.last_frame_buttons = self.current_frame_buttons.copy()
        self.last_frame_hats = self.current_frame_hats.copy()

        self.current_frame_hats = {
            i: self.joystick.get_hat(i) for i in range(self.hat_count)
        }