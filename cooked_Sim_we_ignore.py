import matplotlib.pyplot as plt
import numpy as np

from rocketpy import Environment, Flight, Function, SolidMotor, Rocket


env = Environment(
    latitude=29.749907,
    longitude=-95.358421,
    elevation=59,

)
env.set_date(date=(2023, 6, 24, 9), timezone="America/Chicago")
#env.set_atmospheric_model(type="windy_atmosphere")
env.process_standard_atmosphere()
env.set_atmospheric_model(type="standard_atmosphere")
# env.add_wind_gust(5, 5)


env.max_expected_height = 1000

# env.info()


# MOTOR DIMENSION DONE 2/12/2026 ====================
# https://www.thrustcurve.org/motors/AeroTech/H242T/
# ===================================================
motor_H2427T = SolidMotor(
    # burn specs
    thrust_source="AeroTech_H242T.csv",
    burn_time=1.2,
    dry_mass=.258-.111,
    dry_inertia=(0.0000000000001, 0.0000000000001, 0.0000000000001),
    center_of_dry_mass_position=-0.183,
    # chamber_radius=0.019,
    # chamber_height=0.152,
    # chamber_position=-1.064,
    nozzle_radius=0.00297,
    grain_number=2,
    grain_separation=0.006,
    grain_outer_radius=0.035,
    grain_initial_inner_radius=0.016,
    grain_initial_height=0.15,
    grain_density=1748.9,
    grains_center_of_mass_position=-0.4,
)
# motor_H2427T.info()



def prometheus_cd_at_ma(mach):
    """Gives the drag coefficient of the rocket at a given mach number."""
    if mach <= 0.15:
        return 0.422
    elif mach <= 0.45:
        return 0.422 + (mach - 0.15) * (0.38 - 0.422) / (0.45 - 0.15)
    elif mach <= 0.77:
        return 0.38 + (mach - 0.45) * (0.32 - 0.38) / (0.77 - 0.45)
    elif mach <= 0.82:
        return 0.32 + (mach - 0.77) * (0.3 - 0.32) / (0.82 - 0.77)
    elif mach <= 0.88:
        return 0.3 + (mach - 0.82) * (0.3 - 0.3) / (0.88 - 0.82)
    elif mach <= 0.94:
        return 0.3 + (mach - 0.88) * (0.32 - 0.3) / (0.94 - 0.88)
    elif mach <= 0.99:
        return 0.32 + (mach - 0.94) * (0.37 - 0.32) / (0.99 - 0.94)
    elif mach <= 1.04:
        return 0.37 + (mach - 0.99) * (0.44 - 0.37) / (1.04 - 0.99)
    elif mach <= 1.24:
        return 0.44 + (mach - 1.04) * (0.43 - 0.44) / (1.24 - 1.04)
    elif mach <= 1.33:
        return 0.43 + (mach - 1.24) * (0.42 - 0.43) / (1.33 - 1.24)
    elif mach <= 1.49:
        return 0.42 + (mach - 1.33) * (0.39 - 0.42) / (1.49 - 1.33)
    else:
        return 0.39



# ROCKET DIMENSION DONE 2/13/2026 ====================
# AFS_V1_Rocket - OpenRocket
# ===================================================
avioAFS = Rocket(
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

factor = 0.38 / avioAFS.power_off_drag(0.6)  # From CFD analysis
avioAFS.power_on_drag *= factor
avioAFS.power_off_drag *= factor


# avioAFS_v1.set_rail_buttons(0.69, 0.21, 60)

avioAFS.add_motor(
    motor=motor_H2427T, 
    position=-1.14
    )

nose_cone = avioAFS.add_nose(
    length=0.254, 
    kind="Von Karman", 
    position=0)

canard_set = avioAFS.add_trapezoidal_fins(
    n=4,
    span=0.03,
    root_chord=0.05,
    tip_chord=0.0254,
    position=-0.382,
    sweep_length=0.0145,
    cant_angle=60,
)

fin_set = avioAFS.add_trapezoidal_fins(
    n=4,
    span=0.0635,
    root_chord=0.127,
    tip_chord=0.0762,
    position=-1.02,
    sweep_length=0.025,
    cant_angle=60,
)


# fin_set.draw()

drogue = avioAFS.add_parachute(
    "Drogue",
    cd_s=1.6 * np.pi * 0.3048**2,  # Cd = 1.6, D_chute = 24 in
    trigger=100,
)
main = avioAFS.add_parachute(
    "Main",
    cd_s=2.2 * np.pi * 0.9144**2,  # Cd = 2.2, D_chute = 72 in
    trigger=157.2,  # 1500 ft
)

# avioAFS.draw()
# avioAFS.plots.drag_curves()

print("Before Flight instantiation")
test_flight = Flight(
    rocket=avioAFS,
    environment=env,
    inclination=85,
    heading=105,
    rtol=1e-6,
    atol=1e-6,
    max_time=600,
    rail_length=5.2,
    )
print("After Flight instantiation")






# # test_flight.prints.initial_conditions()
# # test_flight.prints.surface_wind_conditions()
# # test_flight.prints.launch_rail_conditions()
# # test_flight.prints.out_of_rail_conditions()
# # test_flight.prints.burn_out_conditions()
# test_flight.prints.apogee_conditions()
# # test_flight.prints.events_registered()
# # test_flight.prints.impact_conditions()
# test_flight.prints.stability_margin()
# # test_flight.prints.maximum_values()
# # test_flight.prints.numerical_integration_settings()

# # final_roll_rate = test_flight.solution[-1][13]
# # print(f"Final Roll Rate: {final_roll_rate} rad/s")

# # # Print initial roll rate
# # initial_roll_rate = test_flight.solution[0][13]
# # print(f"Initial Roll Rate: {initial_roll_rate} rad/s")


# # for i in range(len(test_flight.solution)):
# #     time = test_flight.solution[i][0]
# #     roll_rate = test_flight.solution[i][13]
# #     print(f"Time: {time:.2f} s, Roll Rate: {roll_rate:.2f} rad/s")


#test_flight.plots.trajectory_3d()








