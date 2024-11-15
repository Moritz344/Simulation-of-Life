import pygame

# Initialisiere Pygame
pygame.init()

# Fenstergröße
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Zellenparameter
cell_size = 20  # Initiale Zellgröße
zoom_factor = 1  # Zoomfaktor
zoom_speed = 1  # Wie schnell der Zoomfaktor ansteigt oder sinkt
max_zoom = 50  # Maximale Zellgröße (max. Zoom-Out)
min_zoom = 5  # Minimale Zellgröße (max. Zoom-In)

# Mauskoordinaten
mousex, mousey = 0, 0

# Haupt-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            mousex, mousey = pygame.mouse.get_pos()

            # Berechne die neue Zellgröße basierend auf der Mausradbewegung
            if event.y > 0:  # Mausrad nach oben
                if cell_size < max_zoom:
                    cell_size *= zoom_speed
            elif event.y < 0:  # Mausrad nach unten
                if cell_size > min_zoom:
                    cell_size /= zoom_speed

            # Berechne die relative Mausposition in Zellenkoordinaten
            mousex, mousey = mousex // cell_size, mousey // cell_size

            # Debug-Ausgabe
            print(f"Zoom: {cell_size}, Mouse Position: {mousex},{mousey}")

    # Bildschirm füllen und Gitter zeichnen (zum Testen)
    screen.fill((255, 255, 255))  # Hintergrundfarbe (weiß)

    for x in range(0, screen_width, cell_size):
        for y in range(0, screen_height, cell_size):
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, cell_size, cell_size), 1)

    pygame.display.flip()

pygame.quit()


