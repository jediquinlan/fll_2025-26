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
    
    wait( 500 )
    print( 'post', hub.imu.heading() )

def dbResetSettings( ):
    db.settings( *db_def_settings )
    db.reset()





async def flag_pull():
    db.reset()
    await db.straight(1200)
    #turning
    accuTurn(-90)
    # goes to the basket-land
    db.settings(50)
    await db.straight(50)
    db.settings(200)
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
    await db.straight(-25,Stop.NONE)
    await db.curve(-80,75,Stop.NONE)
    await db.straight(-500)
    db.stop()
    



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
    #waits
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

    #turns away form the mission
    await db.turn(50)
    #multitasks: brings the rubber arm back to its origin spot, backs up to starting point
    await multitask(
        left.run_angle(500, -500),
        db.straight(-700)
    )
    db.stop()

async def sandy():
    db.reset()
    db.use_gyro( True )
    #move toward the ship
    await db.straight( 500 )
    
    #make sure we are facing the ship head on
    # accuTurn(0, 0.1)
    
    #grind into the sunken ship
    await wait( 500 )
    db.drive(100,15)
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

    db.stop()


# run_task(sandy())

async def mega_trident():
    db.reset()
    await multitask(
        db.straight( 800 ),
        right.run_angle( 500, 360*1.5 )
    )
    accuTurn( -45 )
    await multitask(
        db.straight( -110 ),
        right.run_angle( 500, 360*2 )
    )
    await db.straight( 150 )
    await db.straight( -65 )
    await right.run_angle( 500, -360*3 )
    accuTurn(95,0.1)
    # await db.straight(-74)
    await right.run_angle( 500, 360*3.2 )
    await db.straight(40)
    # await db.straight(75)
    accuTurn(85)
    await right.run_angle( 500, -360*3.5 )
    accuTurn(90)
    await db.straight(-100)
    accuTurn(0)
    await wait(500)
    await db.straight(-215)
    db.settings(300)
    await left.run_angle(500,-360*1.8)
    await db.straight(-800)
    dbResetSettings()

    db.stop()

async def boom():
    db.reset()
    #goes forward
    await db.straight(260)
    #repeats the same proccess 4 times(boom), hammering the silo
    for four_times_cause_four_letters_in_boom in "boo":
        await right.run_time(-500, 1000 )
        await right.run_time(500, 1000 )
        #goes backwards to the starting point
    await db.straight(-300)
    db.stop()




async def stone_slab():
    db.reset()
    #goes forward
    await db.straight(630)
    #turns
    accuTurn( 45 )

    #lowers arm to smack the well-thingy
    await left.run_angle(-500,500)
    await db.turn( 45 )
    await left.run_angle(500,500)
    await db.turn(90)
    await db.straight(1000)
    db.stop()





async def theFinalMission():
    db.reset()
    accuTurn( 15, 0.01 )
    await multitask(
        right.run_angle(500,-350),
        db.straight(1050)
    )
    #turns
    await db.turn(30)
    await accuTurb(15)
    await db.straight(-200)
    await right.run_angle(500,350)
    db.stop()





# given abcd, and b, return bcda
def move_to_front(my_list, value):
    index = my_list.index(value)
    shifted_list = my_list[index:] + my_list[:index]
    return shifted_list

missions = ["1", "2", "3", "4", "5", "X", "7"]
while True:
    # Print battery voltage in millivolts
    voltage = hub.battery.voltage()
    print(f"Battery voltage: {voltage} mV")

    selected = hub_menu( *missions )
    if selected == "1":
        run_task(mega_trident())
        missions = move_to_front(missions, "2")
    if selected == "2":
        run_task(sandy())
        missions = move_to_front(missions, "2")
    if selected == "3":
        run_task(flag_pull())
        missions = move_to_front(missions, "4")
    if selected == "4":
        run_task(scissors())
        missions = move_to_front(missions, "X")
    if selected == "X":
        run_task(boom())
        missions == move_to_front(missions, "6")
    if selected == "6":
        run_task(stone_slab() )
        missions == move_to_front(missions, "7")
    if selected == "7":
        run_task(theFinalMission())
        missions == move_to_front(missions, "1")        
