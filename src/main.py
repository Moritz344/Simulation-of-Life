import time
import random
import sys
import pygame
from termcolor import cprint,colored

# IDEA: gedrückthalten und spawnen

pygame.init()
#   Grüne Zellen :
# - können sich vermehren
# - töten blaue zellen
# - können verhungern

#   Blaue Zellen:
# - können sich vermehren
# - können verhungern

#   Rote Zellen:
# - töten Blaue und Grüne Zellen
# - können sich vermehren
# - können an Hunger sterben

#   Orange Zellen
# - töten rote Zellen
# - sterben an hunger
# - können sich vermehren
# - enstehen durch grüne und blaue Zellen

# FONT
pygame.font.init()
fontSize: int =  20
font = pygame.font.Font("MinecraftRegular.otf", fontSize)
bigFont = pygame.font.Font("MinecraftRegular.otf", 100)
smallFont = pygame.font.Font("MinecraftRegular.otf", 50)
normalFont = pygame.font.Font("MinecraftRegular.otf", 25)
diffFont = pygame.font.Font("MinecraftRegular.otf", 80)
text_farbe = (255, 255, 255)


screenWidth: int = 1920
screenHeight: int = 1080

rows: int = 150#80
cols: int = 105#70
# else:
# rows = 200
# cols = 200
world2: bool = False
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
caption = pygame.display.set_caption("Game Of Life")
clock = pygame.time.Clock()
FPS = 60

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

# fortpflanzuns timer orangene Zellen
orangeCellTimer = pygame.time.get_ticks()
timerDurationOrange = 10000

# Hungertod rote zelle
deathTimer = pygame.time.get_ticks()
deathTimerDuration = timerDurationRed // 2

# Hungertod grüne Zellen 
greenCellTimerDeath = pygame.time.get_ticks()
greenCellTimerDeathDuration = 8000

# Hungertod orangene zellen
orangeCellTimerDeath = pygame.time.get_ticks()
orangeCellTimerDeathDuration = 9000


eventTimer = pygame.time.get_ticks()

# datetime

bodySize = 10#18
cell_size = 10#18
max_cells = 200
num_cells = random.randint(1, 10)
numRedCells = random.randint(1, 10)
numBlueCells = random.randint(1, 10)
numOrangeCells = random.randint(1,10)
killOnes = False
nameTagColor = "white"
nameTagVisible = False
currentEvent = None

bacterial_names = [
    "Bob", "Gustav", "Welten Zerstörer", "Nero", "oh", "neptus",
    "thorii", "luxii", "radicatus", "vim", "nvim", "aurelia",
    "germinans", "tempestus", "noctis"
]

text = random.choice(bacterial_names)
text_2 = random.choice(bacterial_names)
text_3 = random.choice(bacterial_names)

worldEnd = False
ateFood = True
ateFoodGreen = True
ateFoodBlue = True
ateFoodOrange = True

speedGreen = 1
speedRed = 1
speedBlue = 1

