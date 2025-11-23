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
        

        # print( 'c', current_angle, 'd', angle_difference, 'speed', speed )

        direction = speed if clockwise else -speed
        db.drive(0, direction)
    
    wait( 500 )
    print( 'post', hub.imu.heading() )

def dbResetSettings( ):
    db.settings( *db_def_settings )





async def flag_pull():
    await db.straight(1212)
    #turning
    accuTurn(-90)
    # goes to the basket-land
    await db.straight(50)
    #raising table
    await right.run_angle(500, 950)
    #hits basket
    await left.run_angle(500, -500)
    await left.run_angle(500, 500)
    await right.run_angle(500, -950)
    await db.straight(-250)
    accuTurn(0)
    await db.straight(500)
    await db.stop()
    
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
    #moves slightly forward
    # await db.straight(100)
    #turns away form the mission
    await db.turn(50)
    #multitasks: brings the rubber arm back to its origin spot, backs up to starting point
    await multitask(
        left.run_angle(500, -500),
        db.straight(-700)
    )
    await db.stop()

async def sandy():
    db.use_gyro( True )
    #move toward the ship
    await db.straight( 500 )
    
    #make sure we are facing the ship head on
    accuTurn(0, 0.1)
    
    #grind into the sunken ship
    await wait( 500 )
    await db.drive(100,15)
    await wait( 1200 )
    await db.stop()

    #drop the slide / grab the red arm
    await right.run_angle(500, -340)
    #pull the red arm back
    await db.straight( -100 )
    #drop the red arm
    await right.run_angle( 500, 340 )

    #back to base
    await db.straight( -500 )

    await db.stop()


# run_task(sandy())

async def trident_pt_1():
    await db.straight( 700 )
    await db.straight( -175 )
    await left.run_angle( 500, -360*1.5 )
    await db.straight(-700)
    await db.stop()




async def trident_pt_2():
    await db.straight( 800 )
    accuTurn( -45 )
    await db.straight( -100 )
    await right.run_angle( 500, 360*6 )
    await db.straight( 150 )
    await db.straight( -65 )
    await right.run_angle( 500, -360*6 )
    await db.curve( -250, -70, Stop.NONE)
    await db.straight( -600 )
    await db.stop()




async def boom():
    #goes forward
    await db.straight(250)
    #repeats the same proccess 4 times(boom), hammering the silo
    for four_times_cause_four_letters_in_boom in "boo":
        await right.run_time(-500, 1000 )
        await right.run_time(500, 1000 )
        #goes backwards to the starting point
    await db.straight(-300)
    await db.stop()




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
    await db.stop()





async def theFinalMission():
    await right.run_angle(500,-300)
    #going straight
    await db.straight(1000)
    #turns
    await db.turn(45)
    await db.straignt(-200)
    await db.stop()
    # #lifts fossil-thing up a little bit
    # await right.run_angle(270,100)
    # #turns
    # await multitask(
    #     db.turn(45),
    #     right.run_angle(300,300)
    # )





# given abcd, and b, return bcda
def move_to_front(my_list, value):
    index = my_list.index(value)
    shifted_list = my_list[index:] + my_list[:index]
    return shifted_list

missions = ["7", "2", "3","4","5","X","7","1"]
while True:
    # Print battery voltage in millivolts
    voltage = hub.battery.voltage()
    print(f"Battery voltage: {voltage} mV")

    selected = hub_menu( *missions )
    if selected == "1":
        run_task(sandy())
        missions = move_to_front(missions, "2")
    if selected == "2":
        run_task(trident_pt_1())
        missions = move_to_front(missions, "3")
    if selected == "3":
        run_task(trident_pt_2())
        missions = move_to_front(missions, "4")
    if selected == "4":
        run_task(flag_pull())
        missions = move_to_front(missions, "5")
    if selected == "5":
        run_task(scissors())
        missions = move_to_front(missions, "X")
    if selected == "X":
        run_task(boom())
        missions == move_to_front(missions, "7")
    if selected == "7":
        run_task(stone_slab() )
        missions == move_to_front(missions, "8")
    if selected == "8":
        run_task(theFinalMission())
        missions == move_to_front(missions, "1")        
