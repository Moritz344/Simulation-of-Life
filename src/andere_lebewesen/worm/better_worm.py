import pygame 
import math
import random
import noise
import tkinter as tk
from tkinter import *
import threading
import sys

width = 800
height = 600
screen= pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("worm/Snake")

#Kann einen Wurm oder eine Schlange Simulieren

cell_size = 4
food_num = 0
creature_len = 20

# TODO: ein button der alle settings zu standard wechselt
# TODO: 

def settings_ui():
    window = tk.Tk()
    window.title("Settings")
    window.geometry("300x200")
    
    header = tk.Label(window,text="Settings",font=("opensans",30),bg="black",fg="green")
    header.grid(row=0,column=0)

    hello = tk.Label(window,text="Here you can change the settings of the creatures.")
    hello.grid(row=2,column=0,pady=0,padx=10)


    frame0 = tk.Frame(window,width=100,height=100)
    frame0.grid()

    def update_speed(val):
        for _,v in enumerate(life):
            v.speed = int(val)

    def update_time(val):
        for _,v in enumerate(life):
            v.time_add = float(val)
    def change_length(val):
        for _,v in enumerate(life):
            v.snake_len = int(val )

    speed_text = tk.Label(frame0,text="Speed:")
    speed_text.grid(pady=0,padx=20,sticky="w")

    time_text = tk.Label(frame0,text="Verändert Verhalten:")
    time_text.grid(pady=0,padx=20,sticky="w")
    

    slider = tk.Scale(frame0,orient=HORIZONTAL,from_=1,to_=20,command=update_speed)
    slider.set(4)
    slider.grid(row=0,column=1,sticky="n")

    time = tk.Scale(frame0,orient=HORIZONTAL,from_=0.01,resolution=0.01,to_=1,command=update_time)
    time.set(0.01)
    time.grid(row=1,column=1,sticky="n",pady=0,padx=0)

    #creature_length = tk.Scale(frame0,orient=HORIZONTAL,from_=0,resolution=1,to_=30,command=change_length)
    #creature_length.set(20)
    #creature_length.grid(row=2,column=1,sticky="e")

    window.mainloop()

class Food(object):
    def __init__(self,position,size):
        self.position = pygame.Vector2(position)
        self.size = size
        self.food_rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)

    def update(self):
        pygame.draw.rect(screen,"darkgreen",(self.position.x,self.position.y,self.size,self.size))
        self.food_rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)
        

class Worm(object):
    def __init__(self,position,direction,color,snake_len,speed=4):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.time = 0
        self.time_add = 0.01
        self.direction = direction
        self.color = color
        
        self.size = 10
        self.snake_list =  [] 
        self.snake_len = snake_len
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
        
        self.time += self.time_add

    
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

life = [Worm((random.randint(0,width),random.randint(0,height)),random.choice(["LEFT","RIGHT","UP","DOWN"]),"white",creature_len,cell_size) for _ in range(10)]
worm = Worm((random.randint(0,width),random.randint(0,height)),random.choice(["LEFT","RIGHT","UP","DOWN"]),"white",creature_len,cell_size)

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

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                run = False

        screen.fill("black")
    
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            spawn_food()
        elif pressed[2]:
            del_food()
    
        spawn_object(food)
        spawn_object(life)
    
    
        clock.tick(60)
        pygame.display.update()
if __name__ == "__main__":
    try:
     game_thread = threading.Thread(target=main,daemon=True)
     game_thread.start()
     settings_ui()
    except Exception as e:
        print(e)