cellColor2 = (205, 83, 103)
cellColor = (125, 205, 133)
cellColorBlue = (88,123,127)

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
orangeCells = [[random.randint(0, cols - 1),
              random.randint(0, rows - 1)] for _ in range(numOrangeCells)] 



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
        self.eventList = ["wetter"]
        self.timer = None
        self.sickness: bool = False
    def startTimer(self):
        self.timer = pygame.time.get_ticks()
    def handleTimer(self,timerDuration):
        self.dur = timerDuration
        if self.timer is None:
            print("Timer wurde nicht gestartet!")
            return False
        elapsedTime = pygame.time.get_ticks() - self.timer
        # print(elapsedTime,"ms")
        if elapsedTime >= self.dur and random.random() > 0.99 and not worldEnd :
            self.timer = pygame.time.get_ticks()
            e.randomEvent()

    def randomEvent(self):
        self.currentEvent = random.choice(self.eventList)
        if self.currentEvent == "vermehrung" and random.random() > 0.67 and not self.sickness and num_cells >= 1 and numBlueCells >= 1 and num_cells <= max_cells and numBlueCells <= max_cells and numOrangeCells <= max_cells:
            e.fortpflanzungsEvent()
        elif self.currentEvent == "sickness":
            n = random.randint(0,2)
            if n == 1 and num_cells > 40:#voraussetzungen für sickness event ändern:
                self.sickness: bool = True
                e.sicknessGreenCells()
            elif n == 2 and numBlueCells > 10:
                self.sickness: bool = True
                e.sicknessBlueCells()
        elif self.currentEvent == "wetter" and random.random() > 0.3:
            e.wetterEvent()
        else:
            e.reset()
        

    def ausgabe(self):
        print(f"AN EVENT WAS ACTIVATED!!! [{self.currentEvent}]")

    def fortpflanzungsEvent(self):
        global foodTimerDuration,timerDurationGreen,currentEvent,timerDurationOrange
        currentEvent = "Vermehrung"
        cprint("[EVENT]: bacterias can make babies faster now","yellow")
        foodTimerDuration = 1000
        timerDurationGreen = 1000
        timerDurationOrange = 1000
    def sicknessGreenCells(self):
        global currentEvent
        currentEvent = "Sickness"
        cprint("[EVENT]: green cell population is sick.","yellow")
        
        global cellColor,speedGreen,direction
        global foodTimerDuration,timerDurationGreen
        mutationColor = (50,50,50)#(125,150,33)
        cellColor = mutationColor
        speedGreen = 0
        foodTimerDuration = 12000
        timerDurationGreen = 12000

    def wetterEvent(self):
        global currentEvent

        self.rain_chance = random.uniform(0,1)
        self.sturm_chance = random.uniform(0,1)
        self.sunny_chance = random.uniform(0,1)

        if random.random() > self.rain_chance:
            currentEvent = "Regen"
        elif random.random() < self.sturm_chance:
            currentEvent = "Storm"
        elif random.random() < self.sunny_chance:
            currentEvent = "Sunny"


    def sicknessBlueCells(self):
        global currentEvent
        currentEvent = "Sickness"
        cprint("[EVENT]: blue cell population is sick.","blue")
        global cellColorBlue,speedBlue
        global foodTimerDuration,timerDurationGreen,timerDurationOrange
        mutationColorBlue = (50,50,50)
        cellColorBlue = mutationColorBlue
        speedBlue = 0
        foodTimerDuration = 12000
        timerDurationGreen = 12000
        timerDurationOrange = 12000


    def reset(self):
        global foodTimerDuration,timerDurationGreen,cellColor,speedGreen
        global cellColorBlue,speedBlue
        global rightTurn,leftTurn,upTurn,downTurn
        foodTimerDuration = 12000
        timerDurationGreen = 5000
        speedGreen = 1
        speedBlue = 1
        cellColor = (125, 205, 133)
        cellColorBlue = (88,123,127)
        self.sickness: bool = False
        #rightTurn = 0.67
        #leftTurn = 0.67
        #upTurn = 0.67
        #downTurn = 0.67

e = Events()
e.startTimer()



class InfoPanel(object):
    global num_cells
    def __init__(self):
        self.header = font.render("Simulation",False,"white")
    def greenCellData(self,):
        self.numGreen = font.render(f"Green: {num_cells}",False,cellColor)
        screen.blit(self.numGreen,(1610,70))
    def orangeCellData(self,numOrangeCells):
        self.numOrange = font.render(f"Orange: {numOrangeCells}",False,"orange")
        screen.blit(self.numOrange,(1610,90))
    def redCellData(self,numRedCells):
        self.numRedCells = font.render(f"Red: {numRedCells}",False,"red")
        screen.blit(self.numRedCells,(1610,110))
    def blueCellData(self,numBlueCells):
        self.numBlueCells = font.render(f"Blue: {numBlueCells}",False,cellColorBlue)
        screen.blit(self.numBlueCells,(1610,130))
    def getCurrentEvent(self,currentEvent):
        self.event_Text = font.render(f"Event: {currentEvent}",False,"yellow")
        screen.blit(self.event_Text,(1610,160))

    def PanelBlock(self):
        pygame.draw.rect(screen,(49, 47, 47),(1600,30,300,160))
        screen.blit(self.header,(1610,40))

p = InfoPanel()

def world_2():
    # worm
    pass
def world_3():
    # springer
    pass

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
        back_text_box = pygame.draw.rect(screen,(44, 48, 46),(10,940,130,100))
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
        screen.blit(back_text,(10,940))
        screen.blit(text_1,(50,10))
        screen.blit(text_2,(300,10))
        pygame.display.update()
        clock.tick()

    
def worldTimer():

    timer = pygame.time.get_ticks()
    timer = timer // 1000

    timerText = font.render(f"{timer}s", True, "red")
    screen.blit(timerText, (1600, 10))

    return timer


