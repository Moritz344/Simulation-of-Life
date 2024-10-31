import time
import random
import sys
import pygame

#(0,0) (1,0) (2,0) ...
#(0,1) (1,1) (2,1) ...
#(0,2) (1,2) (2,2) ...
#...


pygame.init()

# FONT
pygame.font.init()
font = pygame.font.SysFont("Open Sans",20)
text_farbe = (255,255,255)

screenWidth = 800
screenHeight = 610
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

bodySize = 18
rows = 50
cols = 50
cell_size = 18
bodyColor = (124,252,0)
max_cells = 100
multiplier = 1
delCellRed = []
num_cells = 100
numRedCells = 1
killOnes = False
predatorNear = False
speed = 1

# Warscheinlichkeiten standard werte
rightTurn = 0.97
leftTurn = 0.97
upTurn = 0.97
downTurn = 0.97

cells = [[random.randint(0, cols - 1),random.randint(0,rows - 1)] for _ in range(num_cells)]
redCells = [[random.randint(0,cols - 1),random.randint(0,rows - 1)] for _ in range(numRedCells)]

print(num_cells)
print(numRedCells)

def spawnGrid(screen):
    global x,y
    for breite in range(rows):
        for höhe in range(cols):

            x = breite * cell_size
            y = höhe  * cell_size

            pygame.draw.rect(screen,"black",(x,y,cell_size,cell_size),1)



def spawnCell():
    global num_cells

    mouse_x,mouse_y = pygame.mouse.get_pos()
    
    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size


    print(col ,row )
    
    # GÜLTIGEN BEREICH SPAWNEN
    if 0 <= col < cols and 0 <= row < rows:
        cells.append([row - 1, col - 1])
        num_cells += 1



run = True
while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_SPACE:
                cells = [[random.randint(0, cols - 1),random.randint(0,rows - 1)] for _ in range(num_cells)]
                redCells = [[random.randint(0,cols - 1),random.randint(0,rows - 1)] for _ in range(numRedCells)]
                
                print("random seed ")
                #print("spawned food at random position.")

        if event.type == pygame.MOUSEBUTTONDOWN:
            spawnCell()

    screen.fill("black")
    #print(num_cells)

    

    for i in range(num_cells):
        direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

        col,row = cells[i]

        if direction == "RIGHT" and random.random() > rightTurn and 0 <= col :
            col += speed
            #print(f"moved to the right at {col}")
        elif direction == "LEFT" and col > 0 and random.random() > leftTurn and col < cols:
            col -= speed
            #print(f"moved to the left at {col}")

        elif direction == "UP" and row > 0 and random.random() > upTurn and 0 <= row:
            row -= speed
            #print(f"moved to up at {row}")
        elif direction == "DOWN" and row < rows -1 and random.random() > downTurn and row < rows - 1:
            row += speed
            #print(f"moved down at {row}")
    
        # Update die Position der aktuellen Zelle

            
        print("X",col,"Y:",row)
        cells[i] = [col,row]


    for i in range(numRedCells):
        direction2 = random.choice(["RIGHT","LEFT","UP","DOWN"])

        col2,row2 = redCells[i]

        if direction2 == "RIGHT" and random.random() > 0.97 and 0 <= col2:
            col2 += 1
        elif direction2 == "LEFT" and col2 > 0 and random.random() > 0.97 and col2 < cols:
            col2 -= 1
        elif direction2 == "UP" and row2 > 0 and random.random() > 0.97 and 0 <= row2:
            row2 -= 1
        elif direction2 == "DOWN" and row2 < rows -1 and random.random() > 0.97 and row2 < rows :
            row2 += 1
        
        redCells[i] = col2,row2


    spawnGrid(screen)

    #while numRedCells < 50:
        #numRedCells += 1
        #redCells.append([random.randint(0,cols - 1),random.randint(0,rows - 1)])
        #break
       
    #num_cells += multiplier
    #cells.append([random.randint(0, cols - 1),random.randint(0,rows - 1)])
    #if num_cells == 10:
        #multiplier = 0

    

    #cells.remove(cells[i])


    
    cellAliveText = font.render(f"Cells: {num_cells}",False,(255,255,255))

    for row2,col2 in redCells:
        redCell = pygame.draw.rect(screen,"red",(col2 * cell_size ,row2 * cell_size ,cell_size,cell_size))
        areaDetect = pygame.draw.rect(screen,"black",(col2 * cell_size - 40,row2 * cell_size - 40,cell_size + 300,cell_size + 100),1)

    for row,col in cells:
        greenCell = pygame.draw.rect(screen,bodyColor,(col * cell_size ,row * cell_size ,bodySize,bodySize))
        box = pygame.draw.rect(screen,"black",(col * cell_size,row * cell_size,20,20),2)


        



        
        # Die gesamten Grünen Zellen prüfen
        for g_row, g_col in cells:
            greenRect = pygame.Rect(g_col * cell_size, g_row * cell_size,bodySize,bodySize)
            if redCell.colliderect(greenRect):
                for i in range(num_cells):
                        num_cells -= 1
                        cells.remove(cells[i])
                        break

            elif greenRect.colliderect(areaDetect):
                for row,col in redCells:
                    print(f"green cell at {g_row,g_col}")
                    speed = 2 
                    #upTurn = 0.1
            else:
                #upTurn = 0.97
                speed = 1

    screen.blit(cellAliveText,(10,10))

    #print(collsion)
    #print(num_cells)
    #print(numRedCells)

    pygame.display.flip()
    pygame.time.delay(0)

pygame.quit()
