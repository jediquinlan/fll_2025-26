from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
from pybricks.tools import multitask, run_task

WHEEL_DIAMETER = 62.84
AXLE_TRACK = 110

hub = InventorHub( front_side=Axis.Y )
lw = Motor( Port.A, Direction.COUNTERCLOCKWISE )
rw = Motor( Port.E )
db = DriveBase(lw, rw, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)
db.use_gyro(True)
left = Motor(Port.C)
right = Motor(Port.B)

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
        

        print( 'c', current_angle, 'd', angle_difference, 'speed', speed )

        direction = speed if clockwise else -speed
        db.drive(0, direction)
    
    wait( 500 )
    print( 'post', hub.imu.heading() )

def dbResetSettings( ):
    db.settings( *db_def_settings )


async def shipwreck():
    await multitask(
        #lift up the arm from the ground so we don't drag
        right.run_angle(100,-50),
        #from base, go toward the ship
        db.straight(445)
    )
    #put the arm back down over the sand trap arm
    await right.run_angle(100,50)
    #back up to drop the sand from the ship
    await db.straight(-50)
    #lifts one arm up(the one used to drop the sand) and the other one down
    await right.run_angle(100,-50)
    #backs up
    await db.straight(-50)
    #drops one of the arm down
    await right.run_angle(100,-90)
    #pushes the red thing to raise the ship
    await db.straight(100)
    #backs up from the ship
    await db.straight(-100)
    await left.run_angle(-500,-900, Stop.COAST)
    await left.run_angle(-500,900, Stop.COAST)

# run_task(shipwreck())

# given abcd, and b, return bcda
# def move_to_front(my_list, value):
#     index = my_list.index(value)
#     shifted_list = my_list[index:] + my_list[:index]
#     return shifted_list

# missions = ["1", "2", "3"]
# while True:
#     selected = hub_menu( *missions )
#     if selected == "1":
#         run_task(shipwreck())
#         missions = move_to_front(missions, "2")
#     if selected == "2":
#         run_task(flag_pull())
#         missions = move_to_front(missions, "3")

async def flag_pull():
    await db.straight(1000)
    await db.curve(500, 43)
    await accuTurn(-150)
    await wait(300)
    await db.straight(180)
    await accuTurn(-90)
    await db.straight(150)
    await multitask(
    )

left.run_angle(300, 90)