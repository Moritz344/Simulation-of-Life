import pygame 
import math
import random
import noise

width = 1920
height = 1080
screen= pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("worm/Snake")

# Kann einen Wurm oder eine Schlange Simulieren

cell_size = 10
food_num = 0

# TODO: ui

class Food(object):
    def __init__(self,position,size):
        self.position = pygame.Vector2(position)
        self.size = size
        self.food_rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)

    def update(self):
        pygame.draw.rect(screen,"darkgreen",(self.position.x,self.position.y,self.size,self.size))
        self.food_rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)
        

class Worm(object):
    def __init__(self,position,direction,color,speed=cell_size):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.time = 0
        self.direction = direction
        self.color = color
        
        self.size = 10
        self.snake_len = 30
        self.snake_list =  [] 
        self.snake_head = [self.position.x ,self.position.y ]
        self.snake_list.append(self.snake_head)
        
        self.rect = pygame.Rect(self.position.x,self.position.y,self.size * 2, self.size * 2)

    def move(self):
        self.angle = (noise.pnoise1(self.time,repeat=1024) + 1) * math.pi
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        
        # Damit sie sich nicht in die selbe Richtung bewegen
        if self.direction == "RIGHT":
            self.position.x += self.dx
        else:
            self.position.x -= self.dx 
        if self.direction == "UP":
            self.position.y -= self.dy
        else:
            self.position.y += self.dy 
        
        self.time += 0.1

    
    def collision(self):
       if self.position.x >= width - self.size:
               self.position.x = self.size
               self.dx *= -1
       elif self.position.x <= 0 + self.size:
               self.position.x = width - self.size
               self.dx *= -1
  
       if self.position.y >= height - self.size:
               self.position.y = self.size
               self.dy *= -1
       elif self.position.y <= self.size:
           self.position.y = height - self.size
           self.dy *= -1

       for _,v in enumerate(food):
            if self.rect.colliderect(v.food_rect):
                food.remove(v)

  

    def draw_line(self):
        for snake in self.snake_list:
            pygame.draw.rect(screen,self.color,(snake[0]  ,snake[1],self.size,self.size))
            self.rect = pygame.Rect(snake[0],snake[1],self.size * 2, self.size * 2)
        self.snake_list.append((self.position.x,self.position.y  ))

        if len(self.snake_list ) > self.snake_len :
            del self.snake_list[0]


    def update(self):
        
        self.draw_line()
        self.move()
        self.collision()

life = [Worm((random.randint(0,width),random.randint(0,height)),random.choice(["LEFT","RIGHT","UP","DOWN"]),"white",cell_size) for _ in range(10)]
worm = Worm((random.randint(0,width),random.randint(0,height)),random.choice(["LEFT","RIGHT","UP","DOWN"]),"white",cell_size)

food = [Food((300,0),10) for _ in range(food_num)]

def spawn_object(group):
    for life in group:
        life.update()

def spawn_food():
    global food_num
    mouse_x,mouse_y = pygame.mouse.get_pos()


    food_num += 1
    new_food = Food((mouse_x,mouse_y),20)
    food.append(new_food)
def del_food():
    global food_num

    mouse_pos = pygame.mouse.get_pos()
    
    for _,v in enumerate(food):
        if v.food_rect.collidepoint(mouse_pos):
            food_num -= 1
            food.remove(v)


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            run = False

    screen.fill("black")

    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        spawn_food()
    if pressed[2]:
        del_food()

    spawn_object(food)
    spawn_object(life)


    clock.tick(60)
    pygame.display.update()
pygame.quit()
