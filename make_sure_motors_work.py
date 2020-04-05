from adafruit_motorfruit import MotorKit
import time


kit = MotorKit()

kit.motor1.throttle = 1.0
time.sleep(0.5)
kit.motor1 = 0