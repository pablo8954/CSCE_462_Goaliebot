#Libraries
import RPi.GPIO as GPIO
from gpiozero import LED

from adafruit_motorkit import MotorKit 
import time

kit = MotorKit()

#GPIO Mode
left_trig = 27
left_echo = 22

right_trig = 21
right_echo = 20

button = 24

red_left = LED(12)
red_center = LED(16)
green = LED(5)

trig_chan = [left_trig, right_trig]
echo_chan = [left_echo, right_echo]

run = [False]

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

            throttle_speed = 1.0

            left_val = left_readings()
            right_val = right_readings()

            print("Left: ", left_val)
            print("Right: ", right_val)

            left_sees_ball = False
            right_sees_ball = False

            """
            right - broken
            left - good

            """
            if (right_val > 1750):
                right_sees_ball = True
            if (left_val > 1750):
                left_sees_ball = True

            if (left_val < 150):
                left_sees_ball = True
            if (right_val < 150):
                right_sees_ball = True
            
            # 1750 < right_sensor < 2200 - throw the value out

            # #if movement is detected behind our "boundary line", move the opposite direction as read in attempt to preemtively position itself to block ball
            # boundaryLine = 250
            # if right_val < 1750 and right_val > boundaryLine:
            #     throttle_speed = 0.7 #set speed to half to creep on ball if detected movement behind boundary line
            #     left_sees_ball = True
            # else:   #right_val < 250 or right_val =1750 (close)
            #     right_sees_ball = True
            
            # if left_val < 1750 and left_val > boundaryLine:
            #     throttle_speed = 0.7
            #     right_sees_ball = True
            # else:   #left_val < 250 or left_val =1750 (close)
            #     left_sees_ball = True

            #bad reading from ultrasonic sensors - try again
            if (right_val < 0 or left_val < 0):
                break               

            #case 1 - when the ball is in the center - either both sensors read the ball or read nothing in front
            elif (right_sees_ball and left_sees_ball) or (not right_sees_ball and not left_sees_ball):
                kit.motor1.throttle = 0
                kit.motor2.throttle = 0
                print("standing still")

            #case 2 - ball is in front of right sensor -> strafe right
            elif right_sees_ball:
                kit.motor1.throttle = -throttle_speed
                kit.motor2.throttle = -throttle_speed
                print("moving right")
            
            #case 3 - ball is in right of left sensor -> strafe left
            elif left_sees_ball:
                kit.motor1.throttle = throttle_speed
                kit.motor2.throttle = throttle_speed
                print("moving left")

        elif run[0] == False:
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0
            
def left_readings():
    GPIO.output(trig_chan[0], False) #let sensors settle
    GPIO.output(trig_chan[0], True)  
    time.sleep(0.01)
    GPIO.output(trig_chan[0], False) 

    pulse_start = 0
    pulse_end = 0
    while_loop_flag = 0

    while GPIO.input(echo_chan[0]) == 0:
        pulse_start = time.time()
        while_loop_flag = while_loop_flag + 1
        
    while GPIO.input(echo_chan[0]) == 1:
        pulse_end = time.time()
        while_loop_flag = while_loop_flag + 1

    if while_loop_flag > 1:
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 171250
        distance = round(distance, 2)/10
        
        # if distance > 400:
        #     distance = 400
    
    else:   
        distance = -1

    return distance


def right_readings():
    GPIO.output(trig_chan[1],False)
    GPIO.output(trig_chan[1], True) #take reading  
    time.sleep(0.01)
    GPIO.output(trig_chan[1], False) #turn off reading

    pulse_start = 0
    pulse_end = 0
    while_loop_flag = 0

    while GPIO.input(echo_chan[1]) == 0:
        pulse_start = time.time()
        while_loop_flag = while_loop_flag + 1

    while GPIO.input(echo_chan[1]) == 1:
         pulse_end = time.time()
         while_loop_flag = while_loop_flag + 1

    if while_loop_flag > 1:
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 171250
        distance = round(distance, 2)/10

        # if distance > 400:
        #     distance = 400

    else:
        distance = -1

    return distance

#reset device (either turn on or off)
def callButtonEventHandler(pin): 
    
    #countdown to start only if device is being turned on
    if run[0] == False:
        # 6 seconds to get into position
        green.off()
        red_left.on()
        time.sleep(2)

        red_left.off()
        red_center.on()
        time.sleep(2)
        
        red_center.off()
        green.on()
        time.sleep(2)

    #set flag to opposite (either turn on or off)
    run[0] = not run[0]


if __name__=="__main__":
    main()