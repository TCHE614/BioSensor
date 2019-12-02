import serial
import sqlite3
import time
import sys, select, os
import serial.tools.list_ports
#Future additions that can be added: encryption so that user data eg bpm is encrypted
#set up security so a password and username set up to ensure only the doctor can access the information

# s=b'0000'
sample =0
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

while 1:
    #set up serial connection with Arduino
    # print("test1")
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
    # elif sample> 10 and NoDatatimer >30:
    #     print("Data is now being captured")
    #     previousValue = IntBPM
    #     sampleFlag = False

    #Using epoch time 12:00am, January 1, 1970 as reference 
    currenttime = time.time() #number of seconds since the reference point

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

                
    #print("Sample = %d", sample)
    try:
        print(int(BPMDecoded))
    except: 
        pass
    


