import pygame
from functions import get_songs_volume, get_sounds_volume

class SoundManager:
    def __init__(self):
        # Attempt to initialize the Pygame mixer module
        try:
            pygame.mixer.init()
        except Exception as e:
            print("We could not inicializate the sound, do u have audio output?")
        
        # Dictionaries to store songs and sound effects
        self.songs = {}
        self.sounds = {}

    def load_song(self, name, file_path):
        # Loads a song and stores it in the dictionary with volume applied
        try:
            song = pygame.mixer.Sound(file_path)
            song.set_volume(get_songs_volume())
            self.songs[name] = song
        except pygame.error as e:
            print(f"Error loading '{file_path}': {e}")
        
    def load_sound(self, name, file_path):
        # Loads a sound effect and stores it in the dictionary with volume applied
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(get_sounds_volume())
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Error loading '{file_path}': {e}")

    def play_song(self, name, loops=0):
        # Plays the specified song if it exists
        if name in self.songs:
            self.songs[name].play(loops)
        else:
            print(f"Song '{name}' not found.")
    
    def play_sound(self, name, loops=0):
        # Plays the specified sound effect if it exists
        if name in self.sounds:
            self.sounds[name].play(loops)
        else:
            print(f"Sound '{name}' not found.")

    def stop_song(self, name):
        # Stops the specified song if it exists
        if name in self.songs:
            self.songs[name].stop()
    
    def stop_sound(self, name):
        # Stops the specified sound effect if it exists
        if name in self.sounds:
            self.sounds[name].stop()

    def update_volumes(self):
        # Updates the volume of all loaded songs and sounds
        for song in self.songs.values():
            song.set_volume(get_songs_volume())
        for sound in self.sounds.values():
            sound.set_volume(get_sounds_volume())

    def stop_all(self):
        # Stops all currently playing sounds and songs
        pygame.mixer.stop()