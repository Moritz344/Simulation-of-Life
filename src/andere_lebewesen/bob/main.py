import pygame
import random
import noise
import math
import sys
import threading
import tkinter
from ui import start_ui

# Diese Simulation könnte beispielsweise eine Schlange simulieren oder eine Spielende Katze.


width = 1920
height = 1080
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Bob")
clock = pygame.time.Clock()

cell_size = 25
num_cells = 1

# TODO: ui

def start_ui_thread() -> None:
        start_ui()
    # Thread für Tkinter starten
ui_thread = threading.Thread(target=start_ui_thread)
ui_thread.start()

class Nahrung(object):
    def __init__(self):
        pass

def help_function():
    for i,v in enumerate(bob_family):
        print(i+1,v.position)


class Bob(object):
    def __init__(self,position,size,color,speed=cell_size * 2):
        self.position = pygame.Vector2(position)
        self.size: int = size
        self.speed: int = speed
        self.time = 0
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))


        
        self.erb_color = color

        self.rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)



        
    def noise_bewegung(self):
        self.angle = (noise.pnoise1(self.time, repeat=1024) + 1)  * math.pi 
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed 
        
        self.position.x += self.dx * 0.5
        self.position.y += self.dy * 0.5
        if random.random() > 0.78:
            self.time += 0.1
        else:
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
        self.rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size )
        #points = [(self.position.x + self.size, self.position.y + self.size), (self.size , self.size), (self.position.x + self.size, self.position.y + self.size)]
        pygame.draw.circle(screen, self.erb_color, self.position,self.size)

    def update(self) -> None:
        self.draw_bob()
        self.noise_bewegung()
        self.kollision_prüfen()
        #self.life_span()
        #self.move()

        print(num_cells)

bob = Bob((300,400),10,random.choice(["white","black"]),15)
bob_family = [
        Bob((300,400),cell_size,"white",cell_size)
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
    screen.fill(( 19, 21, 21 ))
    #help_function()
    spawn_cells(bob_family)

    clock.tick(60)
    pygame.display.update()
    
pygame.quit()
ui_thread.join()
