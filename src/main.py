import time
import random
import sys
import pygame


pygame.init()

# TODO: Rote zellen können auch blaue töten
# IDEE: Rote Zellen können sich vermehren? 

# FONT
pygame.font.init()
fontSize = 20
font = pygame.font.Font("MinecraftRegular.otf",fontSize)
bigFont = pygame.font.Font("MinecraftRegular.otf",100)
smallFont = pygame.font.Font("MinecraftRegular.otf",50)
normalFont = pygame.font.Font("MinecraftRegular.otf",25)
diffFont = pygame.font.Font("MinecraftRegular.otf",80)
text_farbe = (255,255,255)


screenWidth = 800
screenHeight = 610
screen = pygame.display.set_mode((screenWidth,screenHeight))
caption = pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

wormSizex = 20
wormSizey = 20

greenCellTimer = pygame.time.get_ticks()
timerDurationGreen = 10000

foodTimer = pygame.time.get_ticks()
foodTimerDuration = 10000

deathTimer = pygame.time.get_ticks()
deathTimerDuration = 5000

if screenWidth == 800 and screenHeight == 610:
    rows = 50
    cols = 50
else:
    rows = 200
    cols = 200

bodySize = 18
cell_size = 18
max_cells = 100
multiplier = 1
num_cells =  random.randint(1,10)
numRedCells = random.randint(1,10)
numBlueCells = random.randint(1,10)
killOnes = False
nameTagColor = "white"
nameTagVisible = False

bacterial_names = [
    "vulcanus",
    "draconis",
    "ferno",
    "acidophilus",
    "frostii",
    "neptus",
    "thorii",
    "luxii",
    "radicatus",
    "hydrophilus",
    "xylonii",
    "aurelia",
    "germinans",
    "tempestus",
    "noctis"
]

text = random.choice(bacterial_names)
text_2 = random.choice(bacterial_names)
text_3 = random.choice(bacterial_names)

worldEnd = False
ateFood = True

speedGreen = 1
speedRed = 1

cellColor2= (205,83,103)
cellColor = (125,205,133)


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
blueCells = [[random.randint(0,cols - 1),random.randint(0,rows - 1)] for _ in range(numBlueCells)]


def worldTimer():

        timer = pygame.time.get_ticks()
        timer = timer // 1000
        
        timerText = font.render(f"{timer}s",True,"white")
        screen.blit(timerText,(750,5))

        return timer

def worldEnding():
    quitButtonBox = pygame.draw.rect(screen,(30,32,25),(300,400,220,100))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitButtonBox.collidepoint(event.pos):
                sys.exit("Bye!")


    deadEnd = bigFont.render("World ended.",True,"white")
    
    mouse = pygame.mouse.get_pos()
    quitButton = font.render("QUIT",True,"white")

    if quitButtonBox.collidepoint(mouse):
        quitButton = diffFont.render("QUIT",True,"red")
    else:
        quitButton = diffFont.render("QUIT",True,"white")


    screen.blit(deadEnd,(100,250))
    screen.blit(quitButton,(300,400))



def spawnGrid(screen):
    global x,y
    for breite in range(rows):
        for höhe in range(cols):

            x = breite * cell_size
            y = höhe  * cell_size

            pygame.draw.rect(screen,(30,32,25),(x,y,cell_size,cell_size),1)

