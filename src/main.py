import time
import random
import sys
import pygame
from termcolor import cprint,colored

pygame.init()



# Zellen aussehen verändern

# Grüne Zellen :
# - können sich vermehren
# - töten blaue zellen
# - TODO: können verhungern

# Blaue Zellen:
# - können sich vermehren
# - TODO: können verhungern

# Rote Zellen:
# - töten Blaue und Grüne Zellen
# - können sich vermehren
# - können an Hunger sterben

# FONT
pygame.font.init()
fontSize: int =  20
font = pygame.font.Font("MinecraftRegular.otf", fontSize)
bigFont = pygame.font.Font("MinecraftRegular.otf", 100)
smallFont = pygame.font.Font("MinecraftRegular.otf", 50)
normalFont = pygame.font.Font("MinecraftRegular.otf", 25)
diffFont = pygame.font.Font("MinecraftRegular.otf", 80)
text_farbe = (255, 255, 255)


screenWidth: int =  800 
screenHeight: int = 610 

#rows = screenWidth // 4
#cols = screenHeight // 4

# if screenWidth == 800 and screenHeight == 610:
rows: int =  70 
cols: int = 70
# else:
# rows = 200
# cols = 200
world2: bool = False
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
caption = pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()

wormSizex: int = 10#20
wormSizey: int = 10#20

blueCellBodyBlock: int = 0


# Timer 1000 = 1sk
greenCellTimer = pygame.time.get_ticks()
timerDurationGreen = 5000

# fortpflanzungs timer blaue zellen
foodTimer = pygame.time.get_ticks()
foodTimerDuration = 12000

# Hungertod timer blaue zellen
deathTimerBlue = pygame.time.get_ticks()
deathTimerBlueDur = 1000

# fortpflanzungs timer rote Zelle
redCellTimer = pygame.time.get_ticks()
timerDurationRed = 15000

# Hungertod rote zelle
deathTimer = pygame.time.get_ticks()
deathTimerDuration = timerDurationRed // 2

# Hungertod grüne Zellen 
greenCellTimerDeath = pygame.time.get_ticks()
greenCellTimerDeathDuration = 8000

eventTimer = pygame.time.get_ticks()

# datetime

bodySize = 10#18
cell_size = 10#18
max_cells = 100
multiplier = 1
num_cells = random.randint(1, 10)
numRedCells = random.randint(1, 10)
numBlueCells = random.randint(1, 10)
killOnes = False
nameTagColor = "white"
nameTagVisible = False

bacterial_names = [
    "vulcanus", "draconis", "ferno", "acidophilus", "frostii", "neptus",
    "thorii", "luxii", "radicatus", "hydrophilus", "xylonii", "aurelia",
    "germinans", "tempestus", "noctis"
]

text = random.choice(bacterial_names)
text_2 = random.choice(bacterial_names)
text_3 = random.choice(bacterial_names)

worldEnd = False
ateFood = True
ateFoodGreen = True
ateFoodBlue = True

speedGreen = 1
speedRed = 1

cellColor2 = (205, 83, 103)
cellColor = (125, 205, 133)

# Warscheinlichkeiten standard werte
rightTurn = 0.97
leftTurn = 0.97
upTurn = 0.97
downTurn = 0.97

rightTurnRed = 0.97
leftTurnRed = 0.97
upTurnRed = 0.97
downTurnRed = 0.97

cells = [[random.randint(0, cols - 1),
          random.randint(0, rows - 1)] for _ in range(num_cells)]
redCells = [[random.randint(0, cols - 1),
             random.randint(0, rows - 1)] for _ in range(numRedCells)]
blueCells = [[random.randint(0, cols - 1),
              random.randint(0, rows - 1)] for _ in range(numBlueCells)]

colorText = "+--- Logs will appear here ---+"
colorText = colored(colorText,"red")
def textAnimation(text: str):

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)
    print()

# textAnimation(colorText)

