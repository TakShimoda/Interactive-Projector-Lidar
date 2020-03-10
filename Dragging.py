import serial, time, numpy, concurrent.futures, queue, threading
import pyautogui as m
from math import *
from tkinter import *
from MyGUI import *

#Initialize, define global variables
ser = serial.Serial('COM8', baudrate = 115200,  timeout = 1)
time.sleep(2)
Ang = numpy.zeros(88)
Dist = numpy.zeros(88)
Ity = numpy.zeros(88)
f = open('Data.csv', 'w')
print(m.size())

#-----------------Define Functions
def RearrangeData(data):
    if (250 in data):                                                               #If 250=0xFA start byte exists                       
        ind = [i for i, x in enumerate(data) if x == 250]
        for i in ind:
            if i == 19:                                                             #If found in index 19
                if ((data[20] > 159) & (data[21] == 0) & (data[0] == 0)):           #Check if next bye is angle, and 2 bytes after are zero
                    y = numpy.roll(data,-19)
                    return y
            elif i == 20:                                                           #If found in index 20
                if ((data[21] > 159) & (data[0] == 0) & (data[1] == 0)):
                    y = numpy.roll(data,-20)
                    return y
            elif i == 21:                                                           #If found in index 21
                if ((data[0] > 159) & (data[1] == 0) & (data[2] == 0)):
                    y = numpy.roll(data,-21)
                    return y
            elif ((data[i+1] > 159) & (data[i+2] == 0) & (data[i+3] == 0)):         #All other cases
                y = numpy.roll(data,-i)
                return y
            else:                                                                   #All other, return nothing
                pass
    else:
        y = numpy.roll(data,1)                                                      #If start byte not 250, it will be the last index                      
        return y

def DecimaltoBinary(data):
    dist = numpy.array([0,0,0,0])                   #Initiate array of 4                                 
    ang = numpy.array([0,0,0,0])                    #Conversion from 160-189 to 0-118
    it = [None]*4 
    for i in range(0, 4):                       
        dist1 = data[4*i+4]                         #BYTE0 of all 4 data points is index 4, 8, 12, 16
        dist2 = data[4*i+5]                         #BYTE1 of all 4 data points is index 5, 9, 13, 17
        it1 = data[4*i+6]                           #BYTE2 of all 4 data points i index 6, 10, 14, 18
        it2 = data[4*i+7]                           #BYTE3 of all 4 data points i index 7, 11, 15, 19
        dist2 = dist2 & (~0b11000000)               #Clear flag0 and flag1 bit from BYTE1
        dist[i] = (dist2<<8) | dist1                #Shift 8 bits left to add LSB to BYTE1 bits 0-6, and place BYTE0 to the right of it
        it[i] = (it2<<8) | it1                      #Intensity is 8 bits from BYTE3 MSB and 8 bits from BYTE2 LSB
        ang[i] = int(((data[1]-160)/29)*118)+i      #Conversion from 160-189 to 0-118  
    return ang, dist, it

def Sph2Cart(ang, r):                               #Convert spherical to cartesian coordinates
    offset = 0#4*pi/180
    x = r*cos(radians(ang)-offset) 
    y = r*sin(radians(ang)-offset)
    return x, y

