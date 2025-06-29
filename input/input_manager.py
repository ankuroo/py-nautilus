import pygame
from .controller import Controller

class InputManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(InputManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        pygame.joystick.init()

        self.current_input_mode = "KBM"

        # Keyboard
        self.current_frame_keys = set()
        self.last_frame_keys = set()

        # Mouse
        self.mouse_position = (0, 0)
        self.current_mouse_buttons = (False, False, False)
        self.last_mouse_buttons = self.current_mouse_buttons

        # Controllers
        self.controllers: dict[str, Controller] = {}
        self.controller_ids: list[str] = []
        self.scan_controllers()

        # Close Input
        self.close = False

        self._initialized = True

    def get_input_mode(self):
        return self.current_input_mode

    def is_input_exit(self):
        return self.close

    # Mouse Functions
    def get_mouse_position(self):
        return self.mouse_position

    def was_mouse_pressed(self, button=0):
        return self.current_mouse_buttons[button] and not self.last_mouse_buttons[button]

    # Keyboard Functions
    def was_key_pressed(self, key):
        return key in self.current_frame_keys and key not in self.last_frame_keys

    def was_key_released(self, key):
        return key not in self.current_frame_keys and key in self.last_frame_keys

    def is_key_held(self, key):
        return key in self.current_frame_keys and key in self.last_frame_keys

    # Controller Functions
    def get_controller_by_id(self, device_id):
        if device_id not in self.controllers:
            return None
        return self.controllers[device_id]

    def get_controller_by_index(self, index):
        if not (0 <= index < len(self.controller_ids)):
            return None
        return self.get_controller_by_id(self.controller_ids[index])

    def get_controller_count(self):
        return len(self.controllers)

    def scan_controllers(self):
        for joystick_index in range(pygame.joystick.get_count()):
            self._controller_added(joystick_index)

    # Hotswapping Functions
    def _controller_added(self, joystick_index: int):
        _joystick = pygame.joystick.Joystick(joystick_index)
        _controller = Controller(_joystick)
        if _controller.instance_id not in self.controllers:
            self.controller_ids.append(_controller.instance_id)
            self.controllers[_controller.instance_id] = _controller

    def _controller_removed(self, instance_id):
        controller = self.controllers.pop(instance_id, None)

        if controller and instance_id in self.controller_ids:
            self.controller_ids.remove(instance_id)

    def update(self):

        self.last_frame_keys = self.current_frame_keys.copy()
        self.last_mouse_buttons = self.current_mouse_buttons

        for controller in self.controllers.values():
            controller.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.close = True

            # Check Input Mode
            if event.type in [pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self.current_input_mode = "KBM"
            elif event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION]:
                self.current_input_mode = "Controller"

            # Mouse Events
            if event.type == pygame.MOUSEMOTION:
                self.mouse_position = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.current_mouse_buttons = pygame.mouse.get_pressed()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.current_mouse_buttons = pygame.mouse.get_pressed()

            # Keyboard Events
            elif event.type == pygame.KEYDOWN:
                self.current_frame_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                self.current_frame_keys.discard(event.key)

            # Controller Events
            elif event.type == pygame.JOYBUTTONDOWN:
                controller = self.get_controller_by_id(event.instance_id)
                if controller:
                    controller.button_down(event.button)
            elif event.type == pygame.JOYBUTTONUP:
                controller = self.get_controller_by_id(event.instance_id)
                if controller:
                    controller.button_up(event.button)

            # Hotswapping Events
            elif event.type == pygame.JOYDEVICEADDED:
                self._controller_added(event.device_index)
            elif event.type == pygame.JOYDEVICEREMOVED:
                self._controller_removed(event.instance_id)