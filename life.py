import time
import random
import sys
import pygame

#(0,0) (1,0) (2,0) ...
#(0,1) (1,1) (2,1) ...
#(0,2) (1,2) (2,2) ...
#...

# IDEE MAN KAN MIT MAUSTASTE FOOD SPAWNEN WO DIE ZELLEN SICH HINBEWEGEN KÖNNEN



screenWidth = 800
screenHeight = 610
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

rows = 50
cols = 50
cell_size = 18
bodyColor = "green"
spawning = False
max_cells = 100
num_cells = 0
cells = [[random.randint(0, cols - 1),random.randint(0,rows - 1)] for _ in range(num_cells)]
print(num_cells)

def spawnGrid(screen):
    global x,y
    for breite in range(rows):
        for höhe in range(cols):

            x = breite * cell_size
            y = höhe  * cell_size

            pygame.draw.rect(screen,"black",(x,y,cell_size,cell_size),1)





run = True
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill("black")
    
    #print(num_cells)
    

    for i in range(num_cells):
        direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

        col,row = cells[i]

        if direction == "RIGHT" and random.random() > 0.97:
            col += 1
            #print(f"moved to the right at {col}")
        elif direction == "LEFT" and col > 0 and random.random() > 0.97:
            col -= 1
            #print(f"moved to the left at {col}")

        elif direction == "UP" and row > 0 and random.random() > 0.97:
            row -= 1
            #print(f"moved to up at {row}")
        elif direction == "DOWN" and row < rows -1 and random.random() > 0.97:
            row += 1
            #print(f"moved down at {row}")
    
        # Update die Position der aktuellen Zelle
        cells[i] = [col,row]



    spawnGrid(screen)
    
    while num_cells < max_cells:
        time.sleep(0.01)
        print(f"spawning cells {num_cells}")
        num_cells += 1
        cells.append([random.randint(0, cols - 1),random.randint(0,rows - 1)])
        break

    #cells.remove(cells[i])

    for col,row in cells:
        pygame.draw.rect(screen,bodyColor,(col * cell_size ,row * cell_size ,cell_size,cell_size))


        

    pygame.display.flip()
    pygame.time.delay(0)

pygame.quit()
