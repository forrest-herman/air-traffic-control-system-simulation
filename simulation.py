import pygame

SIZE = 1200


def pixel_convert(value):
    try:
        return value / 20
    except TypeError:
        return value[0] / 20, value[1] / 20


def correct_for_y(value, screen_size):
    # account for py game coordinate system
    return value * -1 + screen_size


# Define a Plane object by extending pygame.sprite.Sprite
class PlaneSprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super(PlaneSprite, self).__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(
            center=(x, y)
        )


# Define a Runway object by extending pygame.sprite.Sprite
class RunwaySprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super(RunwaySprite, self).__init__()
        self.image = pygame.Surface((10, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(
            center=(x, y)
        )


def pygame_init(size):
    pygame.init()

    # Set up the drawing window screen
    size = pixel_convert(size)*2 + 200  # give boarder around traffic control zone
    screen = pygame.display.set_mode([size, size])

    # Create group to hold all plane sprites
    all_sprites = pygame.sprite.Group()

    return screen, all_sprites


def new_plane_sprite(coords, screen):
    x, y = pixel_convert(coords)

    # account for py game coordinate system
    w, h = screen.get_size()
    x = x + w/2
    y = -y + h/2

    new_plane = PlaneSprite((0, 0, 0), x, y)
    return new_plane


def new_runway_sprite(coords, screen):
    x, y = pixel_convert(coords)

    # account for py game coordinate system
    w, h = screen.get_size()
    x = x + w/2
    y = -y + h/2

    new_plane = RunwaySprite((120, 120, 120), x, y)
    return new_plane


def refresh_screen(screen, all_sprites, size):
    all_sprites.sprites()

    # Fill the background with blue
    screen.fill((100, 150, 255))

    zone_size = pixel_convert(size)  # get the size of the traffic control zone
    w, h = screen.get_size()

    # draw the traffic control zone
    pygame.draw.circle(screen, (180, 220, 180), (w/2, h/2), zone_size, 0)

    # scale bars grid
    grid_color = (100, 150, 255)
    for i in range(0, 23):
        pygame.draw.rect(screen, grid_color, (0, 50*i+50, w, 1), 0)
        pygame.draw.rect(screen, grid_color, (50*i+50, 0, 1, h), 0)

    myfont = pygame.font.SysFont("monospace", 15)
    label = myfont.render("Traffic Control Zone, Grid Scale 1 km", 1, (0, 0, 0))
    screen.blit(label, (25, h - 25))

    # Draw all sprites
    all_sprites.draw(screen)
    # for entity in all_sprites:
    #     screen.blit(entity.image, entity.rect)

    # Update the display
    pygame.display.flip()

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False  # new plane, running
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True, True  # new plane, running

    return False, True  # new plane, running
