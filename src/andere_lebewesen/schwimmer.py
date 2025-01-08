import pygame
import random

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Schwimmer Organismus")


# global var
cell_size = 5
num_life = 1
num_food = 0
color_choice = random.choice(["blue","red","yellow"])


different = random.choice(["small","big","normal"])
# font
pygame.font.init()
font = pygame.font.Font("../MinecraftRegular.otf",30)



class Schwimmer(object):
    def __init__(self,name,position,colour,lebenszeit,alive,hungry,energie,different,speed=cell_size):
        self.position = list(position)
        self.speed = speed
        self.move_chance = 0.77
        self.colour = colour
        self.body_colour = "white"
        self.alive = alive
        self.hungry = hungry
        self.energie = energie
        self.name = name
        self.different = different


        
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
                new_life = Schwimmer("",(self.position[0],self.position[1]),random.choice(["red","blue","green","orange",]),random.randint(1000,100000),True,False,random.randint(1000,5000),random.choice([False,True]))
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

        for food in food_objekte:
            if self.rect.colliderect(food.food_rect):
                self.death_timer_dur += 100
                self.energie += 1000
                food_objekte.remove(food)



    
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


        for i in range(self.startwert,self.endwert) :
                self.body_1 = pygame.draw.rect(screen,self.body_colour,(self.position[0] + self.abstand * i,self.position[1] - self.abstand * i,self.body_1_block,self.body_1_block))

        for i in range(self.startwert,self.endwert) :
                self.body_2 = pygame.draw.rect(screen,self.body_colour,(self.position[0] - self.abstand * i,self.position[1] - self.abstand * i,self.body_2_block,self.body_2_block))

        for i in range(self.startwert,self.endwert):
                self.body_3 = pygame.draw.rect(screen,self.body_colour,(self.position[0] - self.abstand * i,self.position[1] + self.abstand * i,self.body_3_block,self.body_3_block))

        for i in range(self.startwert,self.endwert):
                self.body_4 = pygame.draw.rect(screen,self.body_colour,(self.position[0] + self.abstand * i,self.position[1] + self.abstand * i,self.body_4_block,self.body_4_block))

    def update(self):
        self.schwimmer_create()

        if num_life <= 0:
            self.next_generation()


class Food(object):
    def __init__(self,position,size):
        self.size = size
        self.position = list(position)

    def update(self):
        self.food = pygame.draw.rect(screen,(95, 115, 103),(self.position[0],self.position[1],self.size,self.size))
        self.food_rect = pygame.Rect(self.position[0],self.position[1],self.size,self.size)


food_objekte = [Food((0,0),20.0) for _ in range(num_food)]
schwimmer_generation = [Schwimmer("",(random.randint(0,width - cell_size * 2),random.randint(0,height - cell_size * 2)),"blue",random.randint(1000,100000),True,True,random.randint(1000,5000),random.choice([False,True]) ) for _ in range(num_life)]
s = Schwimmer("",(random.randint(0,width ),random.randint(0,height )),"white",random.randint(1000,100000),True,True,random.randint(1000,5000) ,random.choice([False,True]))

def berechne_durschnitt(objekte):
    # lebenszeit durschnitt berechnen
    gesamte_lebenszeit = 0
    anzahl_objekte = 0

    for objekt in objekte:
        gesamte_lebenszeit = objekt.death_timer_dur
        anzahl_objekte += 1

    return gesamte_lebenszeit / anzahl_objekte if anzahl_objekte > 0 else 0

def different_life():
    for i,v in enumerate(schwimmer_generation):
            if v.different == True and different == "small" and v.alive:
                    v.endwert = 4
                    v.startwert = 3
                    v.abstand = 2
                    
            elif v.different == True and different == "big" and v.alive:
                    v.endwert = 5
                    v.abstand = 4

            if v.different == False:
                continue
            


def spawn_food():
    global num_food,cell_size
    mouse_x,mouse_y = pygame.mouse.get_pos()


    scaled_x = mouse_x  
    scaled_y = mouse_y
    
    num_food += 1
    new_food = Food((scaled_x,scaled_y),20.0)
    food_objekte.append(new_food)

def del_food():
    global num_food

    mouse_pos = pygame.mouse.get_pos()
    for i,v in enumerate(food_objekte):
        if v.food_rect.collidepoint(mouse_pos):
            num_food -= 1
            food_objekte.remove(v)
            break

#    for life in food_objekte:
#        num_food -= 1
#        food_objekte.remove(life)


for i,v in enumerate(schwimmer_generation):
    print(f"{i+1},Lebensstatus: {v.alive},Lebenszeit: {v.death_timer_dur} ms, Hungrig: {v.hungry} Energie: {v.energie} Different: {v.different}")

#erstes_objekt = schwimmer_generation[0]


def main():
    global zoom_factor,camera_offset
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

        screen.fill((7, 30, 34))






        average_lebenszeit = berechne_durschnitt(schwimmer_generation)
        average_lebenszeit = round(average_lebenszeit,(2))
        average_lebenszeit_text = font.render(f"{average_lebenszeit}ms",False,"white")
        anzahl_lifes = font.render(f"{num_life}",False,"white")
        screen.blit(average_lebenszeit_text,(0,0))
        screen.blit(anzahl_lifes,(0,25))

        s.klone_schwimmer()

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            spawn_food()
        elif mouse_pressed[2]:
            del_food()
        
        
        for food in food_objekte:
            food.update()

        for life in schwimmer_generation:
            life.move()
            life.update()
            life.eating_process()

        different_life()


        pygame.display.flip()
        clock.tick(fps)
main()
