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

    #This is what I added, IDK if it helps :sob: -Jonathan        
def canard_controller_function(
    self,
    time, 
    sampling_rate, 
    state, state_history, 
    observed_variables, 
    interactive_objects, 
    sensors,

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



def update_canards(canards: TrapezoidalFins, angle: float):
    '''
    Update the canard fin angles during flight
    canards: The canard fin object
    angle: The new angle of the canard fins in degrees
    '''
    canards.cant_angle = angle

