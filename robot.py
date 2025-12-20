from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, hub_menu
from pybricks.tools import multitask, run_task
from pybricks.tools import StopWatch

WHEEL_DIAMETER = 62.84
AXLE_TRACK = 110

hub = InventorHub( front_side=Axis.Y )
lw = Motor( Port.E, Direction.COUNTERCLOCKWISE )
rw = Motor( Port.A )
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
    timer = StopWatch()
    dbResetSettings()
    #approach ship
    await multitask(
        db.straight(580),
        right.run_angle(500,500)
    )

    #drop arm on sand
    await right.run_angle(500,250)
    #pull back the sand
    await db.straight(-150)

    #position arm to push the ship
    await right.run_angle(500,-100)

    #slow down and push the ship out of the way
    db.settings(75)
    await db.straight(325, Stop.BRAKE)
    
    #drop the flag
    await left.run_angle(500, -250)
    await left.run_angle(500, 250)
    
    #arm up and on we go, not hitting the yellow mission
    db.settings(*db_def_settings)
    await multitask(
        right.run_angle(500,-600),
        db.straight(435)
    )

    #turning
    await accuTurn(-90)
    # goes to the basket-land hi
    db.drive(100, 0)
    await wait(700)
    db.stop()
    
    # raising table
    await multitask(
        right.run_angle(500, 850)
    )
    #move back a bit to avoid blowback
    await db.straight( -30 )
    #drop the arm to drop basket
    await left.run_angle(500, -450)

    await multitask(
        db.straight( -100 ),
        left.run_angle(500, 300),
        right.run_angle(500, -500)
    )
    
    await db.turn(-90)
    # #race on home
    db.settings(400)
    await db.straight(-800)
    db.stop()

    elapsed = timer.time()
    print(f'=== FLAG_PULL COMPLETE ===')
    print(f'Total time: {elapsed/1000:.2f} seconds ({elapsed} ms)')


async def scissors():
    timer = StopWatch()
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

    await db.straight( -220 )
    await db.straight( 40 )
    await left.run_angle(500, -100)
    db.settings( 500 )
    await multitask(
        db.straight(-400),
        left.run_angle(500, -320)
    )

    db.stop()
    elapsed = timer.time()
    print(f'=== SCISSORS COMPLETE ===')
    print(f'Total time: {elapsed/1000:.2f} seconds ({elapsed} ms)')


async def mega_trident():
    timer = StopWatch()
    dbResetSettings()

    #move toward the trident & tip it
    await multitask(
        right.run_angle( 500, 360*1 ),
        db.straight( 800 )
    )
    #turn toward the three green things
    await accuTurn( -46 )
    #back up and drop our forklift
    await multitask(
        db.straight( -120 ),
        right.run_angle( 500, 360*2.75 )
    )
    #advance and push
    await db.straight( 130 )

    #back up a bit, then lift up
    await db.straight( -50 )
    await right.run_angle( 500, -360*2.5 )
    await db.straight(-30)

    # #turn to minecart, then put arm down
    await accuTurn( 76 )
    await right.run_angle(500, 360*2.5 )

    # #go fwd and lift up the mine cart
    await multitask(
        db.straight(100),
        right.run_angle(500, -360*3)
    )

    await db.straight( -190 )
    await accuTurn( 0 )

    await db.straight( -200 )
    await db.straight( 50 )

    #pick up the trident and drop the flag
    await left.run_time(-500, 1500)

    #quick back to home
    db.settings( straight_speed=300, turn_rate=300)
    await db.curve(-800,-45)

    #done
    db.stop()
    elapsed = timer.time()
    print(f'=== MEGA TRIDENT COMPLETE ===')
    print(f'Total time: {elapsed/1000:.2f} seconds ({elapsed} ms)')



async def theFinalMission():
    timer = StopWatch()
    dbResetSettings()
    # await db.straight( -30 )
    db.settings(None, 100 )

    await db.straight(810)
    db.settings(*db_def_settings)

    await accuTurn(-19)
    await left.run_angle(500, 360*0.8)

    await accuTurn(29)
    await db.straight(350)
    await right.run_angle(-500,360*1)

    await accuTurn(29)

    db.settings( *db_def_settings )
    await multitask(
        right.run_angle( 500, 360*0.5),
        db.straight( -300 )
    )

    await accuTurn(29)

    await right.run_angle( -500, 360*0.5 )

    await db.straight( 295 )

    # push up the statue
    db.drive(0,300)
    await wait(200)
    db.stop()

    await right.run_angle( 500, 360 )

    await accuTurn( 20 )


    db.settings( 350, 450 )
    await db.straight( -800, Stop.NONE )
    elapsed = timer.time()

    print(f'=== THEFINALMISSION COMPLETE ===')
    print(f'Total time: {elapsed/1000:.2f} seconds ({elapsed} ms)')

    db.settings(150)
    await db.straight(-500)

    db.stop()



# given abcd, and b, return bcda
def move_to_front(my_list, value):
    index = my_list.index(value)
    shifted_list = my_list[index:] + my_list[:index]
    return shifted_list

missions = ["1", "2", "3", "4"]
while True:
    # Print battery voltage in millivolts
    voltage = hub.battery.voltage()
    print(f"Battery voltage: {voltage} mV")

    dbResetSettings()
    db.use_gyro( True )

    selected = hub_menu( *missions )
    print(f"Selected mission: {selected}")
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
        missions = move_to_front(missions, "4")

