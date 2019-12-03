import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from dateutil import parser
from matplotlib import style
import sqlite3
import time
import datetime
import random
#STYLES
style.use('fivethirtyeight')
plt.rcParams.update({'font.size': 10})


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
name = "Ting-Kai Chen"
def animate(i):
    #OPEN DATABASE
    conn = sqlite3.connect('BPMDatabase.db')
    c = conn.cursor()
    c.execute('SELECT Time, BPMValue FROM BPM WHERE Patient = ?',(name,))
    data = c.fetchall()
    dates = []
    values = []

    for row in data:
        ts = datetime.datetime.fromtimestamp(int(row[0])).strftime('%M:%S')
        dates.append(str(ts))
        values.append(row[1])

    ax1.clear()
    ax1.plot(dates,values)
    conn.close()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()