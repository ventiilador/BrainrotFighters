import json
import pygame

"""
In this module I create the functions that i usually need
"""

def position(x, y):
    # Returns a position in pixels based on a percentage of the screen resolution
    resolution = get_resolution()
    return ((resolution[0] * x) // 100, (resolution[1] * y) // 100)

def size(w, h):
    # Returns a size in pixels based on a percentage of the screen resolution
    resolution = get_resolution()
    return ((resolution[0] * w) // 100, (resolution[1] * h) // 100)

def position_x(x):
    # Returns the x position in pixels based on a percentage of the screen width
    resolution = get_resolution()
    return resolution[0] * x // 100

def position_y(y):
    # Returns the y position in pixels based on a percentage of the screen height
    resolution = get_resolution()
    return resolution[1] * y // 100

def size_x(w):
    # Returns the width in pixels based on a percentage of the screen width
    resolution = get_resolution()
    return resolution[0] * w // 100

def size_y(h):
    # Returns the height in pixels based on a percentage of the screen height
    resolution = get_resolution()
    return resolution[1] * h // 100

def get_songs_volume():
    # Retrieves the configured volume level for songs
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["SongsVolume"]

def get_sounds_volume():
    # Retrieves the configured volume level for sound effects
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["SoundsVolume"]

def set_songs_volume(volume):
    # Sets the volume level for songs and saves it in the config file
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["SongsVolume"] = volume
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def set_sounds_volume(volume):
    # Sets the volume level for sound effects and saves it in the config file
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["SoundsVolume"] = volume
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_resolution():
    # Retrieves the screen resolution from the config file
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["Resolution"]

def set_resolution(resolution:list):
    # Sets and saves the screen resolution in the config file
    with open("data.json", "r") as file:
        data = json.load(file)
        data["Config"]["Resolution"] = resolution
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_fps():
    # Retrieves the target frames per second from the config file
    with open("data.json") as file:
        data = json.load(file)
        return data["Config"]["Fps"]

def set_fps(fps):
    # Sets and saves the target FPS in the config file
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["Fps"] = fps
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_fullscreen():
    # Retrieves whether the game is set to run in fullscreen
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["Fullscreen"]

def set_fullscreen(value):
    # Sets and saves the fullscreen setting in the config file
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["Fullscreen"] = value
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def get_showfps():
    # Retrieves whether the FPS counter should be displayed
    with open("data.json", "r") as file:
        data = json.load(file)
        return data["Config"]["Showfps"]

def set_showfps(value):
    # Sets and saves the setting to show or hide the FPS counter
    with open("data.json", "r") as file:
        data = json.load(file)
    data["Config"]["Showfps"] = value
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_sprites(path_pattern: str, count: int, size: tuple):
    """Load and scale a sequence of sprites from a formatted file path."""
    return tuple(pygame.transform.scale(pygame.image.load(path_pattern.format(i + 1)), size)
                 for i in range(count))

def render_text_with_border(text, font, text_color, border_color):
    # Renders text with a simple border effect by drawing the text multiple times
    text_surface = font.render(text, True, border_color)
    
    border_surface = pygame.Surface((text_surface.get_width() + 2, text_surface.get_height() + 2), pygame.SRCALPHA)
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        border_surface.blit(font.render(text, True, border_color), (dx + 1, dy + 1))
    
    border_surface.blit(font.render(text, True, text_color), (1, 1))
    
    return border_surface

def grayscale_image(surface):
    # Converts a surface to grayscale while maintaining alpha transparency
    gray_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            r, g, b, a = surface.get_at((x, y))
            gray = int((r + g + b) / 3)
            gray_surface.set_at((x, y), (gray, gray, gray, a))
    
    return gray_surface
