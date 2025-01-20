import pygame
import random
import noise
import math
import sys
import sys


width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Bob")
clock = pygame.time.Clock()

class Bob(object):
    def __init__(self,position,size,speed):
        self.position = pygame.Vector2(position)
        self.size: int = size
        self.speed: int = speed
        self.time = 0

        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))

    def noise_bewegung(self):

        self.angle = (noise.pnoise1(self.time, repeat=1024) + 1)  * math.pi 
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed 

        self.position.x += self.dx 
        self.position.y += self.dy 
        self.time += 0.01

        print(self.position.x,self.position.y)

    def kollision_prüfen(self):
        if self.position.x >= width - self.size:
            self.position.x = self.size
        elif self.position.x <= 0 + self.size:
            self.position.x = width - self.size

        if self.position.y >= height - self.size:
            self.position.y = self.size
        elif self.position.y <= 0 + self.size:
            self.position.y = height - self.size


    def draw_bob(self) -> None:
        # einfacher bob zum testen
        simple_bob = pygame.draw.rect(screen,"white",(self.position.x,self.position.y,self.size,self.size))
    def update(self) -> None:
        self.draw_bob()
        self.noise_bewegung()
        self.kollision_prüfen()


bob = Bob((400,500),10,3)

run: bool = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run: bool = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run: bool = False

    screen.fill("black")
    
    bob.update()


    clock.tick(60)
    pygame.display.update()
    
pygame.quit()
