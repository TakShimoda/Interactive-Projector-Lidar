import serial, re, logging, time, concurrent.futures, queue, threading, numpy, sys
import pyautogui as m
import tkinter as tk
from math import *
from Test_GUI import *

logging.basicConfig(level = logging.DEBUG, format = '%(message)s', filename = 'timer', filemode = 'w')
ser = serial.Serial('COM8', baudrate = 115200,  timeout = 1)
regex1 = re.compile('fa', re.I)
regex2 = re.compile('^fa', re.I)
regex3 = re.compile(r'''fa((A[0-9A-F])|(B[0-5]))0000
                        (([0-9A-F]{2})|.){16}''', re.I | re.VERBOSE)
# Globals
xbound, ybound = 1000, 750                              #Screen size
global_time = time.time()                               #Initialize epoch clock
width, height = m.size()                                #Computer screen in pixels
[x_previous, y_previous] = m.position()                 #Initialize mouse position
window = tk.Tk()
my_gui = My_Window(window)

#logging.disable(logging.CRITICAL)
logging.debug('x cord\ty cord\tintensity\t time\t\tMouse command')         #Logger header
print('\033[95m' + 'x cord\ty cord\tintensity\ttime' + '\033[0m')

def new_data(data):
    data = data*2
    mo = regex3.search(data)
    if not mo is None:
        return bytes.fromhex(mo.group())
    else:
        return None

def convert_data(data):
    distance, angle, intensity = [], [], []
    for i in range(4):
        dist1 = data[4*i+4]                         #BYTE0 of all 4 data points is index 4, 8, 12, 16
        dist2 = data[4*i+5]                         #BYTE1 of all 4 data points is index 5, 9, 13, 17
        it1 = data[4*i+6]                           #BYTE2 of all 4 data points i index 6, 10, 14, 18
        it2 = data[4*i+7]                           #BYTE3 of all 4 data points i index 7, 11, 15, 19
        dist2 = dist2 & (~0b11000000)               #Clear flag0 and flag1 bit from BYTE1
        distance.append((dist2<<8) | dist1)         #Shift 8 bits left to add LSB to BYTE1 bits 0-6, and place BYTE0 to the right of it
        intensity.append((it2<<8) | it1)            #Intensity is 8 bits from BYTE3 MSB and 8 bits from BYTE2 LSB
        angle.append(int(((data[1]-160)/29)*118)+i) #Conversion from 160-189 to 0-118  
    return angle, distance, intensity

def sph2cart(ang, r, intensity):
    x = r*cos(radians(ang)) 
    y = r*sin(radians(ang))
    return x, y, intensity

def producer(queue, event):
    t = time.time()
    angle, distance, intensity = [], [], []
    run = True
    while run:
        raw_string = ser.read(22).hex()
        m1 = regex1.search(raw_string)
        m2 = regex2.search(raw_string)
        if not m2 is None:
            data = raw_string
        elif not m1 is None:
            data = new_data(raw_string)
        else: 
            continue
        if data is None:
            continue
        a, d, i = convert_data(data)
        if i[3] >= 62976:
            i[3] -= 62976
        angle.extend(a)
        distance.extend(d)
        intensity.extend(i)
        if a[3] > 85:
            message = zip(angle, distance, intensity) #iterator
            queue.put_nowait(message)
            angle, distance, intensity = [], [], []
            run = False

def consumer(queue, prev_queue, event): 
    valid_points = []
    while not queue.empty():
        data = queue.get()
        for i in data:
            x, y, intensity = sph2cart(*i)
            if x<xbound and y<ybound and 10<intensity<100:
                valid_points.append((x, y, intensity))
        if valid_points == []:
            return
        intensity = [i[2] for i in valid_points]
        i = intensity.index(max(intensity))
        x, y  = int(valid_points[0][i]*width/xbound), int(valid_points[1][i]*height/ybound)         #Convert to pixels
        x_prev, y_prev, intensity_prev, time_prev = prev_queue.get()
        prev_queue.put_nowait((x, y, max(intensity), time.time()))
        mouse((x, y, max(intensity), time.time()),(x_prev, y_prev, intensity_prev, time_prev))
        my_gui.label_change(x, y)

def mouse_wrapper(mouse_func):
    def wrapper_function(*args, **kwargs):
        command = mouse_func(*args, **kwargs)
        current_time = time.time() - global_time
        logging.debug('%-4d\t%-4d\t%-4.2f\t\t %-5.2f\t\t%-s' %(args[0][0],args[0][1], args[0][2], current_time, command))
    return wrapper_function

@mouse_wrapper
def mouse(current_data, previous_data):
    diff = tuple(map(lambda x, y: x - y, current_data, previous_data))
    time_dif = diff[3]
    normdist = numpy.linalg.norm([diff[0], diff[1]])
    print('%-4d\t   %-4d\t    %-4.2f\t    %-5.2f' %(current_data[0],current_data[1], current_data[2], current_data[3] - global_time))
    #m.click(current_data[0], current_data[1])
    if (time_dif) < 0.2 and normdist < 50:
        return('drag')
    else:
        return('tap')

def create_buttons(frame, gridsize):
    for i in range(gridsize):
        frame.rowconfigure(i, weight = 0)
        frame.columnconfigure(i, weight = 0)
        for j in range(gridsize):
            btn = Grid_Buttons(frame, gridsize)

#--------------------MAIN FUNCTION----------------------------------------
if __name__ == '__main__':
    #Choose how many buttons to create
    create_buttons(my_gui.bottom_frame, 5)
    event = threading.Event()
    pipeline = queue.Queue()                                                        #Initialize the queue, size as large as computer memory             
    prev_queue = queue.Queue()                                                      #Previous state queue
    prev_queue.put((x_previous, y_previous, 0, global_time))
    while 1:
        window.update_idletasks()
        #window.update()
        #my_gui.current_value.insert(0, 'ello')                                                       
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:      #Create three threads, join all afterwards
            executor.submit(producer, pipeline, event)                              #Create producer, pass the queue object
            executor.submit(consumer, pipeline, prev_queue, event)                  #Create consumer, pass the queue object
            window.update()
