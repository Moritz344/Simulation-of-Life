import pygame
import random
import math
import noise
import sys
import threading
import tkinter as tk 
from tkinter import *

# Diese Simulation könnte beispielsweise eine Schlange simulieren oder eine Spielende Katze.


width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Bob")
clock = pygame.time.Clock()

cell_size = 25
num_cells = 1


slider_speed_value = 2 
slider_size_value = 30



def start_ui():
    global slider_speed_value, slider_size_value

    def update_speed(value):
        global slider_speed_value
        slider_speed_value = int(value)

    def update_size(value):
        global slider_size_value
        slider_size_value = int(value)

    window = tk.Tk()
    window.title("Bob Simulation Control")
    window.geometry("500x400")  

    bild1 = tk.PhotoImage(file="icon.png")
    bild1 = bild1.subsample(2, 2)
    label2 = tk.Label(window, image=bild1)
    label2.grid(row=0, column=0, columnspan=2, pady=(10, 20),padx=(65,10))

    # Überschrift und Beschreibung
    label = tk.Label(window, text="Welcome to the Bob-Simulation!", fg="black", font=("Arial", 16))
    label.grid(row=1, column=0, columnspan=2, pady=(0, 10),padx=(60,10))

    label_0 = tk.Label(window, text="This project is part of the Simulation-of-Life GitHub repo.")
    label_0.grid(row=2, column=0, columnspan=2, pady=(0, 20),padx=(60,10))

    # Geschwindigkeitsslider
    label4 = tk.Label(window, text="Speed:", font=("Arial", 12))
    label4.grid(row=3, column=0, sticky="e", padx=(10, 5),pady=(20, 5))

    slider_speed = tk.Scale(window, from_=0, to=10, orient=HORIZONTAL, command=update_speed)
    slider_speed.set(slider_speed_value)
    slider_speed.grid(row=3, column=1, sticky="w", padx=(5, 5))

    # Größenslider
    label5 = tk.Label(window, text="Size:", font=("Arial", 12))
    label5.grid(row=4, column=0, sticky="e", pady=(20, 5))

    slider_size = tk.Scale(window, from_=0, to=30, orient=HORIZONTAL, command=update_size)
    slider_size.set(slider_size_value)
    slider_size.grid(row=4, column=1, sticky="w", padx=(5, 10))

    # Dankeschön-Label
    label3 = tk.Label(window, text="Thank you for playing this Simulation!")
    label3.grid(row=5, column=0, columnspan=2, pady=(20, 10),padx=(60,10))

    window.mainloop()



    



def help_function():
    for i,v in enumerate(bob_family):
        print(i+1,v.position)


class Bob(object):
    def __init__(self,position,size,color,speed=cell_size * 2):
        self.position = pygame.Vector2(position)
        self.size: int = size
        self.speed: int = speed
        self.time = 0
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))


        
        self.erb_color = color

        self.rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size)



        
    def noise_bewegung(self):
        self.angle = (noise.pnoise1(self.time, repeat=1024) + 1)  * math.pi 
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed 
        
        self.position.x += self.dx * 0.5
        self.position.y += self.dy * 0.5
        if random.random() > 0.78:
            self.time += 0.1
        else:
            self.time += 0.01

    def kollision_prüfen(self):
        if self.position.x >= width - self.size:
            self.position.x = self.size
        elif self.position.x <= 0 + self.size:
            self.position.x = width - self.size

        if self.position.y >= height - self.size:
            self.position.y = self.size
        elif self.position.y <= 0 + self.size:
            self.position.y = height - self.size

        

    def draw_bob(self) -> None:
        # einfacher bob zum testen
        self.rect = pygame.Rect(self.position.x,self.position.y,self.size,self.size )
        #points = [(self.position.x + self.size, self.position.y + self.size), (self.size , self.size), (self.position.x + self.size, self.position.y + self.size)]
        pygame.draw.circle(screen, self.erb_color, self.position,self.size)

    def update(self) -> None:
        self.draw_bob()
        self.noise_bewegung()
        self.kollision_prüfen()
        #self.life_span()
        #self.move()

size = 0
bob = Bob((300,400),slider_size_value,"white",slider_speed_value)
bob_family = [
        Bob((300,400),slider_size_value,"white",slider_speed_value)
]

def spawn_cells(group: list):
    for life in group:
        life.update()

def main():
    run: bool = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run: bool = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run: bool = False
        
        screen.fill(( 19, 21, 21 ))
        #help_function()
        #spawn_cells(bob_family)
        bob.speed = slider_speed_value
        bob.size = slider_size_value
        bob.update()
        clock.tick(60)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    game_thread = threading.Thread(target=main,daemon=True)
    game_thread.start()
    start_ui()
