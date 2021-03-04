import georinex as gr
import math
from datetime import date
import datetime as dt
import numpy as np
import sys
from netCDF4 import Dataset as dt
import numpy as np


def removeSpaces(s):
	s = s.strip()
	list = [] 
	for i in range(len(s)): 
		if s[i] == ' ':
			list.append('0')
		else:
			list.append(s[i]) 
	return ''.join(list)	
		 
	

sat  = removeSpaces('   G 5')
print(sat)
file = '/srv/data/nav/2019/350/auto3500.19n'
nav = gr.load(file)
satellite = nav.sel(sv=sat);
#print(satellite)