class Events(object):
    def __init__(self,):
        self.eventList = ["vermehrung"]
        self.timer = None
    def startTimer(self):
        self.timer = pygame.time.get_ticks()
    def handleTimer(self,timerDuration):
        self.dur = timerDuration
        if self.timer is None:
            print("Timer wurde nicht gestartet!")
            return False
        elapsedTime = pygame.time.get_ticks() - self.timer
        # print(elapsedTime,"ms")
        if elapsedTime >= self.dur and random.random() > 0.99:
            self.timer = pygame.time.get_ticks()
            e.randomEvent()

    def randomEvent(self):
        self.currentEvent = random.choice(self.eventList)
        if self.currentEvent == "vermehrung" and random.random() > 0.67:
            e.fortpflanzungsEvent()
        else:
            e.reset()
    def ausgabe(self):
        print(f"AN EVENT ACCURED!!! [{self.currentEvent}]")

    def fortpflanzungsEvent(self):
        global foodTimerDuration,timerDurationGreen
        cprint("[EVENT]: fortpflanzung","yellow")
        foodTimerDuration = 1000
        timerDurationGreen = 1000

    def reset(self):
        global foodTimerDuration,timerDurationGreen
        foodTimerDuration = 12000
        timerDurationGreen = 5000

e = Events()
e.startTimer()
print(foodTimerDuration)
def world_2():
    global x,y
    num_cells_2 = 1
    cells_2 = [[random.randint(0, cols - 1),
          random.randint(0, rows - 1)] for _ in range(num_cells_2)]
    run: bool = True

    t: int = 0
    p: float = 1.15
    init_cell = num_cells_2
    color = "green"
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run: bool = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run: bool = False

        
        screen.fill((30, 32, 25))
        spawnGrid(screen)
        twert: int =  1  
        t += twert
        #print(t)
        new_cell_count = round(init_cell * p ** t) - len(cells_2)
        # print(new_cell_count)
        for _ in range(new_cell_count):
            new_cell = [random.randint(0, cols - 1), random.randint(0, rows - 1)]
            #new_cell = [100,100]
            cells_2.append(new_cell)
        #if new_cell_count >= 1:
            #t = 0
        #else:
        #t += 1

        for row,col in cells_2:
            pygame.draw.rect(screen,color,(row * cell_size,col * cell_size ,cell_size,cell_size))


        if new_cell_count >= 6253:
            time.sleep(3)
            run: bool = False
            


            
        pygame.display.update()
        clock.tick(60)

def world_3():
    # BLUE CELL INVASION
    blueCellTimer = pygame.time.get_ticks()
    blueCellTimerDur = 100

    numNewCells = 100
    new_cells = [[random.randint(0, cols - 1), random.randint(0, rows - 1)] for _ in range(numNewCells)]

    num_blue_new = 1
    blue_new_cells = [[random.randint(0, cols - 1), random.randint(0, rows - 1)] for _ in range(num_blue_new)] 
    cprint(f"[INVASION]: BLUE CELL INVASION!","blue")
    run: bool = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run: bool = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    run: bool = False

        screen.fill((30,32,25))
        # screen.fill("black")
        spawnGrid(screen)

        def blueCellInvasion(blueCellTimer,num_blue_new,blue_new_cells):

            elapsedTime = pygame.time.get_ticks() - blueCellTimer

            if elapsedTime >= blueCellTimerDur:
                    # print("spawn")
                    blueCellTimer = pygame.time.get_ticks()

                    for row,col in blue_new_cells:
                        #print("work")
                        num_blue_new += 1
                        blue_new_cells.append((row,col))
                        break

            # print(elapsedTime)
            return blueCellTimer,num_blue_new,blue_new_cells
                    
        blueCellTimer, num_blue_new,blue_new_cells= blueCellInvasion(blueCellTimer,num_blue_new,blue_new_cells)           
            
        def NewCellMovement():
            for i in range(numNewCells):

             direction = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])

             col, row = new_cells[i]

             if direction == "RIGHT" and random.random() > 0.97:
                 if col < cols - 1:
                     col += 1
                 else:
                     direction = "LEFT"

                 # print(f"moved to the right at {col}")
             elif direction == "LEFT" and random.random() > 0.97:
                 if col > 0:
                     col -= 1
                 else:
                     direction = "RIGHT"

             elif direction == "UP" and random.random() > 0.97:
                 if row > 0:
                     row -= 1
                 else:
                     direction = "DOWN"

             elif direction == "DOWN" and random.random() > 0.97:
                 if row < rows - 1:
                     row += 1
                 else:
                     direction = "UP"

             # Update die Position der aktuellen Zelle
             new_cells[i] = [col, row]

        NewCellMovement()


        def NewCellMovementBlue():
            for i in range(num_blue_new):

             direction = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])

             col, row = blue_new_cells[i]

             if direction == "RIGHT" and random.random() > 0.97:
                 if col < cols - 1:
                     col += 1
                 else:
                     direction = "LEFT"

                 # print(f"moved to the right at {col}")
             elif direction == "LEFT" and random.random() > 0.97:
                 if col > 0:
                     col -= 1
                 else:
                     direction = "RIGHT"

             elif direction == "UP" and random.random() > 0.97:
                 if row > 0:
                     row -= 1
                 else:
                     direction = "DOWN"

             elif direction == "DOWN" and random.random() > 0.97:
                 if row < rows - 1:
                     row += 1
                 else:
                     direction = "UP"

             # Update die Position der aktuellen Zelle
             blue_new_cells[i] = [col, row]

        NewCellMovementBlue()

        for row2,col2 in blue_new_cells:
            b = pygame.draw.rect(screen,"blue",(row2 * cell_size ,col2 * cell_size,cell_size,cell_size))

        for row,col in new_cells:
            g = pygame.draw.rect(screen,"green",(row * cell_size ,col * cell_size,cell_size,cell_size))
        




        pygame.display.update()
        clock.tick(60)


