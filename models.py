import math
import random

# plane statuses
FLYING = 0
HOLDING = 1
LANDING = 2

# ATC statuses
AVAILABLE = 0
BUSY = 1

# Temp
RETRIES = 20


class Plane:
    def __init__(self, coords, speed):
        self.x = coords[0]
        self.y = coords[1]
        self.speed = speed
        # direction towards the center of the circle in radians
        direction = math.atan2(coords[1], coords[0]) + math.pi  # face plane inwards
        self.angle = direction  # in rad
        self.status = FLYING
        self.target_point = None  # if given a point to circle

    def get_angle_in_degrees(self):
        return math.degrees(self.angle)

    def move(self, time_delta):
        if (self.status == HOLDING):
            # TODO: remember angular velocity
            return
        self.x += self.speed * math.cos(self.angle) * time_delta
        self.y += self.speed * math.sin(self.angle) * time_delta

    def set_path_to_runway(self, runway):
        return math.hypot(self.x - runway.x, self.y - runway.y)

    def update_path_to_point(self, point):
        self.target_point = point
        adjusted_coords = (point[0] - self.x, point[1] - self.y)
        self.angle = math.atan2(adjusted_coords[1], adjusted_coords[0])

    def land(self, runway):
        self.status = 1  # landing
        # TODO: figure out direction
        self.angle = math.pi/2


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
        plane_speed, 
        transmit_rate_hz,
        collision_distance, 
        max_planes=None, 
        name=""
    ):
        self.zone_radius = zone_radius
        self.plane_speed = plane_speed
        self.time_delta = 1 / transmit_rate_hz
        self.collision_distance = collision_distance
        self.holding_pattern_radius = 1000  # metres
        self.max_planes = max_planes
        self.name = name

        # self.runways = [Runway(i, *runway_dimensions) for i in range(num_runways)]  # create runways
        self.planes = []  # store planes
        self.runways = []  # store runways
        self.place_runways(num_runways, runway_dimensions, runway_spacing)

        self.status = AVAILABLE
        self.spawn_attemps = 0

    def __str__(self):
        return f"{self.name} ATC System".strip()

    def place_runways(self, num_runways, dimensions, spacing):
        width = dimensions[0]
        height = dimensions[1]
        
        span = num_runways * (spacing + width)
        starting_point = -span / 2

        # create the runways with the correct spacing
        for i in range(num_runways):
            coords = (starting_point+i*(spacing+width), 0)
            print("Runway coords: ", coords)
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
            # print(plane.x, plane.y, plane.get_angle_in_degrees())

    def spawn_plane(self):
        if self.max_planes is None:
            pass  # ignore this check
        elif len(self.planes) >= self.max_planes:
            return False

        print("Attempting to spawn plane...")
        new_plane = create_plane(self.zone_radius, self.plane_speed)

        # check new plane coords don't intersect with any existing planes
        for i, plane in enumerate(self.planes):
            print(f"Plane {i}: ", plane.x, plane.y)
            print("Plane new: ", new_plane.x, new_plane.y)
            if check_collision(plane, new_plane, self.collision_distance):
                del new_plane
                print("Collision detected. Plane not spawned.")
                # TODO: maybe track the angle used and blacklist it?

                # TODO: track attempts?
                self.spawn_attemps += 1  # count number of unalowable positions
                if self.spawn_attemps >= RETRIES:
                    self.max_planes = len(self.planes)  # set max planes to current number of planes
                    return False

                print("Retrying...")
                self.spawn_plane()

        print("Plane spawned.\n")
        self.planes.append(new_plane)
        return True

    def set_holding_point(self, plane):
        # find a suitable point to hold the plane in
        point = (100, 100)
        plane.update_path_to_point(point)


# helper function for ATC class
def create_plane(zone_radius, speed):
    # spawn plan at a random location on the edge of the zone
    rand_angle = random.uniform(0, 2*math.pi)  # get an angle inside the circle zone

    # rand_angle = math.pi/2  # temp

    # create coordinates along perimeter of circle
    current_coords = (zone_radius*math.cos(rand_angle), zone_radius*math.sin(rand_angle))
    # create plane
    new_plane = Plane(current_coords, speed)  
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
