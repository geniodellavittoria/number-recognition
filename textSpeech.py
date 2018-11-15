import pygame
from gtts import gTTS
from time import sleep

tts = gTTS(text="3", lang='de')
tts.save("txt.mp3")
pygame.mixer.init()
pygame.mixer.music.load("txt.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue