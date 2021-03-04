# -*- coding: utf-8 -*-
import numpy as np
import math
import sys
from netCDF4 import Dataset 
import time
from scipy.interpolate import RegularGridInterpolator

def sin(x):
        return math.sin(x);

def cos(x):
        return math.cos(x);


def getDistance(t1, f1, r1, t2, f2, r2):
	R = 6371000;
	x1 = (r1+R) * cos(t1) * cos(f1);
	y1 = (r1+R) * cos(t1) * sin(f1);
	z1 = (r1+R) * sin(t1);

	x2 = (r2+R) * cos(t2) * cos(f2);
	y2 = (r2+R) * cos(t2) * sin(f2);
	z2 = (r2+R) * sin(t2);

	d = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2) + pow(z1 - z2, 2))
	return d;

def densityIntegral(p1, p2, ncfile):  #p1 - satellite, p2 - station
	#print(ncfile)
	#print(ncfile.variables['Electron_Density'])

	ED = ncfile.variables['Electron_Density'][:][0];
	Geo_Lon = ncfile.variables['Geo_Lon'][0][:, 0, 0]; #60
	Geo_Radius = ncfile.variables['Geo_Radius'][0][0, :, 0]; #150. 6458136..8339478.5 (6458km - 8339km)
	Geo_Lat = ncfile.variables['Geo_Lat'][:][0][0, 0, :];  #80

	p1[1] = Geo_Radius[149]  # верхняя граница
	p2[1] = Geo_Radius[0]    # нижняя граница


	f = RegularGridInterpolator(points=(Geo_Lon, Geo_Radius, Geo_Lat), values=ED)


	# генерация сетки 
	lon = np.linspace(p1[0], p2[0], 150); 
	rad = np.linspace(p1[1], p2[1], 150);
	lat = np.linspace(p1[2], p2[2], 150);

	#print(ED)

	A = [];
	for i in range(0, 150):
		A.append([lon[i], rad[i], lat[i]]);


	pts = np.array(A) # массив точек интерполяции

	distance = getDistance(p1[2], p1[0], p1[1], p2[2], p2[0], p2[1]);
	d = distance/150; #dl 

	I = 0;
	try:
		res = f(pts);
	except Exception:
		return I;

	for i in res:
		I+=i*d

	return I
























