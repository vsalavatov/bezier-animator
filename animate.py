import pygame
import sys
from bezier import *
import time
import os

if len(sys.argv) != 2:
    print('Usage: ./script <bezier curve desc file>')
    exit(0)

frame_folder = './frames/'
os.makedirs(frame_folder, exist_ok=True)

curves = BezierCurves(sys.argv[1])

pygame.init()

skip_animation = False

WIDTH = 1080
HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT = (255, 255, 255, 6)

animation_time = 0.5
fps = 240
spf = 1.0 / fps

display = pygame.display.set_mode((WIDTH, HEIGHT))

display.fill(WHITE)
pygame.display.update()

surface = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)
framebuffer = pygame.Surface((WIDTH, HEIGHT))

total_frames = int(animation_time * fps)

def gen_frame_filename(index):
    return frame_folder + str(index) + '.png'

imgs = []
for _ in range(2):
    imgs = []
    for index in range(total_frames):
        t_start = time.time()
        # display.fill(WHITE)
        surface.fill(TRANSPARENT)

        t = index / total_frames

        curves.draw(surface, t, True, True, True)

        display.blit(surface, (0, 0))
        if not skip_animation: pygame.display.update()
        filename = gen_frame_filename(index)
        imgs.append(filename)
        pygame.image.save(display, filename)

        t_end = time.time()
        t_sleep = spf - (t_end - t_start)
        if not skip_animation and t_sleep > 0:
            time.sleep(t_sleep)

pygame.display.update()
print('making gif...')

from PIL import Image

frames = []
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

frames[0].save('animation.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=int(animation_time * 1000 // len(frames)), loop=0,
               fps=fps)