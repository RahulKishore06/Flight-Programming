from template import SimulatedRocket
from rocketSim import RocketPySimulation
import math
import time
def main():
    #constants here
    #FILL WITH ACTUAL VALUES
    #General constants

    """
    Inputs:

    Inertia Tensor: Current mass of rocket (including fuel), rocket radius, rocket length
    Error: current roll, pitch, yaw
    Ang. Velocity: current ang. vel of yaw, pitch, roll
    Fin Deflection (delta): dynamic air pressure (possibly made of other inputs), canard surface area, 
                            control effectiveness matrix (represents how one fin affects r, p, y)

    Steps:
    - Assign rocket with the diagonal moment elements
    - Calculate the error in roll, pitch, and yaw
    - Calculate desired angular velocity along each axis (reference doc for detailed explanation)
    - Calculate error between desired and current ang. velocities
        - Store in list
    - Calculate the rate of change in the error in angular velocity
        - Store in list
    - Compute desired angular accelerations abt each axis
        - Multiply the error in ang. vel by the K_p constants and adding eorr in ROC of ang. vel by K_d constants.
    - Calculate desired moments
        - Multiply angular accel. vector by inertia tensor, and then subtract angular vel. x I * ang. vel.
    - desired M = qSE_delta_ to find _delta_

    """


    
    #This is the minimum altitude (in meters) before the rocket is allowed to turn on AFS
    min_alt=10 #since this is for a hypothetical L2 launch, the min_alt is probably just a couple meters above
    # the launch rail

    #this is the maximum error tolerated in pitch and yaw
    max_yaw_error=0.01 

    #Yaw and pitch start at zero
    current_yaw=0
    current_pitch=0

    # for derivative term
    prev_roll_error = 0
    prev_yaw_error = 0
    prev_pitch_error = 0

    last_time = 0 # Should be kept from the last run

    #kalman filters
    #REMIND ME TO FILL WITH ACTUAL VALUES
    # roll_filter= KalmanFilter(0,0,0,0)
    # yaw_filter= KalmanFilter(0,0,0,0)
    # pitch_filter= KalmanFilter(0,0,0,0)



    while (True):
        #the change in time between the last cycle and the current cycle
        current_time = 0 # Given by schedular
        dt = (current_time - last_time) / 1e9  # convert to seconds
        last_time = current_time

        #change for the actual function later
        angular_velocities=SimulatedRocket.getGyroscopeValue()
        altitude=SimulatedRocket.getAltitude()

        pitch_rate=angular_velocities[0]
        yaw_rate=angular_velocities[1]
        roll_rate=angular_velocities[2]

        #Use kalman filter to get true angular velocities
        # filtered_pitch_rate=pitch_filter.update(angular_velocities[0])
        # filtered_yaw_rate=yaw_filter.update(angular_velocities[1])
        # filtered_roll_rate=roll_filter.update(angular_velocities[2])

        #update current pitch and yaw
        current_pitch+=pitch_rate*dt
        current_yaw+=yaw_rate*dt

        #check if above min alt
        if (altitude>min_alt):
            pass

class PDScript:
    '''
    Contains the logic that will actually be running inside the microcontroller
    Contains the following Parameters
    simulation_ (RocketPySimulation): The simulation object passed by reference
    '''           
    def __init__(self, simulation: RocketPySimulation):
        '''
        Initialize all the starting variables for the script

        '''
        self.simulation_=simulation
    def get_canard_deflections():
        '''
        Runs the PD script
        Outputs 4 deflection angles calculated by the script'''

        #default value for now, just wanna check that plotting works 
        return [0,0,0,0]


# class KalmanFilter:
#     '''
#     Make a copy of the Kalman Filter class for each value that needs to be filtered.
#     So there is 1 KalmanFilter for each of Roll, Yaw, Pitch and Altitude.
#     Attributes: 
#     X: the estimate of the thing being measured
#     P: The error covariance
#     Q: The process noise
#     R: The measurement noise
#     '''
#     def __init__(self, process_noise:float, measurement_noise:float, initial_estimate:float, initial_covariance:float):
#         '''
#         The process_noise and measurement_noise are constant parameters that should never really be changed
#         These are the parameters required
#         initial_estimate: The most likely start value for the state being measured. For yaw, it should (hopefully)
#         start as 0
#         initial_covariance: The error covariance
#         process_noise: The process noise covariance
#         measurement_noise: The measurement noise covariance
#         '''
#         self.x = initial_estimate      
#         self.P = initial_covariance    
        
#         # NEVER CHANGE THIS AFTER IT IS DEFINED!
#         self.Q = process_noise         
#         self.R = measurement_noise     

#     def predict(self):
#         """Prediction step, apparently its called each time before update is called"""
#         # Error covariance increases
#         self.P = self.P + self.Q  
    
#     def update(self, measurement:float):
#         """
#         Update step
#         Receives a noisy measurement
#         Returns the (hopefully) less noisy measurement
#         """
#         #Predict
#         self.predict()
        
#         # Calculate Kalman gain
#         K = self.P / (self.P + self.R)
        
#         # Update estimate
#         self.x = self.x + K * (measurement - self.x)
        
#         # Update covariance
#         self.P = (1 - K) * self.P
        
#         return self.x
    
#     def get_state(self):
#         """Get current filtered value. No updating is being done in this one"""
#         return self.x
    
#     def get_covariance(self):
#         """Get current uncertainty (for when things inevitably go wrong)"""
#         return self.P


    



