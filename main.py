import math
import time

from models import ATC, prep_for_landing
from simulation import refresh_screen, pygame_init, new_plane_sprite, new_runway_sprite

from statuses import *

ZONE_RADIUS = 10000  # metres
CIRCLING_RADIUS = 1000  # metres
PLANE_SPEED = 1400  # m/s
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
        CIRCLING_RADIUS,
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

            # check if runway is available
            free_runways = atc.get_available_runway()

            # check for planes that are waiting to land
            if plane.status == FLYING:
                if atc.status == AVAILABLE:
                    prep_for_landing(free_runways, plane)
                elif plane.close_to_runway_or_hold_point(atc.circling_points):
                    plane.status = HOLDING
                    atc.circling_points.append(plane.find_hold_point())
                    
            elif plane.status == HOLDING:
                if atc.status == AVAILABLE:
                    prep_for_landing(free_runways, plane)

            elif plane.status == LANDING:
                if math.hypot(plane.x - plane.target_point[0], plane.y - plane.target_point[1]) <= plane.runway.width:
                    print("Plane has landed.")
                    # TODO: move plane down runway
                    atc.landed_planes.append(plane)
                    print("ATC Landed Planes:", len(atc.landed_planes))
                    atc.planes.remove(plane)
                    print("ATC Planes Remaining:", len(atc.planes))
                    plane.runway.status = AVAILABLE
                    plane.runway = None

        for runway in atc.runways:
            # add each to the drawing library
            coords = (runway.x, runway.y)
            new_plane = new_runway_sprite(coords, screen)
            all_sprites.add(new_plane)

        # visual simulation
        add_plane, running = refresh_screen(screen, all_sprites, ZONE_RADIUS)

        time.sleep(time_delta)  # community at given rate


if __name__ == '__main__':
    print("Starting simulation...")
    main()
