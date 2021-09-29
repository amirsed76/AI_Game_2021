import base64
import sys
import io

import pygame
import json
import time
import tkinter as tk
from tkinter import filedialog
import numpy as np

TILE_COLOR = (200, 200, 200)
BLOCK_SIZE = 50
PADDING = 5 * BLOCK_SIZE
BACKGROUND_COLOR = (191, 215, 253)
BOARDER_COLOR = (0, 0, 0)
BOX_COLOR = (100, 100, 100)
TELEPORT_COLOR = (0, 0, 0)
WINDOWS_PADDING = 20 * BLOCK_SIZE

ICON = "download.jpeg"
GEM = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAADKHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHja7ZddcuQqDIXfWcVdApIQEsvB/FTdHczy78F2O+lOT25SydS8xJQNlkGSzyfTSRi//p3hHxxUCoek5rnkHHGkkgpXDDweR9mvFNN+PW/ibXBnD9cDhknQy3Fr9ZxfYdeXBbcYtN3bg59P2E9HdDneD1mR17i/ThJ2PuyUTkdlHINc3F6nup2O2jlxT+U805XW0a37cGcwqNQVgYR5CEnEleXMQI6z4iy4kpQ1D30VEQroWG6ZQJC717sEjK8FuhP5NgqP6l+jB/G5nnZ50DKfGmHw9AHpg12uMPw6sFwZ8f2DQjdXb0Wes/uc43i7mjIUzWdF7WLTzQ0mbpBc9mUZzXAqxra3guaxxgbkPba4oTUqxKAyAyXqVGnS2PtGDSkmHmzomRuwLJuLceEGYiRpNZpsoNfFAavxCECXhK9caI9b9niNHJE7YSoTnBGW/LaF9x5+poU525KIol9aIS9edY00Frl1xSwAoXly013gWzvxx1f1g1IFQd1ldrxgjdvhYlN6qS3ZOQvmKfrjE6Jg/XQAiRBbkQwJCMRMopQpGrMRQUcHoIrM8SHwBgKkyh1JchLJHIydV2ysMdrnsnLmZcbeBBAqWQxs8H0BVkqK+rHkqKGqoklVs5p60KI1S05Zc86W1yZXTSyZWjYzt2LVxZOrZzd3L14LF8EeqCUXK15KqZVDRaAKXxXzKywbb7KlTbe82eZb2WpD+bTUtOVmzVtptXOXjm2i527de+l1UBjYKUYaOvKw4aOMOlFrU2aaOvO06bPMelE7qb5pn6BGJzXeSa15dlGDNZjdXNDaTnQxAzFOBOK2CKCgeTGLTinxIreYxcL4KJSRpC42odMiBoRpEOuki90LuQ9xC+of4sb/Ry4sdN9BLgDdW25PqPX1O9d2YsdXuDSNgq8Pz4fXwF7Xj1r9av/j6MfRn3c0t1W0H/IVrjX+tbzC8/ifdxu+tvylD5/K5h3N/oJG72SzZoevV9C9Ru9n9SSbx5zD99T1c0cfiP+sjvh7VPpx9OPozzia+MsD/wGH/wBAKrNQlaZ9kwAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfW6UqFZF2EHHIUJ0siIroplUoQoVQK7TqYHLpFzRpSFJcHAXXgoMfi1UHF2ddHVwFQfADxMnRSdFFSvxfUmgR48FxP97de9y9A/z1MlPNjjFA1SwjlYgLmeyqEHxFN8LoBzAjMVOfE8UkPMfXPXx8vYvxLO9zf45eJWcywCcQzzLdsIg3iKc2LZ3zPnGEFSWF+Jx41KALEj9yXXb5jXPBYT/PjBjp1DxxhFgotLHcxqxoqMSTxFFF1Sjfn3FZ4bzFWS1XWfOe/IWhnLayzHWaQ0hgEUsQIUBGFSWUYSFGq0aKiRTtxz38g45fJJdMrhIYORZQgQrJ8YP/we9uzfzEuJsUigOdL7b9MQwEd4FGzba/j227cQIEnoErreWv1IHpT9JrLS16BPRtAxfXLU3eAy53gIEnXTIkRwrQ9OfzwPsZfVMWCN8CPWtub819nD4AaeoqeQMcHAIjBcpe93h3V3tv/55p9vcDaOtyo1c11ZYAAAAJUExURQAAAAAAAP///4Pdz9IAAAABdFJOUwBA5thmAAAAAWJLR0QAiAUdSAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+QJExEBGBkuCWQAAAAgSURBVAjXY2DACbRWAImpYSBiFZBQBXE5FwAJpgbcmgDMbgT176eVGgAAAABJRU5ErkJggg=="


def get_game_log_json():
    root = tk.Tk()
    root.withdraw()
    file_name = filedialog.askopenfilename()
    with open(file_name) as file:
        content = json.load(file)
    return content


def draw_wall(pygame, screen, x, y):
    image = pygame.image.load("assets/wall.jpg")
    image = pygame.transform.scale(image, (blockSize, blockSize))
    X = PADDING + x * blockSize
    Y = PADDING + y * blockSize
    screen.blit(image, (X, Y))


def draw_player(pygame, screen, x, y, character):
    # image = pygame.image.load(r'download.jpeg')
    image = pygame.image.load(io.BytesIO(base64.b64decode(GEM)))
    transColor = (0, 0, 255)
    image.set_colorkey(transColor)

    image = pygame.transform.scale(image, (blockSize, blockSize))
    X = PADDING + x * blockSize
    Y = PADDING + y * blockSize
    screen.blit(image, (X, Y))
    # screen.blit(image, (X, Y),)


def draw_teleport(pygame, screen, x, y):
    X = PADDING + x * blockSize + blockSize // 2
    Y = PADDING + y * blockSize + blockSize // 2
    pygame.draw.circle(screen, TELEPORT_COLOR, (X, Y), (6 * blockSize) // 13)


def draw_gem(pygame, screen, x, y):
    pass


def draw_characters(pygame, screen, x, y, characters):
    if "T" in characters:
        draw_teleport(pygame, screen, x, y)
    if "A" in characters:
        draw_player(pygame, screen, x, y, "A")
    if "W" in characters:
        draw_wall(pygame,screen,x,y)
    if "1" in characters:
        pass
        # draw_gem(pygame)


if __name__ == '__main__':
    json_content = get_game_log_json()
    height, width = np.array(json_content[0]["map"]).shape
    blockSize = BLOCK_SIZE  # Set the size of the grid block
    HEIGHT, WIDTH = height * blockSize, width * blockSize
    pygame.init()

    screen = pygame.display.set_mode((WIDTH + 2 * PADDING, HEIGHT + 2 * PADDING))
    grid_rect = pygame.Rect(PADDING, PADDING, WIDTH, HEIGHT)

    i = 0
    while True:
        screen.fill(BACKGROUND_COLOR)
        screen.fill(color=TILE_COLOR, rect=grid_rect)

        current_map = json_content[i]["map"]
        for x in range(width):
            for y in range(height):
                X = x * blockSize + PADDING
                Y = y * blockSize + PADDING
                center = (X + blockSize + blockSize // 2, Y + blockSize + blockSize // 2)

                tile = current_map[y][x]
                rect = pygame.Rect(X, Y, blockSize, blockSize)
                pygame.draw.rect(screen, BOARDER_COLOR, rect, 1)
                draw_characters(pygame, screen, x, y, tile)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        time.sleep(1)
        if i < len(json_content) - 1:
            i += 1
