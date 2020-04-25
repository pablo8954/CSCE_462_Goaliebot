#Libraries
# import RPi.GPIO as GPIO
# from gpiozero import LED

# from adafruit_motorkit import MotorKit 
import time
import tkinter as tk

# kit = MotorKit()

#GPIO mode
left_trig = 27
left_echo = 22

right_trig = 21
right_echo = 20

button = 24

# red_left = LED(12)
# red_center = LED(16)
# green = LED(5)

trig_chan = [left_trig, right_trig]
echo_chan = [left_echo, right_echo]

run = [False]
throttle_speed_mult = 0

def single_player():
    print("Run Solo Game")

def remote_control():
    print("Multiplayer")
    
    while run[0]:#change to true
        right_command = False
        left_command = False
        
        
        #take user input here to change right/left command
        user_input()


        #kit.motor1.throttle = throttle_speed_mult#negative throttle speed is right
        #kit.motor2.throttle = throttle_speed_mult
        if (throttle_speed_mult > 0):
            print("moving left")
        elif (throttle_speed_mult < 0):
            print("moving left")
        else:
            print("not moving")

def user_input():
        variable = ""
        if variable == "d" and throttle_speed_mult != -1:
            throttle_speed_mult -= 1
        elif variable == "a" and throttle_speed_mult != 1:
            throttle_speed_mult += 1
            
class Application(tk.Frame):

    direction = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
    
    #initialize window widgets
    def create_widgets(self):
        # self.winfo_toplevel.title("Goalie Bot")

        self.single_player = tk.Button(self, borderwidth = "5");
        self.single_player["text"] = "Single Player"
        self.single_player["command"] = self.passSingle
        self.single_player.grid(row = 1, column = 1, ipadx = "25", ipady = "15", pady = "50")

        self.multiplayer = tk.Button(self, borderwidth = "5")
        self.multiplayer["text"] = "Multiplayer"
        self.multiplayer["command"] = self.pass_remote
        self.multiplayer.grid(row = 1, column = 3, ipadx = "25", ipady = "15", pady = "50")

        self.quit = tk.Button(self, borderwidth = "5", text="QUIT", fg="red",command=self.master.destroy)
        self.quit.grid(row = 3, column = 2, ipadx = "25", ipady = "15")

  
    def passSingle(self):
        single_player()
    
    def pass_remote(self):
        self.direction = "d or a or something"
        remote_control(self.direction)
    


root = tk.Tk()
root.title("GoalieBot")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='img/ball.png'))

#sets window size on screen
root.geometry("400x300")
root.grid_rowconfigure(2, )
root.grid_columnconfigure(2, minsize=400)

app = Application(master=root)
app.mainloop()