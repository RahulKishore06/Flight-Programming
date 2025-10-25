from rocketpy import Rocket, Motor, TrapezoidalFins
def makeDefaultRocket(motor:Motor , fins: list):
    '''Set up the rocket to launch in the sim'''
    #REMIND ME TO FILL IN ACTUAl VALUES
    # default values
    rocket = Rocket(
        radius= 0,
        inertia= 0,
        power_off_drag= (),
        power_on_drag=0,
        center_of_mass_without_motor=0,
        coordinate_system_orientation=""
    )
    # add nose
    rocket.add_nose(length=0,kind="",position=0,bluffness=0.0,power=0.0)

    # add motor
    rocket.add_motor(motor, 0)
    for fin in fins():
        rocket.add_trapezoidal_fins(fin)
    
    

    
