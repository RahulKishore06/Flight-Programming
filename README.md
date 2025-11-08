# Flight-Programming

Takes in 
1. Yaw 
2. Pitch
3. Rate of Roll
4. Acceleration
5. 4 Motor Encoder Values

Outputs
1. 4 control outputs used for each of the 4 motor controllers.
## Assumptions made 
1. Small angle approximation for deflection angle (frankly, it anything can bump us more than 10 degrees in under 10ms, we cooked anyway)
2. Assuming that the inertia tensor matrix is diagonal