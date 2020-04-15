#Libraries
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit 
import time

kit = MotorKit()

#GPIO Mode
left_trig = 27
left_echo = 22

right_trig = 21
right_echo = 20

button = 24

trig_chan = [left_trig, right_trig]
echo_chan = [left_echo, right_echo]

run = [True]


"""
Note - Direction is described using the robot's point of view as reference.
For example, if an observer were to say "your left eye", you would think of the left eye from your left, not the 
observer's left (that is, their right).

In regards to the robot, its left eye would be its right sensor if you were looking at it face on.

"""

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_chan, GPIO.OUT)
    GPIO.setup(echo_chan, GPIO.IN)

    #button callback to turn robot on & off
    GPIO.setup(button, GPIO.IN)
    GPIO.add_event_detect(button, GPIO.RISING)
    GPIO.add_event_callback(button, callButtonEventHandler)

    #be default, motors are off
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

    while True:
        if run[0] == True:
            
            # left_val = left_readings()
            # right_val = right_readings()
            # print(left_val)
            # print(right_val)

            GPIO.setwarnings(False)
            #left sensor (from robot's perspective)

            TRIG = 27
            ECHO = 22

            #print("Distance Measurement in Progress")

            GPIO.setup(TRIG,GPIO.OUT)
            GPIO.setup(ECHO,GPIO.IN)

            GPIO.output(TRIG, False)
            #print("Waiting for Sensor To Settle")
            #time.sleep(2)

            GPIO.output(TRIG, True)
            time.sleep(.01)
            GPIO.output(TRIG,False)

            while GPIO.input (ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input (ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration *17150

            left_val = round(distance, 2)

            print ("Left Distance:", distance, "cm")
            #leftsensorArray.append(distance)
            GPIO.cleanup()
            # right sensor
            GPIO.setmode(GPIO.BCM)

            TRIG_right = 21
            ECHO_right = 20

            #print("Distance Measurement in Progress")

            GPIO.setup(TRIG_right,GPIO.OUT)
            GPIO.setup(ECHO_right,GPIO.IN)

            GPIO.output(TRIG_right, False)
            #print("Waiting for Sensor To Settle")
            #time.sleep(2)

            GPIO.output(TRIG_right, True)
            time.sleep(0.00001)
            GPIO.output(TRIG_right,False)

            while GPIO.input (ECHO_right) == 0:
                pulse_start = time.time()

            while GPIO.input (ECHO_right) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration *17150

            right_val = round(distance, 2)

            print ("Right Distance:", distance, "cm\n")
            #rightsensorArray.append(distance)
            GPIO.cleanup()

            time.sleep(.01)

            # move bot left if readings are skewed towards left
            if (left_val < 250 or left_val > 500) and (right_val > 250 and right_val < 500):
                kit.motor1.throttle = 0.1
                kit.motor2.throttle = 0.1
                print("moving forward")
                time.sleep(1)
            
            # move bot right if readings are skewed towards right 
            elif (right_val < 250 or right_val > 500) and (left_val > 250 and left_val < 500):
                kit.motor1.throttle = -0.1
                kit.motor2.throttle = -0.1
                print("moving back")
                time.sleep(1)

            #ball in in center/not in vision - don't move
            else: 
                kit.motor1.throttle = 0
                kit.motor2.throttle = 0
                print("standing still")

        elif run[0] == False:
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0
            


def left_readings():
    GPIO.output(trig_chan[0], False) #let sensors settle
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
    GPIO.output(trig_chan[1],False)
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

def callButtonEventHandler(pin):
    run[0] = not run[0]

if __name__=="__main__":
    main()

"""
TODO: 

- add code so motors run indefinitely until new readings come in saying otherwise
- adjust sensor tolorence
"""