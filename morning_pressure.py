#!/usr/bin/env python

""" File used to generat the morning pressure graph for the Logging paper """

import MySQLdb
import numpy as np
from datetime import timedelta, datetime
import matplotlib.pyplot as plt

try:
    DB = MySQLdb.connect(host="servcinf", user="cinf_reader",
                         passwd="cinf_reader", db="cinfdata")
except MySQLdb.OperationalError:
    DB = MySQLdb.connect(host="127.0.0.1", port=9995,
                         user="cinf_reader", passwd="cinf_reader",
                         db="cinfdata")

CURSOR = DB.cursor()

FROM_DATE = '2012-03-08 00:30'
TO_DATE = '2012-04-21 2:00'
TABLE = 'pressure_microreactorNG'

CURSOR.execute("select unix_timestamp(date(time)), avg(pressure) from "
               "{table} where hour(time) = 1 and minute(time) "
               "between 00 and 20 and time between \"{from_date}\" and "
               "\"{to_date}\" group by date(time) order by time desc"\
                   .format(from_date=FROM_DATE, to_date=TO_DATE, table=TABLE)
               )
DATA = np.array(CURSOR.fetchall())

# Reduction factor for the number of xticks
REDUCTION = 3

# Generate xticks
TZ = timedelta(hours=1)
XTICK_POSITIONS = []
DATETIMES = []
for n, timestamp in enumerate(reversed(DATA[:, 0])):
    if n % REDUCTION == 0:
        XTICK_POSITIONS.append(timestamp + 3600)
        DATETIMES.append(datetime.fromtimestamp(timestamp) + TZ)
XLABELS = [date_time.strftime('%b-%d %H:%M') for date_time in DATETIMES]

# Make the figure
FIG, AX = plt.subplots(1, 1, 1)
AX.bar(DATA[:, 0] + 3600, DATA[:, 1], width=12000, color='black',
       align='center', log=True)
AX.set_ylabel('Pressure / torr')

# Exchange the xticks
AX.set_xticks(XTICK_POSITIONS)
AX.set_xticklabels(XLABELS, rotation=30, horizontalalignment='right')
plt.subplots_adjust(bottom=0.2)

plt.show()
