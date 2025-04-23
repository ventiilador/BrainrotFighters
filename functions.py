import json
import pygame

"""
In this module i create the functions that i need usually
"""

def position(x, y):
    resolution = get_resolution()
    return ((resolution[0] * x) // 100, (resolution[1] * y) // 100)

def size(w, h):
    resolution = get_resolution()
    return ((resolution[0] * w) // 100, (resolution[1] * h) // 100)

def position_x(x):
    resolution = get_resolution()
    return resolution[0] * x // 100

def position_y(y):
    resolution = get_resolution()
    return resolution[1] * y // 100

def size_x(w):
    resolution = get_resolution()
    return resolution[0] * w // 100

def size_y(h):
    resolution = get_resolution()
    return resolution[1] * h // 100

def get_songs_volume():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["SongsVolume"]

def get_sounds_volume():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["SoundsVolume"]

def set_songs_volume(volume):
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["SongsVolume"] = volume
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def set_sounds_volume(volume):
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["SoundsVolume"] = volume
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_resolution():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["Resolution"]

def set_resolution(resolution:list):
    with open("data.json", "r") as file:
        data = json.load(file)
        data["Config"]["Resolution"] = resolution
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_fps():
    with open("data.json") as file:
        data = json.load(file)
        return data["Config"]["Fps"]

def set_fps(fps):
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["Fps"] = fps
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_fullscreen():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["Fullscreen"]

def set_fullscreen(value):
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["Fullscreen"] = value
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_showfps():
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["Showfps"]

def set_showfps(value):
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["Showfps"] = value
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_sprites(path_pattern: str, count: int, size: tuple):
    """Load and scale a sequence of sprites from a formatted file path."""
    return tuple(pygame.transform.scale(pygame.image.load(path_pattern.format(i + 1)), size)
                 for i in range(count))
