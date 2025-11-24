import pygame 
import random 
from questions import *

def bruitage_collision():
    bruit1=pygame.mixer.Sound(r"son/Fouet1.wav")
    bruit2=pygame.mixer.Sound(r"son/Fouet2.wav")

    nombre=random.choice([1,2])
    if nombre==1 : 
        bruit1.play()
    else : 
        bruit2.play()

def musique_fond(selected_questions):
    if selected_questions==QUESTIONS_FACILES:
        fastoche=pygame.mixer.Sound(r"son/fastoche.wav")
        fastoche.play()
    
    elif selected_questions==QUESTIONS_MOYENNES:
        mid=pygame.mixer.Sound(r"son/mid.wav")
        mid.play()

    else : 
        hardcore=pygame.mixer.Sound(r"son/hardcore.wav")
        hardcore.play()
