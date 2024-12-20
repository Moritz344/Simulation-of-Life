import pygame
import random

width = 1920
height = 1080
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Worm Organism")

rows: int = 50
cols: int = 50
cell_size: int = 10

# LETZE VERÄNDERUNGEN:
# schlange braucht energie zum leben
# schlange wird müder

def spawn_grid():
    global rows,cols,x,y

    for höhe in range(rows):
        for breite in range(cols):
            x = breite * cell_size
            y = höhe * cell_size

            #pygame.draw.rect(screen,"white",(x ,y ,cell_size ,cell_size),1)



class Snake(object):
    def __init__(self,x,y,energie,length=20,speed=cell_size,):
        global num_snakes
        self.snake_speed: int = speed
        self.snake_x = x
        self.snake_y = y
        self.warscheinlichkeit: float = 0#0.50
        self.energie = energie


        self.v_timer = pygame.time.get_ticks()
        self.v_timer_duration = 1000

        self.snake_len: int = length
        self.snake_list = []

        self.direction = "RIGHT"

        self.snake_head = [self.snake_x ,self.snake_y ]
        self.snake_list.append(self.snake_head)



        
    
    def fortpflanzung(self):
        global num_snakes
        self.elapsedTime = pygame.time.get_ticks() - self.v_timer
        

        if self.elapsedTime >= self.v_timer_duration and num_snakes >= 2 and self.energie >= 150:
            self.v_timer = pygame.time.get_ticks()
            self.new_snake = Snake(random.randint(0, width // cell_size - 1) * cell_size,
                                  random.randint(0, height // cell_size - 1) * cell_size,random.randint(0,50))
            num_snakes += 1           
            snakes.append(self.new_snake)



    def energieHandler(self):
        # lösche eine schlange wenn sie zu wenig energie hat
        global num_snakes
        #for i,v in enumerate(snakes):
            #print(f"Snake {i+1}: Energie: {v.energie}")

        if self.energie <= 0:
            if self in snakes:
                num_snakes -= 1
                snakes.remove(self)
        # schlange wird müder
        elif self.energie <= 100:
            self.warscheinlichkeit = 0.67

        return num_snakes

    def update(self):
        global num_snakes
        self.direction = random.choice(["DOWN","RIGHT","LEFT","UP"])
            
        if self.direction == "UP" and random.random() > self.warscheinlichkeit:
            self.snake_y -= self.snake_speed
            self.energie -= 1
        elif self.direction == "DOWN" and random.random() > self.warscheinlichkeit:
            self.snake_y += self.snake_speed
            self.energie -= 1
        elif self.direction == "LEFT" and random.random() > self.warscheinlichkeit:
            self.snake_x -= self.snake_speed
            self.energie -= 1
        elif self.direction == "RIGHT" and random.random() > self.warscheinlichkeit:
            self.energie -= 1
            self.snake_x += self.snake_speed

        self.snake_list.append((self.snake_x ,self.snake_y  ))
        

        if len(self.snake_list) > self.snake_len:
            del self.snake_list[0]

        
        for snake in self.snake_list:
            self.snake = pygame.draw.rect(screen,(125,205,133),(snake[0] ,snake[1] ,cell_size,cell_size))
            self.snakeRect = pygame.Rect(snake[0],snake[1],cell_size,cell_size)

        self.snake_head = pygame.draw.rect(screen,"white",(self.snake_x,self.snake_y ,cell_size,cell_size))

        if self.snake_y < 1:
            self.snake_y = height -200
        elif self.snake_y > height -50:
            self.snake_y = 1

        if self.snake_x > width - 350:
            self.snake_x = 0
        elif self.snake_x < 1:
            self.snake_x = width - 350

    def get_position(self):
        return self.snake_x,self.snake_y

num_snakes = 2
snakes = [Snake(random.randint(0, 10), random.randint(0, 10), random.randint(0,1000)) for _ in range(num_snakes)]

for i,v in enumerate(snakes):
    print(f"Snake {i+1}: Energie: {v.energie}")


s = Snake(300,300,1000)

run: bool = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run: bool = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                run: bool = False

    screen.fill((30,32,25))
    spawn_grid()

    for snake in snakes:
        snake.update()

    s.fortpflanzung()
    s.energieHandler()

    clock.tick(60)
    pygame.display.update()
