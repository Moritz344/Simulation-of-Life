import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("3")

rows: int = 50
cols: int = 50
cell_size: int = 40
num_flieger: int = 1

def spawn_grid():
    for breite in range(rows):
        for höhe in range(cols):
            x = breite * cell_size
            y = höhe * cell_size

            #pygame.draw.rect(screen,"white",(x,y,cell_size,cell_size),1)

class Flieger(object):
    def __init__(self,x,y,speed=cell_size):
        self.flieger_x = x
        self.flieger_y = y
        self.flieger_speed = speed


        self.direction = "RIGHT"
        self.move: float = 0.87

        self.fliegerRect = pygame.Rect(self.flieger_x,self.flieger_y,cell_size,cell_size)

    def debug_info(self):
        for i,_ in enumerate(flieger):
            print(f"{i+1} Typ: Flieger: Direction: {self.direction}")

    def update(self):
        self.direction = random.choice(["LEFT","UP","RIGHT","DOWN"])
        
        if self.direction == "LEFT" and random.random() > self.move:
            self.flieger_x -= self.flieger_speed
        elif self.direction == "RIGHT" and random.random() > self.move:
            self.flieger_x += self.flieger_speed
        elif self.direction == "UP" and random.random() > self.move:
            self.flieger_y -= self.flieger_speed
        elif self.direction == "DOWN" and random.random() > self.move:
            self.flieger_y += self.flieger_speed

        self.flieger = pygame.draw.rect(screen,"dark green",(self.flieger_x,self.flieger_y,cell_size,cell_size))
        self.fliegerBody = pygame.draw.rect(screen,"yellow",(self.flieger_x - cell_size,self.flieger_y - cell_size,cell_size,cell_size))
        self.fliegerLeg = pygame.draw.rect(screen,"blue",(self.flieger_x - cell_size - cell_size,self.flieger_y - cell_size - cell_size,cell_size,cell_size))
        self.fliegerRect = pygame.Rect(self.flieger_x,self.flieger_y,cell_size,cell_size)

        if self.flieger_y < 1:
            self.flieger_y = height
        elif self.flieger_y > height:
            self.flieger_y = 1

        if self.flieger_x > width:
            self.flieger_x = 1
        elif self.flieger_x < 1:
            self.flieger_x = width



flieger = [Flieger(random.randint(0,800),random.randint(0,600)) for _ in range(num_flieger)]
run: bool = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run: bool = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                run: bool = False

    screen.fill((30,32,25))
    spawn_grid()
    for fl in flieger:
        fl.update()
        fl.debug_info()

    clock.tick(60)
    pygame.display.update()
