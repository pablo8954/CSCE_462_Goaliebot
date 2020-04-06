#Libraries
import RPi.GPIO as GPIO
from adafruit_motorfruit import MotorKit 
import time

kit = Motorkit()

#GPIO Mode
left_trig = 21
left_echo = 20

right_trig = 25
right_echo = 24

trig_chan = [left_trig, right_trig]
echo_chan = [left_echo, right_echo]

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_chan, GPIO.OUT)
GPIO.setup(echo_chan, GPIO.IN)

"""
Note - Direction is described to using the robot's point of view as reference.
For example, if an observer were to say "your left eye", you would think of the left eye from your left, not the 
observer's left (that is, their right).

In regards to the robot, it's left eye would be it's right sensor if you were looking at it face on.

"""


def main():

    #be default, motors are off
    kit.motor1.throttle = 0
    kit.motor3.throttle = 0

    while True:
        GPIO.output(trig_chan, False) #let sensors settle
    
        left_val = left_readings()
        right_val = right_readings()

        # move bot left if readings are skewed towards left
        if (left_val < 250 or left_val > 350) and (right_val > 250 and right_val < 350):
            kit.motor1.throttle = 0.5
            kit.motor3.throttle = 0.5
            time.sleep(5)
        
        elif (right_val < 250 or right_val > 350) and (left_val > 250 and left_val < 350):
            kit.motor1.throttle = -0.5
            kit.motor3.throttle = -0.5
            time.sleep(5)

def left_readings():
    
    GPIO.output(trig_chan[0], True)  
    time.sleep(0.01)
    GPIO.output(trig_chan[0], False) 

    while GPIO.input(echo_chan[0]) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_chan[0]) == 1:
         pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 171250

    return round(distance, 2)


def right_readings():
    
    GPIO.output(trig_chan[1], True) #take reading  
    time.sleep(0.01)
    GPIO.output(trig_chan[1], False) #turn off reading

    while GPIO.input(echo_chan[1]) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_chan[1]) == 1:
         pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 171250

    return round(distance, 2)


if __name__=="__main__":
    main()