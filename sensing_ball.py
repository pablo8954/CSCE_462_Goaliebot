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

    time.sleep(5);
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_chan, GPIO.OUT)
    GPIO.setup(echo_chan, GPIO.IN)

    #be default, motors are off
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

    while True:
        if run[0] == True:
            GPIO.setmode(GPIO.BCM);
            #button callback to turn robot on & off
            GPIO.setup(button, GPIO.IN)
            GPIO.add_event_detect(button, GPIO.RISING)
            GPIO.add_event_callback(button, callButtonEventHandler)
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
            if left_val > 500:
                left_val = 500;

            print ("Left Distance:", left_val, "cm")
            #leftsensorArray.append(distance)
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)

            #button callback to turn robot on & off
            GPIO.setup(button, GPIO.IN)
            GPIO.add_event_detect(button, GPIO.RISING)
            GPIO.add_event_callback(button, callButtonEventHandler)
            # right sensor
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
            if right_val > 500:
                right_val = 500

            print ("Right Distance:", right_val, "cm\n")
            #rightsensorArray.append(distance)
            GPIO.cleanup()
            
            #button callback to turn robot on & off
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(button, GPIO.IN)
            GPIO.add_event_detect(button, GPIO.RISING)
            GPIO.add_event_callback(button, callButtonEventHandler)
            time.sleep(.01)

            # move bot left if readings are skewed towards left
            if left_val - right_val > 50:
                kit.motor1.throttle = 1
                kit.motor2.throttle = 1
                print("moving forward")
                
            
            # move bot right if readings are skewed towards right 
            elif right_val - left_val > 50:
                kit.motor1.throttle = -1
                kit.motor2.throttle = -1
                print("moving back")
                

            #ball in in center/not in vision - don't move
            else: 
                kit.motor1.throttle = 0
                kit.motor2.throttle = 0
                print("standing still")

        elif run[0] == False:

            kit.motor1.throttle = 0
            kit.motor2.throttle = 0
            
def callButtonEventHandler(pin):
    run[0] = not run[0]

if __name__=="__main__":
    main()

"""
TODO: 

- add code so motors run indefinitely until new readings come in saying otherwise
- adjust sensor tolorence
"""