#####音效区#####
"""
以后这段代码可以使用字典进行重构,参考BV1Kz4y1m7PZ-P5-末尾部分
"""
import os
import pygame
pygame.init()
# start=pygame.mixer.Sound("assets/audio/start.wav")
# die=pygame.mixer.Sound("assets/audio/die.wav")
# hit=pygame.mixer.Sound("assets/audio/hit.wav")
# score=pygame.mixer.Sound("assets/audio/score.wav")
# flap=pygame.mixer.Sound("assets/audio/flap.wav")
AUDIOS={}
for audio in os.listdir("assets/audio"):
    name,extension=os.path.splitext(audio)
    path=os.path.join("assets/audio",audio)
    AUDIOS[name]=pygame.mixer.Sound(path)