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

def dbFast( how_fast ):
    straight_speed, straight_acc, turn_rate, turn_acc = db_def_settings
    db.settings(
        straight_speed * how_fast,
        straight_acc,          # keep acceleration
        turn_rate * how_fast,
        turn_acc               # keep turn acceleration
    )

async def accuTurn(target_angle, tolerance=0.25, speed=80):
    while True:
        current_angle = hub.imu.heading()
        angle_difference = target_angle - current_angle

        # Check if we're within the tolerance range of the target angle
        if abs(angle_difference) <= tolerance:
            # print( 'W00t', current_angle )
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
    # print( 'post', hub.imu.heading() )

async def flag_pull():
    dbResetSettings()

    dbFast( 2 )

    #approach ship
    await multitask(
        db.straight(580),
        right.run_angle(500,430)
    )

    #drop arm on sand
    await right.run_angle(500,270)
    #pull back the sand
    await db.straight(-150)

    #position arm to push the ship
    await right.run_angle(500,-100)

    #slow down and push the ship out of the way
    # db.settings(75)

    dbFast( 1 )
    await db.straight(325, Stop.BRAKE)
    
    #drop the flag
    await left.run_angle(500, -250)

    await multitask(
        #finish drop the flag
        left.run_angle(500, 250),

        #arm up
        right.run_angle(500,-300)
    )

    #get back
    dbFast( 2 );
    await db.straight( -400, then=Stop.NONE )
    await db.arc(500,-45)

    #done
    db.stop()


async def scissors():
    dbResetSettings()

    #curves to an angle
    await db.curve(475,-40.2, Stop.NONE)
    dbFast( 2 )
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

    db.settings( *db_def_settings )

    #straighten out and back up and extend scissors
    await accuTurn(0)
    await multitask(
        db.straight( -138 ), 
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
    await wait(650)
    #done
    db.stop()

    # pull back
    await right.run_angle(500, -505)

    #center up/align
    await accuTurn(0)
    
    #curve into the boulders area
    await db.curve( 361, 45, Stop.NONE )
    #moves forward more
    await db.straight(10)
    #arm down
    await left.run_angle(300, 445)
    
    # push boulders and stone in, raise arm back up
    await multitask(
        right.run_angle(500, 485),
        left.run_angle(500, -410)
    )
    await right.run_angle(500, -505)

    #arcs backward to start
    dbFast(2)
    await db.arc(350,-90, then = Stop.NONE)
    #backs the rest of the distance to the starting point
    await db.straight(-200)

    #done
    db.stop()


async def mega_trident():
    dbResetSettings()

    dbFast( 1 )

    #move toward the trident & tip it
    await multitask(
        right.run_angle( 500, 360*1 ),
        db.straight( 800 )
    )

    db.settings( *db_def_settings )

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
    # db.settings( straight_speed=300, turn_rate=300)
    dbFast( 2 )
    await db.curve(-800,-45,Stop.NONE)
    await db.straight (-200)
    #done
    db.stop()

async def drop():
    dbResetSettings()
    dbFast( 2 )

    #drives forward to the dinosaur thing
    await db.straight(500)
    await accuTurn(3)
    await db.straight(60)
    await left.run_angle(500,-550)

    #turns to put left arm under the dino-thing
    await accuTurn(13)

    #raises the thing
    await left.run_angle(150, 170)
    await db.turn(-15)
    #slow step back
    db.settings(50,50)
    await db.straight(-20)

    #curves out and goes back to starting area
    how_fast =2
    straight_speed, straight_acc, turn_rate, turn_acc = db_def_settings
    db.settings(
        straight_speed * how_fast,
        straight_acc * how_fast,       # keep acceleration
        turn_rate * how_fast,
        turn_acc  )

    await multitask(
        db.arc(500, -50,then = Stop.NONE),
        left.run_angle(500,300)
    )
    #done
    db.stop()

async def Crossy_Board():
    dbResetSettings()

    #fast to the ship
    dbFast( 2 )
    await db.straight(810)

    #smooth for middle of mission
    db.settings(*db_def_settings)

    #turn to spin up the treasure
    await accuTurn(-20)
    await left.run_angle(500, 360*0.8)
    await accuTurn(0)
    await db.straight(-80)
    await accuTurn(95)

    #dock to pick up the slide panel
    db.settings(None, 100 )
    await db.straight(100)
    
    #back up & head home
    dbFast( 2 )
    await db.straight(-100)
    await accuTurn(15)
    await db.straight(200,Stop.NONE)
    await db.arc(-800,60)

    #done
    db.stop()

async def spinnyThing():
    dbResetSettings()
    #go fast since so close
    dbFast( 2 )
    await accuTurn(-10)
    await db.straight(285)
    #slam!
    for x in range (3):
        await right.run_angle(500,-100)
        await right.run_angle(500,100)
    await db.straight(-285+67-67)
    #done
    db.stop()
    
async def AfterScissors():
    dbResetSettings()
    #face table
    # await right.run_angle(500, -100)
    await db.straight(120)
    await accuTurn(-42)
    await db.straight(365)
    await left.run_angle(300,445)

    #pull the table up
    # db.settings(*db_def_settings)
    await db.straight(-200)
    await db.straight(50)

    # await db.straight(-460)
    
    #back up to lift little table
    await left.run_angle(300,-145)
    dbFast( 2 )
    await multitask (
        db.straight(-500),
        left.run_angle (300,-300)
    )
    # await db.straight(-110)
    # await multitask(
    #     right.run_angle(-400, 500),
    #     accuTurn(120)
    # )
    # await db.arc(300,-60)

    # dbFast( 2 )
    # await db.arc(240, 60, None, Stop.NONE)
    # await db.straight(300)
    #done
    db.stop()


# given abcd, and b, return bcda
def move_to_front(my_list, value):
    index = my_list.index(value)
    shifted_list = my_list[index:] + my_list[:index]
    return shifted_list

missions = ["1", "2", "3", "4", "5", "6", "7"]
while True:

    # Print battery voltage in millivolts
    voltage = hub.battery.voltage()
    print(f"Battery voltage: {voltage} mV")
    if voltage > 8000:
        hub.light.on(Color.GREEN)
    else:
        hub.light.on(Color.RED)

    selected = hub_menu( *missions )
    print(f"Selected mission: {selected}")
    
    timer = StopWatch()

    dbResetSettings()
    db.use_gyro( True )

    if selected == "1":
        run_task(scissors())
        missions = move_to_front(missions, "2")
    if selected == "2":
        run_task(AfterScissors())
        missions = move_to_front(missions, "3")
    if selected == "3":
        run_task(spinnyThing())
        missions = move_to_front(missions, "4") 
    if selected == "4":
        run_task(Crossy_Board())
        missions = move_to_front(missions, "5")
    if selected == "5":
        run_task(mega_trident())
        missions = move_to_front(missions, "6")
    if selected == "6":
        run_task(flag_pull())
        missions = move_to_front(missions, "7")
    if selected == "7":
       run_task(drop())
       missions = move_to_front(missions, "7") 

    elapsed = timer.time()
    print(f'Total time: {elapsed/1000:.2f} seconds ({elapsed} ms)')
