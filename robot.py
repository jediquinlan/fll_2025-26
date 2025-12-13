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

# async def accuTurn(target_angle, tolerance=0.25, speed=80, final_settle_time=200):
#     """
#     Accurate turn to target angle with drift compensation.
    
#     Args:
#         target_angle: Target heading in degrees
#         tolerance: Acceptable error in degrees
#         speed: Maximum turn speed
#         final_settle_time: Time to wait after stopping for gyro to settle (ms)
#     """
#     MAX_SPEED = speed
    
#     while True:
#         current_angle = hub.imu.heading()
#         angle_difference = target_angle - current_angle
#         abs_diff = abs(angle_difference)
        
#         # Check if we're within tolerance
#         if abs_diff <= tolerance:
#             db.stop()
#             # Wait for gyro to settle and motors to fully stop
#             await wait(final_settle_time)
            
#             # Check again after settling
#             final_angle = hub.imu.heading()
#             final_error = abs(target_angle - final_angle)
            
#             if final_error <= tolerance:
#                 print('W00t - Final:', final_angle, 'Error:', final_error)
#                 break
#             else:
#                 # We drifted - continue correcting
#                 print('Drift detected, correcting...', final_angle)
#                 continue
        
#         # Determine direction
#         clockwise = angle_difference > 0
        
#         # Progressive speed reduction with more aggressive slowdown
#         if abs_diff > 45:
#             turn_speed = MAX_SPEED
#         elif abs_diff > 30:
#             turn_speed = min(50, MAX_SPEED)
#         elif abs_diff > 15:
#             turn_speed = 30
#         elif abs_diff > 5:
#             turn_speed = 15
#         else:
#             turn_speed = 10  # Force slow speed near target
        
#         direction = turn_speed if clockwise else -turn_speed
#         db.drive(0, direction)
        
#         # Small delay to prevent CPU spinning
#         await wait(10)
    
#     # Final verification
#     final_heading = hub.imu.heading()
#     print('Final heading:', final_heading, 'Target:', target_angle)

# async def accuTurn(target_angle, tolerance=0.25, speed=80):
#     """Turn with predictive stopping to compensate for momentum."""
#     MAX_SPEED = speed
    
#     # Estimate drift based on current speed (tune these values)
#     DRIFT_COEFFICIENTS = {
#         80: 3.0,  # At speed 80, expect ~3° drift
#         50: 1.5,
#         30: 0.8,
#         15: 0.3,
#         10: 0.1
#     }
    
#     current_speed = 0
    
#     while True:
#         current_angle = hub.imu.heading()
#         angle_difference = target_angle - current_angle
#         abs_diff = abs(angle_difference)
        
#         # Determine turn speed
#         if abs_diff > 45:
#             turn_speed = MAX_SPEED
#         elif abs_diff > 30:
#             turn_speed = 50
#         elif abs_diff > 15:
#             turn_speed = 30
#         elif abs_diff > 5:
#             turn_speed = 15
#         else:
#             turn_speed = 10
        
#         # Get expected drift for current speed
#         expected_drift = DRIFT_COEFFICIENTS.get(turn_speed, 0.5)
        
#         # Stop BEFORE target, accounting for drift
#         if abs_diff <= expected_drift:
#             db.stop()
#             await wait(200)  # Let everything settle
            
#             final_angle = hub.imu.heading()
#             final_error = abs(target_angle - final_angle)
            
#             if final_error <= tolerance:
#                 print('Success! Final:', final_angle, 'Error:', final_error)
#                 break
#             else:
#                 # Need micro-adjustment
#                 print('Micro-adjusting from:', final_angle)
#                 continue
        
#         # Apply turn
#         clockwise = angle_difference > 0
#         direction = turn_speed if clockwise else -turn_speed
#         db.drive(0, direction)
#         current_speed = turn_speed
        
#         await wait(10)
    
#     # Final verification
#     final_heading = hub.imu.heading()
#     print('Final heading:', final_heading, 'Target:', target_angle)


# async def accuTurn(target_angle, tolerance=0.5, speed=80):
#     """Turn with damped approach to prevent oscillation."""
#     MAX_SPEED = speed
#     last_error = None
#     oscillation_count = 0
    
#     while True:
#         current_angle = hub.imu.heading()
#         error = target_angle - current_angle
#         abs_error = abs(error)
        
#         # Detect oscillation (error changing sign rapidly)
#         if last_error is not None and (error * last_error) < 0:
#             oscillation_count += 1
#         else:
#             oscillation_count = 0
        
#         last_error = error
        
#         # If oscillating too much, we're close enough
#         if oscillation_count >= 3:
#             db.stop()
#             await wait(150)
#             print(f'Stopped due to oscillation. Final: {hub.imu.heading():.2f}')
#             break
        
