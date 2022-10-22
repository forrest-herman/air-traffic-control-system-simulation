import math
import random

from statuses import *

# Temp
RETRIES = 20


class Plane:
    def __init__(self, coords, speed, circling_radius):
        self.x = coords[0]
        self.y = coords[1]
        self.speed = speed
        self.circling_radius = circling_radius
        # direction towards the center of the circle in radians
        direction = math.atan2(coords[1], coords[0]) + math.pi  # face plane inwards
        self.angle = direction  # in rad
        self.status = FLYING
        self.target_point = None  # if given a point to circle
        self.runway = None  # if given a runway to land on

    def get_angle_in_degrees(self):
        return math.degrees(self.angle)

    def move(self, td):
        # td = time_delta
        if (self.status == HOLDING):
            # how many rad/sec to turn
            angular_velocity = self.speed / self.circling_radius

            # get angle to target point
            adjusted_coords = (self.x - self.target_point[0], self.y - self.target_point[1])
            angle_to_target = math.atan2(
                adjusted_coords[1], adjusted_coords[0]) + angular_velocity * td

            # calculate next position
            self.x = self.circling_radius * math.cos(angle_to_target) + self.target_point[0]
            self.y = self.circling_radius * math.sin(angle_to_target) + self.target_point[1]
        else:
            self.x += self.speed * math.cos(self.angle) * td
            self.y += self.speed * math.sin(self.angle) * td

    def find_hold_point(self):
        # find the point to circle around
        angle = self.angle + math.pi  # get outward facing angle
        self.target_point = (
            self.x - self.circling_radius * math.cos(angle),
            self.y - self.circling_radius * math.sin(angle)
        )
        return self.target_point

    def close_to_runway_or_hold_point(self, occupied_pts):
        # check if another plane is circling between plane and the runway
        for point in occupied_pts:
            distance_to_point = math.hypot(self.x - point[0], self.y - point[1])
            if distance_to_point <= 4 * self.circling_radius:
                print("Plane is too close to another plane")
                return True
        if math.hypot(self.x, self.y) <= 4 * self.circling_radius:
            print("Plane is too close to a runway")
            return True
        return False

    def set_path_to_runway(self, runway, target_top):
        if(target_top):
            coords = runway.get_north_coords()
        else:
            coords = runway.get_south_coords()
        self.runway = runway
        self.update_path_to_point(coords)

    def update_path_to_point(self, point):
        self.target_point = point
        adjusted_coords = (point[0] - self.x, point[1] - self.y)
        self.angle = math.atan2(adjusted_coords[1], adjusted_coords[0])


class Runway:
    def __init__(self, num, width, length, coords):
        self.num = num
        self.width = width
        self.length = length
        self.status = AVAILABLE
        self.x = coords[0]
        self.y = coords[1]

    def __str__(self):
        return f"Runway {self.num}"

    def get_north_coords(self):
        return (self.x, self.y + self.length/2)

    def get_south_coords(self):
        return (self.x, self.y - self.length/2)


