from template import SimulatedRocket
import math
import time
def main():
    #constants here
    #FILL WITH ACTUAL VALUES
    #General constants


    #This is for controlling rate of roll
    kP_roll= 0
    kD_roll=0

    #This is for controlling yaw/pitch
    kP_yaw= 0
    kD_yaw=0

    #This is the minimum altitude (in meters) before the rocket is allowed to turn on AFS
    min_alt=10 #since this is for a hypothetical L2 launch, the min_alt is probably just a couple meters above
    # the launch rail

    #initialize some values

    #this is the maximum error tolerated in pitch and yaw
    max_yaw_error=0.01 

    #Yaw and pitch start at zero
    current_yaw=0
    current_pitch=0

    # for derivative term
    prev_roll_error = 0
    prev_yaw_error = 0
    prev_pitch_error = 0

    last_time = time.monotonic_ns()  # remember that this is in nanoseconds

    #kalman filters
    #REMIND ME TO FILL WITH ACTUAL VALUES
    roll_filter= KalmanFilter(0,0,0,0)
    yaw_filter= KalmanFilter(0,0,0,0)
    pitch_filter= KalmanFilter(0,0,0,0)
    while (True):
        #the change in time between the last cycle and the current cycle
        current_time = time.monotonic_ns()
        dt = (current_time - last_time) / 1e9  # convert to seconds
        last_time = current_time

        #change for the actual function later
        angular_velocities=SimulatedRocket.getGyroscopeValue()
        altitude=SimulatedRocket.getAltitude()

        #Use kalman filter to get true angular velocities
        filtered_pitch_rate=pitch_filter.update(angular_velocities[0])
        filtered_yaw_rate=yaw_filter.update(angular_velocities[1])
        filtered_roll_rate=roll_filter.update(angular_velocities[2])

        #update current pitch and yaw
        current_pitch+=filtered_pitch_rate*dt
        current_yaw+=filtered_yaw_rate*dt

        #check if above min alt
        if (altitude>min_alt):
            #I'm aware I don't need these variables, but this is for clarity
            roll_error=filtered_roll_rate
            yaw_error=current_yaw
            pitch_error=current_pitch

            # Derivative terms
            if dt > 0:  
                roll_derivative = (roll_error - prev_roll_error) / dt
                yaw_derivative = (yaw_error - prev_yaw_error) / dt
                pitch_derivative = (pitch_error - prev_pitch_error) / dt
            
            # Calculate PD control outputs
            roll_output = kP_roll * roll_error + kD_roll * roll_derivative
            yaw_output = kP_yaw * yaw_error + kD_yaw * yaw_derivative
            pitch_output = kP_yaw * pitch_error + kD_yaw * pitch_derivative
            
            #convert into deflection angles using dynamics equations
            #TODO!
            
            # update prev errors
            prev_roll_error = roll_error
            prev_yaw_error = yaw_error
            prev_pitch_error = pitch_error


class KalmanFilter:
    '''
    Make a copy of the Kalman Filter class for each value that needs to be filtered.
    So there is 1 KalmanFilter for each of Roll, Yaw, Pitch and Altitude.
    Attributes: 
    X: the estimate of the thing being measured
    P: The error covariance
    Q: The process noise
    R: The measurement noise
    '''
    def __init__(self, process_noise:float, measurement_noise:float, initial_estimate:float, initial_covariance:float):
        '''
        The process_noise and measurement_noise are constant parameters that should never really be changed
        These are the parameters required
        initial_estimate: The most likely start value for the state being measured. For yaw, it should (hopefully)
        start as 0
        initial_covariance: The error covariance
        process_noise: The process noise covariance
        measurement_noise: The measurement noise covariance
        '''
        self.x = initial_estimate      
        self.P = initial_covariance    
        
        # NEVER CHANGE THIS AFTER IT IS DEFINED!
        self.Q = process_noise         
        self.R = measurement_noise     

    def predict(self):
        """Prediction step, apparently its called each time before update is called"""
        # Error covariance increases
        self.P = self.P + self.Q  
    
    def update(self, measurement:float):
        """
        Update step
        Receives a noisy measurement
        Returns the (hopefully) less noisy measurement
        """
        #Predict
        self.predict()
        
        # Calculate Kalman gain
        K = self.P / (self.P + self.R)
        
        # Update estimate
        self.x = self.x + K * (measurement - self.x)
        
        # Update covariance
        self.P = (1 - K) * self.P
        
        return self.x
    
    def get_state(self):
        """Get current filtered value. No updating is being done in this one"""
        return self.x
    
    def get_covariance(self):
        """Get current uncertainty (for when things inevitably go wrong)"""
        return self.P


    



