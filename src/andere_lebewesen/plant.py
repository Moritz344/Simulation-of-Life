import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("plant organismen")

# global var
num_plants = 1
cell_size = 10


class Plant(object):
    def __init__(self,position,lebenszeit,speed=cell_size):
        self.position = list(position)
        self.speed = speed
        self.abstand = 10
        
        self.lebenszeit = lebenszeit
        self.lebenszeit_timer = pygame.time.get_ticks()
        self.vermehrungs_timer = pygame.time.get_ticks()
        self.vermehrungs_duration = 150

        self.max_plant = 220
        self.colour = "yellow"
        self.body_colour = "green"
        self.alive = True

        self.rect = pygame.Rect(self.position[0] - cell_size,self.position[1] - 20,40,40)

    def dead_plants(self):
        global num_plants
        elapsedTime = pygame.time.get_ticks() - self.lebenszeit_timer
        if elapsedTime >= self.lebenszeit and self.alive:
            num_plants -= 1
            self.body_colour = "grey"
            self.colour = "grey"
            self.alive = False

            # nach einer zeit soll self removed werden 
            plant_generation.remove(self)

            self.lebenszeit_timer = pygame.time.get_ticks()



    def plant_vermehrung(self):
        global num_plants
        for life in plant_generation:
            self.position_oben = (life.position[0] + life.abstand * 3,life.position[1] - life.abstand * 3)
            self.position_unten = (life.position[0] - life.abstand * 3,life.position[1] + life.abstand * 3)
            self.position_mitte_rechts = (life.position[0] + life.abstand,life.position[1] + life.abstand)
            self.position_mitte_links = (life.position[0] - life.abstand,life.position[1] - life.abstand)
        

        

        elapsedTime = pygame.time.get_ticks() - self.vermehrungs_timer 
        self.random_pos = random.choice([self.position_oben,self.position_unten,self.position_mitte_links,self.position_mitte_rechts])
        
        if elapsedTime >= self.vermehrungs_duration :
            num_plants += 1
            self.vermehrungs_timer = pygame.time.get_ticks()
            new_life = Plant(self.random_pos,random.randint(3000,5000))
            plant_generation.append(new_life)


    def collision_detection(self):
        if self.position[0] >= width - cell_size:
            self.position[0] = width - cell_size
        elif self.position[0] <= 0 + cell_size:
            self.position[0] = cell_size

        if self.position[1] >= height - cell_size:
            self.position[1] = height - cell_size
        elif self.position[1] <= 0 + cell_size:
            self.position[1] = cell_size



    def plant_organismen(self):
        self.erb = pygame.draw.rect(screen,self.colour,(self.position[0],self.position[1],cell_size,cell_size))
        self.body_1 = pygame.draw.rect(screen,self.body_colour,(self.position[0] + self.abstand,self.position[1] - self.abstand,cell_size,cell_size))
        self.body_2 = pygame.draw.rect(screen,self.body_colour,(self.position[0] - cell_size ,self.position[1] + cell_size,cell_size,cell_size))

        self.rect = pygame.Rect(self.position[0] - cell_size,self.position[1] - 20,40,40)

    def update(self):
        global num_plants
        self.plant_organismen()
        self.dead_plants()
 
        if num_plants <= 0 and not self.alive :
                plant_generation.remove(self)

        

plant_generation = [Plant((random.randint(0,width - cell_size),random.randint(0,height - cell_size)),random.randint(3000,5000) ) for _ in range(num_plants)]
plant = Plant((random.randint(0,width - cell_size),random.randint(0,height - cell_size)),random.randint(3000,5000))


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill("black")

    plant.plant_vermehrung()

    for life in plant_generation:
        life.collision_detection()
        life.update()
   

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
