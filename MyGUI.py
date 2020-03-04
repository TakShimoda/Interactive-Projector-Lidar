#GUI class
#Run as admin(i.e. from command prompt) if you want to press keys on the on-screen keyboard

from tkinter import *
import pyautogui as m
import time

class My_GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("Apex Solutions")
        px = 1  #Pad x
        py = 1  #Pad y
        #self.columnconfigure(0, weight=1, minsize=150) # each grid cell is 150 pixels wide and 100 pixals tall
        #self.rowconfigure([0,1], weight=1, minsize =100)
        self.frame_a = Frame(master=self)
        self.frame_b = Frame(master=self)
        self.frame_c = Frame(master=self)
        self.frame_d = Frame(master=self)
        self.frame_e = Frame(master=self)
        self.frame_f = Frame(master=self)
        self.frame_g = Frame(master=self)
        self.frame_h = Frame(master=self)
        self.frame_i = Frame(master=self)
        self.frame_a.grid(row=0, column=0, padx = 5, pady=5)
        self.frame_b.grid(row=0, column=1, padx = 5, pady=5)
        self.frame_c.grid(row=0, column=2, padx = 5, pady=5)
        self.frame_d.grid(row=1, column=0, padx = 5, pady=5)
        self.frame_e.grid(row=1, column=1, padx = 5, pady=5)
        self.frame_f.grid(row=1, column=2, padx = 5, pady=5)
        self.frame_g.grid(row=2, column=0, padx = 5, pady=5)
        self.frame_h.grid(row=2, column=1, padx = 5, pady=5)
        self.frame_i.grid(row=2, column=2, padx = 5, pady=5)

        self.PreviousButton = Button(master = self.frame_d, text="Previous\n Slide", command=self.PrevSlide, height = 3, width = 8, relief = RAISED, borderwidth = 5)
        self.PreviousButton.pack(padx = px, pady = py)

        self.NextButton = Button(master = self.frame_f, text="Next Slide", command=self.NextSlide, height = 3, width = 8, relief = RAISED, borderwidth = 5)
        self.NextButton.pack(padx = px, pady = py)

        self.ExitButton = Button(master = self.frame_e, text="Exit", command=self.ClickToExit, height = 3, width = 8, relief = RAISED, borderwidth = 5)
        self.ExitButton.pack(padx = px, pady = py)

        self.Up = Button(master = self.frame_b, text="Up", command=self.Up, height = 3, width = 8, relief = RAISED, borderwidth = 5)
        self.Up.pack(padx = px, pady = py)

        self.Down = Button(master = self.frame_h, text="Down", command=self.Down, height = 3, width = 8, relief = RAISED, borderwidth = 5)
        self.Down.pack(padx = px, pady = py)

        self.KeyButton = Button(master = self.frame_a, text="Keyboard", command=self.KeyBoard, height = 3, width = 8, relief = RAISED, borderwidth = 5)
        self.KeyButton.pack(padx = px, pady = py)

        self.screen_width = self.winfo_screenwidth()       #finds the width of your computer's resolution
        self.screen_height = self.winfo_screenheight()     #finds the height of your computer's resolution
        # calculate position x and y coordinates
        self.x = (self.screen_width/25) #the 15 and 2 are just values that made it so it was on the bottom left of my screen
        self.y = (self.screen_height/1.8) #tried to make it so it would be on the bottom left for most/every screen resolution
        self.geometry('500x600+%d+%d' % (self.x, self.y)) # .geometry('width_of_window x height_of_window + X coordinate + Y coordinate' of the window)
        self.attributes('-topmost', 'true') #makes it so it always stays on top of all windows
    
    def PrevSlide(self):
        m.hotkey('up')

    def NextSlide(self): 
        m.hotkey('down')

    def KeyBoard(self):
        m.hotkey('win','ctrl','o')
    
    def Down(self):
        m.hotkey('down')
    
    def Up(self):
        m.hotkey('up')

    def ClickToExit(self): #random function so far, when a button with this command is pressed, exits the program
        exit()

#Rough prototype
class My_GUI2:
    def __init__(self, window):
        window.title("Apex Solutions")
        window.columnconfigure(0, weight=1, minsize=150) # each grid cell is 150 pixels wide and 100 pixals tall
        window.rowconfigure([0,1], weight=1, minsize =100)
        window.frame_a = Frame(master=window)
        window.frame_b = Frame(master=window)
        window.frame_c = Frame(master=window)
        window.frame_a.grid(row=0, column=0, padx = 5, pady=20)
        window.frame_b.grid(row=1, column=0, padx = 5, pady=20)
        window.frame_c.grid(row=2, column=0, padx = 5, pady=20)

        self.PreviousButton = Button(master = window.frame_a, text="Previous Slide", command=self.PrevSlide, height = 5, width = 10, relief = RAISED, borderwidth = 5)
        self.PreviousButton.pack(padx = 10, pady=10)

        self.NextButton = Button(master = window.frame_b, text="Next Slide", command=self.NextSlide, height = 5, width = 10, relief = RAISED, borderwidth = 5)
        self.NextButton.pack(padx = 10, pady=10)

        self.KeyBrd = Button(master = window.frame_b, text="KeyBoard", command=self.KeyBoard, height = 5, width = 10, relief = RAISED, borderwidth = 5)
        self.KeyBrd.pack(padx = 10, pady=10)


        self.screen_width = window.winfo_screenwidth()       #finds the width of your computer's resolution
        self.screen_height = window.winfo_screenheight()     #finds the height of your computer's resolution
        # calculate position x and y coordinates
        self.x = (self.screen_width/15) #the 15 and 2 are just values that made it so it was on the bottom left of my screen
        self.y = (self.screen_height/3) #tried to make it so it would be on the bottom left for most/every screen resolution
        window.geometry('300x800+%d+%d' % (self.x, self.y)) # .geometry('width_of_window x height_of_window + X coordinate + Y coordinate' of the window)
        window.attributes('-topmost', 'true') #makes it so it always stays on top of all windows

    def PrevSlide(self):
        m.hotkey('up')

    def NextSlide(self): 
        m.hotkey('down')

    def KeyBoard(self):
        m.hotkey('win','ctrl','o')

if __name__ == '__main__':
    gui = My_GUI()
    gui.mainloop()
    # window = Tk()
    # gui = My_GUI2(window)
    # window.mainloop()