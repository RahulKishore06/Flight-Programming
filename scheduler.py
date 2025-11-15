from rocketSim import RocketPySimulation

def scheduler():
    previous_height=0
    current_time=0
    #1 millisecond
    time_change=1e-3
    while True:
        RocketPySimulation.advanceOneTimeSlice()
        
        #exit condition
        if (RocketPySimulation.getAltitude()<previous_height):
            #rocket falling, the PD loop should turn off at this point
            break