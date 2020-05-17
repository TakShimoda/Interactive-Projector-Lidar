# Test GUI
import tkinter as tk

class My_Window:
    def __init__(self, window):
        self.window = window
        self.window.title('Apex Solution')
        self.window.rowconfigure(0, weight = 0)
        self.window.rowconfigure(1, weight = 1)
        self.window.columnconfigure(0, weight = 1)

        self.x = self.window.winfo_screenwidth()
        self.y = self.window.winfo_screenheight()

        self.window.geometry(f'{int(self.x/4)}x{int(self.y/3)}+{int(self.x/5)}+{int(self.y/5)}')

        self.top_frame = tk.Frame(master = self.window, relief = tk.SUNKEN, height = self.y/12)
        self.bottom_frame = tk.Frame(master = self.window, height = self.y/12)
        self.top_frame.grid(row = 0, column = 0)
        self.bottom_frame.grid(row = 1, column = 0)

        self.top_frame.rowconfigure(0, weight = 1)
        self.top_frame.rowconfigure(1, weight = 1)
        self.top_frame.columnconfigure(0, weight = 1)
        self.top_frame.columnconfigure(1, weight = 1)

        self.current_label = tk.Label(master = self.top_frame, bg = "white", text = "Current Coordinates: ")
        self.previous_label = tk.Label(master = self.top_frame, bg = "white", text = "Previous Coordinates: ")
        self.current_label.grid(row = 0, column = 0, sticky = "nsew")
        self.previous_label.grid(row = 1, column = 0, sticky = "nsew")
        self.current_value = tk.Entry(master = self.top_frame)
        self.previous_value = tk.Entry(master = self.top_frame)
        self.current_value.grid(row = 0, column = 1, sticky = "nsew")
        self.previous_value.grid(row = 1, column = 1, sticky = "nsew")

class Grid_Buttons:
    # Initialize grid
    row = 0
    column = 0
    def __init__(self, bottom_frame, gridnum):
        self.button = tk.Button(master = bottom_frame, command = self.change_color,
                                height = int(10/gridnum), width = int(28/gridnum**0.80),
                                bg = 'white')
        self.button.grid(row = Grid_Buttons.row, column = Grid_Buttons.column)
        self.colorstate = 0

        if Grid_Buttons.row == gridnum-1:
            if Grid_Buttons.column < gridnum:
                Grid_Buttons.column += 1
            else:
                pass
                #Exceeded grid limits
        else:
            if Grid_Buttons.column < gridnum-1:
                Grid_Buttons.column += 1
            else:
                Grid_Buttons.row += 1
                Grid_Buttons.column = 0

    def change_color(self):
        if self.colorstate % 2 == 0:
            self.button.configure(bg = "red")
        else:
            self.button.configure(bg = "white")
        self.colorstate += 1

def create_buttons(frame, gridsize):
    for i in range(gridsize):
        frame.rowconfigure(i, weight = 0)
        frame.columnconfigure(i, weight = 0)
        for j in range(gridsize):
            btn = Grid_Buttons(frame, gridsize)

if __name__ == '__main__':
    window = tk.Tk()
    my_gui = My_Window(window)
    create_buttons(my_gui.bottom_frame, 5)
    window.mainloop()

