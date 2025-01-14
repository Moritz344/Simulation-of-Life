import pygame
import random

width = 1920
height = 1080
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Worm Organism")

rows: int = 50
cols: int = 50
cell_size: int = 30




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


        self.snake_len: int = length
        self.snake_list = []

        self.direction = "RIGHT"

        self.snake_head = [self.snake_x ,self.snake_y ]
        self.snake_list.append(self.snake_head)

        self.snakeRect = pygame.Rect(self.snake_x, self.snake_y, cell_size, cell_size)


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

        self.snakeRect = pygame.Rect(self.snake_x, self.snake_y, cell_size, cell_size)
        
        for snake in self.snake_list:
            self.snake = pygame.draw.rect(screen,(125,205,133),(snake[0] ,snake[1] ,cell_size,cell_size))
            self.snakeRect = pygame.Rect(snake[0],snake[1],cell_size,cell_size)

        self.snake_head = pygame.draw.rect(screen,"white",(self.snake_x,self.snake_y ,cell_size,cell_size))

        if self.snake_y < 1:
            self.snake_y = height 
        elif self.snake_y > height :
            self.snake_y = 1

        if self.snake_x > width :
            self.snake_x = 0
        elif self.snake_x < 1:
            self.snake_x = width

    def get_position(self):
        return self.snake_x,self.snake_y

num_snakes = 1
num_food = 100
snakes = [Snake(random.randint(0, 900), random.randint(0, 900), random.randint(0,50000)) for _ in range(num_snakes)]


s: object = Snake(0,0,0)

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

    clock.tick(60)
    pygame.display.update()
