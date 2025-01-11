import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

num = 15

# TODO: Plankton als Nahrung, Fortpflanzung, Fischarten


pygame.font.init()
font = pygame.font.SysFont("opensans",30)

# var

temp: float = 0.0
temp_rate = 1.0
max_temp = 30.0
min_temp = 10.0
temp_timer = pygame.time.get_ticks()
temp_timer_dur = 1000
change_temp = pygame.time.get_ticks()
change_temp_dur = 1000

hohe_schwimmhöhe: float = 25.0
mittlere_schwimmhöhe: float = min(15.0,24.0)
niedrige_schwimmhöhe: float = 15.0
direction = None

print(mittlere_schwimmhöhe)

def temperature_level(temp,):
        temp_text = font.render(f"{temp}°C",False,"white")
        screen.blit(temp_text,(10,0))
def aktualisiere_temperatur():
    global temp
    temp += random.uniform(-temp_rate, temp_rate)
    temp = max(min_temp, min(max_temp, temp))

    
class Nahrung(object):
    def __init__(self,position):
        self.position = list(position)
        self.size = 10

        self.startwert = 0
        self.endwert = 4
        self.abstand = 10

        self.rect = pygame.Rect(self.position[0] - 30 , self.position[1] - 30,self.size  * 7,self.size * 4)

    def draw_plankton(self):
            for i in range(self.startwert,self.endwert):
                self.body_1 = pygame.draw.rect(screen,"dark green",(self.position[0] , self.position[1] - i * 10,self.size,self.size))
            for i in range(self.startwert,self.endwert):
                self.body_2 = pygame.draw.rect(screen,"dark green",(self.position[0] + i * 10, self.position[1] - i * 10,self.size,self.size))
            for i in range(self.startwert,self.endwert):
                self.body_2 = pygame.draw.rect(screen,"dark green",(self.position[0] - i * 10, self.position[1] - i * 10,self.size,self.size))

            self.rect = pygame.Rect(self.position[0] - 30 , self.position[1] - 30,self.size  * 7,self.size * 4)

    def collision_detection(self,other):
        return (self.rect.colliderect(other.rect))


    def update(self):
        self.draw_plankton()




class Fish(object):
    def __init__(self,position,speed,direction,):
        self.position = list(position)
        self.speed = speed
        self.size = 10
        self.direction = direction
        self.dx = 1
        self.dy = 1


        self.move_chance = 0.69
        self.down_chance = 0.69
        self.up_chance = 0.69

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
            self.position[0] = width - self.size
        elif self.position[0] <= 0 + self.size:
            self.position[0] = self.size

        if self.position[1] >= height - self.size:
            self.position[1] = height - self.size
        elif self.position[1] <= 0 + self.size:
            self.position[1] = self.size

    def move(self):
        elapsedTime = pygame.time.get_ticks() - self.next_move_timer


        if self.direction == "RIGHT" and random.random() > self.move_chance:
                self.position[0] += self.speed * self.dx
        elif self.direction == "LEFT" and random.random() > self.move_chance:
                self.position[0] -= self.speed * self.dx

        if self.direction == "UP" and random.random() > self.up_chance:
                self.position[1] -= self.speed * self.dy
        elif self.direction == "DOWN" and random.random() > self.down_chance:
                self.position[1] += self.speed * self.dy
    

        if elapsedTime >= self.duration:
            self.next_move_timer = pygame.time.get_ticks()
            self.direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

#            if temp < 15:
#                if random.random() > self.move_chance:
#                    self.direction = "DOWN"
#            elif temp >= 13 and temp < 24:
#                self.direciton = "UP"
#                self.up_chance = 0.3
#            else:
#                self.up_chance = 0.69
#
            if self.direction == "RIGHT" and random.random() > self.move_chance:
                self.position[0] += self.speed * self.dx
            elif self.direction == "LEFT" and random.random() > self.move_chance:
                self.position[0] -= self.speed * self.dx

            if self.direction == "UP" and random.random() > self.up_chance:
                self.position[1] -= self.speed * self.dy

            elif self.direction == "DOWN" and random.random() > self.down_chance:
                self.position[1] += self.speed * self.dy
        
    

    def update(self):
        self.move()
        self.collision_detection()
        self.fish = pygame.draw.rect(screen, "blue", (self.position[0],self.position[1],self.size,self.size))
        self.rect = pygame.Rect(self.position[0],self.position[1],40,40)

fish_group = [Fish((random.randint(0,width),random.randint(0,height)),2,random.choice(["RIGHT","LEFT","UP","DOWN"])) for _ in range(num)]
food_group = [Nahrung((random.randint(20,width - 30),height - 11) ) for _ in range(3)]
kollision_food = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill("black")
    elapsedTime = pygame.time.get_ticks() - temp_timer
    if elapsedTime >= temp_timer_dur:
        temp_timer = pygame.time.get_ticks()
        aktualisiere_temperatur()

    temp = round(temp,2)
    temperature_level(temp,)

    # Kollision zwischen Nahrung
    for i in range(len(food_group)):
        for j in range(i+1,len(food_group)):
            try:
                if food_group[i].collision_detection(food_group[j]) :
                 kollision_food = True
                 food_group.remove(food_group[i])
            except IndexError :
                continue
            else:
                kollsion_food = False

    for life in fish_group:
        life.update()
    for food in food_group:
        food.update()

    clock.tick(60)
    pygame.display.update()

