"""
2ver.py

"""

from link import *
from tex_osco import *
from datetime import datetime
import os
import csv

########################################
# Usage: 2ver.py
#
#	python 2ver.py [num_chans, num_events, prefix]
#
#	All input values are optional. The defaults are num_chans=1,
#		num_events = 5, prefix=""
########################################
# Run settings


# number of channels
num_chan = 1
if len(sys.argv) > 1:
    num_chan = int(sys.argv[1])

# number of events
num_events = 5
if len(sys.argv) > 2:
    num_events = int(sys.argv[2])

# prefix for the output file
prefix = "tekScope"
if(len(sys.argv) > 3):
    prefix = sys.argv[3]+"_"

# path for the outputfile
dircPrefix = "/home/radio/data/tekScope/"

######################################

# From tex_osco library
# Link may be set up using Ethernet, GPIB, or RS232, see library
# LAN ethernet address of scope with switch
scope3 = tektronix(addr='169.254.62.22')
print(scope3.identification)
scope_name = scope3.scope_name()
print(scope_name)
print("Successfully connected to scope")
recordlen = int(scope3.horiz_record_len)
scope3.data_stop = recordlen
scope3.acq_state = 0
scope3.acq_stop_after = "SEQUENCE"
# scope3.acq_stop_after="RUNSTOP"
scope3.waveform_out_encoding = "ASC"
# scope3.data_stop=recordlen
print("Record Length: "+format(recordlen))
# scope3.horiz_sample="100e6"
date = datetime.now().strftime("%Y%m%d")
now = datetime.now().strftime("%H-%M-%S-%f")
data = []

dirc = "%s/%s/" % (dircPrefix, date)
if not os.path.isdir(dirc):
    os.system("mkdir %s" % dirc)

finame = dirc+prefix+"%s_" % (date)+format(now)+".csv"
print("Writing %d events on %d channels to file %s" %
      (num_events, num_chan, finame))
with open(finame, 'a') as csvfile:
    writer = csv.writer(csvfile)
    scope3.acq_state = 1
    scope3.header = 0
    i = 0
    print("Standby...")
    while (i < num_events):
        scope3.acq_state = 1
        while 1 == scope3.acq_state:
            pass
        print("Event number "+format(i+1)+" Time: " +
              datetime.now().strftime("%H:%M:%S.%f"))
        scope3.acq_state = 0
        for j in range(num_chan):
            scope3.data_source = j+1
            preamble = scope3.preamble.split(";")
            # print "Preamble is: "+format(preamble)
            # preamble1=scope3.preamble[5].split(",")
            # print "Preamble 1 is: "+format(preamble1)
            y_mult = float(preamble[13])
            y_off = float(preamble[14])
            x_zero = float(preamble[10])
            x_inc = float(preamble[9])
            data = scope3.curve.split(",")
            # print "Data: "+format(data)
            # print "Length is: "+format(len(data))
            for x in range(recordlen):  # convert data to mV
                data[x] = ((float(data[x])-y_off)*y_mult)*1000
            # print "Data: "+format(data)
            writer.writerow([j+1, i+1, datetime.now().strftime("%H:%M:%S.%f"),
                             x_inc, x_zero, ','.join(map(str, data))])

        i = i + 1
