import georinex as gr
import math
from datetime import date
import datetime as dt
import numpy as np
import sys
from netCDF4 import Dataset as dt
import numpy as np



file = './auto0330.19n';
Time='2019-02-02-22-00'
sat='G01'

Args = sys.argv;
file = Args[1];
sat = Args[2];
Time = Args[3];

nav = gr.load(file);


satellite = nav.sel(sv=sat, time=Time)

def getParam(param):
        for i in satellite[param]:
                if(i!='nan'):
                        break;
        return i.item(0);

def sin(x):
        return math.sin(x);

def cos(x):
        return math.cos(x);


i0 = getParam('Io')
Omega = getParam('Omega0')
e = getParam('Eccentricity')
omega = getParam('omega')
M0 =  getParam('M0')
Cuc = getParam('Cuc')
Cus = getParam('Cus')
Crc = getParam('Crc')
Crs = getParam('Crs')
Cic = getParam('Cic')
Cis = getParam('Cis')
IDOT = getParam('IDOT') 
OmegaDot = getParam('OmegaDot')
DeltaN = getParam('DeltaN')
sqrtA = getParam('sqrtA')

SECINWEEK = 603148.6923 
SECINWEEK = 604800.00

sT = Time.split('-');
d0 = dt.datetime(1999, 8, 22, 00, 00, 00);
d1 = dt.datetime(int(sT[0]), int(sT[1]), int(sT[2]), int(sT[3]), int(sT[4]));
#print(d1, d0)
delta = (d1 - d0).total_seconds()
#print(delta);
tdata = (delta/SECINWEEK - int(delta/SECINWEEK))*SECINWEEK;
#print(tdata)

toe = getParam('Toe')
tShift = 10653;
t = tdata - toe - tShift;

#print(t)

M = M0 + (math.sqrt(398600441800000) / (sqrtA*sqrtA*sqrtA) + DeltaN) * t;
#print(M0, M, e, sqrtA, DeltaN, t, toe, tdata)

d = 0.00000000001;
def getE(E):
	return M + e*sin(E);
	
E0 = M;
E = getE(E0)  
while(abs(1-(E0/E)) > d):
	E0 = E;
	E = getE(E0); 
	#print(E0, E, 1-E0/E)


#print('E:',E)
v = math.atan2(math.sqrt(1 - e*e)*sin(E), (cos(E)-e));
#print('v:', v)

w = omega + Cuc*cos(2*(omega+v)) + Cus*sin(2*(omega+v));
r = sqrtA*sqrtA*(1-e*cos(E)) + Crc*cos(2*(omega+v)) + Crs*sin(2*(omega+v));
#r = sqrtA*sqrtA*(1 - e*cos(E));
i = i0 + IDOT*t + Cic*cos(2*(omega+v)) + Cis*sin(2*(omega+v));

#print(w, r, i)

we = 0.000072921151467;
O = Omega + t*(OmegaDot - we) - (we * toe);
#print('O:', O)

x = r*cos(v);
y = r*sin(v);
z = 0;

#print(x, y, z)
q = np.array([x, y, z]);



R = np.array([[cos(O)*cos(w)-sin(O)*sin(w)*cos(i), -cos(O)*sin(w)-sin(O)*cos(w)*cos(i), sin(O)*sin(i)],
     [sin(O)*cos(w)+cos(O)*sin(w)*cos(i), -sin(O)*sin(w)+cos(O)*cos(w)*cos(i), -cos(O)*sin(i)],
     [sin(w)*sin(i), cos(w)*sin(i), cos(i)]]);

#print('R:', R)

ro = R.dot(q);


print(ro[0], ro[1], ro[2]);
#print(math.atan(math.sqrt(ro[0]*ro[0] + ro[1]*ro[1])/ro[2])*57.32, math.atan(ro[1]/ro[2])*57.32)


