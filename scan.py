from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Axis, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, multitask, run_task
from usys import stdout

# ─── Robot dimensions (mm) ───
WHEEL_DIAMETER_MM = 87
AXLE_TRACK_MM = 148

# ─── Mosaic dimensions (mm) ───
MOSAIC_W_MM = 8382
MOSAIC_H_MM = 3000

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
RESOLUTION_MM = 50
GRID_WIDTH = MOSAIC_W_MM // RESOLUTION_MM
GRID_HEIGHT = MOSAIC_H_MM // RESOLUTION_MM
SENSOR_OFFSET_MM = 100


hub = PrimeHub(front_side=Axis.Y)
lw = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rw = Motor(Port.A)
db = DriveBase(lw, rw, wheel_diameter=WHEEL_DIAMETER_MM, axle_track=AXLE_TRACK_MM)
db.use_gyro(False)
db.settings(
    straight_speed=100,
    straight_acceleration=200,
    turn_rate=100,
    turn_acceleration=200
)
sensor = ColorSensor(Port.C)

def accuTurn(target_angle, tolerance=0.25, speed=80):
    while True:
        current_angle = hub.imu.heading()
        angle_difference = target_angle - current_angle

        # Check if we're within the tolerance range of the target angle
        if abs(angle_difference) <= tolerance:
            print( 'W00t', current_angle )
            db.stop()
            break

        # Determine direction based on whether we've overshot or not
        clockwise = angle_difference > 0

        abs_angle_diff = abs(angle_difference)
        if (abs_angle_diff < 30 ):
            speed = 30
        if (abs_angle_diff < 20 ):
            speed = 20
        if (abs_angle_diff < 10):
            speed = 10
        
        # print( 'c', current_angle, 'd', angle_difference, 'speed', speed )

        direction = speed if clockwise else -speed
        db.drive(0, direction)
    
    wait( 100 )
    print( 'post', hub.imu.heading() )

def scan():
    odd = True
    scan_w = 0

    for x in range(GRID_WIDTH):
        db.reset()
        scan_times = 0 if odd else (GRID_HEIGHT - 1)
        db.drive(100, 0)

        while db.distance() < MOSAIC_H_MM:
            target = scan_times * RESOLUTION_MM if odd else (GRID_HEIGHT - 1 - scan_times) * RESOLUTION_MM
            if target <= db.distance():
                color = sensor.color()
                color_code = COLOR_MAP.get(color, 0)
                stdout.buffer.write(bytes([0xFF, scan_w, scan_times, color_code]))
                hub.speaker.beep()
                if odd:
                    scan_times += 1
                    if scan_times >= GRID_HEIGHT:
                        break
                else:
                    scan_times -= 1
                    if scan_times < 0:
                        break

        db.stop()

        if x < GRID_WIDTH - 1:
            if odd:
                accuTurn(90, tolerance=0.05)
                db.straight(RESOLUTION_MM)
                accuTurn(180, tolerance=0.05)
                db.straight(-100)
            else:
                accuTurn(-90, tolerance=0.05)
                db.straight(RESOLUTION_MM)
                accuTurn(-180, tolerance=0.05)
                db.straight(-100)

        odd = not odd
        scan_w += 1

scan()
# async def drive():
#     db.drive( 300, 0 )
#     await wait ( 500 )
#     db.stop()


# async def beep():
#     for x in range (5):
#         hub.speaker.beep()
#         wait(200)

# run_task(multitask( drive(), beep() ))
def scan():
    odd = True
    scan_w = 0

    for x in range(GRID_WIDTH):
        db.reset()
        scan_times = 0 if odd else (GRID_HEIGHT - 1)
        db.drive(100, 0)

        while db.distance() < MOSAIC_H_MM:
            target = scan_times * RESOLUTION_MM if odd else (GRID_HEIGHT - 1 - scan_times) * RESOLUTION_MM
            if target <= db.distance():
                color = sensor.color()
                color_code = COLOR_MAP.get(color, 0)
                stdout.buffer.write(bytes([0xFF, scan_w, scan_times, color_code]))
                print([0xFF, scan_w, scan_times, color_code])
                hub.speaker.beep()
                if odd:
                    scan_times += 1
                else:
                    scan_times -= 1

        db.stop()

        if x < GRID_WIDTH - 1:
            if odd:
                accuTurn(90, tolerance=0.05)
                db.straight(RESOLUTION_MM)
                accuTurn(180, tolerance=0.05)
            else:
                accuTurn(-90, tolerance=0.05)
                db.straight(RESOLUTION_MM)
                accuTurn(-180, tolerance=0.05)

        odd = not odd
        scan_w += 1

scan()
