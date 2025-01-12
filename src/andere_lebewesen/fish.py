import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

num = 2
max_num = 20
num_plankton = 20

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
        self.abstand = 5

        self.block_1 = 5
        self.block_2 = 5
        self.block_3 = 5

        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_timer_dur = 5000

        self.rect = pygame.Rect(self.position[0] - 30 , self.position[1] - 30,self.size  * 7,self.size * 4)

    def spawn_nahrung(self):
        global num_plankton
        elapsedTime = pygame.time.get_ticks() - self.spawn_timer
        if elapsedTime >= self.spawn_timer_dur:
            new_food = Nahrung((random.randint(20,width - 30),random.randint(50,200)) ) 
            food_group.append(new_food)
            num_plankton += 1
            self.spawn_timer = pygame.time.get_ticks()

    def draw_plankton(self):
            for i in range(self.startwert,self.endwert):
                self.body_1 = pygame.draw.rect(screen,"dark green",(self.position[0] , self.position[1] - i * self.abstand,self.block_1,self.block_1))
            for i in range(self.startwert,self.endwert):
                self.body_2 = pygame.draw.rect(screen,"dark green",(self.position[0] + i * self.abstand, self.position[1] - i * self.abstand,self.block_2,self.block_2))
            for i in range(self.startwert,self.endwert):
               self.body_3 = pygame.draw.rect(screen,"dark green",(self.position[0] - i * self.abstand, self.position[1] - i * self.abstand,self.block_3,self.block_3))
            

            for life in fish_group:
                if self.body_1.colliderect(life.rect) :
                    self.block_1 -= 1

            for life in fish_group:
                if self.body_2.colliderect(life.rect) :
                    self.block_2 -= 1

            for life in fish_group:
                if self.body_3.colliderect(life.rect) :
                    self.block_3 -= 1


            self.rect = pygame.Rect(self.position[0] - 30 , self.position[1] - 30,self.size  * 7,self.size * 4)
            

    def collision_detection(self,other):
        return (self.rect.colliderect(other.rect))



    def update(self):
        self.draw_plankton()




class Fish(object):
    def __init__(self,position,speed,direction,lebenszeit,size):
        self.position = list(position)
        self.speed = speed
        self.direction = direction
        self.dx = 1
        self.dy = 1
        self.size = size

        self.alive = True
        
        self.lebenszeit = lebenszeit # in ms
        self.leben = pygame.time.get_ticks()


        self.move_chance = 0.69
        self.down_chance = 0.69
        self.up_chance = 0.69

        self.colour = "blue"

        self.rect = pygame.Rect(self.position[0],self.position[1],20,20)

        self.next_move_timer = pygame.time.get_ticks()
        self.duration = 1000

        self.paarung = pygame.time.get_ticks()
        self.paarung_dur = 1000

    def vermehrung(self):
        global num
        if temp >= 10 and temp < 20 and num >= 2 and num < 20:
            elapsedTime = pygame.time.get_ticks() - self.paarung
            if elapsedTime >= self.paarung_dur:
                num += 1
                new_fish = Fish((random.randint(0,width),random.randint(0,height)),2,random.choice(["RIGHT","LEFT","UP","DOWN"]),random.randint(10000,20000),10)
                fish_group.append(new_fish)
                self.paarung = pygame.time.get_ticks()
            #print(elapsedTime,num)





    def handling_death(self):
        global num
        if not self.alive:
            self.colour = "grey"
            self.speed = 0
            fish_group.remove(self)
            num -= 1


    def age_death(self):
        global num
        elapsedTime = pygame.time.get_ticks() - self.leben
        if elapsedTime >= self.lebenszeit:
            self.alive = False
            #fish_group.remove(self)
        else:
            self.alive = True
            #self.leben = pygame.time.get_ticks()

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
        self.handling_death()
        self.move()
        self.collision_detection()
        self.fish = pygame.draw.rect(screen, self.colour, (self.position[0],self.position[1],self.size,self.size))
        self.rect = pygame.Rect(self.position[0],self.position[1],40,40)

fish_group = [Fish((random.randint(0,width),random.randint(0,height)),2,random.choice(["RIGHT","LEFT","UP","DOWN"]),random.randint(10000,20000),10) for _ in range(num)]
fish = Fish((random.randint(0,width),random.randint(0,height)),2,random.choice(["RIGHT","LEFT","UP","DOWN"]),random.randint(10000,20000),10)
food_group = [Nahrung((random.randint(20,width - 30),random.randint(50,200)) ) for _ in range(num_plankton)]
food = Nahrung((random.randint(20,width - 30),random.randint(50,200)) )
kollision_food = False

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill((29, 45, 68))


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
                 num_plankton -= 1
            except IndexError :
                continue
            else:
                kollsion_food = False

    food.spawn_nahrung()
    fish.vermehrung()

    for life in fish_group:
        life.age_death()
        life.update()
    for food in food_group:
        food.update()

    clock.tick(60)
    pygame.display.update()
pygame.quit()
