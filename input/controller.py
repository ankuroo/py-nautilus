import pygame

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

        self.current_frame_buttons = set()
        self.last_frame_buttons = set()

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