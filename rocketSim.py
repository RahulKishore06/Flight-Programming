# Importing libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

#dfhtmfuy
from rocketpy import Rocket, Flight, Function, TrapezoidalFins, SolidMotor, Motor, Environment

# def makeDefaultRocket(motor:Motor , fins: TrapezoidalFins, fin_positions: list = [], sensors: list = []):
#     '''Set up the rocket to launch in the sim'''
#     #REMIND ME TO FILL IN ACTUAl VALUES
#     # default values
#     rocket = Rocket(
#         radius= 0.0381,
#         mass= 1.04,
#         inertia= 0,
#         power_off_drag= (),
#         power_on_drag=0,
#         center_of_mass_without_motor=0,
#         coordinate_system_orientation="tail_to_nose"
#     )
#     # add nose
#     rocket.add_nose(length=0,kind="",position=0,bluffness=0.0,power=0.0)


#     # add motor
#     rocket.add_motor(motor, 0)
    
#     rocket.add_surfaces(fins,fin_positions)
    
#     # add sensors
#     for sensor in sensors:
#         rocket.add_sensor(sensor)

# r1 = makeDefaultRocket()

# def makeMotor(option):
#     '''
#     Set up the rocket motor to be simulated
#     Available options are 
#     1. Cert
#     2. Spaceshot (TO BE ADDED!)
#     '''
#     if option=="Cert":
#         motor = SolidMotor(
#             thrust_source="FILENAME HERE!",
#             dry_mass=0,
#             dry_inertia=(0),
#             nozzle_radius=0,
#             grain_number=0,
#             grain_density=0,
#             grain_outer_radius=0,
#             grain_initial_inner_radius=0,
#             grain_initial_height=0,
#             grain_separation=0,
#             grains_center_of_mass_position=0,
#             center_of_dry_mass_position=0,
#             nozzle_position=0,
#             burn_time=0,
#             throat_radius=0,
#             coordinate_system_orientation="nozzle_to_combustion_chamber"
#         )
#         return motor
#     else:
#         raise ValueError("Motor option not recognised")





motor_H242T = SolidMotor(
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
# motor_H242T.draw()

drag_curve = .65


r1 = Rocket(
    radius=0.0655,
    mass=24.05,
    inertia=(15.07, 15.07, 0.067),
    power_off_drag=drag_curve,
    power_on_drag=drag_curve,
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)
r1.add_motor(motor_H242T, 0)

r1.add_nose(
    length=0.565,
    kind="vonKarman",
    position=1.477,
).draw()

    
r1.add_trapezoidal_fins(
    n=4,
    root_chord=0.20,
    tip_chord=0.12,
    span=0.130,
    position=-0.928,
    cant_angle=0,
    airfoil=(Function([[0, 0.0002], [2, 0.3320], [4, 0.6335], [6, 0.6877]]), "degrees"),
).draw()


tail = r1.add_tail(
    top_radius=0.0655, bottom_radius=0.0535, length=0.068, position=-1.226
)

drogue = r1.add_parachute(
    "Drogue",
    cd_s=0.885,
    trigger="apogee",
    sampling_rate=105,
    noise=(0, 8.3, 0.5),
    lag=0.5,
)

factor = 0.38 / r1.power_off_drag(0.6)  # From CFD analysis

r1.power_on_drag *= factor
r1.power_off_drag *= factor

r1.info()
r1.draw()

# --------------------------------------------------------------
# --------------------------------------------------------------

# Environment conditions
env = Environment(
    gravity=9.81,
    latitude=47.213476,
    longitude=9.003336,
    date=(2020, 2, 22, 13),
    elevation=407,
)


env.max_expected_height = 1000
    
env.set_date(date=(2025, 10, 23, 17), timezone="America/Denver")

    
est_flight = Flight(
    rocket=r1,
    environment=env,
    inclination=85,
    heading=105,
    rtol=1e-6,
    atol=1e-6,
    max_time=600,
    rail_length=5.2,
)    

print(est_flight.plots.trajectory_3d())
