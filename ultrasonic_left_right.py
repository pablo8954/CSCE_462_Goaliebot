import RPi.GPIO as GPIO
import time

while True:

    #left sensor (from robot's perspective)
    GPIO.setmode(GPIO.BCM)

    TRIG = 23
    ECHO = 24

    print("Distance Measurement in Progress")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    print("Waiting for Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)

    while GPIO.input (ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input (ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration *17150

    distance = round(distance, 2)

    print ("Left Distance:", distance, "cm")
    GPIO.cleanup()
    # right sensor
    GPIO.setmode(GPIO.BCM)

    TRIG_right = 17
    ECHO_right = 27

    print("Distance Measurement in Progress")

    GPIO.setup(TRIG_right,GPIO.OUT)
    GPIO.setup(ECHO_right,GPIO.IN)

    GPIO.output(TRIG_right, False)
    print("Waiting for Sensor To Settle")
    time.sleep(2)

    GPIO.output(TRIG_right, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_right,False)

    while GPIO.input (ECHO_right) == 0:
        pulse_start = time.time()

    while GPIO.input (ECHO_right) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration *17150

    distance = round(distance, 2)

    print ("Right Distance:", distance, "cm")
    GPIO.cleanup()
    time.sleep(1)
 
## if any distance larger than (400 cm) round down to 400 cm 

##write code for motors - take key input instead of ultrasonic sensor input
# a - move left
# d - move right
