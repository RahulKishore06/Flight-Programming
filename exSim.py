import matplotlib.pyplot as plt
import numpy as np

from rocketpy import Environment, Flight, Function, GenericMotor, Rocket
from rocketpy.simulation.flight_data_importer import FlightDataImporter


env = Environment(
    latitude=32.939377,
    longitude=-106.911986,
    elevation=1401,
)
env.set_date(date=(2023, 6, 24, 9), timezone="America/Denver")



env.max_expected_height = 6000

# env.info()

motor_M1520 = GenericMotor(
    # burn specs
    thrust_source="AeroTech_H242T.csv",
    burn_time=4.897,
    propellant_initial_mass=3.737,
    dry_mass=2.981,
    # casing specs: Pro98 3G Gen2 casing
    chamber_radius=0.064,
    chamber_height=0.548,
    chamber_position=0.274,
    nozzle_radius=0.027,
)


# motor_M1520.info()

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


prometheus = Rocket(
    radius=0.06985,  # 5.5" diameter circle
    mass=13.93,
    inertia=(
        4.87,
        4.87,
        0.05,
    ),
    power_off_drag=prometheus_cd_at_ma,
    power_on_drag=lambda x: prometheus_cd_at_ma(x) * 1.02,  # 5% increase in drag
    center_of_mass_without_motor=0.9549,
    coordinate_system_orientation="tail_to_nose",
)

prometheus.set_rail_buttons(0.69, 0.21, 60)

prometheus.add_motor(motor=motor_M1520, position=0)
nose_cone = prometheus.add_nose(length=0.742, kind="Von Karman", position=2.229)
fin_set = prometheus.add_trapezoidal_fins(
    n=3,
    span=0.13,
    root_chord=0.268,
    tip_chord=0.136,
    position=0.273,
    sweep_length=0.066,
)
drogue = prometheus.add_parachute(
    "Drogue",
    cd_s=1.6 * np.pi * 0.3048**2,  # Cd = 1.6, D_chute = 24 in
    trigger="apogee",
)
main = prometheus.add_parachute(
    "Main",
    cd_s=2.2 * np.pi * 0.9144**2,  # Cd = 2.2, D_chute = 72 in
    trigger=457.2,  # 1500 ft
)

# prometheus.draw()
# prometheus.plots.drag_curves()

test_flight = Flight(
    rocket=prometheus,
    environment=env,
    inclination=80,
    heading=75,
    rail_length=5.18,
)

# test_flight.prints.initial_conditions()
# test_flight.prints.surface_wind_conditions()
# test_flight.prints.launch_rail_conditions()
test_flight.prints.out_of_rail_conditions()
test_flight.prints.burn_out_conditions()
test_flight.prints.apogee_conditions()
# test_flight.prints.events_registered()
# test_flight.prints.impact_conditions()
test_flight.prints.stability_margin()
test_flight.prints.maximum_values()
# test_flight.prints.numerical_integration_settings()

test_flight.plots.trajectory_3d()