def worldMenu():
    run: bool = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run: bool = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run: bool = False
                elif event.key == pygame.K_q:
                    run: bool = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if box_1.collidepoint(event.pos):
                    world_2()
                    # print("klick!")
                if back_text_box.collidepoint(event.pos):
                    run: bool = False

                if box_2.collidepoint(event.pos):
                    world_3()

        mouse = pygame.mouse.get_pos()
        screen.fill((44, 48, 46))
        text_1 = smallFont.render("world_2",False,"white")
        text_2 = smallFont.render("world_3",False,"white")
        box_1 = pygame.draw.rect(screen,"green",(40,60,200,200),5)
        box_2 = pygame.draw.rect(screen,"green",(300,60,200,200),5)
        
        back_text = smallFont.render("BACK",False,"blue")
        back_text_box = pygame.draw.rect(screen,(44, 48, 46),(10,540,130,100))
        pygame.draw.rect(screen,"green",(40,60, 200, 200))
        pygame.draw.rect(screen,"blue",(300,60, 200, 200))
        image_box_2 = smallFont.render("2",False,"white")
        image_text_3 = smallFont.render("3",False,"white")
        if box_2.collidepoint(mouse):
            box_2 = pygame.draw.rect(screen,"green",(300,60,200,200),5)
        else:
            box_2 = pygame.draw.rect(screen,"white",(300,60,200,200),5)

        if box_1.collidepoint(mouse):
            box_1 = pygame.draw.rect(screen,"green",(40,60,200,200),5)
        else:
            box_1 = pygame.draw.rect(screen,"white",(40,60,200,200),5)
        
        if back_text_box.collidepoint(mouse):
            back_text = smallFont.render("BACK",False,"green")
        else:
            back_text = smallFont.render("BACK",False,"white")

    
        screen.blit(image_box_2,(120,130))
        screen.blit(image_text_3,(380,130))
        screen.blit(back_text,(10,540))
        screen.blit(text_1,(50,10))
        screen.blit(text_2,(300,10))
        pygame.display.update()
        clock.tick()

    
def worldTimer():

    timer = pygame.time.get_ticks()
    timer = timer // 1000

    timerText = font.render(f"{timer}s", True, "red")
    screen.blit(timerText, (750, 5))

    return timer


def worldEnding():
    quitButtonBox = pygame.draw.rect(screen, (30, 32, 25),
                                     (300, 400, 220, 100))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitButtonBox.collidepoint(event.pos):
                sys.exit("Bye!")

    deadEnd = bigFont.render("World ended.", True, "white")

    mouse = pygame.mouse.get_pos()
    quitButton = font.render("QUIT", True, "white")

    if quitButtonBox.collidepoint(mouse):
        quitButton = diffFont.render("QUIT", True, "red")
    else:
        quitButton = diffFont.render("QUIT", True, "white")

    screen.blit(deadEnd, (100, 250))
    screen.blit(quitButton, (300, 400))


def spawnGrid(screen):
    global x, y
    for breite in range(rows):
        for höhe in range(cols):

            x = breite * cell_size
            y = höhe * cell_size
            # 30 32 25
            pygame.draw.rect(screen, (30,32,25),
                             (x, y, cell_size, cell_size), 1)


