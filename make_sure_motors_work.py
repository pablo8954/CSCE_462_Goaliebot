import time
from adafruit_motorkit import MotorKit


kit = MotorKit()

#move positive direction 
kit.motor1.throttle = 1.0
kit.motor2.throttle = 1.0
time.sleep(5)

#move negative direction
kit.motor1.throttle = -1.0
kit.motor2.throttle = -1.0