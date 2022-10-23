import math
import time

from models import ATC, prep_for_landing
from simulation import refresh_screen, pygame_init, new_plane_sprite, new_runway_sprite

from statuses import *  # import all plane and atc statuses

ZONE_RADIUS = 10000  # metres
CIRCLING_RADIUS = 1000  # metres
PLANE_SPEED = 140  # m/s
NUM_RUNWAYS = 2
RUNWAY_DIMENSIONS = (100, 500)  # metres
RUNWAY_SPACING = 500  # metres
TRANSMIT_RATE = 10  # Hz
COLLISION = 100  # metres
MAX_PLANES = 50  # (optional) maximum number of planes allowed in the zone


def main():
    # create the ATC system
    atc = ATC(
        NUM_RUNWAYS,
        RUNWAY_DIMENSIONS,
        RUNWAY_SPACING,
        ZONE_RADIUS,
        CIRCLING_RADIUS,
        PLANE_SPEED,
        TRANSMIT_RATE,
        COLLISION,
        max_planes=MAX_PLANES,
        name="Forrest Herman's ATC System")

    # spawn plane #1 (this is optional)
    atc.spawn_plane()

    # loop every 0.1 seconds (10 Hz)
    time_delta = 1 / TRANSMIT_RATE

    # prepare pygame
    screen, all_sprites = pygame_init(ZONE_RADIUS)
    plane_sprites, runway_sprites = all_sprites

    # tracking variables for the GUI
    running = True
    add_plane = False

    while(running):
        if add_plane:
            # this triggers if the spacebar is pressed
            atc.spawn_plane()
            add_plane = False

        # move the planes at their corresponding speed at their current angle
        atc.update_planes()

        # clear old sprites
        plane_sprites.empty()
        runway_sprites.empty()

        # loop through all planes and check logic
        for plane in atc.planes:
            # add each to the drawing library
            coords = (plane.x, plane.y)
            new_plane = new_plane_sprite(coords, screen)
            plane_sprites.add(new_plane)

            # check what runways are available
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
                    atc.circling_points.remove(plane.target_point)
                    prep_for_landing(free_runways, plane)

            if plane.status == LANDING:
                if math.hypot(plane.x - plane.target_point[0], plane.y - plane.target_point[1]) <= plane.runway.width * 1.5:
                    plane.status = RUNWAY
                    print("Plane is on the runway")

            if plane.status == RUNWAY:
                # check the plane's direction of approach
                if plane.angle > 0 and plane.angle < math.pi:
                    # plane is approaching from the south
                    # set tartget to the north end of the runway
                    plane.set_path_to_runway(plane.runway, True)
                    condition = plane.y >= (plane.runway.length/2)
                else:
                    # plane is approaching from the north
                    # set target to the south end of the runway
                    plane.set_path_to_runway(plane.runway, False)
                    condition = plane.y <= -(plane.runway.length/2)

                if condition:
                    # plane has reached the end of the runway
                    atc.landed_planes.append(plane)
                    print(f"ATC Landed {len(atc.landed_planes)} Planes")
                    atc.planes.remove(plane)
                    plane.runway.status = AVAILABLE
                    plane.runway = None

        for runway in atc.runways:
            # add each runway to the drawing library
            coords = (runway.x, runway.y)
            new_runway = new_runway_sprite(coords, screen)
            runway_sprites.add(new_runway)

        # visual simulation
        all_sprites = (plane_sprites, runway_sprites)
        # spawn a plane by pressing the space key
        # quit by pressing the window close button
        add_plane, running = refresh_screen(screen, all_sprites, ZONE_RADIUS)

        time.sleep(time_delta)  # communicate with ATC at given rate


if __name__ == '__main__':
    print("Starting simulation...")
    main()
