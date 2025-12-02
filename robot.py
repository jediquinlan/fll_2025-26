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
db_def_settings = db.settings()

def dbResetSettings( ):
    db.settings( *db_def_settings )
    db.reset()

async def accuTurn(target_angle, tolerance=0.25, speed=80):
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
    
    await wait( 100 )
    print( 'post', hub.imu.heading() )


async def flag_pull():
    dbResetSettings()
    await db.straight(580)
    await right.run_angle(500,750)
    await db.straight(-150)
    db.settings(75)
    await right.run_angle(500,-75)
    await db.straight(300, Stop.NONE)
    db.settings(*db_def_settings)
    await multitask(
        right.run_angle(500,-600),
        db.straight(460)
    )
    #turning
    await accuTurn(-90)
    # goes to the basket-land hi
    db.drive(100, 0)
    await wait(700)
    db.stop()
    # raising table
    await multitask(
        right.run_angle(500, 850),
        left.run_angle(200, -450)
    )
    # lifts arm back up
    await multitask(
        left.run_angle(500, 300),
        right.run_angle(500, -500)
    )
    await db.straight(-35,Stop.NONE)
    await db.curve(-60,75,Stop.NONE)
    db.settings(500)
    await db.straight(-800)
    db.stop()

async def scissors():
    dbResetSettings()
    #curves to an angle
    await db.curve(475,-40.2, Stop.NONE)
    await multitask(
        #heads forward more
        db.straight(240),
        #expands the scissor to put the flag in spot
        right.run_angle(200,505)
    )
    #closes the scissors
    await right.run_angle(400,-550)

    #goes backward
    await db.straight(-155)

    #straighten out and back up and extend scissors
    await accuTurn(0)
    await multitask(
        db.straight( -130 ), 
        right.run_angle( 500, 505 )
    )

    #release the boulders
    db.drive(0,500 )
    await wait( 500 )
    db.stop()
    await db.straight(-30)
    await accuTurn(8)
    db.settings(None, 100)
    await db.straight( 80 )

    db.settings(*db_def_settings)

    #slam table to the left
    db.drive(0,-500)
    await wait(500)
    db.stop()

    # pull back
    await right.run_angle(500, -505)

    #center up
    await accuTurn(0)
    
    #knock the stone off
    await db.curve( 361, 40, Stop.BRAKE )
    #arm down
    await left.run_angle(500, 390)
    
    #slam the stone
    await db.turn( 30 )
    db.stop( )
    
    #push boulders and stone in
    await accuTurn( 50 )
    await multitask(
        right.run_angle(500, 505),
        left.run_angle(500, -390)
    )
    await right.run_angle(500, -505)
    
    #back up to face the table
    await db.curve( -300, 82 )

    # approach the table
    await db.straight( 180 )
    await left.run_angle(500, 420)
    await db.straight( -170 )
    await db.straight(40)
    await db.turn(-25)

    #OPTIMIZE HERE - SPEED UP ON RETURN

    await multitask(
        db.straight(-500),
        left.run_angle(500, -420)
    )
    db.stop()

async def mega_trident():
    dbResetSettings()

    #move toward the trident & tip it
    await multitask(
        right.run_angle( -500, 360*2.9 ),
        db.straight( 800 )
    )
    #turn toward the three green things
    await accuTurn( -45 )
    #back up and drop our forklift
    await multitask(
        db.straight( -120 ),
        right.run_angle( 500, 360*2.75 )
    )
    #advance and push
    await db.straight( 160 )

    #back up a bit and lift up
    await multitask(
        db.straight( -65 ),
        right.run_angle( 500, -360*2.3 )
    )

    #turn toward the mine cart
    await accuTurn( 68, 0.1 )
    await db.straight( 100 )

    #quick push the mine cart
    await db.turn(-25)

    #TODO: accuturn measurement needed here
    print( "okokok", hub.imu.heading())

    #back up
    await db.straight(-80)

    #curve into position
    await db.curve(-220,45)
    #line up
    await accuTurn(0)
    #back and forth to flip the back green flap
    await db.straight(-90)
    await db.straight(40)

    # #pick up the trident and drop the flag
    await left.run_time(-500,1750)

    # #quick back to home
    db.settings( straight_speed=300, turn_rate=300)
    await db.curve(-800,-45)

    db.stop()

async def boom():
    dbResetSettings()
    #just slowly slam the hammer
    db.settings( turn_acceleration=50 )
    await db.straight( 100 )
    await wait( 500 )
    await db.turn(45)
    #and push it away
    await db.straight( 200 )
    await db.straight( -150 )

    db.stop( )

async def theFinalMission():
    

    #pick up the trident and drop the flag
    await left.run_angle(500,-360*1.8)

    #quick back to home
    db.settings( straight_speed=300, turn_rate=300)
    await db.curve(-800,-45)

    db.stop()

async def boom():
    #just slowly slam the hammer
    db.settings( turn_acceleration=50 )
    await db.straight( 100 )
    await wait( 500 )
    await db.turn(45)
    #and push it away
    await db.straight( 200 )
    await db.straight( -150 )

    db.stop( )

async def theFinalMission():
    dbResetSettings()
    deg = 17
    
    #turn then drop the arm
    await accuTurn( deg, 0.05, speed = 50 )
    await right.run_angle(500,-350),

    #accelerate slowly
    db.settings( None, 100 )
    await db.straight(100,Stop.NONE)

    #then keep on moving at normal speed
    db.settings( *db_def_settings )
    await db.straight(965)

    #turn and push up the statue
    db.drive(0,500)
    await wait(500)
    db.stop()
    #drop the stuff in the middle
    await left.run_time( 500, 1000 )

    #make sure we have our original alignment
    await accuTurn(deg)
    #put the arm down
    await right.run_angle(500,350)
    #back up
    await db.straight( -295 )
    #rear to the thing we need to lift up
    await accuTurn( 90 )
    #slowly back up into the thing we need to lift
    db.settings( 110 )
    await db.straight(-175)
    #push our spinner onto the gear
    db.drive(0,-50)
    await wait(800)
    db.stop()
    #spin it to raise it up
    await left.run_time( 500, 2000 )

    #get away fast and come home
    db.settings(*db_def_settings)
    await db.straight( 200 )
    await db.turn(-50)
    db.settings( 500 )
    await db.straight(-1000)
    db.stop()

# given abcd, and b, return bcda
def move_to_front(my_list, value):
    index = my_list.index(value)
    shifted_list = my_list[index:] + my_list[:index]
    return shifted_list

missions = ["1", "2", "3", "4", "5"]
while True:
    # Print battery voltage in millivolts
    voltage = hub.battery.voltage()
    print(f"Battery voltage: {voltage} mV")

    dbResetSettings()
    db.use_gyro( True )

    selected = hub_menu( *missions )
    if selected == "1":
        run_task(mega_trident())
        missions = move_to_front(missions, "2")
    if selected == "2":
        run_task(flag_pull())
        missions = move_to_front(missions, "3")
    if selected == "3":
        run_task(scissors())
        missions = move_to_front(missions, "4")
    if selected == "4":
        run_task(theFinalMission())
        missions == move_to_front(missions, "5")
    if selected == "5":
        run_task(boom())
        missions == move_to_front(missions, "1")

