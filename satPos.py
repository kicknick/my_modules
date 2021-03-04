# -*- coding: utf-8 -*-
import math
# from datetime import date
import datetime as dt
import numpy as np
import sys
# from netCDF4 import Dataset as dt
import numpy as np
import time

def checkNumber(x):
    if(x<10):
        return "0"+str(x)
    else:
        return str(x);

def sin(x):
        return math.sin(x);

def cos(x):
        return math.cos(x);

def getParam(satellite, param):
    for i in satellite[param]:
            if(i!='nan'):
                    break;
    return i.item(0);

def removeSpaces(s):
        s = s.strip()
        list = []
        for i in range(len(s)):
                if s[i] == ' ':
                        list.append('0')
                else:
                        list.append(s[i])
        return ''.join(list)

def satellitePosition(sat, year, month, day, hour, mm, sec, nav):
    sat = removeSpaces(sat)
    year = checkNumber(year)
    month = checkNumber(month);
    day = checkNumber(day)
    hour = checkNumber(hour)
    mm = checkNumber(mm)
    sec = checkNumber(sec);
    Time = year+'-'+month+'-'+day+'-'+hour+'-'+mm+'-'+sec;
    satellite = nav.sel(sv=sat, time=Time);

    if(math.isnan(getParam(satellite, "Io"))):  #если не удалось достать значения элементов
        return False

    i0 = getParam(satellite, 'Io')
    Omega = getParam(satellite, 'Omega0')
    e = getParam(satellite, 'Eccentricity')
    omega = getParam(satellite, 'omega')
    M0 =  getParam(satellite, 'M0')
    Cuc = getParam(satellite, 'Cuc')
    Cus = getParam(satellite, 'Cus')
    Crc = getParam(satellite, 'Crc')
    Crs = getParam(satellite, 'Crs')
    Cic = getParam(satellite, 'Cic')
    Cis = getParam(satellite, 'Cis')
    IDOT = getParam(satellite, 'IDOT') 
    OmegaDot = getParam(satellite, 'OmegaDot')
    DeltaN = getParam(satellite, 'DeltaN')
    sqrtA = getParam(satellite, 'sqrtA')
    toe = getParam(satellite, 'Toe')

    #SECINWEEK = 603148.6923 
    SECINWEEK = 604800.00

    sT = Time.split('-');
    d0 = dt.datetime(1999, 8, 22, 00, 00, 00);
    d1 = dt.datetime(int(sT[0]), int(sT[1]), int(sT[2]), int(sT[3]), int(sT[4]));
    #print(d1, d0)
    delta = (d1 - d0).total_seconds()
    #print(delta);
    tdata = (delta/SECINWEEK - int(delta/SECINWEEK))*SECINWEEK; 
    #print(tdata)

    tShift = 10653; 
    t = tdata - toe - tShift;

    #print(t)

    M = M0 + (math.sqrt(398600441800000) / (sqrtA*sqrtA*sqrtA) + DeltaN) * t;
    #print(M0, M, e, sqrtA, DeltaN, t, toe, tdata)

    d = 0.00000000001; #точность вычисления эксцентриситета
    def getE(E):
        return M + e*sin(E);
        
    E0 = M;
    E = getE(E0)  
    while(abs(1-(E0/E)) > d):
        E0 = E;
        E = getE(E0); 


    v = math.atan2(math.sqrt(1 - e*e)*sin(E), (cos(E)-e));

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

    #Поворот
    R = np.array([[cos(O)*cos(w)-sin(O)*sin(w)*cos(i), -cos(O)*sin(w)-sin(O)*cos(w)*cos(i), sin(O)*sin(i)],
         [sin(O)*cos(w)+cos(O)*sin(w)*cos(i), -sin(O)*sin(w)+cos(O)*cos(w)*cos(i), -cos(O)*sin(i)],
         [sin(w)*sin(i), cos(w)*sin(i), cos(i)]]);


    ro = R.dot(q); # x, y, z

    return [ro[0], ro[1], ro[2]];



