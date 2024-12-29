import pygame
import random

# IDEA: Kollision mit einzelnen partikeln hinzufügen

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("particle life")

# global var
num = 200
colors = ["red","white"]

class Life(object):
    def __init__(self,position,speed,velocity,color,id):
        self.position = list(position)
        self.speed = speed
        self.velocity = velocity
        self.color = color
        self.size = 1
        self.id = id
        self.id = round(self.id,2)
        self.direction = "RIGHT"

        self.move_right_chance = 0.67
        self.move_left_chance = 0.67
        self.move_down_chance = 0.67
        self.move_up_chance = 0.67


        self.rect = pygame.Rect(self.position[0] - 10,self.position[1] - 10,self.size * 5,self.size * 5)


    def move(self):
        self.direction = random.choice(["DOWN","RIGHT","UP","LEFT"])
        
        if self.direction == "RIGHT" and random.random() > self.move_right_chance:
            self.position[0] += self.speed 
        elif self.direction == "DOWN" and random.random() > self.move_down_chance:
            self.position[1] += self.speed 
        elif self.direction == "UP" and random.random() > self.move_up_chance:
            self.position[1] -= self.speed
        elif self.direction == "LEFT" and random.random() > self.move_left_chance:
            self.position[0] -= self.speed
        
        if self.position[0] > width - 10:
            self.position[0] = 0 + 10
        elif self.position[0] < 0 + 10:
            self.position[0] = 0 + 10

        if self.position[1] > height - 10:
            self.position[1] = 0 + 10
        elif self.position[1] < 0 + 10:
            self.position[1] = 0 + 10

    def move_group(self,group,direction):
        for life in group:
            if group == white_color_lifes:
                if direction == "RIGHT" and random.random() < self.move_right_chance:
                    self.position[0] += self.speed * 0.05
                elif direction == "LEFT" and random.random() < self.move_left_chance:
                    self.position[0] -= self.speed * 0.05
                elif direction == "UP" and random.random() < self.move_up_chance:
                    self.position[1] -= self.speed * 0.05
                elif direction == "DOWN" and random.random() < self.move_down_chance:
                    self.position[1] += self.speed * 0.05
                else:
                    group.remove(life)

        for life in group:
            if group == red_color_lifes:
                if direction == "RIGHT" and random.random() < self.move_right_chance:
                    self.position[0] += self.speed * 0.1
                elif direction == "LEFT" and random.random() < self.move_left_chance:
                    self.position[0] -= self.speed * 0.1
                elif direction == "UP" and random.random() < self.move_up_chance:
                    self.position[1] -= self.speed * 0.1
                elif direction == "DOWN" and random.random() < self.move_down_chance:
                    self.position[1] += self.speed * 0.1
                else:
                    group.remove(life)

    def check_collision(self):
        global white_color_lifes,red_color_lifes

        new_life = Life((random.randint(0,width),random.randint(0,height)),3,random.uniform(1,2),random.choice(colors),random.uniform(1,100))
        red_color_lifes = [red for red in lifes if red.color == "red"]
        white_color_lifes = [white for white in lifes if white.color == "white"]
        groups = {0: [white_color_lifes]}

        dead_lifes = []

        for pixel in white_color_lifes:
                if self.eye.colliderect(pixel.rect) :
                    pixel.move_group(white_color_lifes,random.choice(["RIGHT","UP","LEFT","DOWN"]))
                    
        for pixel in red_color_lifes:
                if pixel != self and self.eye.colliderect(pixel.rect):
                    pixel.move_group(red_color_lifes,random.choice(["RIGHT","UP","LEFT","DOWN"]))
                else:
                    dead_lifes.append(pixel)


        for all in lifes:
            if all.position[0] > width - self.size:
                all.position[0] = width - self.size
            elif all.position[0] < 0 + self.size:
                all.position[0] = self.size

            if all.position[1] > height - self.size:
                all.position[1] = height - self.size
            elif all.position[1] < 0 + self.size:
                all.position[1] = self.size

        # remove all white ones
        #for life in white_color_lifes:
            #lifes.remove(life)

    def update(self):
        #self.move()
        self.life = pygame.draw.circle(screen,self.color,self.position,self.size,1)
        #self.eye = pygame.draw.rect(screen,self.color,(self.position[0] - 20,self.position[1] - 20,50,50),1)
        self.eye = pygame.Rect(self.position[0] - 100,self.position[1] - 50,200,100)
        self.rect = pygame.Rect(self.position[0] - 10,self.position[1] - 10,self.size * 5,self.size * 5)
        
        #pygame.draw.rect(screen,"red",(self.position[0] - 100,self.position[1] - 50,200,200),1)
        #pygame.draw.rect(screen,"blue",(self.position[0] - 10,self.position[1] - 10,self.size * 5,self.size * 5),1)


lifes = [Life((random.randint(0,width),random.randint(0,height)),3,random.uniform(1,2),random.choice(colors),random.uniform(1,100)) for _ in range(num)]


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
        life.check_collision()

    clock.tick(60)
    pygame.display.update()

pygame.quit()