def densityIntegralMy(p1, p2, ncfile):  #p1 - satellite, p2 - station
	#ncfile = Dataset(file, 'r');

	ED = ncfile.variables['Electron_Density'][:][0];
	Geo_Lon = ncfile.variables['Geo_Lon'][:][0];
	Geo_Radius = ncfile.variables['Geo_Radius'][:][0];
	Geo_Lat = ncfile.variables['Geo_Lat'][:][0];

	P1 = [];
	P2 = [];

	#start_time = time.time()
	#LONGITUDE
	for i in range(0, len(Geo_Lon)-1):
		if Geo_Lon[i][0][0]<=p1[0] and p1[0]<= Geo_Lon[i+1][0][0]:
			break;
	P1.append(i);
	for i in range(0, len(Geo_Lon)-1):
		if Geo_Lon[i][0][0]<=p2[0] and p2[0]<= Geo_Lon[i+1][0][0]:
			break;
	P2.append(i);

	#RADIUS
	for i in range(0, len(Geo_Radius[0])-1):
		if Geo_Radius[0][i][0]<=p1[1] and p1[1]<= Geo_Radius[0][i+1][0]:
			break;
	P1.append(i+1);
	for i in range(0, len(Geo_Radius[0])-1):
		if Geo_Radius[0][i][0]<=p2[1] and p2[1]<= Geo_Radius[0][i+1][0]:
			break;
	#P2.append(i);
	P2.append(0)  #  radius of station 
	#print(Geo_Radius[0][0][0], Geo_Radius[0][149][0])

	#LATITUDE
	for i in range(0, len(Geo_Lat[0][0])-1):
		if Geo_Lat[0][0][i]<=p1[2] and p1[2]<=Geo_Lat[0][0][i+1]:
			break;
	P1.append(i);
	for i in range(0, len(Geo_Lat[0][0])-1):
		if Geo_Lat[0][0][i]<=p2[2] and p2[2]<=Geo_Lat[0][0][i+1]:
			break;
	P2.append(i);
	#print("--- %s seconds loop---" % (time.time() - start_time))
	#print(P1, P2)	
	p1[1] = Geo_Radius[0][P1[1]][0]
	p2[1] = Geo_Radius[0][P2[1]][0]
	#print(p1, p2);

	#t - latitude, f - longitude, 
	distance = getDistance(p1[2], p1[0], p1[1], p2[2], p2[0], p2[1]);
	#print(distance)


	lon1=P1[0]; rad1=P1[1]; lat1=P1[2];
	lon2=P2[0]; rad2=P2[1]; lat2=P2[2];
	order = [];

	#print(Geo_Lon[lon1, 0, 0], Geo_Radius[0, rad1, 0], Geo_Lat[0, 0, lat1])
	#print(Geo_Lon[lon2, 0, 0], Geo_Radius[0, rad2, 0], Geo_Lat[0, 0, lat2])


	def getAverageValue(A):
		S = 0;
		for i in A:
			#print(i, order)
			S = S + ED[i[calcOrder[0]], i[calcOrder[1]], i[calcOrder[2]]];
		S/=len(A);	
		#print S;
		return S; 

	#c<a && c<b
	a=lon2-lon1;
	b=rad2-rad1;
	c=lat2-lat1;


	B = [[a, lon1, lon2], [b, rad1, rad2], [c, lat1, lat2]];
	A = [abs(a), abs(b), abs(c)]; 
	order = np.argsort(A)[::-1]; #order of sides #[0,1,2] [0,2,1] [1,2,0] [1,0,2] [2,0,1] [2,1,0]
	#print(order)
	calcOrder = []
	for i in range(0, 3):
		for j in range(0, 3):
			if(order[j] == i):
				calcOrder.append(j)

	a = B[order[0]][0]
	b = B[order[1]][0]
	c = B[order[2]][0]
	d = distance/abs(a); #step in 3d
	#print(d, a)

	gx=gy=gz=0; #gradient
	if(a != 0):
		gx=int(a/abs(a)); 
	if(b != 0):
		gy=int(b/abs(b));
	if(c != 0):
		gz=int(c/abs(c));
	#print(gx, gy, gz)

	I = 0;  #integral of ED
	q = 0;  #in q steps make shift along shorter line 
	p = 0;  #in p steps make shift along shorter line (3d deimension)

	rangeFrom = B[order[0]][1];
	rangeTo = B[order[0]][2];
	j = B[order[1]][1];
	k = B[order[2]][1];

	if(b != 0):
		if(a%b != 0):
			q=math.ceil(abs(int(a/b))+1)
		else: q=a/b
	if(c != 0): 
		if(a%c != 0):
			p=math.ceil(abs(int(a/c))+1)
		else: p=a/c;
	p = abs(p);
	q = abs(q);

	tq=tp=0;
	for i in range(rangeFrom, rangeTo, gx):
		#print(i, j, k)
		tq+=1;
		tp+=1;
		if tq==q and tp==p:
			#print "getAverageValue16";
			I+=getAverageValue([[i,j,k],[i+gx,j,k],[i,j+gy,k],[i+gx,j+gy,k],[i,j+gy+gy,k],[i+gx,j+gy+gy,k]  ,  [i,j,k+gz],[i+gx,j,k+gz],[i,j+gy,k+gz],[i+gx,j+gy,k+gz],[i,j+gy+gy,k+gz],[i+gx,j+gy+gy,k+gz]])*d;
			j+=gy; k+=gz; tq=tp=0;
		elif tq==q:
			#print "shift b";
			I+=getAverageValue([[i,j,k],[i+gx,j,k],[i,j+gy,k],[i+gx,j+gy,k],[i,j+gy+gy,k],[i+gx,j+gy+gy,k]  ,  [i,j,k+gz],[i+gx,j,k+gz],[i,j+gy,k+gz],[i+gx,j+gy,k+gz],[i,j+gy+gy,k+gz],[i+gx,j+gy+gy,k+gz]])*d;
			j+=gy; tq=0;
		elif tp==p:
			#print "shift c";
			I+=getAverageValue([[i,j,k],[i+gx,j,k],[i,j+gy,k],[i+gx,j+gy,k] , [i,j,k+gz],[i+gx,j,k+gz],[i,j+gy,k+gz],[i+gx,j+gy,k+gz] , [i,j,k+gz+gz],[i+gx,j,k+gz+gz],[i,j+gy,k+gz+gz],[i+gx,j+gy,k+gz+gz]])*d;
			k+=gz; tp=0; 
		else:
			I+=getAverageValue([[i,j,k],[i+gx,j,k],[i,j+gy,k],[i+gx,j+gy,k], [i,j,k+gz],[i+gx,j,k+gz],[i,j+gy,k+gz],[i+gx,j+gy,k+gz]])*d;

	return I;
