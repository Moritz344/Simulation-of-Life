import pygame
import random


width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("particle life")

# global var
num = 100
max_partikel = 200
colors = ["red","white"]
names = [
            "Bob",
            "Peter",
            "Harald",
            "BastiGHG"
        ]
pygame.font.init()

font = pygame.font.SysFont("opensans",20)


class Life(object):
    def __init__(self,position,speed,velocity,color,name):
        self.position = list(position)
        self.speed = speed
        self.velocity = velocity
        self.color = color
        self.size = 1
        self.name = name
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

    def show_name(self):
        for i,v in enumerate(lifes):
            name = font.render(f"{v.name}",False,"white")
            screen.blit(name,(v.position[0] - 10,v.position[1] - 20))


    def check_collision(self):
        global white_color_lifes,red_color_lifes

        red_color_lifes = [red for red in lifes if red.color == "red"]
        white_color_lifes = [white for white in lifes if white.color == "white"]

        for partikel in lifes:
            if partikel != self and self.eye.colliderect(partikel.rect):
                partikel.move()



        for all in lifes:
            if all.position[0] > width - self.size:
                all.position[0] = width - self.size
            elif all.position[0] < 0 + self.size:
                all.position[0] = self.size

            if all.position[1] > height - self.size:
                all.position[1] = height - self.size
            elif all.position[1] < 0 + self.size:
                all.position[1] = self.size


    def update(self):
        self.life = pygame.draw.circle(screen,self.color,self.position,self.size,1)
        #self.eye = pygame.draw.rect(screen,self.color,(self.position[0] - 20,self.position[1] - 20,50,50),1)
        self.eye = pygame.Rect(self.position[0] - 10,self.position[1] - 10,50,50)
        self.rect = pygame.Rect(self.position[0] - 20,self.position[1] - 20,100,100)

        
        

lifes = [Life((random.randint(0,width),random.randint(0,height)),3,random.uniform(1,2),random.choice(colors),random.choice(names)) for _ in range(num)]


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill("black")

    mouse_button = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    new_life = Life(mouse_pos,3,random.uniform(1,2),random.choice(colors),random.choice(names))
    if mouse_button[0] and num < max_partikel:
        num += 1
        lifes.append(new_life)
    elif mouse_button[2]:
        for life in lifes:
            num -= 1
            lifes.remove(life)

    for life in lifes:
        life.update()
        life.check_collision()
        # life.show_name()

    clock.tick(60)
    pygame.display.update()

pygame.quit()
