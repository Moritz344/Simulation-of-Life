import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Schwimmer Organismus")

# nametags?
# Agressive Zellen?

# global var
cell_size = 5
num_life = 1
color_choice = random.choice(["blue","red","yellow"])

# font
pygame.font.init()
font = pygame.font.Font("../MinecraftRegular.otf",30)


class Schwimmer(object):
    def __init__(self,name,position,colour,lebenszeit,alive,hungry,energie,speed=cell_size):
        self.position = list(position)
        self.speed = speed
        self.move_chance = 0.77
        self.colour = colour
        self.body_colour = "white"
        self.alive = alive
        self.hungry = hungry
        self.energie = energie
        self.name = name


        
        # schwimmer_create variablen
        self.startwert = 1
        self.endwert = 3
        self.abstand = cell_size

        self.rect = pygame.Rect(self.position[0],self.position[1],cell_size,cell_size)
        self.last_updated = pygame.time.get_ticks()

        self.death_timer = pygame.time.get_ticks()
        self.death_timer_dur = lebenszeit

        self.klon_timer = pygame.time.get_ticks()
        self.klon_timer_dur = 500

        self.block = cell_size

        self.body_1_block = cell_size 
        self.body_2_block = cell_size
        self.body_3_block = cell_size
        self.body_4_block = cell_size
    

    def klone_schwimmer(self):
        global num_life
        elapsedTime = pygame.time.get_ticks() - self.klon_timer
        if elapsedTime >= self.klon_timer_dur and num_life >= 1 :
            self.klon_timer = pygame.time.get_ticks()
            self.klon_timer_dur += 500
            num_life += 1
            self.create_new_schwimmer()

        


    def create_new_schwimmer(self):
            if num_life >= 1 :
                new_life = Schwimmer("",(self.position[0],self.position[1]),random.choice(["red","blue","green","orange",]),random.randint(1000,100000),True,False,random.randint(1000,5000))
                schwimmer_generation.append(new_life)
            
    def delete_schwimmer(self):
        schwimmer_generation.remove(self)


    def eating_process(self):
        global num_life
        for life in schwimmer_generation:
            if life != self and self.body_1.colliderect(life.rect) and not self.alive and self in schwimmer_generation :
                self.body_1_block -= 1
            elif life != self and self.body_2.colliderect(life.rect) and not self.alive and self in schwimmer_generation:
                self.body_2_block -= 1
                self.death_timer_dur += 100
                self.energie += 1500
            elif life != self and self.body_3.colliderect(life.rect) and not self.alive and self in schwimmer_generation:
                self.body_3_block -= 1
                self.death_timer_dur += 100
                self.energie += 1500
            elif life != self and self.body_4.colliderect(life.rect) and not self.alive and self in schwimmer_generation:
                self.body_4_block -= 1
                self.death_timer_dur += 100
                self.energie += 1500
            if life != self and self.erb.colliderect(life.rect) and not self.alive and self in schwimmer_generation:
                self.block -= 1
                self.death_timer_dur += 100
                self.energie += 500


            
    
    def next_generation(self):
        global num_life,next_generation
        print("Jedes Organismus ist gestorben!")

        for life in schwimmer_generation:
            schwimmer_generation.remove(life)
        

    def move(self):
        global num_life
        self.direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

        elapsedTime = pygame.time.get_ticks() - self.last_updated
        if elapsedTime >= 50 :
            self.last_updated = pygame.time.get_ticks()

            if self.direction == "RIGHT" and random.random() > self.move_chance:
                self.position[0] += self.speed 
            elif self.direction == "LEFT" and random.random() > self.move_chance:
                self.position[0] -= self.speed

            if self.direction == "UP" and random.random() > self.move_chance:
                self.position[1] -= self.speed
            elif self.direction == "DOWN" and random.random() > self.move_chance:
                self.position[1] += self.speed


        elapsedTimeDeath = pygame.time.get_ticks() - self.death_timer
        if elapsedTimeDeath >= self.death_timer_dur and self.alive != False:
            num_life -= 1
            self.alive = False
            self.death_timer = pygame.time.get_ticks()
            self.colour = "grey"
            self.body_colour = "grey"
            self.speed = 0

        


        if self.position[0] > width - cell_size:
            self.position[0] = width - cell_size 
        elif self.position[0] < 0 + cell_size:
            self.position[0] = cell_size 

        if self.position[1]  > height - cell_size:
            self.position[1] = height - cell_size
        elif self.position[1]  < 0 + cell_size:
            self.position[1] = cell_size



    def schwimmer_create(self):
        self.erb = pygame.draw.rect(screen,self.colour,(self.position[0] ,self.position[1],self.block,self.block))
        self.rect = pygame.Rect(self.position[0] - cell_size * 2,self.position[1] - cell_size * 2,cell_size * 5,cell_size * 5)
        #pygame.draw.rect( screen,"white",(self.position[0] - cell_size * 2,self.position[1] - cell_size * 2,cell_size * 5,cell_size * 5),1)


        for i in range(self.startwert,self.endwert):
                self.body_1 = pygame.draw.rect(screen,self.body_colour,(self.position[0] + self.abstand * i,self.position[1] - self.abstand * i,self.body_1_block,self.body_1_block))

        for i in range(self.startwert,self.endwert) :
                self.body_2 = pygame.draw.rect(screen,self.body_colour,(self.position[0] - self.abstand * i,self.position[1] - self.abstand * i,self.body_2_block,self.body_2_block))

        for i in range(self.startwert,self.endwert):
                self.body_3 = pygame.draw.rect(screen,self.body_colour,(self.position[0] - self.abstand * i,self.position[1] + self.abstand * i,self.body_3_block,self.body_3_block))

        for i in range(self.startwert,self.endwert):
                self.body_4 = pygame.draw.rect(screen,self.body_colour,(self.position[0] + self.abstand * i,self.position[1] + self.abstand * i,self.body_4_block,self.body_4_block))

    def update(self):
        self.schwimmer_create()

        if num_life == 0:
            self.next_generation()
        




