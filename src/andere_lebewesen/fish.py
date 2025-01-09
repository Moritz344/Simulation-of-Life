import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

num = 15

# Idea: temperaturen bestimmen wie hoch fische schwimmen
# move: bewegung langsamer 

class Fish(object):
    def __init__(self,position,speed,direction,):
        self.position = list(position)
        self.speed = speed
        self.size = 10
        self.direction = direction

        self.dx = 1
        self.dy = 1

        self.move_chance = 0.69

        self.rect = pygame.Rect(self.position[0],self.position[1],20,20)

        self.next_move_timer = pygame.time.get_ticks()
        self.duration = 1000

    def collision_detection(self):
        for life in fish_group:
            if life != self and self.rect.colliderect(life.rect):
                if self.direction == "RIGHT":
                    self.position[0] += self.speed * self.dx
                elif self.direction == "LEFT":
                    self.position[0] -= self.speed * self.dx

                if self.direction == "UP":
                    self.position[1] -= self.speed * self.dy
                elif self.direction == "DOWN":
                    self.position[1] += self.speed * self.dy

        if self.position[0] > width - self.size:
            self.dx = (self.dx * -1)
        elif self.position[0] <= 0 + self.size:
            self.dx = (self.dx * -1)

        if self.position[1] >= height - self.size:
            self.dy = (self.dy * -1)
        elif self.position[1] <= 0 + self.size:
            self.dy = (self.dy * -1)

                

    def move(self):
        elapsedTime = pygame.time.get_ticks() - self.next_move_timer

        if self.direction == "RIGHT" and random.random() > self.move_chance:
                self.position[0] += self.speed * self.dx
        elif self.direction == "LEFT" and random.random() > self.move_chance:
                self.position[0] -= self.speed * self.dx

        if self.direction == "UP" and random.random() > self.move_chance:
                self.position[1] -= self.speed * self.dy
        elif self.direction == "DOWN" and random.random() > self.move_chance:
                self.position[1] += self.speed * self.dy
    

        if elapsedTime >= self.duration:
            self.next_move_timer = pygame.time.get_ticks()
            self.direction = random.choice(["RIGHT","LEFT","UP","DOWN"])
            if self.direction == "RIGHT" and random.random() > self.move_chance:
                self.position[0] += self.speed * self.dx
            elif self.direction == "LEFT" and random.random() > self.move_chance:
                self.position[0] -= self.speed * self.dx

            if self.direction == "UP" and random.random() > self.move_chance:
                self.position[1] -= self.speed * self.dy
            elif self.direction == "DOWN" and random.random() > self.move_chance:
                self.position[1] += self.speed * self.dy
    

    def update(self):
        self.move()
        self.collision_detection()
        self.fish = pygame.draw.rect(screen, "blue", (self.position[0],self.position[1],self.size,self.size))
        self.rect = pygame.Rect(self.position[0],self.position[1],40,40)

fish_group = [Fish((random.randint(0,width),random.randint(0,height)),2,random.choice(["RIGHT","LEFT","UP","DOWN"])) for _ in range(num)]

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill("black")
    for life in fish_group:
        life.update()
    clock.tick(60)
    pygame.display.update()

