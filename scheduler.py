from rocketSim import RocketPySimulation
from motionControl import PDScript
def scheduler():
    previous_height=0
    current_time=0
    #1 millisecond
    time_change=1e-3
    sim=RocketPySimulation()
    controller = PDScript(sim)
    while True:
        sim.advanceOneTimeSlice(time_change)
        deflection_angles=controller.get_canard_deflections(current_time)
        sim.setControlOutputs(deflection_angles)
        current_time+=time_change
        #exit condition
        if (sim.getAltitude()<previous_height):
            #rocket falling, the PD loop should turn off at this point
            break