def worldEnding():
    quitButtonBox = pygame.draw.rect(screen, (30, 32, 25),
                                     (300, 400, 220, 100))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitButtonBox.collidepoint(event.pos):
                sys.exit("Bye!")

    deadEnd = bigFont.render("World ended", True, "white")

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
            #pygame.draw.rect(screen, (30,32,25),
                             #(x, y, cell_size, cell_size), 1)


def spawnCell():
    global num_cells

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size

    # print(col ,row )

    # GÜLTIGEN BEREICH SPAWNEN
    if 0 <= col < cols + 40 and 0 <= row < rows and num_cells < max_cells:
        cells.append([row - 1, col - 1])
        num_cells += 1
        cprint(f"[USER] [{num_cells}] spawned green cell with mouse button.","green")


def spawnCellRed():
    global numRedCells

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # WIR MÜSSEN DIE MAUSPOSITION UMRECHNEN ICH IDIOT!!!
    col = mouse_x // cell_size
    row = mouse_y // cell_size

    # print(col ,row )

    # GÜLTIGEN BEREICH SPAWNEN
    if 0 <= col < cols + 40 and 0 <= row < rows and numRedCells < max_cells:
        redCells.append([row, col])
        numRedCells += 1

        cprint(f"[USER] [{numRedCells}] spawned red cell with mouse button.","red")


