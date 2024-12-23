import pygame
import random

width = 1920
height = 1080
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("SPRINGER")

rows: int = 100
cols: int = 100
cell_size: int = 10
num_flieger: int = 100
switch_timer = pygame.time.get_ticks()
switch_dur = 100000
def spawn_grid():
    for breite in range(rows):
        for höhe in range(cols):
            x = breite * cell_size
            y = höhe * cell_size

            #pygame.draw.rect(screen,"white",(x,y,cell_size,cell_size),1)


class Flieger(object):
    def __init__(self,x,y,moving_chance,erb,speed=cell_size):
        self.flieger_x = x
        self.flieger_y = y
        self.flieger_speed = speed
        self.erb = erb

        self.right_value = 10
        self.left_value = 20


        self.state = ""
        self.direction = "RIGHT"
        self.move: float = moving_chance
        self.last_pos = (self.flieger_x,self.flieger_y)

        self.timer = pygame.time.get_ticks()

        self.fliegerRect = pygame.Rect(self.flieger_x,self.flieger_y,cell_size,cell_size)

    def debug_info(self):
            for i,_ in enumerate(flieger):
               print(f"{i+1} Typ: Flieger: Direction: {self.direction} STATE: {self.state}")

    def draw_left(self):
            self.fliegerBody = pygame.draw.rect(screen,"yellow",(self.flieger_x - cell_size,self.flieger_y - cell_size,cell_size,cell_size))
            self.fliegerLeg = pygame.draw.rect(screen,"blue",(self.flieger_x - cell_size - cell_size,self.flieger_y - cell_size - cell_size,cell_size,cell_size))
            self.flieger = pygame.draw.rect(screen,self.erb,(self.flieger_x,self.flieger_y,cell_size,cell_size))
    def draw_right(self):
            self.fliegerBody = pygame.draw.rect(screen,"yellow",(self.flieger_x + cell_size,self.flieger_y - cell_size,cell_size,cell_size))
            self.fliegerLeg = pygame.draw.rect(screen,"blue",(self.flieger_x + cell_size + cell_size,self.flieger_y - cell_size - cell_size,cell_size,cell_size))
            self.flieger = pygame.draw.rect(screen,self.erb,(self.flieger_x,self.flieger_y,cell_size,cell_size))

    def update(self):
        elapsedTime = pygame.time.get_ticks() - self.timer
        if elapsedTime >= 100 :
            self.direction = random.choice(["RIGHT","LEFT","UP","DOWN","NORMAL"])
            self.timer = pygame.time.get_ticks()
            



        if self.direction == "LEFT" and random.random() > self.move:
            self.flieger_x -= self.flieger_speed
            self.draw_left()
        elif self.direction == "RIGHT" and random.random() > self.move:
            self.flieger_x += self.flieger_speed
            self.draw_right()
        elif self.direction == "UP" and random.random() > self.move:
            self.flieger_y -= self.flieger_speed
            self.draw_right()
        elif self.direction == "DOWN" and random.random() > self.move:
            self.flieger_y += self.flieger_speed
            self.draw_right()
        else:
            pygame.draw.rect(screen,self.erb,(self.flieger_x,self.flieger_y,cell_size,cell_size))
        self.fliegerRect.topleft = (self.flieger_x, self.flieger_y)
        

        if self.flieger_y < 1:
            self.flieger_y = height
        elif self.flieger_y > height:
            self.flieger_y = 1

        if self.flieger_x > width:
            self.flieger_x = 1
        elif self.flieger_x < 1:
            self.flieger_x = width

        if self.fliegerRect.topleft != self.last_pos:
            pass
            #print("Bewegung erkannt")
        else:
            self.direction = "NORMAL"

        self.last_pos = self.fliegerRect.topleft

flieger = [Flieger(random.randint(0,(width  // cell_size ) - 1 ) * cell_size,random.randint(0,(height // cell_size) -1 ) * cell_size, random.uniform(0,1), random.choice(["red","green","blue","yellow"])) for _ in range(num_flieger)]

def movingChanceAusgabe():
    for i,v in enumerate(flieger):
        print(i+1,v.move)
movingChanceAusgabe()


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
        #fl.debug_info()

    clock.tick(60)
    pygame.display.update()
