import pygame
import random
import math

width = 1920
height = 1080
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Fish Simulation")

num = 10
max_num = 20
num_plankton = 20


pygame.font.init()
font = pygame.font.SysFont("opensans",30)
# var


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
    def __init__(self,position,fish_art="normal",speed=2,size=16):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.size = size
        self.fish_art = fish_art
        
        self.direction = ""
        
        self.fish_image = pygame.image.load("fish.png")
        self.fish_scaled = pygame.transform.scale(self.fish_image,(self.size,self.size))
        self.fish_rot = pygame.transform.flip(self.fish_scaled,True,True)


        self.rect = pygame.Rect(self.position.x,self.position.y,20,20)

        
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.perception_radius = 70
        self.max_speed = 2
        self.not_zero = 0.01
        self.max_force = 0.1 # Maximale Steuerkraft





    def collision_detection(self):
        if self.position.x >= width - self.size * 2:
            self.position.x = self.size * 3
        elif self.position.x <= 0 + self.size * 2:
            self.position.x = width - self.size * 3

        if self.position.y >= height - self.size * 2:
            self.position.y = self.size * 2
        elif self.position.y <= 0 + self.size * 2:
            self.position.y = height - self.size * 2

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


        if self.direction == "Rechts" or self.direction == "Oben":
                self.fish_rot = pygame.transform.flip(self.fish_scaled,True,False)
        else:
                self.fish_rot = pygame.transform.flip(self.fish_scaled,False,False)

        return self.direction
        

    def move(self):
        # Begrenze die Geschwindigkeit
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.position += self.speed * self.velocity 

        self.collision_detection()


    def apply_behaviour(self):
        alignment = self.align()
        cohesion = self.cohere()
        seperation = self.seperate()

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed


        self.velocity += alignment * 1.5
        self.velocity += cohesion * 1.1
        self.velocity += seperation * 2


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
                if distance > self.not_zero: # Vermeidung von Division durch 0
                    diff /= distance # Gewichtung Entfernen
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering += self.velocity
            if steering.length() > self.max_force:
                steering = steering.normalize() * self.max_force
        return steering




    def update(self):
        global steering
        self.apply_behaviour()

        screen.blit(self.fish_rot,(self.position))
        self.rect = pygame.Rect(self.position[0],self.position[1],20,20)

        #print(f"{id(self)}:{self.velocity}")

class Fish_2():
    def __init__(self,position,speed=0,size=20):
        self.position = pygame.Vector2(position)
        self.size = size

        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.perception_radius = 70
        self.max_force = 0.1
        self.max_speed = 4
        self.not_zero = 0.01
        self.speed = 3

        
        self.fish_image = pygame.image.load("fish_2.png")
        self.fish_image_scaled = pygame.transform.scale(self.fish_image,(self.size,self.size))
        self.fish_rot = pygame.transform.flip(self.fish_image_scaled,True,False)
        self.rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)


    def collision_detection(self):
        if self.position.x >= width - self.size * 2:
            self.position.x = 0 + self.size * 2
        elif self.position.x <= 0 + self.size * 2:
            self.position.x = width - self.size * 2

        if self.position.y >= height - self.size * 2:
            self.position.y = self.size * 2
        elif self.position.y <= 0 + self.size * 2:
            self.position.y = height - self.size * 2
    def move(self):
        # Begrenze die Geschwindigkeit
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.position += self.speed * self.velocity 

        self.collision_detection()


    def collision_detection_2(self,other):
        return (self.rect.colliderect(other.rect))

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


        if self.direction == "Rechts" or self.direction == "Oben":
                self.fish_rot = pygame.transform.flip(self.fish_image_scaled,True,False)
        else:
                self.fish_rot = pygame.transform.flip(self.fish_image_scaled,False,False)

        return self.direction

    def apply_behaviour(self):
        alignment = self.align()
        cohesion = self.cohere()
        seperation = self.seperate()

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed


        self.velocity += alignment 
        self.velocity += cohesion 
        self.velocity += seperation 


    def align(self):
        """Passe die Richtung an die Nachbarn an."""
        steering = pygame.Vector2(0,0)
        total = 0
        for fish in fish_group_2:
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
        for fish in fish_group_2:
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
        for fish in fish_group_2:
            if fish == self:
                continue
            distance = self.position.distance_to(fish.position)
            if 0 < distance < self.perception_radius / 2: # nur fische in der nähe berücksichtigen
                diff = self.position - fish.position
                if distance > self.not_zero: # Vermeidung von Division durch 0
                    diff /= distance # Gewichtung Entfernen
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering += self.velocity
            if steering.length() > self.max_force:
                steering = steering.normalize() * self.max_force
        return steering



    def update(self):
        screen.blit(self.fish_rot,(self.position))
        self.rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)
        self.apply_behaviour()
        

fish_group = [Fish((random.randint(200,300),random.randint(200,300)),"normal") for _ in range(num)]
fish_group_2 = [Fish_2(random.randint(500,700),random.randint(300,500)) for _ in range(num + 10)]
fish_group_3 = [Fish_2(random.randint(200,700),random.randint(100,500)) for _ in range(num + 10)]
fish = Fish((random.randint(200,300),random.randint(200,300)),"normal")

food_group = [Nahrung((random.randint(20,width - 30),random.randint(50,200)) ) for _ in range(num_plankton)]
food = Nahrung((random.randint(20,width - 30),random.randint(50,200)) )
kollision_food = False

def spawn_collision_fish(fish):
        for i in range(len(fish)):
                for j in range(i+1,len(fish)):
                    try:
                        if fish[i].collision_detection_2(fish[j]) :
                         fish.remove(fish[i])
                    except IndexError :
                        continue

spawn_collision_fish(fish_group_2)

def Nahrungs_kollision(num_plankton,kollision_food):
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

def spawning_fish(group):
    for life in group:
        life.Richtung_bestimmen()
        life.move()
        life.update()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    screen.fill((29, 45, 68))



    Nahrungs_kollision(num_plankton,kollision_food)

    food.spawn_nahrung()

    for food in food_group:
        food.update()
    spawning_fish(fish_group)
    spawning_fish(fish_group_2)
    spawning_fish(fish_group)
    spawning_fish(fish_group_2)


    clock.tick(60)
    pygame.display.update()
pygame.quit()
