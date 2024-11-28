import os
import time
import glob
import sys
import pprint

from sys import exit
module_directory = #add local directory here
sys.path.append(module_directory)

#from timetable import getBusTimes
from liveLocation import getBusLocation
from plotMap import create_map

my_location = 'Fowlmere'
my_operator = 'A2BR'
#my_lineref = '31,26,75'

#timetable = getBusTimes(my_location).getNextBus()
#locations = getBusLocation(my_lineref,my_operator).getBusLocation()
locations = getBusLocation(my_operator).getBusLocation()
print(locations)
create_map(locations)
#print(timetable.keys())
#print(timetable)
#for bus in timetable.values():
#    print(bus)
#    type(bus)
#print(f"Next bus: ", timetable['serviceNumber'],timetable["destination"], timetable["time"])

