import pygame
from enum import Enum
from ..core import Component
from ..core.components import Transform

class AudioSpace(Enum):
    LOCAL= "local"
    GLOBAL= "global"


class AudioSource(Component):

    def __init__(self, audio, space: AudioSpace):
        self.sound = pygame.mixer.Sound(audio)
        self.audio_space = space
        self.channel = pygame.mixer.find_channel()
        self.muted = False
        self.set_volume(1.0)

    def start(self):
        super().start()
        self.transform = self.owner.get_component(Transform)
        if self.audio_space == AudioSpace.LOCAL and self.transform is None:
            print(f"[AudioSource] No audio channels available for: {self.sound}")

    def play(self, loops=0):
        if self.is_playing():
            self.stop_playing()

        self.channel = pygame.mixer.find_channel()
        if self.channel:
            self.channel.play(self.sound, loops=loops)
        else:
            raise RuntimeError("No audio channels available.")

    def stop_playing(self):
        if self.channel:
            self.channel.stop()
            self.channel = None

    def is_playing(self):
        return self.channel is not None and self.channel.get_busy()

    def mute(self):
        self.muted = True

    def unmute(self):
        self.muted = False

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))

    def set_stereo_volume(self, l_vol, r_vol):
        if self.channel:
            multiplier = self.volume * (0 if self.muted else 1)
            self.channel.set_volume (l_vol * multiplier, r_vol * multiplier)

    def update(self, dt):
        super().update(dt)
        if self.channel and not self.channel.get_busy():
            self.channel = None

    def stop(self):
        super().stop()
        self.stop_playing()