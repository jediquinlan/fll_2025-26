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
    #brings the right arm up
    await right.run_angle(500,-200)
    await db.straight(1212)
    #turning
    accuTurn(-90)
    #goes to the basket-land
    await db.straight(70)

    #puts right arm down
    await right.run_time(500, 200)

    #puts left arm down to hit the basket
    await left.run_angle(500, -180)
    #moves left arm back up
    await left.run_angle(500, 180)

    #puts right arm back up
    await right.run_time(500, -200)

    #backs up
    await db.straight(-90),
   
    
async def scissors():
    db.reset()
    #curves to an angle
    await db.curve(475,-40.2, Stop.NONE)
    await multitask(
        #heads forward more
        db.straight(240),
        #expands the scissor to put the flag in spot
        right.run_angle(300,505)
    )
    #closes the scissors
    await right.run_angle(400,-550)
    #goes backward
    await db.straight(-100)
    #turns to another mission
    accuTurn(4)
    wait(30)
    #extends the scissor
    await right.run_angle(400,300)
    
     #timed base turn
    db.drive(0, -500)
    #waits that long before running stoppinjg
    await wait(700) 
    #stops the turning
    db.stop()
    #closes scissor
    await right.run_angle(400,-140)
    #turns to the next mission
    db.drive(0, 500)
    #wait
    await wait(500)
    db.stop()
    #closes the scissor a little bit
    await right.run_angle(400,-200)
    #accute turns to the final mission we are doing for this run
    accuTurn(-51)
    #lowers the rubber arm onto the table
    await left.run_angle(500, 720)
    #backs up to lift the structure off the ground
    await db.straight(-250)
    #moves slightly forward
    # await db.straight(100)
    #turns away form the mission
    await db.turn(50)
    #multitasks: brings the rubber arm back to its origin spot, backs up to starting point
    await multitask(
        left.run_angle(500, -500),
        db.straight(-700)
    )

async def sandy():
    db.use_gyro( True )
    #move toward the ship
    await db.straight( 500 )
    
    #make sure we are facing the ship head on
    accuTurn(0, 0.1)
    
    #grind into the sunken ship
    await wait( 500 )
    db.drive(100,7)
    await wait( 1200 )
    db.stop()

    #drop the slide / grab the red arm
    await right.run_angle(500, -340)
    #pull the red arm back
    await db.straight( -100 )
    #drop the red arm
    await right.run_angle( 500, 340 )

    #back to base
    await db.straight( -500 )


run_task(sandy())
