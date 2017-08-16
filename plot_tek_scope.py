import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyp
import numpy.fft as fft

channel_names = {1:'Chan1', 2:'Chan2', 3:'Chan3', 4:'Chan4'}

def read_line(line, old = False, samprate=1e-9):
	if( old ):
		stuff = line.split(',') 
		channel = int(stuff[0])
		eventid    = int(stuff[1])
		vals = []
		vals.append(float( stuff[2][2:] ) )
		for i in range(3, len(stuff)-1):
			vals.append(float(stuff[i]))
		vals.append(float(stuff[len(stuff)-1][:-4]))
		return pd.DataFrame({'channel':channel, 'eventid':eventid,'volt':pd.Series(np.array(vals), index=np.arange(0.,len(vals))*samprate)})
	else:
		stuff = line.split(',')
		#print stuff
		channel = int(stuff[0])
		eventid   = int(stuff[1])
		timestamp = stuff[2]
		samprate  = float(stuff[3])
		trigtime  = float(stuff[4])
		vals = []
		vals.append(float(stuff[5][2:]))
		for i in range(6, len(stuff)-1):
			vals.append(float(stuff[i]))
		try:
			vals.append(float(stuff[len(stuff)-1][:-4]))
		except:
			try:
				vals.append(float(stuff[len(stuff)-1][:-3]))
			except:
				try:
					vals.append(float(stuff[len(stuff)-1][:-2]))
				except:
					try:
						vals.append(float(stuff[len(stuff)-1][:-1]))
					except:
						print "",


		
		return pd.DataFrame({'channel':channel, 'eventid':eventid,'samprate':samprate,'trigtime':trigtime, 'volt':pd.Series(np.array(vals), index=np.arange(0.,len(vals))*samprate)})

def read_file(fname):
	events = {}
	with open(fname, 'r') as fi:
		for line in fi:
			event = read_line(line)
			if( event.channel.iloc[0] == 1 ):
				evs = []
			evs.append(event)
			if( event.channel.iloc[0] == 4):
				events[event.eventid.iloc[0]] = evs
	return events

def draw_event(events, eventid):
	event = events[eventid]

	for ich in range(0,4):
		channel = event[ich]	
		print "Drawing channel ", channel.channel.iloc[0], " event ", channel.eventid.iloc[0], " with ", len(channel.volt), " points "
		pyp.figure(1, figsize=(6,8))
		ax = pyp.subplot(2, 2, ich+1)
		pyp.plot(channel.volt.index*1e9, channel.volt)
		ax.set_title(channel_names[ich+1])
		fv = fft.rfft(channel.volt.values)
		freq = fft.rfftfreq(len(channel.volt.values), d=channel.samprate.iloc[0])	
		if(ich == 3):	
			pyp.show()

	
#########
# new file
dirc = '/Users/wissels/Dropbox/CP-510/test_data/'
fname = dirc + 'TDS_dat_10-42-33-602510.csv'
start_event = 1
nevents     = 5
if( len(sys.argv) == 4):
	fname = dirc + sys.argv[1]
	start_event = int(sys.argv[2])
	nevents     = int(sys.argv[3])
print "usage: python plot_tek_scope.py fname start_event nevents"
print fname, start_event, nevents
	
events = read_file(fname )

for eid in range(start_event, start_event + nevents ):
	if( len(events ) > 100 and eid < len(events)-100 ):
		# avoid sync slips
		print "Skipping event ", eid, " / ", len(events)
	else:
		draw_event(events, eid)


