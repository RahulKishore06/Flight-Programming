from rocketSim import RocketPySimulation
from motionControl import PDScript
import numpy as np
import matplotlib.pyplot as plt
def scheduler():
    previous_height=0
    current_time=0
    #1 millisecond
    time_change=1e-3
    sim=RocketPySimulation()
    controller = PDScript(sim)
    #for plotting
    rocket_coordinates_over_time=[]
    rocket_yaw_over_time=[]
    rocket_pitch_over_time=[]
    rocket_roll_over_time=[]

    #FOR TESTING!
    counter=0
    current_altitude=sim.getAltitude()
    while (current_altitude>previous_height):
        previous_height=current_altitude
        current_time+=time_change

        sim.advanceOneTimeSlice(current_time)

        current_altitude=sim.getAltitude()

        #Calculating deflection angles and then updating the simulation
        deflection_angles=controller.get_canard_deflections(current_time)
        sim.setControlOutputs(deflection_angles)
        
        #Plotting Coordinates
        rocket_coordinates_over_time.append(sim.getRocketPosition())

        #Plotting Pitch, Yaw, Roll
        rocket_attitude=sim.getRocketOrientation()
        rocket_pitch_over_time.append([current_time, rocket_attitude[0]])
        rocket_yaw_over_time.append([current_time, rocket_attitude[1]])
        rocket_roll_over_time.append([current_time, sim.getGyroscopeValue()[2]])
        
        #FOR TESTING
        counter+=1
        if (counter>10000):
            break
    coords_array = np.array(rocket_coordinates_over_time)
    x_coords = coords_array[:, 0]
    y_coords = coords_array[:, 1]
    z_coords = coords_array[:, 2]
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot(x_coords, y_coords, z_coords)

    plt.show()
    pitch_array = np.array(rocket_pitch_over_time)
    yaw_array = np.array(rocket_yaw_over_time)
    roll_array = np.array(rocket_roll_over_time)

    # Extract time and angle data
    time_pitch = pitch_array[:, 0]
    pitch_values = pitch_array[:, 1]

    time_yaw = yaw_array[:, 0]
    yaw_values = yaw_array[:, 1]

    time_roll = roll_array[:, 0]
    roll_values = roll_array[:, 1]

    # Plot pitch, yaw, and roll over time
    fig2, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

    ax1.plot(time_pitch, pitch_values)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Pitch")
    ax1.set_title("Pitch over Time")
    ax1.grid(True)

    ax2.plot(time_yaw, yaw_values)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Yaw")
    ax2.set_title("Yaw over Time")
    ax2.grid(True)

    ax3.plot(time_roll, roll_values)
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Roll")
    ax3.set_title("Roll over Time")
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
scheduler()