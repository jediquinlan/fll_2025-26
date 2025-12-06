from pybricks.hubs import PrimeHub
from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from usys import stdout
from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase

WHEEL_DIAMETER = 88
AXLE_TRACK = 142.24

hub = InventorHub( front_side=Axis.Y )
lw = Motor( Port.B, Direction.COUNTERCLOCKWISE )
rw = Motor( Port.A )
db = DriveBase(lw, rw, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
db.use_gyro(True)
sensor = ColorSensor(Port.C)

# Map Color enum to numbers
COLOR_MAP = {
    Color.RED: 1,
    Color.GREEN: 2,
    Color.BLUE: 3,
    Color.YELLOW: 4,
    Color.WHITE: 5,
    Color.BLACK: 6,
    None: 0  # No color detected
}




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

room_w = 470
room_h = 250
# robot_l = 203.2
# robot_w = 152.4
resolution = 40

# Packet header to identify valid data packets
PACKET_HEADER = 0xAA  # Changed from 0xFF to 0xAA (170)


cell_width_num = int (room_w / resolution)
cell_height_num = int (room_h / resolution)
print(cell_width_num, cell_height_num)
def scan_color(x, y):
    color = sensor.color()
    color_code = COLOR_MAP.get(color, 0)
    
    # Send packet: [header, color_code, x, y, grid_width, grid_height]
    stdout.buffer.write(bytes([PACKET_HEADER, color_code, x, y, cell_width_num, cell_height_num]))
    hub.speaker.beep()


xcord = 1
ycord = 1



db.reset()
db.settings(100)
db.straight(300)
accuTurn(-90)
db.straight(0.5*room_w)
accuTurn(0)
db.reset()
distance_current = db.distance()
for x in range (cell_width_num):
    scan_color(xcord,ycord)
    db.drive(200, 0)
    # drive forward
    counter = 0
    while (db.distance() < room_h):
        distance_current = db.distance()- (counter * (room_h/cell_height_num))
        if (distance_current > room_h/cell_height_num):
            distance_current = 0
            if (x % 2 == 0):
                ycord += 1
            else:
                ycord -= 1
            scan_color(xcord,ycord)
            counter +=1
            print(xcord,ycord)
    db.stop()
    # turn around
    if ( x % 2 == 0 ):
        accuTurn(90)
        db.straight(resolution)
        xcord += 1
        accuTurn(180)
        db.straight(-83)
        scan_color(xcord,ycord)
        db.reset()
    else:
        accuTurn(-90)
        db.straight(resolution)
        xcord += 1
        accuTurn(-180)
        db.straight(-83)
        scan_color(xcord,ycord)
        db.reset()


    
    
