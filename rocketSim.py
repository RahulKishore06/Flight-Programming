# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import math

from rocketpy import Rocket, Flight, Function, TrapezoidalFins, SolidMotor, Motor, Environment

from template import SimulatedRocket

def makeDefaultRocket(motor:Motor , numFins: int, sensors: list = []):
    '''
    Set up the rocket to launch in the sim
    motor: An instance of a motor class (SolidMotor etc)
    numFins: The number of fins to be used on the rocket (3 or 4)
    sensors: A list of sensors on the rocket'''
    #REMIND ME TO FILL IN ACTUAl VALUES
    # default values
    rocket = Rocket(
        radius=0.0655,
        mass=24.05,
        inertia=(15.07, 15.07, 0.067),
        power_off_drag=0.65,
        power_on_drag=0.65,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )

    factor = 0.38 / rocket.power_off_drag(0.6)  # From CFD analysis
    rocket.power_on_drag *= factor
    rocket.power_off_drag *= factor

    # add nose
    rocket.add_nose(
        length=0.565,
        kind="vonKarman",
        position=1.477,
    )

    # add tail
    rocket.add_tail(
        top_radius=0.0655, bottom_radius=0.0535, length=0.068, position=-1.226
    )

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
        root_chord=0.20,
        tip_chord=0.12,
        span=0.130,
        position=-0.928,
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
            reshape_thrust_curve=(5.8, 8800),
            grain_number=5,
            grain_separation=0.006,
            grain_outer_radius=0.0465,
            grain_initial_inner_radius=0.016,
            grain_initial_height=0.156,
            grain_density=1748.9,
            nozzle_radius=0.0335,
            throat_radius=0.0114,
            interpolation_method="linear",
            dry_mass=0.00000000001,
            grains_center_of_mass_position=-0.683,
            center_of_dry_mass_position=-0.683,
            dry_inertia=(0.0000000000001, 0.0000000000001, 0.0000000000001),
            nozzle_position=-1.294,
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



class RocketPySimulation(SimulatedRocket):
    '''
    Contains the following attributes
    rocket_ (Rocket): The rocket used in the simulation. Uses makeDefaultRocket to make it
    env_ (Environment): The environment the rocket is launched in. 
    rocket_state_ (list): A list that contains details about the rocket state at the current timestamp 
    dictated by the scheduler
    acceleration_ (float): The Rocket's current acceleration magnitude at the current timestamp dictated
    by the scheduler
    goal_angles_ (list): A list of 4 (maybe 3 if we change it) goal angles for the fins at the current timestamp
    dictated by the scheduler.
    cur_pitch_ (float): A float representing the rocket's current pitch relative to launch orientation at the 
    current timestamp dictated 
    by the scheduler
    cur_yaw_ (float): A float representing the rocket's current yaw relative to laucnh orientation at the current
    timestamp dictated
    '''
    def __init__(self):
        '''
        Sets up the rocketPy Simulation.
        Stores the rocket state after it leaves the rail
        '''
        motor = makeMotor("Test")

        self.rocket_= makeDefaultRocket(motor, 4, [])

        # r1.info()
        # r1.draw()

        # --------------------------------------------------------------
        # --------------------------------------------------------------

        # Environment conditions
        self.env_= makeEnvironment((2025, 10, 23, 17), "America/Denver", 47.213476, 9.003336, 1000)
            
        flight = Flight(
            rocket=self.rocket_,
            environment=self.env_,
            inclination=85,
            heading=105,
            rtol=1e-6,
            atol=1e-6,
            max_time=600,
            rail_length=5.2,
        )  
        self.rocket_state_=flight.out_of_rail_state
        self.cur_pitch_=0
        self.cur_yaw_=0
       
    def getAccelerometerValue(self):
        return self.acceleration_
    def getAltitude(self):
        # From the state vector at index 3:
        # state = [t, x, y, z, vx, vy, vz, e0, e1, e2, e3, omega1, omega2, omega3]
        #          0  1  2  3   4   5   6   7   8   9  10    11      12      13
        return self.rocket_state_[3]
    def getEncoderValues(self):
        pass
    def getGyroscopeValue(self):
        # From the state vector at indices 11, 12, 13:
        # state = [t, x, y, z, vx, vy, vz, e0, e1, e2, e3, omega1, omega2, omega3]
        #          0  1  2  3   4   5   6   7   8   9  10    11      12      13
        
        omega1 = self.rocket_state_[11]  # pitch rate (w1)
        omega2 = self.rocket_state_[12]  # yaw rate (w2)
        omega3 = self.rocket_state_[13]  # roll rate (w3)
        
        #should we introduce some arbritrary noise here?

        return [omega1, omega2, omega3]  # pitch, yaw, roll
    def setControlOutputs(list):
        #this should set the goal angles, but the updating of the actual
        #angles should be kept separate
        pass
    def moveFins(self, time_slice):
        '''
        A Helper function to make advanceOneTimeSlice look less horrific
        '''
        pass
    def advanceOneTimeSlice(self, time_slice:int):
        #Calculate new fin positions
        self.moveFins()
        #Update rocket

        #Make new Flight
        flight = Flight(
            rocket=self.rocket_,
            env=self.env_,
            initial_solution=self.rocket_state_
        )
        #Fetch rocket state and all relevant parameters
        self.rocket_state_=flight.get_solution_at_time(time_slice)
        self.acceleration_= math.sqrt(flight.ax.get_value(time_slice)**2 + flight.ay.get_value(time_slice)**2 + flight.az.get_value(time_slice) **2 )
        self.cur_pitch_+=self.rocket_state_[11]
        self.cur_yaw_+=self.rocket_state[12]
    def getRocketPosition(self) -> list:
        '''
        DO NOT LET THE PD SCRIPT CALL THIS!
        Returns the rocket's current position in the order
        [ x_coord, y_coord, z_coord ]
        '''
        return [self.rocket_state[1], self.rocket_state_[2], self.rocket_state_[3]]
    def getRocketOrientation(self) -> list:
        '''
        DO NOT LET THE PD SCRIPT CALL THIS!
        Returns the rocket's true pitch and yaw in the order
        [ pitch, yaw ]
        '''
        return [self.cur_pitch_, self.cur_yaw_]

    

        