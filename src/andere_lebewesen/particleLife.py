import pygame
import random


width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("particle life")

# global var
num = 100
colors = ["red","white","blue","yellow"]

class Life(object):
    def __init__(self,position,speed,velocity,color):
        self.position = list(position)
        self.speed = speed
        self.velocity = velocity
        self.color = color
        self.size = 5


    def move(self):
        self.direction = random.choice(["DOWN","RIGHT","UP","LEFT"])
        
        if self.direction == "RIGHT" and random.random() > 0.67:
            self.position[0] += self.speed 
        elif self.direction == "DOWN" and random.random() > 0.67:
            self.position[1] += self.speed 
        elif self.direction == "UP" and random.random() > 0.67:
            self.position[1] -= self.speed
        elif self.direction == "LEFT" and random.random() > 0.67:
            self.position[0] -= self.speed
        
        if self.position[0] > width - 10:
            self.position[0] = 0 + 10
        elif self.position[0] < 0 + 10:
            self.position[0] = 0 + 10

        if self.position[1] > height - 10:
            self.position[1] = 0 + 10
        elif self.position[1] < 0 + 10:
            self.position[1] = 0 + 10

    def update(self):
        self.move()
        pygame.draw.circle(screen,self.color,self.position,self.size,1)
        #pygame.draw.circle(screen,self.color,(self.position[0] - 7,self.position[1] - 7),self.size,1)
        #pygame.draw.circle(screen,self.color,(self.position[0] + 7,self.position[1] - 7),self.size,1)
        
        self.rect = pygame.Rect(self.position[0] - 10,self.position[1] - 10,self.size * 5,self.size * 5)
        # pygame.draw.rect(screen,"white",(self.position[0] - 10,self.position[1] - 10,self.size * 5,self.size * 5))


lifes = [Life((random.randint(0,width),random.randint(0,height)),3,random.uniform(1,2),random.choice(colors)) for _ in range(num)]


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill("black")

    for life in lifes:
        life.update()

    clock.tick(60)
    pygame.display.update()

pygame.quit()