def consumer(queue, timqequeue, cqueue, event):
    width, height = m.size()              
    while not queue.empty() or not event.isset():                              #Continue while queue is not empty
        Data = queue.get()                                                      #Get the array from the queue
        x = []
        y = []
        Data1 = []
        Data2 = []
        Cart = list(map(Sph2Cart, [i[0] for i in Data], [i[1] for i in Data]))  #Convert all 88 data points from spherical to cartesian coordinate
        x = [i[0] for i in Cart]
        y = [i[1] for i in Cart]
        ity = [i[2] for i in Data]
        Data1 = list(zip(x, y, ity))                                            #New array: x, y, and intensities
        for i in range(0,88):                                                   #Check all 88 points
            if ((x[i]<1800) & (y[i]<950)&(ity[i]>3)):                           #If point within screen and intensity is greater than 15
                Data2 += [Data1[i]]                                             #Place inside a new array Data2  
            else:
                pass
        x = [i[0] for i in Data2]
        y = [i[1] for i in Data2]
        Intensity = [i[2] for i in Data2]
        if (len(Data2)==0):                                                     #If Data2 is empty, do nothing
            return
        else:
            t = timequeue.get()
            prev = cqueue.get()
            i = Intensity.index(max(Intensity))                                 #If Data2 not empty, pick the maximum intensity
            cur = [x[i], y[i]]                                                  #Current position
            normdist = numpy.linalg.norm([cur[1]-prev[1],cur[0]-prev[0]])       #The norm between previous/current position
            if ((time.time() - t) < 0.2) and (normdist < 20):                                         
                timequeue.put_nowait(time.time())
                cqueue.put_nowait([x[i], y[i]])  
                #m.dragRel((x[i]-prev[1])*(width/1800), ((prev[0]-y[i])*height/1050), tween = m.easeInCirc, duration = 0.05)
                #print(abs((x[i]-prev[1])*width/1800), abs(height-((prev[0]-y[i])*height/1050)))
                print(x[i]*width/1800, (height - y[i]*height/1150))
                m.dragTo(x[i]*width/1800, (height - y[i]*height/1150), tween = m.easeInCirc, duration = 0.05)
            else:
                #m.moveTo(x[i]*width/1800, height-(y[i]*height/1150), duration = 0.001)
                timequeue.put_nowait(time.time())                                   #Stamp the time here
                cqueue.put_nowait([x[i],y[i]])           
                #print(x[i]*width/1800,y[i]*height/1000)
    event.clear()

def producer(queue, event):
    count = 0
    ser.reset_input_buffer()
    while (count <89):
        Data = list(ser.read(22))                       #Read 22 bytes: class 'bytes': not mutable; convert ASCII/HEX to decimal equivalent values
        if Data[0] != 250:                              #If data's first index is not start byte 0xFA or 250(in decimal)
            Data = RearrangeData(Data)                  #Rearrange Data so first byte is 0xFA(250)
        if (Data is None):                              #If RearrangeData function returns nothing, skip to next iteration of loop
            return
        if Data[1] > 181:                               #If angle is greater than 88, skip to next iteration of loop(garbage data)
            return
        (ang, d, intense) = DecimaltoBinary(Data)       #Plug Data to get angle, distance and intensity values, 4 each
        if intense[3] >= 62976:                         #Correct any unusual intensities detected at 3rd index of intensity
            intense[3] = intense[3] - 62976    
    #------Code to make 3 arrays of size 88, each with 22 packets of angles/distances/intensities

        Ang[count:count+4] = ang                        #Assign the 4 values from ang to the larger Ang array
        Dist[count:count+4] = d                         #Assign the 4 values from d to the larger Dist array
        Ity[count:count+4] = intense                    #Assign the 4 values from intense to the larger Ity array
        count += 4                                      #Increment the count by 4
        if count >= 88:
            #count = 0                                  #Reset count to 0
            if ((max(Ity) > 10) & (max(Ity) < 300)):    #If maximum intensity is greater than 30 and less than 500(object detected, valid intensity)
                Data = list(zip(Ang,Dist,Ity))          #[(Ang[0],Dist[0],Ity[0]),(Ang[1],Dist[1],Ity[1]), ..] -> an array of 88 tuples, each sized 3
                queue.put_nowait(Data)                  #Place the above array inside the queue
            else:                                               
                pass                                    #No intensities in this range? Pass
            event.set()
#--------------------MAIN FUNCTION----------------------------------------
if __name__ == '__main__':
    mygui = My_GUI()
    event = threading.Event()
    pipeline = queue.Queue()                                                        #Initialize the queue, size as large as computer memory
    timequeue = queue.Queue()
    cqueue = queue.Queue()
    timequeue.put(time.time())                                                      #Initialize first instance of time
    [xi, yi] = m.position()                                                         #Initial screen positions
    xi = (xi*500)/3840
    yi = (xi*375)/2160
    cqueue.put([xi, yi])
    while (ser.in_waiting>0):                                                       #While serial buffer is not empty
        # mygui.update_idletasks()
        # mygui.update()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:      #Create two threads, join both afterwards
            executor.submit(producer, pipeline, event)                              #Create producer, pass the queue object
            executor.submit(consumer, pipeline, timequeue, cqueue, event)           #Create consumer, pass the queue object