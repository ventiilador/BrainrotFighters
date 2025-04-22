import pygame
from functions import get_songs_volume, get_sounds_volume

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.songs = {}
        self.sounds = {}

    def load_song(self, name, file_path):
        try:
            song = pygame.mixer.Sound(file_path)
            song.set_volume(get_songs_volume())
            self.songs[name] = song
        except pygame.error as e:
            print(f"Error loading '{file_path}': {e}")
        
    def load_sound(self, name, file_path):
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(get_sounds_volume())
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Error loading '{file_path}': {e}")

    def play_song(self, name, loops=0):
        if name in self.songs:
            self.songs[name].play(loops)
        else:
            print(f"Song '{name}' not found.")
    
    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops)
        else:
            print(f"Sound '{name}' not found.")

    def stop_song(self, name):
        if name in self.songs:
            self.songs[name].stop()
    
    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()

    def update_volumes(self):
        for song in self.songs.values():
            song.set_volume(get_songs_volume())
        for sound in self.sounds.values():
            sound.set_volume(get_sounds_volume())

    def stop_all(self):
        pygame.mixer.stop()
