# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

from rocketpy import Rocket, Flight, Function, TrapezoidalFins, SolidMotor, Motor, Environment

# =================

# Based on "AFS Rocket V1" in the AFS Mech Drive folder. 

# =================



def makeDefaultRocket(motor:Motor , numFins: int, sensors: list = []):
    '''
    Set up the rocket to launch in the sim
    motor: An instance of a motor class (SolidMotor etc)
    numFins: The number of fins to be used on the rocket (3 or 4)
    sensors: A list of sensors on the rocket'''
    
    # ROCKET DIMENSIONS DONE 2/12/2026 ====================
    # https://www.thrustcurve.org/motors/AeroTech/H242T/
    # =====================================================
    rocket = Rocket(
        radius=0.04015,  # 5.5" diameter circle
        mass=1.197,
        inertia=(15.07, 15.07, 0.067),
        power_off_drag=0.65,
        power_on_drag=0.65,
        # power_off_drag=0.1,
        # power_on_drag=0.1,
        center_of_mass_without_motor=-.512,
        coordinate_system_orientation="tail_to_nose",
    )

    # ============== DO WE NEED CFD ANALYSIS? =========================
    factor = 0.38 / rocket.power_off_drag(0.6)  # From CFD analysis
    rocket.power_on_drag *= factor
    rocket.power_off_drag *= factor
    # =================================================================

    # NOSE DIMESIONS DONE 2/13/2026 ====================
    # AFS_V1_Rocket - OpenRocket
    # ==================================================
    rocket.add_nose(
        name="Nose Cone",
        length=0.254,
        kind="vonKarman",
        position=0,
    )

    # MOTOR DIMENSIONS DONE 2/13/2026 ====================
    # AFS_V1_Rocket - OpenRocket
    # ====================================================
    rocket.add_motor(motor, -1.14)
    
    # add parachute
    rocket.add_parachute(
        "Drogue",
        cd_s=0.885,
        trigger="apogee",
        sampling_rate=105,
        noise=(0, 8.3, 0.5),
        lag=0.5,
    )



    # MAIN FIN DIMENSIONS DONE 2/13/2026 ====================
    # AFS_V1_Rocket - OpenRocket
    # =======================================================
    rocket.add_trapezoidal_fins(
        name="Main Fins",
        n=numFins,
        span=0.0635,
        root_chord=0.127,
        tip_chord=0.0762,
        position=-1.02,
        sweep_length=0.025,
        cant_angle=0,
    )

    # DNF YET ============================================
    for sensor in sensors:
        rocket.add_sensor(sensor)
    return rocket

def makeMotor(option):
    '''
    Set up the rocket motor to be simulated
    Available options are 
    1. motor_H242T
    2. Cert (TO BE ADDED!)
    3. Spaceshot (TO BE ADDED!)
    '''
    if option=="motor_H242T":
        #update values as required
        motor = SolidMotor(
            thrust_source = "AeroTech_H242T.csv",
            # reshape_thrust_curve=(5.8, 8800),
            grain_number=4,
            grain_separation=0.006,
            grain_outer_radius=0.035,
            grain_initial_inner_radius=0.016,
            grain_initial_height=0.075,
            grain_density=0.065,
            nozzle_radius=0.0085,
            throat_radius=0.0114,
            interpolation_method="linear",
            dry_mass=0.00000000001,
            grains_center_of_mass_position=0.16,
            center_of_dry_mass_position=0.15,
            dry_inertia=(0.0000000000001, 0.0000000000001, 0.0000000000001),
            nozzle_position=-0.004,
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
    env.set_atmospheric_model(type="wyoming_sounding", file="http://weather.uwyo.edu/cgi-bin/sounding?region=samer&TYPE=TEXT%3ALIST&YEAR=2025&MONTH=02&FROM=0200&TO=0200&STNM=72357")

    env.set_elevation("Open-Elevation")

    env.max_expected_height=max_expected_height
    # env.plots.atmospheric_model()

    return env











motor_H242T = makeMotor("motor_H242T")

r1 = makeDefaultRocket(motor_H242T, 4, [])

# CANARD FIN DIMENSIONS DONE 2/13/2026 ====================
# AFS_V1_Rocket - OpenRocket
# =========================================================


canards = r1.add_trapezoidal_fins(
            name="canards",
            n=4,
            root_chord=0.05,
            tip_chord=0.0254,
            span=0.03,
            position=-0.382,
            sweep_length=0.0145,
            cant_angle=0,
            airfoil=(Function([[0, 0.0002], [2, 0.3320], [4, 0.6335], [6, 0.6877]]), "degrees"),
        )


# r1.info()
# r1.draw()



# --------------------------------------------------------------
# --------------------------------------------------------------

# Environment conditions
env = makeEnvironment((2025, 10, 23, 17), "America/Denver", 40.213476, 9.003336, 1000)
env.set_elevation(0)
env.prints.launch_site_details()
env.add_wind_gust(100, 70)




test_flight = Flight(
    rocket=r1,
    environment=env,
    inclination=60,
    heading=105,
    rtol=1e-6,
    atol=1e-6,
    max_time=600,
    rail_length=5.2,

)




test_flight.plots.angular_kinematics_data()



test_flight.plots.trajectory_3d()
# # test_flight.plots.flight_path_angle_data()
test_flight.plots.attitude_data()