#         # Check if within tolerance with damping check
#         if abs_error <= tolerance:
#             db.stop()
#             await wait(100)
            
#             # Re-check after settling
#             recheck_error = abs(target_angle - hub.imu.heading())
#             if recheck_error <= tolerance * 1:  # Allow slight increase after settling
#                 print(f'Success! Final: {hub.imu.heading():.2f}, Error: {recheck_error:.2f}')
#                 break
#             # Otherwise continue correcting
#             continue
        
#         # Speed based on error with more aggressive slowdown
#         if abs_error > 45:
#             turn_speed = MAX_SPEED
#         elif abs_error > 20:
#             turn_speed = 40
#         elif abs_error > 10:
#             turn_speed = 25
#         elif abs_error > 5:
#             turn_speed = 15
#         elif abs_error > 2:
#             turn_speed = 8
#         else:
#             turn_speed = 5

#         print( "py", turn_speed, abs_error )
        
#         # Apply turn
#         direction = turn_speed if error > 0 else -turn_speed
#         db.drive(0, direction)
        
#         await wait(30)

#     final_heading = hub.imu.heading()
#     print('Final heading:', final_heading, 'Target:', target_angle)

# async def accuTurn(target_angle, tolerance=0.5, speed=80, clockwise=None):
#     """
#     Turn with damped approach and drift compensation.
    
#     Args:
#         target_angle: Target heading in degrees
#         tolerance: Acceptable error in degrees (default 1.5)
#         speed: Maximum turn speed
#         clockwise: If True, force clockwise turn. If False, force counter-clockwise.
#                    If None (default), use shortest path.
#     """
#     MAX_SPEED = speed
    
#     # Calculate initial direction
#     start_angle = hub.imu.heading()
#     initial_error = target_angle - start_angle
    
#     print(f'=== START TURN ===')
#     print(f'Start: {start_angle:.2f}, Target: {target_angle}')
    
#     # Normalize to -180 to 180
#     while initial_error > 180:
#         initial_error -= 360
#     while initial_error < -180:
#         initial_error += 360
    
#     # Determine initial turn direction
#     if clockwise is None:
#         # Shortest path
#         initial_turn_clockwise = initial_error > 0
#         forced_direction = False
#         long_way_target_travel = 0
#     else:
#         # Force the specified direction
#         initial_turn_clockwise = clockwise
#         forced_direction = True
        
#         # Check if this is the long way
#         natural_clockwise = initial_error > 0
#         if initial_turn_clockwise == natural_clockwise:
#             # Same as natural direction - this is the short way
#             long_way_target_travel = abs(initial_error)
#         else:
#             # Opposite of natural direction - this is the long way
#             long_way_target_travel = 360 - abs(initial_error)
    
#     direction_str = "CW" if initial_turn_clockwise else "CCW"
#     if clockwise is None:
#         print(f'Direction: {direction_str} (shortest path)')
#     else:
#         is_long = long_way_target_travel > 180
#         print(f'Direction: {direction_str} (forced, {"long way" if is_long else "short way"})')
#         print(f'Travel required: {long_way_target_travel:.1f}°')
    
#     # Track if we've completed the "forced direction" portion
#     forced_direction_completed = not forced_direction
#     total_travel = 0
#     last_angle = start_angle
    
#     while True:
#         current_angle = hub.imu.heading()
        
#         # Calculate how much we've traveled this iteration
#         angle_delta = current_angle - last_angle
#         # Don't normalize angle_delta - we want to track total rotation
#         total_travel += abs(angle_delta)
#         last_angle = current_angle
        
#         # Calculate error to target
#         error = target_angle - current_angle
        
#         # Normalize error to -180 to 180 range
#         while error > 180:
#             error -= 360
#         while error < -180:
#             error += 360
        
#         abs_error = abs(error)
        
#         # For forced direction, check if we've traveled far enough
#         if forced_direction and not forced_direction_completed:
#             # Switch to normal correction once we've traveled 80% of required distance
#             if total_travel >= long_way_target_travel * 0.8:
#                 print(f'Forced direction phase complete (traveled {total_travel:.1f}°), switching to normal correction')
#                 forced_direction_completed = True
        
#         # Check if within tolerance
#         if abs_error <= tolerance:
#             print(f'*** WITHIN TOLERANCE ({abs_error:.2f}) - STOPPING ***')
#             db.stop()
#             await wait(150)
            
#             # Re-check after settling
#             post_settle_angle = hub.imu.heading()
#             recheck_error = target_angle - post_settle_angle
            
#             # Normalize the recheck error
#             while recheck_error > 180:
#                 recheck_error -= 360
#             while recheck_error < -180:
#                 recheck_error += 360
            
#             recheck_abs_error = abs(recheck_error)
            
