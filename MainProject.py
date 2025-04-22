import pygame
from pygame.locals import*
import os
import sys
import math
import random

pygame.init()

pygame.mixer.music.load("music/music.mp3")
deadmusic = pygame.mixer.Sound("music/dead.wav")


W = 1480
H = 800
win = pygame.display.set_mode((W,H))
pygame.display.set_caption("Drakoncik")

bg = pygame.image.load(os.path.join('photo','background.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):
    run = pygame.image.load(os.path.join('photo','wait.png'))
    dead = pygame.image.load(os.path.join('photo','dead.png'))
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.flying = False
        self.falling = False

    def draw(self,win):
        if self.falling:
            win.blit(self.dead,(self.x,self.y))
            if self.y <= H:
                self.y += 3
        elif self.flying:
            if self.y > 0:
                self.y -= 2
                
            win.blit(self.run, (self.x,self.y))
            
    
        else:
            win.blit(self.run, (self.x,self.y))
        self.hitbox = (self.x+10,self.y+20,self.width-20,self.height-30)#настраиваем хитбокс
        pygame.draw.rect(win,(255,0,0), self.hitbox,2)# отображаем хитбокс



class Vbeams(object):
    img = pygame.image.load(os.path.join('photo','vertical2.png'))
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)

    def draw(self,win):
        self.hitbox = (self.x+25,self.y+20,self.width-60,self.height-40)#настраиваем хитбокс для вертикальных лучей

        win.blit(self.img,(self.x,self.y))

        pygame.draw.rect(win,(255,0,0), self.hitbox,2)#отоброжаем хитбокс вертикальных изображений


    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] <self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(deadmusic)
                return True
            return False


class Hbeams(Vbeams):
    img = pygame.image.load(os.path.join('photo','horizontal1.png'))
    def draw(self,win):
        self.hitbox = (self.x+25,self.y+30,self.width-50,self.height-70) #настраиваем хитбокс для горизонтальных лучей
        win.blit(self.img,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)#отображаем хитбокс
"""
class beams(Vbeams):
    img = pygame.image.load(os.path.join('photo','left-right2.png'))
    def draw(self,win):
        self.hitbox = (self.x,self.y,self.width,self.height) #настраиваем хитбокс для горизонтальных лучей
        win.blit(self.img,(self.x,self.y))
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)#отображаем хитбокс
пока не работает((
"""
        
def redrawWindow():
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))
    dragon.draw(win)
    for x in objects:
        x.draw(win)

    font = pygame.font.SysFont('comicsans',30)
    text = font.render('Score ' + str(score),1,(255,255,255))
    win.blit(text,(W-150,10))
    pygame.display.update()


def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt','w')
        file.write(str(score))
        file.close

        return score
    
    return last


def endScreen():
    global pause,objects,speed,score
    pause = 0
    objects = []
    speed = 60
    
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        win.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        previousScore = largeFont.render('Previous Score: ' + str(updateFile()),1,(255,255,255))
        win.blit(previousScore,(W/2 - previousScore.get_width()/2,100))
        newScore = largeFont.render('Score: ' + str(score),1,(255,255,255))
        win.blit(newScore,(W/2 - newScore.get_width()/2,220))
        pygame.display.update()
        
        
    score = 0
    dragon.falling = False       

dragon = player(200,H/2,118,118)
pygame.time.set_timer(USEREVENT+1,500)
pygame.time.set_timer(USEREVENT+2,random.randrange(1000,1500))
speed = 60
run = True

pygame.mixer.music.play(1)
pygame.mixer.music.set_volume(0.05)

pause = 0
fallSpeed = 0


objects = []


while run:
    score = speed - 60
    
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()


    for objectt in objects:
        if objectt.collide(dragon.hitbox):
            dragon.falling = True

            if pause == 0:
                if speed < 300 :
                    fallSpeed = speed
                    pause = 1


        objectt.x -= 2
        if objectt.x < objectt.width * -1:
            objects.pop(objects.index(objectt))


    bgX -= 2
    bgX2 -= 2
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:# каждый пол секунды ускоряем игру
                speed += 1
        if event.type == USEREVENT+2:# генерируем случайные препятствия
            r = random.randrange(0,2)
            if r == 0:
                Hi = random.randint(272,H) # случайные числа для Y(координат) препядствий
                objects.append(Vbeams(W+10,Hi-272,100,272))
                
            else :
                Hi = random.randint(105,H) # случайные числа для Y(координат) препядствий
                objects.append(Hbeams(W+10,Hi-105,186,105))
            """else:
                Hi = random.randint(105,H) # случайные числа для Y(координат) препядствий
                objects.append(beams(W+10,Hi-219,218,219))
                ждем дальнейших действий"""               
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            dragon.flying = True
    if not (keys[pygame.K_SPACE] or keys[pygame.K_UP]):
            dragon.flying = False
            if dragon.y >= H-120:
                dragon.y = H-120
            else:
                dragon.y += 2
                
    
    clock.tick(speed)
    redrawWindow()
