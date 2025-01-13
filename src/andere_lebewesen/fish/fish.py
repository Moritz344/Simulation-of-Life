import pygame
import random
import math

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

num = 10
max_num = 20
num_plankton = 20


pygame.font.init()
font = pygame.font.SysFont("opensans",30)

# var


hohe_schwimmhöhe: float = 25.0
mittlere_schwimmhöhe: float = min(15.0,24.0)
niedrige_schwimmhöhe: float = 15.0
direction = None



    
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
    def __init__(self,position,direction,lebenszeit,size,speed=0):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.direction = direction
        self.size = size
        self.alive = True
        
        self.lebenszeit = lebenszeit # in ms
        self.leben = pygame.time.get_ticks()

        self.colour = "blue"

        self.rect = pygame.Rect(self.position[0],self.position[1],20,20)

        
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.perception_radius = 50
        self.max_speed = 2
        self.max_force = 0.1 # Maximale Steuerkraft





    def collision_detection(self):

        # BITTE FASS DAS NICHT AN WENN ICH KEINE MACHE GEHEN FISCHE ABHANDEN
        for fish in fish_group:
                if self.position[0] >= width - self.size * 2 or self.position[0] <= 0 + self.size * 2:
                    fish.velocity *= -1
                if self.position[1] >= height - self.size * 2 or self.position[1] <= 0 + self.size * 2 :
                    fish.velocity *= -1

    def move(self):
        # Begrenze die Geschwindigkeit
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Aktualisiere die Position
        self.position += self.velocity 

    def apply_behaviour(self):
        alignment = self.align()
        cohesion = self.cohere()
        seperation = self.seperate()

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed


        self.velocity += alignment 
        #self.velocity += cohesion 
        self.velocity += seperation 


    def align(self):
        """Passe die Richtung an die Nachbarn an."""
        steering = pygame.Vector2(0,0)
        total = 0
        for fish in fish_group:
            if fish == self:
                continue
            distance = self.position.distance_to(fish.position)
            if distance < self.perception_radius:
                steering += fish.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize()
            steering -= self.velocity

        return steering

    def cohere(self):
        """Bewege dich in Richtung des Massenschwerpunkts."""
        steering = pygame.Vector2(0,0)
        total = 0
        for fish in fish_group:
            if fish == self:
                continue
            distance = self.position.distance_to(fish.position)
            if distance < self.perception_radius:
                steering += fish.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering = steering.normalize() * self.max_force
        return steering

    def seperate(self):
        """Vermeide Kollisionen mit Nachbarn."""
        steering = pygame.Vector2(0,0)
        total = 0
        for fish in fish_group:
            if fish == self:
                continue
            distance = self.position.distance_to(fish.position)
            if 0 < distance < self.perception_radius / 2: # nur fische in der nähe berücksichtigen
                diff = self.position - fish.position
                if distance > 0.0001: # Vermeidung von Division durch 0
                    diff /= distance # Gewichtung Entfernen
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering = steering.normalize() * self.max_force

        return steering




    def update(self):
        self.apply_behaviour()
        self.collision_detection()
        self.fish_c = pygame.draw.circle(screen,"white",(self.position[0] + 10,self.position[1]),self.size,self.size,False,False,False,False,)
        self.rect = pygame.Rect(self.position[0],self.position[1],40,40)

        print(f"{id(self)}:{self.velocity}")

fish_group = [Fish((random.randint(200,300),random.randint(200,300)),random.choice(["RIGHT","LEFT","UP","DOWN"]),random.randint(10000,20000),5) for _ in range(num)]
fish = Fish((random.randint(200,300),random.randint(200,300)),random.choice(["RIGHT","LEFT","UP","DOWN"]),random.randint(10000,20000),10)
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
    for life in fish_group:
        #life.age_death()
        life.move()
        life.update()
    for food in food_group:
        food.update()

    clock.tick(60)
    pygame.display.update()
pygame.quit()
