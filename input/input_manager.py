import pygame

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

        # Keyboard
        self.current_frame_keys = set()
        self.last_frame_keys = self.current_frame_keys

        # Mouse
        self.mouse_position = (0, 0)
        self.current_mouse_buttons = (False, False, False)
        self.last_mouse_buttons = self.current_mouse_buttons

        # Close Input
        self.close = False

        self._initialized = True

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

    def update(self):

        self.last_frame_keys = self.current_frame_keys.copy()
        self.last_mouse_buttons = self.current_mouse_buttons

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close = True

            # Mouse Events
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_position = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.current_mouse_buttons = pygame.mouse.get_pressed()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.current_mouse_buttons = pygame.mouse.get_pressed()

            elif event.type == pygame.KEYDOWN:
                self.current_frame_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                self.current_frame_keys.discard(event.key)