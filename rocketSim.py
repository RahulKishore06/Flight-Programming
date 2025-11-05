from rocketpy import Rocket, TrapezoidalFins, SolidMotor, Motor
def makeDefaultRocket(motor:Motor , fins: TrapezoidalFins, fin_positions: list, sensors: list):
    '''Set up the rocket to launch in the sim'''
    #REMIND ME TO FILL IN ACTUAl VALUES
    # default values
    rocket = Rocket(
        radius= 0.0381,
        mass= 1.04,
        inertia= 0,
        power_off_drag= (),
        power_on_drag=0,
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose"
    )
    # add nose
    rocket.add_nose(length=0,kind="",position=0,bluffness=0.0,power=0.0)


    # add motor
    rocket.add_motor(motor, 0)
    
    rocket.add_surfaces(fins,fin_positions)
    
    # add sensors
    for sensor in sensors:
        rocket.add_sensor()
def makeMotor(option):
    '''
    Set up the rocket motor to be simulated
    Available options are 
    1. Cert
    2. Spaceshot (TO BE ADDED!)
    '''
    if option=="Cert":
        motor = SolidMotor(
            thrust_source="FILENAME HERE!",
            dry_mass=0,
            dry_inertia=(0),
            nozzle_radius=0,
            grain_number=0,
            grain_density=0,
            grain_outer_radius=0,
            grain_initial_inner_radius=0,
            grain_initial_height=0,
            grain_separation=0,
            grains_center_of_mass_position=0,
            center_of_dry_mass_position=0,
            nozzle_position=0,
            burn_time=0,
            throat_radius=0,
            coordinate_system_orientation="nozzle_to_combustion_chamber"
        )
        return motor
    else:
        raise ValueError("Motor option not recognised")
    
def makeFins(numFins=3):
    '''
    Set up the fins to be simulated
    '''
    fins=TrapezoidalFins(
        n=numFins,
        root_chord=0,
        tip_chord=0,
        span=0,
        rocket_radius=0,
        cant_angle=0,
        sweep_length=0,
        sweep_angle=0,
        airfoil=0,
    )
    return fins
    
    

    
