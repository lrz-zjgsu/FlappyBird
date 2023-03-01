#####图像区#####
"""
以后重构这段代码,使名字更规范
"""
import os
import pygame
pygame.init()
IMAGES={}
for image in os.listdir("assets/sprites"):
    name,extension=os.path.splitext(image)
    path=os.path.join("assets/sprites",image)
    IMAGES[name]=pygame.image.load(path)
bgpic=pygame.image.load("assets/sprites/day.png")
guide=pygame.image.load("assets/sprites/guide.png")
floor=pygame.image.load("assets/sprites/floor.png")
pipe=pygame.image.load("assets/sprites/green-pipe.png")
gameover=pygame.image.load("assets/sprites/gameover.png")

W,H=288,512
FPS=30
SCREEN=pygame.display.set_mode((W,H))
pygame.display.set_caption("FlappyBird")
CLOCK=pygame.time.Clock()
FLOOR_Y=H-floor.get_height()