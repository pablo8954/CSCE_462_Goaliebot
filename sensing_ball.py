#Libraries
import RPi.GPIO as GPIO
from gpiozero import LED

from adafruit_motorkit import MotorKit 
import time
import tkinter as tk

kit = MotorKit()

#GPIO mode
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
isSinglePlayer = False

"""
right - broken, negative direction
left - good, positive direction

"""

def readings(index):
    GPIO.output(trig_chan[index], False) #let sensors settle
    GPIO.output(trig_chan[index], True)  
    time.sleep(0.01)
    GPIO.output(trig_chan[index], False) 

    pulse_start = 0
    pulse_end = 0
    while_loop_flag = 0

    while GPIO.input(echo_chan[index]) == 0:
        pulse_start = time.time()
        while_loop_flag = while_loop_flag + 1
        
    while GPIO.input(echo_chan[index]) == 1:
        pulse_end = time.time()
        while_loop_flag = while_loop_flag + 1

    if while_loop_flag > 1:
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 171250
        distance = round(distance, 2)/10

    else:   
        distance = -1

    return distance

#pauses single player (either turn on or off)
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


class Application(tk.Frame):
    direction = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.master.bind("a", lambda event: self.remote_control(event, left = False))
        self.master.bind("d", lambda event: self.remote_control(event, left = True))
    
    #initialize window widgets
    def create_widgets(self):
        # self.winfo_toplevel.title("Goalie Bot")

        self.single_player = tk.Button(self, borderwidth = "5");
        self.single_player["text"] = "Single Player"
        self.single_player["command"] = self.passSingle
        self.single_player.grid(row = 1, column = 1, ipadx = "25", ipady = "15", pady = "50")

        self.multiplayer = tk.Button(self, borderwidth = "5")
        self.multiplayer["text"] = "Multiplayer"
        self.multiplayer["command"] = self.setRemote
        self.multiplayer.grid(row = 1, column = 3, ipadx = "25", ipady = "15", pady = "50")

        self.quit = tk.Button(self, borderwidth = "5", text="QUIT", fg="red",command=self.close_program)
        self.quit.grid(row = 3, column = 2, ipadx = "25", ipady = "15")


    def single_playerFun(self):
        global isSinglePlayer

        if isSinglePlayer and run[0]:
            throttle_speed = 1.0

            left_val = readings(0)
            right_val = readings(1)

            print("Left: ", left_val)
            print("Right: ", right_val)

            left_sees_ball = False
            right_sees_ball = False

            if (right_val > 1750):
                right_sees_ball = True
            if (left_val > 1750):
                left_sees_ball = True

            if (left_val < 150):
                left_sees_ball = True
            if (right_val < 150):
                right_sees_ball = True

            #bad reading from ultrasonic sensors - try again & skip to end
            if (right_val > 0 or left_val > 0):
                #case 1 - when the ball is in the center - either both sensors read the ball or read nothing in front
                if (right_sees_ball and left_sees_ball) or (not right_sees_ball and not left_sees_ball):
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

        #button interrupt
        elif run[0] == False:
            kit.motor1.throttle = 0
            kit.motor2.throttle = 0

        self.master.after(100, self.single_playerFun)
  
    def passSingle(self):
        global isSinglePlayer
        if (isSinglePlayer == False):
            isSinglePlayer = True
            self.master.after(100, self.single_playerFun)
    
    def setRemote(self):
        global isSinglePlayer
        print("Set Multiplayer")
        isSinglePlayer = False

    def remote_control(self, event, left):
        global isSinglePlayer
        if isSinglePlayer == False:
            #determine motor direction
            if left and self.direction != 1: 
                self.direction = self.direction + 1
            elif (not left) and self.direction != -1: 
                self.direction = self.direction - 1

            #set motor movements
            print("Direction", self.direction)
            kit.motor1.throttle = self.direction
            kit.motor2.throttle = self.direction

    #quit
    def close_program(self):
        #turn off motors
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0

        # #turn off all LEDs
        green.off()
        red_center.off()
        red_left.off()

        #close gui
        self.master.destroy()



GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_chan, GPIO.OUT)
GPIO.setup(echo_chan, GPIO.IN)

# #button callback to turn robot on & off + GPIO setup
GPIO.setup(button, GPIO.IN)
GPIO.add_event_detect(button, GPIO.RISING)
GPIO.add_event_callback(button, callButtonEventHandler)
kit.motor1.throttle = 0
kit.motor2.throttle = 0

root = tk.Tk()
root.title("GoalieBot")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='img/ball.png'))

#sets window size on screen
root.geometry("400x300")
# root.grid_rowconfigure(2, minsize=400)
root.grid_columnconfigure(2, minsize=400)

app = Application(master=root)
app.mainloop()