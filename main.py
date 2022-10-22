import math
import time

from models import ATC
from simulation import refresh_screen, pygame_init, new_plane_sprite, new_runway_sprite


ZONE_RADIUS = 10000  # metres
PLANE_SPEED = 140  # m/s
NUM_RUNWAYS = 2
RUNWAY_DIMENSIONS = (100, 500)  # metres
RUNWAY_SPACING = 500  # metres
TRANSMIT_RATE = 10  # Hz
COLLISION = 100  # metres
MAX_PLANES = 10  # (optional) maximum number of planes allowed in the zone


def main():
    atc = ATC(
        NUM_RUNWAYS, 
        RUNWAY_DIMENSIONS, 
        RUNWAY_SPACING,
        ZONE_RADIUS, 
        PLANE_SPEED, 
        TRANSMIT_RATE,
        COLLISION, 
        name="SpaceRyde")  # MAX_PLANES


    atc.spawn_plane()

    # prepare pygame
    screen, all_sprites = pygame_init(ZONE_RADIUS)

    # loop every 0.1 seconds (10 Hz)
    time_delta = 1 / TRANSMIT_RATE

    # tracking variables for the GUI
    running = True
    add_plane = False

    while(running):
        if add_plane:
            atc.spawn_plane()
            add_plane = False

        # move the planes at their corresponding speed at their current angle
        atc.update_planes()

        all_sprites.empty()

        for plane in atc.planes:
            # add each to the drawing library
            coords = (plane.x, plane.y)
            new_plane = new_plane_sprite(coords, screen)
            all_sprites.add(new_plane)

        for runway in atc.runways:
            # add each to the drawing library
            coords = (runway.x, runway.y)
            new_plane = new_runway_sprite(coords, screen)
            all_sprites.add(new_plane)


        # visual simulation
        add_plane, running = refresh_screen(screen, all_sprites, ZONE_RADIUS)

        time.sleep(time_delta) # community at given rate



if __name__ == '__main__':
    print("Starting simulation...")
    main()
