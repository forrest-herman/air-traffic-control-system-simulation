# Simple pygame program

# Import and initialize the pygame library
import time
import pygame

from models import Plane

SIZE = 1200
x = 10
y = 10

def update():
    # Flip the display
    pygame.display.flip()

# Define a Plane object by extending pygame.sprite.Sprite
class PlaneSprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super(PlaneSprite, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(
            center=(x, y)
        )
        # self.speed = 1

    def update(self, coords):
        # self.rect.move_ip(1,1)
        self.rect.center = coords

pygame.init()

# Set up the drawing window screen
screen = pygame.display.set_mode([SIZE, SIZE])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player. Right now, this is just a rectangle.
player = PlaneSprite((255, 255, 255), 100, 50)


# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Create a surface and pass in a tuple containing its length and width
surf = pygame.Surface((50, 50))
# Give the surface a color to separate it from the background
surf.fill((0, 0, 0))
rect = surf.get_rect()

# Put the center of surf at the center of the display
surf_center = (
    (SIZE-player.surf.get_width())/2,
    (SIZE-player.surf.get_height())/2
)


def add_plane():
    # Create the new enemy and add it to sprite groups
    new_enemy = PlaneSprite((255, 255, 255), 100, 50)
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                add_plane()

    # Fill the background with blue
    screen.fill((100, 150, 255))
    pygame.draw.circle(screen, (255, 255, 255), (SIZE/2, SIZE/2), 500, 0)
    pygame.draw.rect(screen, (0,0,0), (SIZE/2, SIZE/2, 10, 50), 0)


    x = x + 1
    y = y + 1

    player.update((x, y))


    # Draw surf at the new coordinates
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    

    # time.sleep(1)

    # # Draw a solid white circle in the center
    # pygame.draw.circle(screen, (255, 255, 255), (x, y), 400)

    update()

# Done! Time to quit.
pygame.quit()