#             print(f'After settle: Heading={post_settle_angle:.2f}, Error={recheck_error:.2f}')
            
#             if recheck_abs_error <= tolerance * 1:
#                 print(f'=== SUCCESS! Final: {post_settle_angle:.2f}, Error: {recheck_abs_error:.2f} ===')
#                 break
#             else:
#                 print(f'Drifted, continuing correction')
#                 continue
        
#         # Speed based on error
#         if abs_error > 45:
#             turn_speed = MAX_SPEED
#         elif abs_error > 20:
#             turn_speed = 40
#         elif abs_error > 10:
#             turn_speed = 25
#         elif abs_error > 5:
#             turn_speed = 15
#         elif abs_error > 2:
#             turn_speed = 8
#         else:
#             turn_speed = 5
        
#         # Determine direction
#         if forced_direction_completed:
#             # Normal mode: turn toward target (shortest path)
#             turn_clockwise = error > 0
#         else:
#             # Forced direction mode: maintain initial direction
#             turn_clockwise = initial_turn_clockwise
        
#         direction = turn_speed if turn_clockwise else -turn_speed
#         db.drive(0, direction)
        
#         await wait(30)

async def accuTurn2(target_angle, tolerance=0.5, speed=80, clockwise=None):
    """
    Turn with damped approach, drift compensation, and predictive braking.
    
    Args:
        target_angle: Target heading in degrees
        tolerance: Acceptable error in degrees (default 1.5)
        speed: Maximum turn speed
        clockwise: If True, force clockwise turn. If False, force counter-clockwise.
                   If None (default), use shortest path.
    """
    MAX_SPEED = speed
    
    # Predictive braking parameters - tune these for your robot
    # Format: (speed, degrees_needed_to_stop_safely)
    BRAKING_DISTANCES = {
        300: 45,  # At speed 300, start slowing down 45° before target
        100: 25,
        80: 20,
        40: 12,
        25: 8,
        15: 5,
        8: 3,
        5: 2
    }
    
    # Calculate initial direction
    start_angle = hub.imu.heading()
    initial_error = target_angle - start_angle
    
    print(f'=== START TURN ===')
    print(f'Start: {start_angle:.2f}, Target: {target_angle}')
    
    # Normalize to -180 to 180
    while initial_error > 180:
        initial_error -= 360
    while initial_error < -180:
        initial_error += 360
    
    # Determine initial turn direction
    if clockwise is None:
        # Shortest path
        initial_turn_clockwise = initial_error > 0
        forced_direction = False
        long_way_target_travel = 0
    else:
        # Force the specified direction
        initial_turn_clockwise = clockwise
        forced_direction = True
        
        # Check if this is the long way
        natural_clockwise = initial_error > 0
        if initial_turn_clockwise == natural_clockwise:
            # Same as natural direction - this is the short way
            long_way_target_travel = abs(initial_error)
        else:
            # Opposite of natural direction - this is the long way
            long_way_target_travel = 360 - abs(initial_error)
    
    direction_str = "CW" if initial_turn_clockwise else "CCW"
    if clockwise is None:
        print(f'Direction: {direction_str} (shortest path)')
    else:
        is_long = long_way_target_travel > 180
        print(f'Direction: {direction_str} (forced, {"long way" if is_long else "short way"})')
        print(f'Travel required: {long_way_target_travel:.1f}°')
    
    # Track if we've completed the "forced direction" portion
    forced_direction_completed = not forced_direction
    total_travel = 0
    last_angle = start_angle
    current_speed = 0
    
    while True:
        current_angle = hub.imu.heading()
        
        # Calculate how much we've traveled this iteration
        angle_delta = current_angle - last_angle
        total_travel += abs(angle_delta)
        last_angle = current_angle
        
        # Calculate error to target
        error = target_angle - current_angle
        
        # Normalize error to -180 to 180 range
        while error > 180:
            error -= 360
        while error < -180:
            error += 360
        
        abs_error = abs(error)
        
        # For forced direction, check if we've traveled far enough
        if forced_direction and not forced_direction_completed:
            if total_travel >= long_way_target_travel * 0.8:
                print(f'Forced direction phase complete (traveled {total_travel:.1f}°), switching to normal correction')
                forced_direction_completed = True
        
        # Check if within tolerance
        if abs_error <= tolerance:
            print(f'*** WITHIN TOLERANCE ({abs_error:.2f}) - STOPPING ***')
            db.stop()
            await wait(150)
            
            # Re-check after settling
            post_settle_angle = hub.imu.heading()
            recheck_error = target_angle - post_settle_angle
            
            # Normalize the recheck error
            while recheck_error > 180:
                recheck_error -= 360
            while recheck_error < -180:
                recheck_error += 360
            
            recheck_abs_error = abs(recheck_error)
            
            print(f'After settle: Heading={post_settle_angle:.2f}, Error={recheck_error:.2f}')
            
            if recheck_abs_error <= tolerance * 1.5:
                print(f'=== SUCCESS! Final: {post_settle_angle:.2f}, Error: {recheck_abs_error:.2f} ===')
                break
            else:
                print(f'Drifted, continuing correction')
                continue
        
        # PREDICTIVE SPEED CONTROL
        # Determine what speed we COULD go based on distance
        if abs_error > 100:
            target_speed = MAX_SPEED
        elif abs_error > 60:
            target_speed = min(100, MAX_SPEED)
        elif abs_error > 45:
            target_speed = 80
        elif abs_error > 20:
            target_speed = 40
        elif abs_error > 10:
            target_speed = 25
        elif abs_error > 5:
            target_speed = 15
        elif abs_error > 2:
            target_speed = 8
        else:
            target_speed = 5
        
        # Check if we need to brake early based on CURRENT speed
        braking_distance = BRAKING_DISTANCES.get(current_speed, 0)
        
        # If we're going fast and approaching the braking zone, slow down NOW
        if abs_error <= braking_distance and current_speed > target_speed:
            # We're in the braking zone - drop speed more aggressively
            turn_speed = target_speed
            print(f'BRAKING: Error={abs_error:.1f}°, Current speed={current_speed}, Braking distance={braking_distance:.1f}°, Reducing to {turn_speed}')
        else:
            # Normal speed control
            turn_speed = target_speed
        
        # Determine direction
        if forced_direction_completed:
            # Normal mode: turn toward target (shortest path)
            turn_clockwise = error > 0
        else:
            # Forced direction mode: maintain initial direction
            turn_clockwise = initial_turn_clockwise
        
        direction = turn_speed if turn_clockwise else -turn_speed
        db.drive(0, direction)
        current_speed = turn_speed
        
        await wait(30)

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
    await db.straight( -180 )
    await db.straight(40)
    await db.turn(-25)

    #OPTIMIZE HERE - SPEED UP ON RETURN

    await multitask(
        db.straight(-500),
        left.run_angle(500, -420)
    )
    db.stop()

