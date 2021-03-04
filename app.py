# -*- coding: utf-8 -*-
import pyproj
import math
import datetime as dt
from density import densityIntegral
from density import densityIntegralMy
from satPos import satellitePosition
import time
import georinex as gr
from netCDF4 import Dataset 


def ecefTolla(x, y, z):
	ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
	lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
	lon, lat, alt = pyproj.transform(ecef, lla, x, y, z)
	return [lon, lat, alt]

def grToRad(x):
	return (math.pi*x)/180

def checkLon(lon):
	if lon < 0:  
		return math.pi - lon;
	else:
		return lon


def getIntegral(year, month, day, hour, mm, sec, satellites, RPx, RPy, RPz, nav, ncfile):
# def getIntegral(year, month, day, hour, mm, sec, satellites, ModelRunGeo, RPx, RPy, RPz):
	stationPos = ecefTolla(RPx, RPy, RPz);
	stationLon = checkLon(grToRad(stationPos[0]))
	stationLat = grToRad(stationPos[1])
	P1 = [stationLon, stationPos[2], stationLat] # station position


	# d0 = dt.datetime(int(year), 1, 1, 00, 00, 00);
	# d1 = dt.datetime(int(year), int(month), int(day));
	# delta = (d1 - d0).days + 1;  # день от начала года в который брать координаты спутника
	# print(delta)
	# file = '/data/nav/'+str(year)+'/0'+str(delta)+'/auto0'+str(delta)+'0.19n'; #satellite file
	# nav = gr.load(nav);
	# ncfile = Dataset(ncfile, 'r');

	result = dict();
	for s in satellites:
		if(s[0] == "G"):
			sp = satellitePosition(s, year, month, day, hour, mm, sec, nav)
			if(sp):
				satPos = ecefTolla(sp[0], sp[1], sp[2]); # ECEF -> lla
				
				satLon = checkLon(grToRad(satPos[0])) #longitude [0, 2pi]
				satLat = grToRad(satPos[1])

				P = [satLon, satPos[2], satLat]; #satellite
				result.update({s: densityIntegral(P, P1, ncfile)})
			else:
				result.update({s: 0}) #если не удалось найти координаты по другим причинам
		else: 
			result.update({s: 0}) #если спутник не GPS
	return result






#start_time = time.time()
#r = getIntegral(2019,3, 13, 0, 0, 1, ["G01", "G02", "G03", "G04", "G05", "G06", "G07", "G08", "G09"], "../ModelRunGeo-2019-019-221500.nc", "2304703.4760", "-4874817.1770", "3395186.9500")
# navfile = gr.load("/data/nav/2019/082/auto0820.19n");
# ncfile = Dataset("/app/IonModel/OUTPUT/ModelRunGeo-2019-077-104000.nc", 'r');
# r = getIntegral(2019, 3, 23, 6, 0, 0, ["G08"], "2304703.4760", "-4874817.1770", "3395186.9500", navfile, ncfile)
# print(r)



# ncfile = Dataset("../ModelRunGeo-2019-019-221500.nc", 'r');
# r = densityIntegral([0.62831855, 0, 1.0140584], [0.62831855, 0, 1.0140584 ], ncfile)
# print(r)

# print("--- %s seconds ---" % (time.time() - start_time))

# start_time = time.time()
# for i in range(1, 10):
# 	s = "G0"+str(i)
# 	r = getIntegral(2019,3, 13, 0, 0, 0, [s], "../ModelRunGeo-2019-019-221500.nc", "2304703.4760", "-4874817.1770", "3395186.9500")
# 	#time.sleep(5.5) 
# 	print(r)
# print("--- %s seconds ---" % (time.time() - start_time))







