import time
import random
import sys
import pygame

# Letzte Bearbeitung: 02.11.24

# SPAGHETTI CODE

# TODO: SETTINGS MENU
# IDEE: Predator können satt werden und die grünen zellen nicht mehr essen

pygame.init()

# FONT
pygame.font.init()
font = pygame.font.SysFont("Open Sans",20)
bigFont = pygame.font.SysFont("Open Sans",100)
smallFont = pygame.font.SysFont("Open Sans",50)
normalFont = pygame.font.SysFont("Open Sans",25)

text_farbe = (255,255,255)

screenWidth = 800
screenHeight = 610
screen = pygame.display.set_mode((screenWidth,screenHeight))
caption = pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

if screenWidth == 800 and screenHeight == 610:
    rows = 50
    cols = 50
else:
    rows = 200
    cols = 200

bodySize = 18
cell_size = 18
bodyColor = (124,252,0)
max_cells = 100
multiplier = 1
delCellRed = []
num_cells =  0
numRedCells = 1 # Fix this <-- Program crashed wenn auf 0
killOnes = False
predatorNear = False

speedGreen = 1
speedRed = 1

# Warscheinlichkeiten standard werte
rightTurn = 0.97
leftTurn = 0.97
upTurn = 0.97
downTurn = 0.97

rightTurnRed = 0.97
leftTurnRed = 0.97
upTurnRed = 0.97
downTurnRed = 0.97

cells = [[random.randint(0, cols - 1),random.randint(0,rows - 1)] for _ in range(num_cells)]
redCells = [[random.randint(0,cols - 1),random.randint(0,rows - 1)] for _ in range(numRedCells)]

#print(num_cells)
#print(numRedCells)

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


def spawnCellRed():
    global numRedCells

    mouse_x,mouse_y = pygame.mouse.get_pos()
    
    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size


    print(col ,row )
    
    # GÜLTIGEN BEREICH SPAWNEN
    if 0 <= col < cols and 0 <= row < rows:
        redCells.append([row , col ])
        numRedCells += 1

def infoScreen():
    runner = True
    while runner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit(0)
                if event.key == pygame.K_ESCAPE:
                    runner = False
        screen.fill("black")
        text = "This Game simulates small pixel living in a small grid."
        text_2 = "You can spawn cells with your mouse buttons."
        text_3 = "You can also respawn the cells in a random position with <SPACE>"

        informationHeader = bigFont.render("Game Of Life",False,"white")
        infoText = normalFont.render(text,False,"white")
        infoText_2 = normalFont.render(text_2,False,"white")
        infoText_3 = normalFont.render(text_3,False,"white")

        infoText_4 = normalFont.render("READ MORE ON MY GITHUB: @Moritz344",False,"red")
        
        screen.blit(informationHeader,(100,0))
        screen.blit(infoText,(5,200))
        screen.blit(infoText_2,(5,250))
        screen.blit(infoText_3,(5,300))
        screen.blit(infoText_4,(10,400))

        pygame.display.update()
        clock.tick(60)

def pauseScreen(width,height,font):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if respawnButtonBox.collidepoint(event.pos):
                    running = False

                if infoTextBox.collidepoint(event.pos):
                    infoScreen()
                    running = False

        screen.fill("black")       
        mouse = pygame.mouse.get_pos()

        pauseText = font.render("PAUSED",False,(255,255,255))
        respawnButtonBox = pygame.draw.rect(screen,"black",(width // 2 - 200,height // 2 - 5 ,220,70))

        infoTextBox = pygame.draw.rect(screen,"black",(width // 2 - 200,height // 2 + 80,220,70))

        if respawnButtonBox.collidepoint(mouse):
            respawnButtonText = smallFont.render("Continue",False,"green") 
        else:
            respawnButtonText = smallFont.render("Continue",False,"white") 
        
        if infoTextBox.collidepoint(mouse):
            infoText = smallFont.render("Info",False,"green")
        else:
            infoText = smallFont.render("Info",False,"white")



        

        screen.blit(respawnButtonText,(width // 2 - 200, height // 2 - 5))
        screen.blit(pauseText,(width // 2 - 200 ,height // 2 - 150 ))
        screen.blit(infoText,(width // 2 - 200 ,height // 2 + 80 ))



        clock.tick(60)
        pygame.display.update()


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
            if event.key == pygame.K_ESCAPE:
                pauseScreen(screenWidth,screenHeight,bigFont)


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                spawnCell()
            if event.button == 3:
                spawnCellRed()


    screen.fill("black")
    #print(num_cells)

    

    for i in range(num_cells):
        direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

        col,row = cells[i]

        new_col,new_row = col,row

        if direction == "RIGHT" and random.random() > rightTurn :
            if col < cols - 1:
                col += speedGreen
            else:
                direction = "LEFT"

            #print(f"moved to the right at {col}")
        elif direction == "LEFT" and random.random() > leftTurn :
            if col > 0:
                col -= speedGreen
            else:
                direction = "RIGHT"

        elif direction == "UP" and random.random() > upTurn :
            if row > 0:
                row -= speedGreen
            else:
                direction = "DOWN"

        elif direction == "DOWN" and random.random() > downTurn :
            if row < rows - 1:
                row += speedGreen
    
        # Update die Position der aktuellen Zelle
        cells[i] = [col,row]


    for i in range(numRedCells):
        direction2 = random.choice(["RIGHT","LEFT","UP","DOWN"])

        col2,row2 = redCells[i]

        if direction2 == "RIGHT" and  0 <= col2:
            if col2 < cols - 1:
                col2 += speedRed
            else:
                direction = "LEFT"

        elif direction2 == "LEFT" and col2 > 0 and col2 < cols:
            if col2 > 0:
                col2 -= speedRed
            else:
                direction = "RIGHT"

        elif direction2 == "UP" and row2 > 0 and 0 <= row2:
            if row2 > 0:
                row2 -= speedRed
            else:
                direction = "DOWN"

        elif direction2 == "DOWN" and row2 < rows -1 and row2 < rows :
            if row2 < rows - 1:
                row2 += speedRed
            else:
                direction = "UP"
        

        redCells[i] = col2,row2

        #print(col2,row2)


    spawnGrid(screen)



    
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
                    num_cells -= 1
                    cells.remove([g_row,g_col])
                    break

            elif greenRect.colliderect(areaDetect):
                for row,col in redCells:
                    try:
                        while cells[i] != redCells[i]:
                            row = g_row
                            col = g_col
                            break
                    except Exception as e:
                        print(f"Program Error: Platziere die Rote Zelle nicht auf der Grünen! {e}")
                        sys.exit(0)

            # Überbevölkerung
            elif num_cells >= 250:
                try:
                    while num_cells >= 250:
                        num_cells -= 1
                        cells.remove(cells[i])
                        print(f"Es wurden: {num_cells - 250} getötet.")
                        break
                except Exception as e:
                    print(e)

            else:
                speed = 1

    screen.blit(cellAliveText,(10,10))

    #print(collsion)
    #print(num_cells)
    #print(numRedCells)

    pygame.display.flip()
    pygame.time.delay(0)

pygame.quit()
