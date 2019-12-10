import serial
import sqlite3
import time
import datetime
import random
import sys, select, os
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from dateutil import parser
from matplotlib import style
from matplotlib import gridspec
myfont_size = 10
#STYLES
style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10})

#Future additions that can be added: encryption so that user data eg bpm is encrypted
#set up security so a password and username set up to ensure only the doctor can access the information

# set up plot graph 
fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(10, 10)

# gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1]) 
# fig, (ax1, ax2) = plt.subplots(2)
ax1 = fig.add_subplot(gs[6:, :])
ax2 = fig.add_subplot(gs[3, :])
ax3 = fig.add_subplot(gs[4, :])
ax4 = fig.add_subplot(gs[5, :])
ax5 = fig.add_subplot(gs[0, :])
ax6 = fig.add_subplot(gs[1, :])
ax7 = fig.add_subplot(gs[2, :])
fig.suptitle('Spider movement and heart rate tracker')
# s=b'0000'

sample = 0
sampleFlag = True
CreateDatabaseFlag = False
previousValue = 60 #average value not used
NoDatatimer =0 # if no data has been detected re sample the data. 

# Ask for name of that data that is getting entered
while True:
    PatientsName = input("Please enter in your name: ")
    #wait for a valid name to be given
    if not PatientsName:
        print("The answer given does not compute!! Try again")
        continue
    else:
        break
print("Hi", PatientsName)

#Finding the Arudino port and seeting that as the serial port
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if 'Arduino Uno' in p.description:
        port = p.device
        print('Using ' + p.device + " as the serial")
    if 'USB Serial Device' in p.description:
        port = p.device
        print('Using ' + p.device + " as the serial")

#open either the linux port or windows port
try:
    #linux
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5, parity=serial.PARITY_NONE, rtscts=1) 
except:
    try:
        #windows
        ser = serial.Serial(port, 9600, timeout=5, parity=serial.PARITY_NONE, rtscts=1)
    except:
        #no ports
        print("No Ports Found ")
        exit