def spawnCell():
    global num_cells

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size

    # print(col ,row )

    # GÜLTIGEN BEREICH SPAWNEN
    if 0 <= col < cols and 0 <= row < rows:
        cells.append([row - 1, col - 1])
        num_cells += 1
        cprint(f"[{num_cells}] spawned green cell with mouse button.","green")


def spawnCellRed():
    global numRedCells

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size

    # print(col ,row )

    # GÜLTIGEN BEREICH SPAWNEN
    if 0 <= col < cols and 0 <= row < rows:
        redCells.append([row, col])
        numRedCells += 1

        cprint(f"[{numRedCells}] spawned red cell with mouse button.","red")


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

        informationHeader = bigFont.render("Game Of Life", True, "white")
        infoText = normalFont.render(text, False, "white")
        infoText_2 = normalFont.render(text_2, False, "white")
        infoText_3 = normalFont.render(text_3, False, "white")

        infoText_4 = normalFont.render("READ MORE ON MY GITHUB: @Moritz344",
                                       False, "red")

        screen.blit(informationHeader, (100, 0))
        screen.blit(infoText, (5, 200))
        screen.blit(infoText_2, (5, 250))
        screen.blit(infoText_3, (5, 300))
        screen.blit(infoText_4, (10, 400))

        pygame.display.update()
        clock.tick(60)

