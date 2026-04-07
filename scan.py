from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Color, Direction, Port, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from usys import stdout

WHEEL_DIAMETER = 87
AXLE_TRACK = 148

MOSAIC_L = 8382
MOSAIC_H = 3581.4

hub = PrimeHub(front_side=Axis.Y)
lw = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rw = Motor(Port.A)
db = DriveBase(lw, rw, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
db.use_gyro(True)

sensor = ColorSensor(Port.C)

def accuTurn(target_angle, tolerance=0.25, speed=80):
    while True:
        current_angle = hub.imu.heading()
        angle_difference = target_angle - current_angle
        
        # Normalize angle difference to -180 to 180
        while angle_difference > 180:
            angle_difference -= 360
        while angle_difference < -180:
            angle_difference += 360

        if abs(angle_difference) <= tolerance:
            db.stop()
            break

        clockwise = angle_difference > 0
        abs_angle_diff = abs(angle_difference)
        
        if abs_angle_diff < 30:
            speed = 30
        if abs_angle_diff < 20:
            speed = 20
        if abs_angle_diff < 10:
            speed = 10

# Map Color enum to numbers
COLOR_MAP = {
    Color.RED: 1,
    Color.GREEN: 2,
    Color.BLUE: 3,
    Color.YELLOW: 4,
    Color.WHITE: 5,
    Color.BLACK: 6,
    None: 0
}

# Grid scanning parameters
GRID_SIZE = 50  # Distance between grid points in mm
GRID_WIDTH = 7  # Number of columns (the long direction)
GRID_HEIGHT = 4  # Number of rows

current_heading = 0  # Track absolute heading

OFFSET = 2

# Scan in lawnmower pattern
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        # y is just the row number
        y = row
        
        # x alternates direction based on odd/even row
        if row % 2 == 0:
            # Even row: going right (0 → 6)
            x = col
        else:
            # Odd row: going left (6 → 0)
            x = GRID_WIDTH - 1 - col
        
        # Read color at current position
        color = sensor.color()
        color_code = COLOR_MAP.get(color, 0)
        
        # Transmit position and color (3 bytes: x, y, color)
        stdout.buffer.write(bytes([0xFF, x, y, color_code]))
        
        wait(100)
        
        # Move to next position in the row (except at end)
        if col < GRID_WIDTH - 1:
            db.straight(GRID_SIZE)
    
    # At end of row, do the turn sequence (except on last row)
    if row < GRID_HEIGHT - 1:
        turn = 90
        if (row % 2 == 0):
            turn = -90

        # Turn 90°
        current_heading += turn
        accuTurn(current_heading)
        
        # Move forward 1 cell
        db.straight(GRID_SIZE)
        
        # Turn 90° again
        current_heading += turn
        accuTurn(current_heading)

        db.straight( -(OFFSET*GRID_SIZE))

hub.speaker.beep()
