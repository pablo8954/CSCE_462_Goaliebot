#Libraries
import RPi.GPIO as GPIO
from gpiozero import LED

from adafruit_motorkit import MotorKit 
import time
import tkinter as tk
import RPi.GPIO as GPIO
from gpiozero import LED

from adafruit_motorkit import MotorKit 
import time



def single_player():
    print("Run Solo Game")

def remote_control():
    print("Multiplayer")

class Application(tk.Frame):
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
        remote_control()


root = tk.Tk()
root.title("GoalieBot")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='img/ball.png'))

#sets window size on screen
root.geometry("400x300")
root.grid_rowconfigure(2, )
root.grid_columnconfigure(2, minsize=400)

app = Application(master=root)
app.mainloop()