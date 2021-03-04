# -*- coding: utf-8 -*-
from netCDF4 import Dataset as dt
import numpy as np
import math
import sys
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

Args = sys.argv;
#print Args	
p1=[0.20943952, 6.96069e+06, 1.25266] #lon rad lat
p2=[3.66519, 8.01733e+06, 0.338019]


file = '../ModelRunGeo-2019-019-221500.nc'

#file = Args[1]; 
p1 = [float(Args[2]), float(Args[3]), float(Args[4])];
#p2 = [float(Args[5]), float(Args[6]), float(Args[7])]; 

#print p1, p2
ncfile = dt(file, 'r');

#ED = np.array(ncfile.variables['Electron_Density'][:], dtype=np.float32);

ED = ncfile.variables['Electron_Density'][:][0];
Geo_Lon = ncfile.variables['Geo_Lon'][:][0];
Geo_Radius = ncfile.variables['Geo_Radius'][:][0];
Geo_Lat = ncfile.variables['Geo_Lat'][:][0];
P1 = [];
P2 = [];

def appendCoord(array, len): # вычисление в координатах массива
	for i in range(0, len(Geo_Lon)-1):
		if Geo_Lon[i][0][0]<=p1[0] and p1[0]<= Geo_Lon[i+1][0][0]:
			break;
	return 0


#print(Geo_Radius[0], Geo_Radius[59])

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
P1.append(i);
for i in range(0, len(Geo_Radius[0])-1):
	if Geo_Radius[0][i][0]<=p2[1] and p2[1]<= Geo_Radius[0][i+1][0]:
		break;
P2.append(i);

#LATITUDE
for i in range(0, len(Geo_Lat[0][0])-1):
	if Geo_Lat[0][0][i]<=p1[2] and p1[2]<=Geo_Lat[0][0][i+1]:
		break;
P1.append(i);
for i in range(0, len(Geo_Lat[0][0])-1):
	if Geo_Lat[0][0][i]<=p2[2] and p2[2]<=Geo_Lat[0][0][i+1]:
		break;
P2.append(i);


print(P1, P2)	





#print ED[lon1][rad1][lat1], Geo_Lon[lon1][0][0], Geo_Radius[0][rad1][0], Geo_Lat[0][0][lat1]
#print ED[lon2][rad2][lat2], Geo_Lon[lon2][0][0], Geo_Radius[0][rad2][0], Geo_Lat[0][0][lat2]

lon1=P1[0]; rad1=P1[1]; lat1=P1[2];
lon2=P2[0]; rad2=P2[1]; lat2=P2[2];
order = [];

print(Geo_Lon[lon1, 0, 0], Geo_Radius[0, rad1, 0], Geo_Lat[0, 0, lat1])
print(Geo_Lon[lon2, 0, 0], Geo_Radius[0, rad2, 0], Geo_Lat[0, 0, lat2])

def getAverageValue(A):
	#print A;
	S = 0;
	for i in A:
		S = S + ED[i[order[0]], i[order[1]], i[order[2]]];
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
#print order, A; 




a = B[order[0]][0]
b = B[order[1]][0]
c = B[order[2]][0]

d = math.sqrt(a*a+b*b+c*c)/abs(a); #step in 3d

gx=gy=gz=0; #gradient
if(a != 0):
	gx=int(a/abs(a)); 
if(b != 0):
	gy=int(b/abs(b));
if(c != 0):
	gz=int(c/abs(c));
#print gx, gy, gz


I = 0;  #integral of ED
q = 0;  #in q steps make shift along shorter line 
p = 0;  #in p steps make shift along shorter line (3d deimension)

rangeFrom = B[order[0]][1];
rangeTo = B[order[0]][2];
j = B[order[1]][1];
k = B[order[2]][1];

if(b != 0):
	if(a%b != 0):
		q=math.ceil(int(a/b)+1)
	else: q=a/b
if(c != 0): 
	if(a%c != 0):
		p=math.ceil(int(a/c)+1)
	else: p=a/c;
p = abs(p);
q = abs(q);
#print q, p;


tq=tp=0;
print(rangeFrom, rangeTo, gx)
for i in range(rangeFrom, rangeTo, gx):
	#print i, j, k
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

print(I);



#print ED[lon1][rad1][lat1], Geo_Lon[lon1][0][0], Geo_Radius[0][rad1][0], Geo_Lat[0][0][lat1]
#print ED[lon2][rad2][lat2], Geo_Lon[lon2][0][0], Geo_Radius[0][rad2][0], Geo_Lat[0][0][lat2]




#f = open("demofile.txt", "w")
#print ncfile.variables['Electron_Density'] lat = np.array(ncfile.variables[])