def spawnCell():
    global num_cells

    mouse_x,mouse_y = pygame.mouse.get_pos()
    
    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size


    #print(col ,row )
    
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


    #print(col ,row )
    
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
        text_3 = "You can also respawn the cells in a random position with SPACE"

        informationHeader = bigFont.render("Game Of Life",True,"white")
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
    global nameTagColor,nameTagVisible,nameTagSurface
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

                if quitTextBox.collidepoint(event.pos):
                    sys.exit(0) # exit the whole program
                    #running = False # exit PAUSED tab

                # Aus und Einschalten von Nametags
                if nameTagBox.collidepoint(event.pos):
                    nameTagVisible = not nameTagVisible

                
               
                


        screen.fill((30,32,25))       
        mouse = pygame.mouse.get_pos()
        
        quitTextBox = pygame.draw.rect(screen,(30,32,25),(width // 2 - 200 ,height // 2 + 160,220,70))

        pauseText = font.render("PAUSED",True,(88,123,127))
        respawnButtonBox = pygame.draw.rect(screen,(30,32,25),(width // 2 - 200,height // 2 - 5 ,220,70))
        infoTextBox = pygame.draw.rect(screen,(30,32,25),(width // 2 - 200,height // 2 + 80,220,70))
        visibleText = "NAMETAG ON"
        nameTagBox = pygame.draw.rect(screen,(30,32,25),(0,0,220,50))

        if respawnButtonBox.collidepoint(mouse):
            respawnButtonText = smallFont.render("Continue",True,"green") 
        else:
            respawnButtonText = smallFont.render("Continue",True,(141,171,127)) 
        
        if infoTextBox.collidepoint(mouse):
            infoText = smallFont.render("Info",True,"green")
        else:
            infoText = smallFont.render("Info",True,(141,171,127))

        if nameTagBox.collidepoint(mouse):
            nameTagText = smallFont.render("NAMETAG",True,"green")
        else:
            nameTagText = smallFont.render("NAMETAG",True,"white")


        if quitTextBox.collidepoint(mouse):
            quitText = smallFont.render("Quit",True,"red")
        else:
            quitText = smallFont.render("Quit",True,(141,171,127))
        

        screen.blit(respawnButtonText,(width // 2 - 200, height // 2 - 5))
        screen.blit(pauseText,(width // 2 - 200 ,height // 2 - 150 ))
        screen.blit(infoText,(width // 2 - 200 ,height // 2 + 80 ))
        screen.blit(quitText,(width // 2 - 200,height // 2 + 160))
        screen.blit(nameTagText,(0,0))


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
                blueCells = [[random.randint(0,cols - 1),random.randint(0,rows - 1)] for _ in range(numBlueCells)]
                print("random seed ")
            if event.key == pygame.K_ESCAPE:
                pauseScreen(screenWidth,screenHeight,bigFont)


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not worldEnd:
                    spawnCell()
            if event.button == 3:
                if not worldEnd:
                    spawnCellRed()


    #print(num_cells)
        # NAMENSCHILDER
        
    screen.fill((30,32,25))

    
    def drawNames():
        global nameTagVisible,nameTagColor,numbers,age,text,text_2,text_3
        

        if nameTagVisible:
            nameTagColor = (255,255,255)
        else:
            nameTagColor = (30,32,25)

        greenCellTextName = font.render(text,False,nameTagColor)
        redCellTextName = font.render(text_2,False,nameTagColor)
        blueCellName = font.render(text_3,False,nameTagColor)

        for g_row,g_col in cells:
            screen.blit(greenCellTextName,(g_col * cell_size - 5,g_row * cell_size - 25))
            


        for g_row,g_col in redCells:
           screen.blit(redCellTextName,(g_col * cell_size - 5,g_row * cell_size - 25))
        
        for g_row,g_col in blueCells:
           screen.blit(blueCellName,(g_col * cell_size - 5,g_row * cell_size - 25))


    def greenCellMovement():
        for i in range(num_cells):

            direction = random.choice(["RIGHT","LEFT","UP","DOWN"])

        
            col,row = cells[i]

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
                else:
                    direction = "UP"
    
            # Update die Position der aktuellen Zelle
            cells[i] = [col,row]

    greenCellMovement()

    # FORTPFLANZUNG
    def fortpflanzung():
        global cells,num_cells,greenCellTimer
        elapsedTime = pygame.time.get_ticks() - greenCellTimer
        for row,col in cells:
            if elapsedTime >= timerDurationGreen:
                #print("Timer beim Maximum!")
                greenCellTimer = pygame.time.get_ticks()

                num_cells += 1
                cells.append([col,row])
                break

    fortpflanzung()
    
    def hungerTodRed(deathTimer,deathTimerDuration,ateFood,numRedCells):
        # global deathTimer,deathTimerDuration

        elapsedTime3 = pygame.time.get_ticks() - deathTimer
    
        # Timer zurücksetzen wenn ateFood True ist
        if ateFood:
            deathTimer = pygame.time.get_ticks()
            # print("nicht gelöscht!")

        # Wenn Timer erreicht ist und ateFood == False dann löschen
        if elapsedTime3 >= deathTimerDuration and not ateFood and numRedCells >= 1:
                deathTimer = pygame.time.get_ticks()
            
                numRedCells -= 1
                for row,col in redCells:
                    if (row,col) in redCells:
                        print("gelöscht!")
                        redCells.remove((row,col))
                        break

        elif elapsedTime3 >= deathTimerDuration and ateFood and numRedCells >= 1:
            deathTimer = pygame.time.get_ticks()
            
        # print(elapsedTime3)


        # print(elapsedTime3)

        return deathTimer,deathTimerDuration,ateFood,numRedCells

    deathTimer,deathTimerDuration,ateFood,numRedCells = hungerTodRed(deathTimer,deathTimerDuration,ateFood,numRedCells)


    def spawnFood():
        global foodTimer,foodTimerDuration,numBlueCells

        elapsedTime2 = pygame.time.get_ticks() - foodTimer
        if elapsedTime2 >= foodTimerDuration:
            foodTimer = pygame.time.get_ticks()
            numBlueCells += 1
            for col,row in blueCells:
                blueCells.append([col,row])
                break
        # print(elapsedTime2)


    spawnFood()

    def redCellMovement():
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
    
    redCellMovement()

    spawnGrid(screen)

    # BLAUE ZELLEN
    def blueCellMovement():
        for i in range(len(blueCells)):
            direction3 = random.choice(["RIGHT","LEFT","UP","DOWN"])

            col3,row3 = blueCells[i]

            if direction3 == "RIGHT" and  0 <= col3 and random.random() > rightTurn:
                if col3 < cols - 1:
                    col3 += speedGreen
                else:
                    direction3 = "LEFT"

            elif direction3 == "LEFT" and col3 > 0 and col3 < cols and random.random() > leftTurn:
                if col3 > 0:
                    col3 -= speedGreen 
                else:
                    direction3 = "RIGHT"

            elif direction3 == "UP" and row3 > 0 and 0 <= row3 and random.random() > upTurn:
                if row3 > 0:
                    row3 -= speedGreen
                else:
                    direction3 = "DOWN"

            elif direction3 == "DOWN" and row3 < rows -1 and row3 < rows and random.random() > downTurn:
                if row3 < rows - 1:
                    row3 += speedGreen
                else:
                    direction3 = "UP"
        
            blueCells[i] = col3,row3

    blueCellMovement()

    # Text
    cellAliveText = normalFont.render(f"green {num_cells}",False,(238,238,238))
    cellAliveTextBlue = normalFont.render(f"blue {numBlueCells}",False,(238,238,238))
    cellAliveTextRed = normalFont.render(f"red {numRedCells}",False,(238,238,238))
    ateFood = False

    for row2,col2 in redCells:
        redCell = pygame.draw.rect(screen,cellColor2,(col2 * cell_size ,row2 * cell_size ,cell_size,cell_size))
    
    for row3,col3 in blueCells:
        blueCell = pygame.draw.rect(screen,(88,123,127),(col3 * cell_size , row3 * cell_size, wormSizex,wormSizey)) 
    
    for row,col in cells:
        greenCell = pygame.draw.rect(screen,cellColor,(col * cell_size ,row * cell_size ,wormSizex,wormSizey))

        # Rote Zellen essen grüne Zellen
        for g_row, g_col in cells:
            greenRect = pygame.Rect(g_col * cell_size, g_row * cell_size,bodySize,bodySize)
            if redCell.colliderect(greenRect):
                ateFood = True
                num_cells -= 1
                cells.remove([g_row,g_col])
                break
            # print(ateFood)
    # Rote Zellen essen blaue Zellen
    for row,col in blueCells:
        blueRect = pygame.Rect(col * cell_size, row * cell_size,bodySize,bodySize)
        if redCell.colliderect(blueRect):
            ateFood = True
            numBlueCells -= 1
            blueCells.remove((row,col))
            break



            # Überbevölkerung
            if num_cells >= 250:
                try:
                    while num_cells >= 250:
                        num_cells -= 1
                        cells.remove(cells[i])
                        print(f"Es wurden: {num_cells - 250} getötet.")
                        break
                except Exception as e:
                    print(e)


    for g_row,g_col in redCells:
        if num_cells == 0:
            worldEnd = True
            print("Rote Zellen sterben")
            time.sleep(0.1)
            numRedCells -= 1
            redCells.remove((g_row,g_col))
        else:
            worldEnd = False

    if not worldEnd:
        worldTimer()
    else:
        worldEnding()


    def greenCellEating():
        global numBlueCells
        for row,col in blueCells:
            blueCellRect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
            if greenCell.colliderect(blueCellRect):
                numBlueCells -= 1
                blueCells.remove((row,col))
                break


            
    greenCellEating()

    screen.blit(cellAliveText,(10,20))
    screen.blit(cellAliveTextBlue,(10,50))
    screen.blit(cellAliveTextRed,(10,80))
    
    


    drawNames()
    #print(collsion)
    #print(num_cells)
    #print(numRedCells)

    pygame.display.flip()
    pygame.time.delay(0)

pygame.quit()
