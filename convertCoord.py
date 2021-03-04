import sys
import pyproj

Args = sys.argv;

x = Args[1];
y = Args[2];
z = Args[3]; 
#print(x, y, z)
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=False)
#print(lon, lat, alt)

print(lon)
print(alt)
print(lat)   