schwimmer_generation = [Schwimmer("",(random.randint(0,width - cell_size * 2),random.randint(0,height - cell_size * 2)),"blue",random.randint(1000,100000),True,True,random.randint(1000,5000)) for _ in range(num_life)]
s = Schwimmer("",(random.randint(0,width ),random.randint(0,height )),"white",random.randint(1000,100000),True,True,random.randint(1000,5000))


def berechne_durschnitt(objekte):
    # lebenszeit durschnitt berechnen
    gesamte_lebenszeit = 0
    anzahl_objekte = 0

    for objekt in objekte:
        gesamte_lebenszeit = objekt.death_timer_dur
        anzahl_objekte += 1

    return gesamte_lebenszeit / anzahl_objekte if anzahl_objekte > 0 else 0

def spawn_food():
    global num_life
    mouse_x,mouse_y = pygame.mouse.get_pos()
    
    new_life = Schwimmer("",(mouse_x,mouse_y),random.choice(["red","blue","yellow","green"]),random.randint(1000,100000),True,True,random.randint(1000,5000))
    num_life += 1
    schwimmer_generation.append(new_life)

for i,v in enumerate(schwimmer_generation):
        print(f"{i+1},Lebensstatus: {v.alive},Lebenszeit: {v.death_timer_dur} ms, Hungrig: {v.hungry} Energie: {v.energie}")

erstes_objekt = schwimmer_generation[0]


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
    
        screen.fill((7, 30, 34))
        
        s.klone_schwimmer()

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            spawn_food()
        
        
        if erstes_objekt.alive == False:
            erstes_objekt.colour = "green"
            erstes_objekt.body_colour = "green"


        for life in schwimmer_generation:
            life.move()
            life.update()
            life.eating_process()


        average_lebenszeit = berechne_durschnitt(schwimmer_generation)
        average_lebenszeit = round(average_lebenszeit,(2))
        average_lebenszeit_text = font.render(f"av. life: {average_lebenszeit}ms",False,"white")
        anzahl_lifes = font.render(f"num: {num_life}",False,"white")
        screen.blit(average_lebenszeit_text,(0,0))
        screen.blit(anzahl_lifes,(0,25))

        clock.tick(fps)
        pygame.display.update()
main()
