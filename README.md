# Air Traffic Control System Simulation
 ## Developped in Python

- `main.py`: initialization, main logic and while loop
- `models.py`: stores all classes and helper functions
- `simulation.py`: pygame contents and functions used to visualize the simulation
- `statuses.py`: stores helpful variables that are used to track the status of planes and runways

### ATC System Requirements
The system must:
- Keep track of all airplanes’ positions (latitude, longitude) within the traffic control zone.
- Queue airplanes for landing based on time of arrival into the traffic control zone.
- Command airplanes to go for landing (when it is their turn) to one of two runways (can be scaled to many).
  - Otherwise commands airplanes to fly in a circular “holding pattern” which is a circle with a radius of 1km around a suitable point.
- Never allow for planes to come within 100m of each other, whether
flying or landing.
- The traffic control zone is a circle of radius 10km (can be variable).

[Preview the project here](project_demo.mp4)

![Project Demo](demo.GIF)
