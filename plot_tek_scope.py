import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as pyp
import numpy.fft as fft

channel_names = {1: 'Chan1', 2: 'Chan2', 3: 'Chan3', 4: 'Chan4'}


def read_line(line, old=False, samprate=1e-9):
    if(old):
        stuff = line.split(',')
        channel = int(stuff[0])
        eventid = int(stuff[1])
        vals = []
        vals.append(float(stuff[2][2:]))
        for i in range(3, len(stuff)-1):
            vals.append(float(stuff[i]))
        vals.append(float(stuff[len(stuff)-1][:-4]))
        return pd.DataFrame({'channel': channel, 'eventid': eventid, 'volt': pd.Series(np.array(vals), index=np.arange(0., len(vals))*samprate)})
    else:
        stuff = line.split(',')
        #print("STUFF", stuff, "END STUFF")
        channel = int(stuff[0])
        eventid = int(stuff[1])
        timestamp = stuff[2]
        samprate = float(stuff[3])
        trigtime = float(stuff[4])
        print("HEADER IN THIS LINE: ", channel, eventid, timestamp, samprate, trigtime, "END HEADER")
        vals = []
        vals.append(float(stuff[5][2:]))
        for i in range(6, len(stuff)-1):
            vals.append(float(stuff[i]))
        #print("VALS", vals, "END VALS")
        #print("END OF STUFF \\", stuff[len(stuff)-1], "\\")
        try:
            #print(4)
            vals.append(float(stuff[len(stuff)-1][:-4]))
        except:
            try:
                #print(3)
                vals.append(float(stuff[len(stuff)-1][:-3]))
            except:
                try:
                    #print(2)
                    vals.append(float(stuff[len(stuff)-1][:-2]))
                except:
                    try:
                        #print(1)
                        vals.append(float(stuff[len(stuff)-1][:-1]))
                    except:
                        #print(0)
                        print("", end=' ')
        #print("made it", eventid)
        return pd.DataFrame({'channel': channel, 'eventid': eventid, 'samprate': samprate, 'trigtime': trigtime, 'volt': pd.Series(np.array(vals), index=np.arange(0., len(vals))*samprate)})


#### NOTE: This only works for a 2-channel measurement where the channels used are 1 and 2!
def read_tekscope_file(fname):
    events = {}
    with open(fname, 'r') as fi:
        for line in fi:
            #print(line)
            event = read_line(line)
            #print(event.channel)
            if(event.channel.iloc[0] == 1):
                evs = []
            evs.append(event)
            if(event.channel.iloc[0] == 2):
                events[event.eventid.iloc[0]] = evs
                #print(event.eventid.iloc[0], events[event.eventid.iloc[0]])
    #print(events)
    #print( pd.DataFrame(events) )
    return pd.DataFrame(events)


def draw_event(events, eventid):
    event = events[eventid]

    for ich in range(0, 2):
        channel = event[ich]
        print("Drawing channel ", channel.channel.iloc[0], " event ", channel.eventid.iloc[0], " with ", len(
            channel.volt), " points ")
        pyp.figure(1, figsize=(6, 8))
        ax = pyp.subplot(2, 2, ich+1)
        pyp.plot(channel.volt.index*1e9, channel.volt)
        ax.set_title(channel_names[ich+1])
        fv = fft.rfft(channel.volt.values)
        freq = fft.rfftfreq(len(channel.volt.values),
                            d=channel.samprate.iloc[0])
        if(ich == 1):
            pyp.show()


#########
# new file
dirc = '/home/radio/data/beacon_august2018/testsite//20180802/'
fname = dirc + 'tekScope_run500_20180802_18-42-55-713234.csv'
start_event = 1
nevents = 3
if(len(sys.argv) == 4):
    fname = dirc + sys.argv[1]
    start_event = int(sys.argv[2])
    nevents = int(sys.argv[3])
print("usage: python plot_tek_scope.py fname start_event nevents")
print(fname, start_event, nevents)

events = read_tekscope_file(fname)
print(events)
#for eid in range(start_event, start_event + nevents):
for eid in events.keys()[start_event:start_event+nevents]:
    if(len(events) > 100 and eid < len(events)-100):
        # avoid sync slips
        print("Skipping event ", eid, " / ", len(events))
    else:
        print(events.keys())
        draw_event(events, eid)