def infoScreen():
    runner: bool = True
    while runner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner: bool = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit(0)
                if event.key == pygame.K_ESCAPE:
                    runner: bool = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_text_Rect.collidepoint(event.pos):
                    runner: bool = False

        screen.fill((74, 87, 89))
        mouse_pos = pygame.mouse.get_pos()

        text = "This Game simulates small pixel living in a small grid."
        text_2 = "You can spawn cells with your mouse buttons."
        text_3 = "You can also respawn the cells in a random position with SPACE"
        back_text = bigFont.render("Back",False,"white")

        informationHeader = bigFont.render("Game Of Life", True, "white")
        infoText = normalFont.render(text, False, "white")
        infoText_2 = normalFont.render(text_2, False, "white")
        infoText_3 = normalFont.render(text_3, False, "white")

        back_text_Rect = pygame.Rect(15,1000,200,100)
        if back_text_Rect.collidepoint(mouse_pos):
            back_text = smallFont.render("Back",False,"green")
        else:
            back_text = smallFont.render("Back",False,"white")

        infoText_4 = normalFont.render("READ MORE ON MY GITHUB: @Moritz344",
                                       False, "red")

        screen.blit(informationHeader, (600, 250))
        screen.blit(infoText, (600, 400))
        screen.blit(infoText_2, (600, 450))
        screen.blit(infoText_3, (600, 500))
        screen.blit(infoText_4, (600, 600))
        screen.blit(back_text,(15,1000))
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

                if quitTextBox.collidepoint(event.pos):
                    sys.exit(0)  # exit the whole program

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
                cprint(f"[USER] selected random position for cells","grey")
            if event.key == pygame.K_ESCAPE:
                pauseScreen(screenWidth, screenHeight, bigFont)

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
    
    mouse_button = pygame.mouse.get_pressed()
    if mouse_button[0]:
        spawnCell()
    elif mouse_button[2]:
        spawnCellRed()


    e.handleTimer(random.randint(2000,5000))
    p.PanelBlock()
    p.getCurrentEvent(currentEvent)
    p.greenCellData()
    p.orangeCellData(numOrangeCells)
    p.redCellData(numRedCells)
    p.blueCellData(numBlueCells)






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
        if num_cells >= 1 and not worldEnd:
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

    def orangeCellMovement():
        if numOrangeCells > 0:
            for i in range(numOrangeCells):

                direction = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])

                #col, row = cells[i] #looks cool
                col,row = orangeCells[i]

                if direction == "RIGHT" :
                    if col < cols - 1:
                        col += 1
                    else:
                        direction = "LEFT"

                    # print(f"moved to the right at {col}")
                elif direction == "LEFT":
                    if col > 0:
                        col -= 1
                    else:
                        direction = "RIGHT"

                elif direction == "UP" :
                    if row > 0:
                        row -= 1
                    else:
                        direction = "DOWN"

                elif direction == "DOWN":
                    if row < rows - 1:
                        row += 1
                    else:
                        direction = "UP"

                # Update die Position der aktuellen Zelle
                orangeCells[i] = [col, row]

    orangeCellMovement()

    # FORTPFLANZUNG
    def fortpflanzung():
        global cells, num_cells, greenCellTimer
        elapsedTime = pygame.time.get_ticks() - greenCellTimer
        if num_cells >= 1 and not worldEnd and num_cells < max_cells:
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
        if numRedCells >= 2 and not worldEnd and numRedCells < max_cells:
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

    def fortpflanzungOrange(orangeCellTimer,timerDurationOrange,numOrangeCells):
        if numOrangeCells >= 2 and not worldEnd:
            elapsedTime = pygame.time.get_ticks() - orangeCellTimer

            if elapsedTime >= timerDurationOrange:
                orangeCellTimer = pygame.time.get_ticks()
                cprint(f"[{numOrangeCells}] an orange cell made a baby","light_yellow")
                for row, col in orangeCells:
                    numOrangeCells += 1
                    orangeCells.append((row,col))
                    break

        return orangeCellTimer,timerDurationOrange,numOrangeCells

    orangeCellTimer,timerDurationOrange,numOrangeCells = fortpflanzungOrange( orangeCellTimer,timerDurationOrange,numOrangeCells )


    def hungerTodBlue(deathTimerBlue,deathTimerBlueDur):
        if not worldEnd:
            elapsedTime = pygame.time.get_ticks() - deathTimerBlue

            if ateFoodBlue:
                deathTimerBlue = pygame.time.get_ticks()
            if elapsedTime > deathTimerBlueDur and not ateFoodBlue and numBlueCells >= 2 :
                deathTimerBlue = pygame.time.get_ticks()
                
                numBlueCells -= 1
                for row,col in blueCells:
                    if (row,col) in blueCells:
                        cprint("died to starving","blue")
                        blueCells.remove((row,col))
                        break




    def hungerTodRed(deathTimer, deathTimerDuration, ateFood, numRedCells,):
        # global deathTimer,deathTimerDuration
        if numRedCells >= 1:
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


        return deathTimer, deathTimerDuration, ateFood, numRedCells, 

    deathTimer, deathTimerDuration, ateFood, numRedCells, = hungerTodRed(
        deathTimer, deathTimerDuration, ateFood, numRedCells,)

    def greenCellHungerTod(greenCellTimerDeath, greenCellTimerDeathDuration,num_cells,ateFoodGreen):
        if num_cells >= 1 and not worldEnd:
            elapsedTime_green = pygame.time.get_ticks() - greenCellTimerDeath
        
        
            if ateFoodGreen:
                greenCellTimerDeath = pygame.time.get_ticks()

            if elapsedTime_green >= greenCellTimerDeathDuration and num_cells >= 1 and not ateFood:
                greenCellTimerDeath = pygame.time.get_ticks()

                num_cells -= 1
                for row,col in cells:
                    if (row,col) in cells and num_cells >= 1:
                        cells.remove([row,col])
                        cprint(f"[{num_cells}] green cell died to starving","red")
                        break


        return greenCellTimerDeath,greenCellTimerDeathDuration,num_cells,ateFoodGreen

    greenCellTimerDeath,greenCellTimerDeathDuration,num_cells,ateFoodGreen= greenCellHungerTod(greenCellTimerDeath,greenCellTimerDeathDuration,num_cells,ateFoodGreen,)

    def orangeCellHungerTod(timer,duration,numCells):
        if numCells >= 1 and not worldEnd:
            elapsedTime = pygame.time.get_ticks() - timer
            
            if ateFoodOrange:
                timer = pygame.time.get_ticks()

            if elapsedTime >= duration and numCells >= 1 :
                timer = pygame.time.get_ticks()

                for row,col in orangeCells:
                    cprint(f"[{numOrangeCells}] orange cell died to starving ","light_yellow")
                    numCells -= 1
                    orangeCells.remove([row,col])
                    break




        return timer,duration,numCells
    orangeCellTimerDeath,orangeCellTimerDeathDuration,numOrangeCells = orangeCellHungerTod(orangeCellTimerDeath,orangeCellTimerDeathDuration,numOrangeCells)

    def spawnFood():
        global foodTimer, foodTimerDuration, numBlueCells

        elapsedTime2 = pygame.time.get_ticks() - foodTimer
        if elapsedTime2 >= foodTimerDuration and not worldEnd and numBlueCells < max_cells:
            foodTimer = pygame.time.get_ticks()
            numBlueCells += 1
            for col, row in blueCells:
                cprint(f"[{numBlueCells}] a blue cell made a baby","blue")
                blueCells.append([col, row])
                break

        # print(elapsedTime2)

    spawnFood()

    def redCellMovement():
        if numRedCells >= 1 and not worldEnd:
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
        if numBlueCells >= 1 and not worldEnd:
            for i in range(len(blueCells)):
                direction3 = random.choice(["RIGHT", "LEFT", "UP", "DOWN"])

                col3, row3 = blueCells[i]

                if direction3 == "RIGHT" and 0 <= col3 and random.random(
                ) > rightTurn:
                    if col3 < cols - 1:
                        col3 += speedBlue
                    else:
                        direction3 = "LEFT"

                elif direction3 == "LEFT" and col3 > 0 and col3 < cols and random.random(
                ) > leftTurn:
                    if col3 > 0:
                        col3 -= speedBlue 
                    else:
                        direction3 = "RIGHT"

                elif direction3 == "UP" and row3 > 0 and 0 <= row3 and random.random(
                ) > upTurn:
                    if row3 > 0:
                        row3 -= speedBlue
                    else:
                        direction3 = "DOWN"

                elif direction3 == "DOWN" and row3 < rows - 1 and row3 < rows and random.random(
                ) > downTurn:
                    if row3 < rows - 1:
                        row3 += speedBlue
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
    ateFoodOrange = False

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
        blueCell = pygame.draw.rect(screen, cellColorBlue,(col3 * cell_size, row3 * cell_size, cell_size, cell_size))
    for row4, col4 in orangeCells:
        orangeCell = pygame.draw.rect(screen,"orange",(col4 * cell_size,row4 * cell_size,cell_size,cell_size))

    for row, col in cells:
        greenCell = pygame.draw.rect(screen, cellColor,(col * cell_size, row * cell_size, cell_size, cell_size))

        # Rote Zellen essen grüne Zellen
        for g_row, g_col in cells:
            greenRect = pygame.Rect(g_col * cell_size, g_row * cell_size,
                                    bodySize, bodySize)
            if redCell.colliderect(greenRect) :
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
        if num_cells == 0 and numBlueCells == 0 and numOrangeCells == 0:
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

    def orangeCellCreating():
        global numOrangeCells,ateFoodGreen
        for row, col in blueCells:
            blueCellRect = pygame.Rect(col * cell_size, row * cell_size,
                                       cell_size, cell_size)
            if greenCell.colliderect(blueCellRect) and numOrangeCells > 0 and numOrangeCells < max_cells :
                cprint(f"[{numOrangeCells}] green cell and blue cell made a baby","light_yellow")
                ateFoodGreen = True
                numOrangeCells += 1
                for row, col in orangeCells:
                        orangeCells.append([row,col])
                        break

    orangeCellCreating()

    def orangeCellEating():
        global numOrangeCells
        global numRedCells
        global ateFoodOrange

        if numOrangeCells > 0:
            for row,col in redCells:
                redCellRect = pygame.Rect(col * cell_size,row * cell_size, cell_size, cell_size)
                try:
                    if orangeCell.colliderect(redCellRect) and numOrangeCells >= 1:
                        cprint(f"[{numOrangeCells}] orange cell ate red cell","light_yellow")
                        numRedCells -= 1
                        ateFoodOrange = True
                        redCells.remove((row,col))
                        break
                except Exception as e:
                    print(e)

    orangeCellEating()
    
    def redCellEatsOrangeCell():
        global numOrangeCells
        if numRedCells > 0:
            for row,col in orangeCells:
                orangeCellRect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                if redCell.colliderect(orangeCellRect):
                    cprint(f"[{numOrangeCells}] red cell ate orange cell","red")
                    numOrangeCells -= 1
                    orangeCells.remove([row,col])
                    break

    redCellEatsOrangeCell()

    if numOrangeCells > max_cells:
        for row,col in orangeCells:
            numOrangeCells -= 1
            orangeCells.remove([row,col])
            break

    # screen.blit(cellAliveText, (10, 20))
    # screen.blit(cellAliveTextBlue, (10, 50))
    # screen.blit(cellAliveTextRed, (10, 80))

    # print(collsion)
    # print(num_cells)
    # print(numRedCells)

    clock.tick(FPS)
    pygame.display.update()
    pygame.time.delay(0)

pygame.quit()