def pauseScreen(width, height, font):
    global nameTagColor, nameTagVisible, nameTagSurface
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
                    sys.exit(0)  # exit the whole program
                    # running = False # exit PAUSED tab

                # Aus und Einschalten von Nametags
                if nameTagBox.collidepoint(event.pos):
                    nameTagVisible = not nameTagVisible
                if worldsTextBox.collidepoint(event.pos):
                    worldMenu()
                    

        screen.fill((30, 32, 25))
        mouse = pygame.mouse.get_pos()

        quitTextBox = pygame.draw.rect(
            screen, (30, 32, 25),
            (width // 2 - 200, height // 2 + 160, 220, 70))

        pauseText = font.render("PAUSED", True, (88, 123, 127))
        respawnButtonBox = pygame.draw.rect(
            screen, (30, 32, 25), (width // 2 - 200, height // 2 - 5, 220, 70))
        infoTextBox = pygame.draw.rect(
            screen, (30, 32, 25),
            (width // 2 - 200, height // 2 + 80, 220, 70))
        visibleText = "NAMETAG ON"
        nameTagBox = pygame.draw.rect(screen, (30, 32, 25), (0, 0, 220, 50))

        worldsTextBox = pygame.draw.rect(screen,(30,32,25),(width // 2 - 200, height // 2 + 240, 220, 70))
        
        if worldsTextBox.collidepoint(mouse):
            worldsText = smallFont.render("Worlds",True,"green")
        else:
            worldsText = smallFont.render("Worlds",True,(141,171,127))

        if respawnButtonBox.collidepoint(mouse):
            respawnButtonText = smallFont.render("Continue", True, "green")
        else:
            respawnButtonText = smallFont.render("Continue", True,
                                                 (141, 171, 127))

        if infoTextBox.collidepoint(mouse):
            infoText = smallFont.render("Info", True, "green")
        else:
            infoText = smallFont.render("Info", True, (141, 171, 127))

        if nameTagBox.collidepoint(mouse):
            nameTagText = smallFont.render("NAMETAG", True, "green")
        else:
            nameTagText = smallFont.render("NAMETAG", True, "white")

        if quitTextBox.collidepoint(mouse):
            quitText = smallFont.render("Quit", True, "red")
        else:
            quitText = smallFont.render("Quit", True, (141, 171, 127))

        screen.blit(respawnButtonText, (width // 2 - 200, height // 2 - 5))
        screen.blit(pauseText, (width // 2 - 200, height // 2 - 150))
        screen.blit(infoText, (width // 2 - 200, height // 2 + 80))
        screen.blit(quitText, (width // 2 - 200, height // 2 + 160))
        screen.blit(nameTagText, (0, 0))
        screen.blit(worldsText, (width // 2 - 200, height // 2 + 240))

        clock.tick(60)
        pygame.display.update()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
            if event.key == pygame.K_SPACE:
                cells = [[
                    random.randint(0, cols - 1),
                    random.randint(0, rows - 1)
                ] for _ in range(num_cells)]
                redCells = [[
                    random.randint(0, cols - 1),
                    random.randint(0, rows - 1)
                ] for _ in range(numRedCells)]
                blueCells = [[
                    random.randint(0, cols - 1),
                    random.randint(0, rows - 1)
                ] for _ in range(numBlueCells)]
                print("random seed ")
            if event.key == pygame.K_ESCAPE:
                pauseScreen(screenWidth, screenHeight, bigFont)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not worldEnd:
                    spawnCell()
            if event.button == 3:
                if not worldEnd:
                    spawnCellRed()
        if event.type == pygame.MOUSEWHEEL:
            #  Holen der Mausposition vor dem Zoom
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.y == 1:
                # Zoom rein
                cell_size += 1
                wormSizex += 1
                wormSizey += 1
            else:
                # Zoom raus
                wormSizex -= 1
                wormSizey -= 1
                cell_size -= 1


    # print(num_cells)
    # NAMENSCHILDER
    screen.fill((30, 32, 25))
    e.handleTimer(random.randint(2000,5000))
    def drawNames():
        global nameTagVisible, nameTagColor, numbers, age, text, text_2, text_3

        if nameTagVisible:
            nameTagColor = (255, 255, 255)
        if not nameTagVisible:
            nameTagColor = (30, 32, 25, 0)

        greenCellTextName = font.render(text, False, nameTagColor)
        redCellTextName = font.render(text_2, False, nameTagColor)
        blueCellName = font.render(text_3, False, nameTagColor)

        for g_row, g_col in cells:
            screen.blit(greenCellTextName,
                        (g_col * cell_size - 20, g_row * cell_size - 25))

        for g_row, g_col in redCells:
            screen.blit(redCellTextName,
                        (g_col * cell_size - 20, g_row * cell_size - 25))

        for g_row, g_col in blueCells:
            screen.blit(blueCellName,
                        (g_col * cell_size - 20, g_row * cell_size - 25))

    def greenCellMovement():
        for i in range(num_cells):

            direction = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])

            col, row = cells[i]

            if direction == "RIGHT" and random.random() > rightTurn:
                if col < cols - 1:
                    col += speedGreen
                else:
                    direction = "LEFT"

                # print(f"moved to the right at {col}")
            elif direction == "LEFT" and random.random() > leftTurn:
                if col > 0:
                    col -= speedGreen
                else:
                    direction = "RIGHT"

            elif direction == "UP" and random.random() > upTurn:
                if row > 0:
                    row -= speedGreen
                else:
                    direction = "DOWN"

            elif direction == "DOWN" and random.random() > downTurn:
                if row < rows - 1:
                    row += speedGreen
                else:
                    direction = "UP"

            # Update die Position der aktuellen Zelle
            cells[i] = [col, row]

    greenCellMovement()

    # FORTPFLANZUNG
    def fortpflanzung():
        global cells, num_cells, greenCellTimer
        elapsedTime = pygame.time.get_ticks() - greenCellTimer
        for row, col in cells:
            if elapsedTime >= timerDurationGreen:
                cprint(f"[{num_cells}] a green cell made a baby","green")
                # print("Timer beim Maximum!")
                greenCellTimer = pygame.time.get_ticks()

                num_cells += 2
                cells.append([col, row])
                cells.append([col, row])
                break

    fortpflanzung()

    def fortpflanzungRed(redCellTimer, timerDurationRed, numRedCells,):
        elapsedTime = pygame.time.get_ticks() - redCellTimer

        if elapsedTime >= timerDurationRed:
            numRedCells += 1
            redCellTimer = pygame.time.get_ticks()
            for row, col in redCells:
                cprint(f"[{numRedCells}] a red cell made a baby","red")
                redCells.append((row, col))
                break

        return redCellTimer, timerDurationRed, numRedCells,

    redCellTimer, timerDurationRed, numRedCells, = fortpflanzungRed(
        redCellTimer, timerDurationRed, numRedCells,)

    def hungerTodBlue(deathTimerBlue,deathTimerBlueDur):
        elapsedTime = pygame.time.get_ticks() - deathTimerBlue

        if ateFoodBlue:
            deathTimerBlue = pygame.time.get_ticks()
        if elapsedTime > deathTimerBlueDur and not ateFoodBlue and numBlueCells >= 2:
            deathTimerBlue = pygame.time.get_ticks()
            
            numBlueCells -= 1
            for row,col in blueCells:
                if (row,col) in blueCells:
                    cprint("died to hunger","blue")
                    blueCells.remove((row,col))
                    break




    def hungerTodRed(deathTimer, deathTimerDuration, ateFood, numRedCells,):
        # global deathTimer,deathTimerDuration

        elapsedTime3 = pygame.time.get_ticks() - deathTimer

        # Timer zurücksetzen wenn ateFood True ist
        if ateFood:
            deathTimer = pygame.time.get_ticks()
            # print("nicht gelöscht!")

        # Wenn Timer erreicht ist und ateFood == False dann löschen
        if elapsedTime3 >= deathTimerDuration and not ateFood and numRedCells >= 2:
            deathTimer = pygame.time.get_ticks()

            numRedCells -= 1
            for row, col in redCells[:]:
                if (row, col) in redCells:
                    cprint(f"[{numRedCells}] red cell died to starving.","red")
                    redCells.remove((row, col))
                    break

        elif elapsedTime3 >= deathTimerDuration and ateFood and numRedCells >= 1:
            deathTimer = pygame.time.get_ticks()

        # print(elapsedTime3)

        # print(elapsedTime3)

        return deathTimer, deathTimerDuration, ateFood, numRedCells, 

    deathTimer, deathTimerDuration, ateFood, numRedCells, = hungerTodRed(
        deathTimer, deathTimerDuration, ateFood, numRedCells,)

    def greenCellHungerTod(greenCellTimerDeath, greenCellTimerDeathDuration,num_cells,ateFoodGreen):
        elapsedTime = pygame.time.get_ticks() - greenCellTimerDeath
        
        
        if ateFoodGreen:
            greenCellTimerDeath = pygame.time.get_ticks()

        if elapsedTime >= greenCellTimerDeathDuration and num_cells >= 1 and not ateFood:
            greenCellTimerDeath = pygame.time.get_ticks()

            num_cells -= 1
            for row,col in cells:
                if (row,col) in cells and num_cells >= 1:
                    cells.remove([row,col])
                    cprint(f"[{num_cells}] green cell died to starving","red")
                    break


        #print(elapsedTime)   
        return greenCellTimerDeath,greenCellTimerDeathDuration,num_cells,ateFoodGreen

    greenCellTimerDeath,greenCellTimerDeathDuration,num_cells,ateFoodGreen= greenCellHungerTod(greenCellTimerDeath,greenCellTimerDeathDuration,num_cells,ateFoodGreen,)

    def spawnFood():
        global foodTimer, foodTimerDuration, numBlueCells

        elapsedTime2 = pygame.time.get_ticks() - foodTimer
        if elapsedTime2 >= foodTimerDuration:
            foodTimer = pygame.time.get_ticks()
            numBlueCells += 1
            for col, row in blueCells:
                cprint(f"[{numBlueCells}] a blue cell made a baby","blue")
                blueCells.append([col, row])
                break

        # print(elapsedTime2)

    spawnFood()

    def redCellMovement():
        for i in range(numRedCells):
            direction2 = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])
            
            try:
                col2, row2 = redCells[i]

                if direction2 == "RIGHT" and 0 <= col2:
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

                elif direction2 == "DOWN" and row2 < rows - 1 and row2 < rows:
                    if row2 < rows - 1:
                        row2 += speedRed
                    else:
                        direction = "UP"
            
                redCells[i] = col2, row2

            except Exception as e:
                print(f"Program crashed: {e}")

        # print(col2,row2)

    redCellMovement()

    spawnGrid(screen)

    # BLAUE ZELLEN
    def blueCellMovement():
        for i in range(len(blueCells)):
            direction3 = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])

            col3, row3 = blueCells[i]

            if direction3 == "RIGHT" and 0 <= col3 and random.random(
            ) > rightTurn:
                if col3 < cols - 1:
                    col3 += speedGreen
                else:
                    direction3 = "LEFT"

            elif direction3 == "LEFT" and col3 > 0 and col3 < cols and random.random(
            ) > leftTurn:
                if col3 > 0:
                    col3 -= speedGreen
                else:
                    direction3 = "RIGHT"

            elif direction3 == "UP" and row3 > 0 and 0 <= row3 and random.random(
            ) > upTurn:
                if row3 > 0:
                    row3 -= speedGreen
                else:
                    direction3 = "DOWN"

            elif direction3 == "DOWN" and row3 < rows - 1 and row3 < rows and random.random(
            ) > downTurn:
                if row3 < rows - 1:
                    row3 += speedGreen
                else:
                    direction3 = "UP"

            blueCells[i] = col3, row3

    blueCellMovement()

    # Text
    cellAliveText = normalFont.render(f"green {num_cells}", False, cellColor)
    cellAliveTextBlue = normalFont.render(f"blue {numBlueCells}", False,
                                          (88, 123, 127))
    cellAliveTextRed = normalFont.render(f"red {numRedCells}", False,
                                         cellColor2)
    ateFood = False
    ateFoodGreen = False
    ateFoodBlue = False

    for row2, col2 in redCells:
        redCell = pygame.draw.rect(
            screen, cellColor2,
            (col2 * cell_size, row2 * cell_size, cell_size, cell_size))
    for row3, col3 in blueCells:
        yWert = 10
        yWertGreen = 10
        yWertRed = 0
        yWertOrange = 10


        #blueCellBody3 = pygame.draw.rect(screen,"dark green",(col3 * cell_size ,row3 * cell_size + yWert,wormSizex,wormSizey))
        #blueCellBody2 = pygame.draw.rect(screen,"red",(col3 * cell_size - 10,row3 * cell_size + yWertRed,wormSizex,wormSizey))
        #blueCellBody = pygame.draw.rect(screen,"orange",(col3 * cell_size - 10,row3 * cell_size + yWertOrange,wormSizex,wormSizey))
        blueCell = pygame.draw.rect(screen, (88, 123, 127),(col3 * cell_size, row3 * cell_size, cell_size, cell_size))

    for row, col in cells:
        greenCell = pygame.draw.rect(
            screen, cellColor,
            (col * cell_size, row * cell_size, cell_size, cell_size))

        # Rote Zellen essen grüne Zellen
        for g_row, g_col in cells:
            greenRect = pygame.Rect(g_col * cell_size, g_row * cell_size,
                                    bodySize, bodySize)
            if redCell.colliderect(greenRect):
                if num_cells >= 1:
                    cprint(f"[{numRedCells}] red cell ate green cell.","red")
                    ateFood = True
                    num_cells -= 1
                    cells.remove([g_row, g_col])
                    break
            # print(ateFood)
    # Rote Zellen essen blaue Zellen
    for row, col in blueCells:
        blueRect = pygame.Rect(col * cell_size, row * cell_size, bodySize,
                               bodySize)
        if redCell.colliderect(blueRect):
            ateFood = True
            numBlueCells -= 1
            cprint(f"[{numBlueCells}] red cell ate blue cell","red")
            blueCells.remove((row, col))
            break

            # Überbevölkerung
            if num_cells >= 250:
                try:
                    while num_cells >= 250:
                        num_cells -= 1
                        cells.remove(cells[i])
                        cprint(f"Es wurden: {num_cells - 250} getötet.","red")
                        break
                except Exception as e:
                    print(e)

    for g_row, g_col in redCells:
        if num_cells == 0 and numBlueCells == 0:
            worldEnd = True
            cprint(f"[{numRedCells}] Rote Zellen sterben","red")
            time.sleep(0.1)
            numRedCells -= 1
            redCells.remove((g_row, g_col))
        else:
            worldEnd = False

    if not worldEnd:
        worldTimer()
    else:
        worldEnding()

    if nameTagVisible:
        drawNames()

    def greenCellEating():
        global numBlueCells
        for row, col in blueCells:
            blueCellRect = pygame.Rect(col * cell_size, row * cell_size,
                                       cell_size, cell_size)
            if greenCell.colliderect(blueCellRect):
                cprint(f"[{num_cells}] green cell ate blue cell","green")
                ateFoodGreen = True
                numBlueCells -= 1
                blueCells.remove((row, col))
                break

    greenCellEating()

    # screen.blit(cellAliveText, (10, 20))
    # screen.blit(cellAliveTextBlue, (10, 50))
    # screen.blit(cellAliveTextRed, (10, 80))

    # print(collsion)
    # print(num_cells)
    # print(numRedCells)

    pygame.display.flip()
    pygame.time.delay(0)

pygame.quit()