async def mega_trident():
    timer = StopWatch()
    dbResetSettings()


    #move toward the trident & tip it
    await multitask(
        right.run_angle( 500, 360*1 ),
        db.straight( 800 )
    )
    #turn toward the three green things
    await accuTurn( -45, tolerance=0.5 )
    #back up and drop our forklift
    await multitask(
        db.straight( -120 ),
        right.run_angle( 500, 360*2.75 )
    )
    #advance and push
    await db.straight( 130 )

    #back up a bit, then lift up
    await db.straight( -50 )
    await right.run_angle( 500, -360*2 )

    #turn to minecart, then put arm down
    await accuTurn(80)
    await right.run_angle(500, 360*2 )

    #go fwd and lift up the mine cart
    await multitask(
        db.straight(100),
        right.run_angle(500, -360*3)
    )


    # await db.straight( -75 )

    # # #curve into position
    await db.curve(-160, 90)
    #line up
    await accuTurn(0)
    #back and forth to flip the back green flap
    await db.straight(-120)
    await db.straight(60)

    # #pick up the trident and drop the flag
    await left.run_time(-500,1750)

    # #quick back to home
    db.settings( straight_speed=300, turn_rate=300)
    await db.curve(-800,-45)

    db.stop()
    elapsed = timer.time()
    print(f'=== MEGA TRIDENT COMPLETE ===')
    print(f'Total time: {elapsed/1000:.2f} seconds ({elapsed} ms)')


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
    dbResetSettings()
    await right.run_angle(-500,360*1)
    await db.straight(800)
    await accuTurn(-20)
    # await db.straight(-92)
    # await accuTurn(-2)
    await left.run_angle(500, 360*0.9)
    await accuTurn(26)
    db.settings(100)
    # await db.straight(150)
    # await db.curve(-300, 10)
    # await accuTurn(20)
    await db.straight(300)
    await right.run_angle(500,360*1)
    db.settings(*db_def_settings)
    await db.straight(-150)
    # await db.straight(125)
    # await db.straight(-80)
    await accuTurn(-5)
    await db.straight(-1000)
    # await db.curve(-500,-45)
    db.settings(*db_def_settings)

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
        missions = move_to_front(missions, "5")
    if selected == "5":
        run_task(boom())
        missions = move_to_front(missions, "1")


# async def go():
#     dbResetSettings()
#     await accuTurn( 90, speed=300, clockwise=False )
#     await db.straight( 100 )
#     await accuTurn( 90, tolerance=1.5 )
#     await db.straight( 100 )

# print( "ok" )
# run_task(go())