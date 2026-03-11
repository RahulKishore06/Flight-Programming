import numpy as np
import math
from rocketpy import TrapezoidalFins

def add_afs_canards(
    self,
    drag_coefficient_curve,
    controller_function,
    sampling_rate,
    initial_observed_variables=None,
    override_rocket_drag=False,
    return_controller=False,
    name="Canards",
    controller_name="Canards Controller"
):
    """Creates a new canard set, storing its parameters such as
    drag coefficient curve, controller function, sampling rate, and
    reference area.

    Returns
    -------
    air_brakes : AirBrakes
        AirBrakes object created.
    controller : Controller
        Controller object created.
    """
    canards = self.add_trapezoidal_fins(
        n=4,
        root_chord=0.05,
        tip_chord=0.0254,
        span=0.03,
        position=-0.382,
        sweep_length=0.0145,
        cant_angle=60,
        airfoil=(Function([[0, 0.0002], [2, 0.3320], [4, 0.6335], [6, 0.6877]]), "degrees"),
    )
    _controller = _Controller(
        interactive_objects=canards,
        controller_function=controller_function,
        sampling_rate=sampling_rate,
        initial_observed_variables=initial_observed_variables,
        name=controller_name,
    )
    
    self._add_controllers(_controller)
    if return_controller:
        return canards, _controller
    else:
        return canards

      
def canard_controller_function(
    self,
    time, 
    sampling_rate, 
    state, state_history, 
    observed_variables, 
    interactive_objects, 
    sensors,
    env

):
    canards = self.aerodynamic_surfaces[2]

    if len(self.state_history) == 0:
        previous_state = None
    else:
        previous_state = self.state_history[-1]

    canard_position = canards.cant_angle
    # self.flight.e0[-1][1]
    roll_rate = self.flight.w1[-1][1]
    # deflection_goal = pd_function(roll_rate)
    # 


    #pd_angle needs total velocity,we can maybe use this?
    vx, vy, vz = state[3], state[4], state[5]
    total_velocity = math.sqrt(vx**2 + vy**2 + vz**2)


    altitude_ASL = state[2]
    altitude_AGL = altitude_ASL - env.elevation
    wind_x, wind_y = env.wind_velocity_x(altitude_ASL), env.wind_velocity_y(altitude_ASL)
    e0, e1, e2, e3 = state[6], state[7], state[8], state[9]

    #observed_variables apparently stores anything we return from this function
    #SO we can use this to do smthg idk incase we ever need it - Jonosnon

    if len(observed_variables) > 0:
        observed_variables.append()
    else:
        some_var = 0





    #-----------------
  
    canard_deflection = pd_angle(env.density(altitude_AGL), total_velocity, canards.Af, canard_deflection, canards.evaluate_lift_coefficient(self))
    update_canards(canards, canard_deflection)




def update_canards(canards: TrapezoidalFins, angle: float):
    '''
    Update the canard fin angles during flight
    canards: The canard fin object
    angle: The new angle of the canard fins in degrees
    '''
    canards.changing_attribute_dict['cant_angle'] = angle

def pd_angle(
        rho, # Input air density functions from environment class
        rocket_velocity, # Input current scalar velocity of rocket
        surf_area, # Input from rocket params
        cur_deflection,
        lift_c
    ):
    '''
    Calculate the desired canard fin angle based on the current roll rate and a PD controller.
    Returns the desired angle for the canard fins to achieve the desired roll rate.
    '''
    applied_roll_torque = 0
    roll_moment_of_inertia = 0
    roll_rate = 0

    time_constant=0

    #Changing variables
    kd_phi = 0
    kd_theta = 0
    kd_psi = 0


    

    lift_coe = 2 * math.pi * cur_deflection
    # lift_coe = lift_c
    vel_coe = 0.5 * rho * math.pow(rocket_velocity, 2) * surf_area * lift_coe

    r = 0

    current_phi=0
    current_theta=0
    current_psi=0

    current_rate_phi=0
    current_rate_theta=0
    current_rate_psi=0

    current_attitude_vector=np.array([current_phi], [current_theta], [current_psi])
    current_rate_vector=np.array([current_rate_phi], [current_rate_theta], [current_rate_psi])

    desired_attitude_vec = np.array([current_phi], [current_theta], [current_psi])
    desired_rate_vec = np.array([0], [0], [0])

    error_rates_vec = current_rate_vector - desired_rate_vec

    pd_moments = np.array([0],[0],[0]) # collects from pd function; what we're trying to calculate

    coefficient_matrix = np.array([kd_phi, 0, 0],
                                  [0, kd_theta, 0],
                                  [0, 0, kd_psi])
    
    pd_moments = -coefficient_matrix @ error_rates_vec


    big_L = 10 # distance from center of fin on axis to COG
    big_R = 2 # Radial distance from z axis to COP of canards 
    control_effectiveness_matrix = np.array([0, -vel_coe * big_L, 0, vel_coe * big_L],
                                            [-vel_coe * big_L, 0, vel_coe * big_L, 0],
                                            [big_R * vel_coe, big_R * vel_coe, big_R * vel_coe, big_R * vel_coe])
    
    cem_inv = np.linalg.pinv(control_effectiveness_matrix)

    deflections = cem_inv @ pd_moments


    return deflections