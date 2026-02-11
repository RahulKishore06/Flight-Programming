# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from rocketpy import Rocket, Flight, Function, TrapezoidalFins, SolidMotor, Motor, Environment

# =================

# Based on "rocket 11.6.ork" in the AFS Mech Drive folder. 

# =================



def makeDefaultRocket(motor:Motor , numFins: int, sensors: list = []):
    '''
    Set up the rocket to launch in the sim
    motor: An instance of a motor class (SolidMotor etc)
    numFins: The number of fins to be used on the rocket (3 or 4)
    sensors: A list of sensors on the rocket'''
    #REMIND ME TO FILL IN ACTUAl VALUES
    # default values
    rocket = Rocket(
        radius=0.04013,
        mass=1.18,
        inertia=(15.07, 15.07, 0.067), # IDK how to find this without calculating every second it moves
        power_off_drag=0.65, # Haven't found.
        power_on_drag=0.65,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )

    factor = 0.38 / rocket.power_off_drag(0.6)  # From CFD analysis
    rocket.power_on_drag *= factor
    rocket.power_off_drag *= factor

    # add nose
    rocket.add_nose(
        length=0.254,
        kind="vonKarman",
        position=0.523,
    )

    # add tail
    # rocket.add_tail(
    #     top_radius=0.0655, bottom_radius=0.0535, length=0.508, position=-0.112
    # )

    # add motor
    rocket.add_motor(motor, 0)
    
    # add parachute
    rocket.add_parachute(
        "Drogue",
        cd_s=0.885,
        trigger="apogee",
        sampling_rate=105,
        noise=(0, 8.3, 0.5),
        lag=0.5,
    )

    # add fins
    rocket.add_trapezoidal_fins(
        n=numFins,
        root_chord=0.126,
        tip_chord=0.0744,
        span=0.0762,
        position=-0.366,
        cant_angle=0,
        airfoil=(Function([[0, 0.0002], [2, 0.3320], [4, 0.6335], [6, 0.6877]]), "degrees"),
    )
    
    
    for sensor in sensors:
        rocket.add_sensor(sensor)
    return rocket

def makeMotor(option):
    '''
    Set up the rocket motor to be simulated
    Available options are 
    1. Test
    2. Cert (TO BE ADDED!)
    3. Spaceshot (TO BE ADDED!)
    '''
    if option=="Test":
        #update values as required
        motor = SolidMotor(
            thrust_source = "AeroTech_H242T.csv",
            # reshape_thrust_curve=(5.8, 8800),
            grain_number=2,
            grain_separation=0.006,
            grain_outer_radius=0.035,
            grain_initial_inner_radius=0.016,
            grain_initial_height=0.15,
            grain_density=1748.9,
            nozzle_radius=0.0335,
            throat_radius=0.0114,
            interpolation_method="linear",
            dry_mass=0.00000000001,
            grains_center_of_mass_position=-0.4,
            center_of_dry_mass_position=-0.183,
            dry_inertia=(0.0000000000001, 0.0000000000001, 0.0000000000001),
            nozzle_position=-.624,
        )
        return motor
    if option=="Cert":
        raise ValueError("Motor option not recognised")
    else:
        raise ValueError("Motor option not recognised")

def makeEnvironment(date, timezone, launch_lat, launch_long, max_expected_height):
    '''
    Set up the launch conditions for the flight sim
    date: A tuple (or list) of 4 items in the form (year, month, day, hour)
    timezone: Timezone name. To see full list, print(pytz.all_timezones)
    launch_lat: Latitude in degrees of rocket launch location
    launch_long: Longtitude in degrees of rocket launch location
    max_expected_height: Altitude in meters to keep weather data
    '''
    env = Environment(
        gravity=9.81, # guess I could make gravity 9.80665 but I'm not sure we need that much accuracy in a demo
        latitude=launch_lat,
        longitude=launch_long,
    )   
    env.set_date(date, timezone)
    #Use the open-elevation API to automatically find elevation
    env.set_elevation("Open-Elevation")

    env.max_expected_height=max_expected_height

    return env

motor = makeMotor("Test")

r1= makeDefaultRocket(motor, 4, [])

# r1.info()
r1.draw()

# --------------------------------------------------------------
# --------------------------------------------------------------

# Environment conditions
env = makeEnvironment((2025, 10, 23, 17), "America/Denver", 40.213476, 9.003336, 1000)
env.set_elevation(0)
env.prints.launch_site_details()

test_flight = Flight(
    rocket=r1,
    environment=env,
    inclination=85,
    heading=105,
    rtol=1e-6,
    atol=1e-6,
    max_time=600,
    rail_length=5.2,


  
# Flight.initial_solution = [tInit, x_init,
# y_init, z_init, vx_init, vy_init, vz_init, e0_init, e1_init,
# e2_init, e3_init, w1_init, w2_init, w3_init]



)    

test_flight.plots.trajectory_3d()
