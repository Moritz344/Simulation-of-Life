import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Particle")

# global variables
particle_colors = ["red","white","blue","yellow","green"]
particle_num = 500

def distance(particles: list,color):
    # Distanz berechnen von den nachbarn der Partikel
    same_color = [p for p in particles if p.color == color]
    data = [p.position for p in same_color]
    distances = []

    color = [p.color for p in particles]

    for i in range(len(data) - 1):
            x1, y1 = data[i]
            x2, y2 = data[i+1]
            
            distance_x = x2 - x1 
            distance_y = y2 - y1 
            distances.append((data[i],data[i+1],distance_x,distance_y))


    return distances
        


class Particle(object):
    def __init__(self,position: tuple,color: str,velocity: float):
        self.position = list(position)
        self.color = color
        self.velocity = velocity
        self.particle_size = 3
        
        self.pos_x,self.pos_y = self.position
        self.particleRect = pygame.Rect(self.pos_x,self.pos_y,self.particle_size,self.particle_size)

    def move(self,distance_x,distance_y):

        self.position[0] += distance_x * self.velocity * 0.1 + 0.5
        self.position[1] += distance_y * self.velocity * 0.1 
        
        self.position[0] += random.choice([-1,0,1])
        self.position[1] += random.choice([-1,0,1])

        if self.position[0] > width - self.particle_size:
            self.position[0] = width - self.particle_size
        elif self.position[0] < 0 + self.particle_size:
            self.position[0] = 0 + self.particle_size 

        if self.position[1] > height - self.particle_size:
            self.position[1] = height - self.particle_size
        elif self.position[1] < 0 + self.particle_size:
            self.position[1] = 0 + self.particle_size

    def update(self):
        pygame.draw.circle(screen,self.color,(self.position[0],self.position[1]),self.particle_size)
        self.particleRect.topleft = (self.position[0],self.position[1])
        

particles = [Particle((random.randint(0,width),random.randint(0,height)),random.choice(particle_colors),velocity=2) for _ in range(particle_num)]


p: object = Particle((0,0),"white",1)

# game loop
run: bool = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run: bool = False
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run: bool = False
                exit()
    screen.fill("black")
    
    for particle in particles:
        distances = distance(particles,particle.color)
        for data1,data2,distance_x,distance_y in distances:
            if particle.position == list(data1):
                particle.move(distance_x,distance_y)
        particle.update()

    clock.tick(60)
    pygame.display.update()


pygame.quit()

