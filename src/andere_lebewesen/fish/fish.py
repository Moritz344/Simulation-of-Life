import pygame
import random
import math

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Fish Simulation")

num = 10
max_num = 20
num_plankton = 20


pygame.font.init()
font = pygame.font.SysFont("opensans",30)

# var


hohe_schwimmhöhe: float = 25.0
mittlere_schwimmhöhe: float = min(15.0,24.0)
niedrige_schwimmhöhe: float = 15.0



    
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
    def __init__(self,position,colour,fish_art="normal",speed=0,size=16):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.size = size
        self.alive = True
        self.fish_art = fish_art
        
        self.direction = ""
        self.colour = colour
        
        self.fish_image = pygame.image.load("fish.png")
        self.fish_scaled = pygame.transform.scale(self.fish_image,(self.size,self.size))
        self.fish_rot = pygame.transform.flip(self.fish_scaled,True,True)


        self.rect = pygame.Rect(self.position[0],self.position[1],20,20)

        
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.perception_radius = 70
        self.max_speed = 2
        self.max_force = 0.1 # Maximale Steuerkraft

        self.face_direction_timer = pygame.time.get_ticks()
        self.face_direction_timer_dur = 100




    def collision_detection(self):
        for fish in fish_group:
                if self.position[0] >= width - self.size * 2 or self.position[0] <= 0 + self.size * 2:
                    fish.velocity *= -1
                if self.position[1] >= height - self.size * 2 or self.position[1] <= 0 + self.size * 2 :
                    fish.velocity *= -1

    def Richtung_bestimmen(self):
        angle = math.atan2(self.velocity.y, self.velocity.x)  # Winkel in Radiant
        angle_in_degrees = math.degrees(angle)

        if -45 <= angle_in_degrees < 45:
            self.direction = "Rechts"
        elif 45 <= angle_in_degrees < 135:
            self.direction = "Unten"
        elif -135 <= angle_in_degrees < -45:
            self.direction = "Oben"
        else:
            self.direction = "Links"


        if self.direction == "Rechts":
                self.fish_rot = pygame.transform.flip(self.fish_scaled,True,False)
        else:
                self.fish_rot = pygame.transform.flip(self.fish_scaled,False,False)

        return self.direction
        

    def move(self):
        # Begrenze die Geschwindigkeit
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.position += self.velocity 




    def apply_behaviour(self):
        alignment = self.align()
        cohesion = self.cohere()
        seperation = self.seperate()

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed


        self.velocity += alignment * 1.5
        self.velocity += cohesion * 1.1
        self.velocity += seperation * 1.5


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
            if distance < self.perception_radius :
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
        global steering
        self.apply_behaviour()
        self.collision_detection()

        screen.blit(self.fish_rot,(self.position))
        self.rect = pygame.Rect(self.position[0],self.position[1],20,20)

        #print(f"{id(self)}:{self.velocity}")

fish_group = [Fish((random.randint(200,300),random.randint(200,300)),random.choice(["blue","red","yellow","green"]),"normal") for _ in range(num)]
fish = Fish((random.randint(200,300),random.randint(200,300)),random.choice(["blue","red","yellow","green"]),"normal")
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
        life.Richtung_bestimmen()
        life.move()
        life.update()
    for food in food_group:
        food.update()

    clock.tick(60)
    pygame.display.update()
pygame.quit()
