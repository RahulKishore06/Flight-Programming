from template import SimulatedRocket
import math
import time
def main():
    #constants here
    #FILL WITH ACTUAL VALUES
    #General constants


    #This is for controlling rate of roll
    kP_roll= 0
    kI_roll=0

    #This is for controlling yaw/pitch
    kP_yaw= 0
    kI_yaw=0

    #This is the minimum altitude (in meters) before the rocket is allowed to turn on AFS
    min_alt=10 #since this is for a hypothetical L2 launch, the min_alt is probably just a couple meters above
    # the launch rail

    #initialize some values

    #This is the integral term for the yaw controller
    yaw_integral=0

    #This is the integral term for the pitch controller
    pitch_integral=0

    #this is the maximum error tolerated in pitch and yaw
    max_yaw_error=0.01 

    #Yaw and pitch start at zero
    current_yaw=0
    current_pitch=0
    last_time = time.monotonic_ns()  # remember that this is in nanoseconds
    while (True):
        #the change in time between the last cycle and the current cycle
        current_time = time.monotonic_ns()
        dt = (current_time - last_time) / 1e9  # convert to seconds
        last_time = current_time

        #change for the actual function later
        angular_velocities=SimulatedRocket.getEncoderValues()
        altitude=SimulatedRocket.getAltitude()

        #update current pitch and yaw
        current_pitch+=angular_velocities[0]*dt
        current_yaw+=angular_velocities[1]*dt

        #check if above min alt
        if (altitude>min_alt):
            # if pitch or yaw ever hit 0, the integral term should be reset. This is to ensure that 
            # the integral term doesn't become too large and create an erroneously large control output
            if (math.abs(current_pitch)<max_yaw_error):
                pitch_integral=0
            if (math.abs(current_yaw)<max_yaw_error):
                yaw_integral=0
            



