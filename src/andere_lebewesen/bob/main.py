import pygame
import random
import noise
import math
import sys


width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Bob")
clock = pygame.time.Clock()

cell_size = 20
num_cells = 5

# TODO: orange,blau,weiß -> jeweilige Eigenschaften
# IDEE: Wenn cellen kollidieren nicht mehr bewegen
# TODO: vermehrung
# TODO: Narhungs klasse

class Nahrung(object):
    def __init__(self):
        pass


class Bob(object):
    def __init__(self,position,size,box_x,box_y,lifespan,alive,speed=cell_size * 2):
        self.position = pygame.Vector2(position)
        self.size: int = size
        self.speed: int = speed
        self.time = 0
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.direction = None

        self.alive: bool = alive
        self.lifespan: float = lifespan
        self.lifespan_timer = pygame.time.get_ticks()


        self.box_x = box_x
        self.box_y = box_y

    def move(self):
        box_width,box_height = 100,100
        #pygame.draw.rect(screen,"white",(self.box_x ,self.box_y ,box_width,box_height),1)

        self.direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

        if self.direction == "LEFT" and random.random() > 0.86:
           self.position.x -= self.speed 
        elif self.direction == "RIGHT" and random.random() > 0.86:
           self.position.x += self.speed
        elif self.direction == "UP" and random.random() > 0.86:
           self.position.y -= self.speed
        elif self.direction == "DOWN" and random.random() > 0.86:
           self.position.y += self.speed


        if self.position.x > self.box_x + 60:
            self.position.x = self.box_x + 60
        elif self.position.x < self.box_x :
            self.position.x = self.box_x 

        if self.position.y > self.box_y + 60:
            self.position.y = self.box_y  + 60
        elif self.position.y < self.box_y :
            self.position.y = self.box_y 
        
        

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
        erb= pygame.draw.rect(screen,"white",(self.position.x,self.position.y,self.size,self.size))
        pygame.draw.rect(screen,"orange",(self.position.x + self.size,self.position.y + self.size,self.size,self.size))
        pygame.draw.rect(screen,"blue",(self.position.x + self.size * 2,self.position.y + self.size * 2,self.size,self.size))

    def update(self) -> None:
        self.draw_bob()
        #self.noise_bewegung()
        self.kollision_prüfen()
        self.move()

bob = Bob((300,400),cell_size,3,random.randint(100,500),random.randint(100,500),True) 
bob_family = [
    Bob((random.randint(100, 700), random.randint(100, 500)), cell_size,random.randint(100, 600), random.randint(100, 400),random.uniform(1000,2000),True)
    for _ in range(num_cells)
]

def spawn_cells(group: list):
    for life in group:
        life.update()


run: bool = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run: bool = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run: bool = False

    screen.fill("black")
    
    spawn_cells(bob_family)

    clock.tick(60)
    pygame.display.update()
    
pygame.quit()