class ATC:
    def __init__(self,
                 num_runways,
                 runway_dimensions,
                 runway_spacing,
                 zone_radius,
                 circling_radius,
                 plane_speed,
                 transmit_rate_hz,
                 collision_distance,
                 max_planes=None,
                 name=""
                 ):
        self.zone_radius = zone_radius
        self.plane_speed = plane_speed
        self.circling_radius = circling_radius
        self.circling_points = []
        self.time_delta = 1 / transmit_rate_hz
        self.collision_distance = collision_distance
        self.holding_pattern_radius = 1000  # metres
        self.max_planes = max_planes
        self.name = name

        # self.runways = [Runway(i, *runway_dimensions) for i in range(num_runways)]  # create runways
        self.planes = []  # store planes
        self.landed_planes = []
        self.runways = []  # store runways
        self.place_runways(num_runways, runway_dimensions, runway_spacing)

        self.status = AVAILABLE
        self.spawn_attemps = 0

    def __str__(self):
        return f"{self.name} ATC System".strip()

    def place_runways(self, num_runways, dimensions, spacing):
        width = dimensions[0]
        height = dimensions[1]

        span = (num_runways - 1) * spacing + num_runways * width
        starting_point = -span / 2 + width / 2

        # create the runways with the correct spacing
        for i in range(num_runways):
            coords = (starting_point+i*(spacing+width), 0)
            runway = Runway(i, width, height, coords)
            self.runways.append(runway)

    def get_available_runway(self):
        available_runways = []
        for runway in self.runways:
            if runway.status == AVAILABLE:
                available_runways.append(runway)
        if len(available_runways) == 0:
            self.status = BUSY
        else:
            self.status = AVAILABLE
        return available_runways

    def update_planes(self, time_delta=None):
        if time_delta is None:
            time_delta = self.time_delta
        for plane in self.planes:
            plane.move(time_delta)

    def spawn_plane(self):
        if self.max_planes is None:
            pass  # ignore this check
        elif len(self.planes) >= self.max_planes:
            return False

        new_plane = create_plane(self.zone_radius, self.plane_speed, self.circling_radius)
        distance_factor = self.collision_distance * 2

        # check new plane coords don't intersect with any existing planes
        for plane in self.planes:
            if check_collision(plane, new_plane, distance_factor):
                del new_plane
                print("Collision detected. Plane not spawned.")

                # TODO: track attempts?
                self.spawn_attemps += 1  # count number of unalowable positions
                if self.spawn_attemps >= RETRIES:
                    self.max_planes = len(self.planes)  # set max planes to current number of planes
                    return False

                print("Retrying...")
                self.spawn_plane()

        print("Plane spawned.")
        self.planes.append(new_plane)
        return True

    def set_holding_point(self, plane):
        # find a suitable point to hold the plane in
        point = (100, 100)
        plane.update_path_to_point(point)


# helper function for ATC class
def create_plane(zone_radius, speed, circling_radius):
    # spawn plan at a random location on the edge of the zone
    rand_angle = random.uniform(0, 2*math.pi)  # get an angle inside the circle zone

    # create coordinates along perimeter of circle
    current_coords = (zone_radius*math.cos(rand_angle), zone_radius*math.sin(rand_angle))
    # create plane
    new_plane = Plane(current_coords, speed, circling_radius)
    return new_plane


# checks
def check_plane_status(planes, collision_distance):
    # order the planes by x coordinate, then by y coordinate

    for i, plane in enumerate(planes):
        # check if plane is within 100m of another plane
        if check_collision(planes[i], planes[i+1], planes[i].collision_distance):
            return True


def check_collision(plane1, plane2, collision_distance):
    distance = math.sqrt((plane1.x - plane2.x)**2 + (plane1.y - plane2.y)**2)
    if distance < collision_distance:
        print("Collision detected!")
        return True
    return False


def prep_for_landing(free_runways, plane):
    # find closest runway
    quadrant = get_quadrant(plane)
    if quadrant == 1:
        from_the_top = True
        from_the_left = False
    elif quadrant == 2:
        from_the_top = True
        from_the_left = True
    elif quadrant == 3:
        from_the_top = False
        from_the_left = True
    elif quadrant == 4:
        from_the_top = False
        from_the_left = False

    lenght = len(free_runways)
    if from_the_left:
        # choose innermost available left runway
        runway = free_runways[lenght//2-1]
    else:
        # choose innermost available right runway
        runway = free_runways[lenght//2]

    # set the plane to land
    runway.status = BUSY
    plane.status = LANDING
    # TODO: set target point to landing strip top or bottom
    plane.set_path_to_runway(runway, from_the_top)


def get_quadrant(plane):
    if plane.x > 0 and plane.y > 0:
        return 1
    elif plane.x < 0 and plane.y > 0:
        return 2
    elif plane.x < 0 and plane.y < 0:
        return 3
    elif plane.x > 0 and plane.y < 0:
        return 4
