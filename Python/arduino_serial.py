import serial
import sqlite3
import time
#Future additions that can be added: encryption so that user data eg bpm is encrypted
#set up securoty so a password and username set up to ensure only the docot can access these information

sample =0
sampleFlag = True
# ASk for nmae of that data that is getting entered
PatientsName = input("Please enter in your name: ")
print("Hi", PatientsName)

while 1:
    #set up serial connection with Arduino
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=None, parity=serial.PARITY_NONE, rtscts=1)
    s = ser.read_until()
    BPMDigit = s[:-1]     #Remove \n from serial input
  
    BPMDecoded = BPMDigit.decode("utf-8") #decode byte into string then int 
    IntBPM = int(BPMDecoded)

    #Only after 20 inputs then we will start capturing data ensuring steady state
    sample += 1
    if sample >10 and sampleFlag == True:
        print("Data is now being captured")
        sampleFlag = False

    #Using epoch time 12:00am, January 1, 1970 as reference 
    currenttime = time.time() #number of seconds since the reference point


    #ensure that only valid data is written into the database
    if IntBPM != -1 and sampleFlag == False:
        #Open database 
        conn = sqlite3.connect("BPMDatabase.db")
        c = conn.cursor()
        c.execute("""INSERT INTO BPM 
                (Patient ,BPMValue, Time) 
                values 
                (?,?,?)""",(PatientsName,IntBPM,currenttime,))
        conn.commit()
        conn.close()
    #print("Sample = %d", sample)
    print(int(BPMDecoded))
    