def animate(i):
    global sample
    global sampleFlag
    global CreateDatabaseFlag
    global previousValue
    global NoDatatimer
    global PatientsName
    global port
    global ser

    #Using epoch time 12:00am, January 1, 1970 as reference 
    currenttime = time.time() #number of seconds since the reference point
    secondtime = currenttime -60.0
    #OPEN DATABASE
    conn = sqlite3.connect('BPMDatabase.db')
    c = conn.cursor()
    c.execute('SELECT Time, BPMValue FROM BPM WHERE Patient = ? AND Time > ?',(PatientsName,secondtime,))
    data = c.fetchall()
    conn.close()
    dates = []
    values = []

    for row in data:
        ts = datetime.datetime.fromtimestamp(int(row[0])).strftime('%S')
        dates.append(str(ts))
        values.append(row[1])

    ax1.clear()
    ax1.plot(dates,values)
    
    #Spider 1 movement onto graph
    spiderid1 = "PC_Spider(1)"
    #connect to the spider database
    conn = sqlite3.connect("code\\Assets\\Plugins\\UnityDatabase.db", uri=True)
    c = conn.cursor()
    c.execute('SELECT time, changeDirection FROM Spider_Table WHERE id = ? AND time > ?',(spiderid1,secondtime,))
    SpiderList = c.fetchall()
    conn.close()
    timelists = []
    changes = []
    spiderListcounter =0
    for row in SpiderList:
        ts = datetime.datetime.fromtimestamp(int(row[0])).strftime('%S')
        timelists.append(str(ts))
        changes.append(row[1])
        spiderListcounter += 1

    ax2.clear()
    ax2.set_ylabel(spiderid1, fontsize=myfont_size)
    ax2.plot(timelists,changes)

    #Spider 2 movement onto graph
    spiderid2 = "PC_Spider(2)"
    #connect to the spider database
    conn = sqlite3.connect("code\\Assets\\Plugins\\UnityDatabase.db", uri=True)
    c = conn.cursor()
    c.execute('SELECT time, changeDirection FROM Spider_Table WHERE id = ? AND time > ?',(spiderid2,secondtime,))
    SpiderList = c.fetchall()
    conn.close()
    timelists = []
    changes = []
    spiderListcounter =0
    for row in SpiderList:
        ts = datetime.datetime.fromtimestamp(int(row[0])).strftime('%S')
        timelists.append(str(ts))
        changes.append(row[1])
        spiderListcounter += 1

    ax3.clear()
    ax3.set_ylabel(spiderid2, fontsize=myfont_size)
    ax3.plot(timelists,changes)

    #Spider 5 movement onto graph
    spiderid5 = "PC_Spider(5)"
    #connect to the spider database
    conn = sqlite3.connect("code\\Assets\\Plugins\\UnityDatabase.db", uri=True)
    c = conn.cursor()
    c.execute('SELECT time, changeDirection FROM Spider_Table WHERE id = ? AND time > ?',(spiderid5,secondtime,))
    SpiderList = c.fetchall()
    conn.close()
    timelists = []
    changes = []
    spiderListcounter =0
    for row in SpiderList:
        ts = datetime.datetime.fromtimestamp(int(row[0])).strftime('%S')
        timelists.append(str(ts))
        changes.append(row[1])
        spiderListcounter += 1
    ax4.clear()
    ax4.set_ylabel(spiderid5, fontsize=myfont_size)
    ax4.plot(timelists,changes)


    #x,y and z plot
    #Spider 5 movement onto graph
    spiderid5 = "PC_Spider(5)"
    #connect to the spider database
    conn = sqlite3.connect("code\\Assets\\Plugins\\UnityDatabase.db", uri=True)
    c = conn.cursor()
    c.execute('SELECT time,x,y,z FROM HMD_Table WHERE time > ?',(secondtime,))
    SpiderList = c.fetchall()
    conn.close()
    timelists = []
    x = []
    y = []
    z = []
    for row in SpiderList:
        ts = datetime.datetime.fromtimestamp(int(row[0])).strftime('%S')
        timelists.append(str(ts))
        x.append(row[1])
        y.append(row[2])
        z.append(row[3])
    ax5.clear()
    ax5.set_ylabel("HMD x", fontsize=myfont_size)
    ax5.plot(timelists,x)
    ax6.clear()
    ax6.set_ylabel("HMD y", fontsize=myfont_size)
    ax6.plot(timelists,y)
    ax7.clear()
    ax7.set_ylabel("HMD z", fontsize=myfont_size)
    ax7.plot(timelists,z)



    #set up serial connection with Arduino
    #reading the serial inputs
    s = ser.read_until()
    BPMDigit = s[:-1]     #Remove \n from serial input
  
    BPMDecoded = BPMDigit.decode("utf-8") #decode byte into string then int 
    try:
        IntBPM = int(BPMDecoded)
    except ValueError:
        # no input for 5 seconds so need to re sample the data and ignore the first few data points
        sampleFlag = True
        sample = 0
        IntBPM = -1
        print("Timeout occured")
        
    #Only after 20 inputs then we will start capturing data ensuring steady state
    sample += 1
    if sample >10 and sampleFlag == True:
        print("Data is now being captured")
        previousValue = IntBPM
        sampleFlag = False

    
    #make sure that only valid data is put into the database so random spikes should be ignored

    #ensure that only valid data is written into the database
    if IntBPM != -1 and sampleFlag == False :
        #Open database 
        #try catch statements as different sources require different paths
        #running on VS Code
        
        try:
            conn = sqlite3.connect("Python/BPMDatabase.db")
            #print("one")
            c = conn.cursor()
            c.execute("""INSERT INTO BPM 
                    (Patient ,BPMValue, Time) 
                    values 
                    (?,?,?)""",(PatientsName,IntBPM,currenttime,))
            conn.commit()
            conn.close()
        except:
            #running from termial
            try :
                conn = sqlite3.connect("BPMDatabase.db")
                #print("two")
                c = conn.cursor()
                c.execute("""INSERT INTO BPM 
                        (Patient ,BPMValue, Time) 
                        values 
                        (?,?,?)""",(PatientsName,IntBPM,currenttime,))
                conn.commit()
                conn.close()
            except:
                pass
                #Creating database since not there
                print("Creating database")
                conn = sqlite3.connect("BPMDatabase.db")
                c = conn.cursor()
                if CreateDatabaseFlag == False:
                    #first instances create the table and database
                    c.execute("""CREATE TABLE "BPM" ("Patient"	TEXT, "BPMValue" INTEGER,"Time"	BLOB)""")
                    CreateDatabaseFlag = True
                conn.commit()
                conn.close()

    try:
        print(int(BPMDecoded))
    except: 
        pass


print("Please place index or middle finger on the tracker.")

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()