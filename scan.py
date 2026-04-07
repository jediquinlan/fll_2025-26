from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from usys import stdout

# ─── Robot dimensions (mm) ───
WHEEL_DIAMETER_MM = 87
AXLE_TRACK_MM = 148

# ─── Mosaic dimensions (mm) ───
MOSAIC_W_MM = 8382
MOSAIC_H_MM = 3581

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
GRID_SIZE_MM = 200
GRID_WIDTH = MOSAIC_W_MM // GRID_SIZE_MM
GRID_HEIGHT = MOSAIC_H_MM // GRID_SIZE_MM
SENSOR_OFFSET_MM = 100


hub = PrimeHub(front_side=Axis.Y)
lw = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rw = Motor(Port.A)
db = DriveBase(lw, rw, wheel_diameter=WHEEL_DIAMETER_MM, axle_track=AXLE_TRACK_MM)
db.use_gyro(True)
db.settings(
    straight_speed=100,
    straight_acceleration=200,
    turn_rate=100,
    turn_acceleration=200
)
sensor = ColorSensor(Port.C)

def accuTurn(target_angle, tolerance=0.1, speed=80):
    while True:
        current_angle = hub.imu.heading()
        angle_difference = target_angle - current_angle

        while angle_difference > 180:
            angle_difference -= 360
        while angle_difference < -180:
            angle_difference += 360

        if abs(angle_difference) <= tolerance:
            print( 'angle', current_angle )
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

        direction = speed if clockwise else -speed
        db.drive(0, direction)


current_heading = 0
# Scan in lawnmower pattern
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        y = row

        if row % 2 == 0:
            x = col
        else:
            x = GRID_WIDTH - 1 - col

        color = sensor.color()
        color_code = COLOR_MAP.get(color, 0)

        stdout.buffer.write(bytes([0xFF, x, y, color_code]))
        hub.speaker.beep()

        wait(100)

        if col < GRID_WIDTH - 1:
            db.straight(GRID_SIZE_MM)
            accuTurn(current_heading)

    if row < GRID_HEIGHT - 1:
        turn = 90
        if (row % 2 == 0):
            turn = -90

        current_heading += turn
        accuTurn(current_heading)

        db.straight(GRID_SIZE_MM)
        accuTurn(current_heading)

        current_heading += turn
        accuTurn(current_heading)

        db.straight(-SENSOR_OFFSET_MM)
        accuTurn(current_heading)

hub.speaker.beep()
