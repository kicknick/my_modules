import numpy as np
from scipy.interpolate import RegularGridInterpolator
from netCDF4 import Dataset 


ncfile = Dataset("../ModelRunGeo-2019-019-221500.nc", 'r');
ED = ncfile.variables['Electron_Density'][:][0];
Geo_Lon = ncfile.variables['Geo_Lon'][0][:, 0, 0]; #60
Geo_Radius = ncfile.variables['Geo_Radius'][0][0, :, 0]; #150. 6458136..8339478.5 (6458km - 8339km)
Geo_Lat = ncfile.variables['Geo_Lat'][:][0][0, 0, :];  #80

x = np.linspace(0, 1, 60)
y = np.linspace(0, 1, 150)
z = np.linspace(0, 1, 80)

f = RegularGridInterpolator(points=(Geo_Lon, Geo_Radius, Geo_Lat), values=ED)
pts = np.array([[0.1, 7000000, -0.18]])
print(f(pts))

def data(x, y):
	return x+y



def f(x,y,z):
    return x+y+z

x = np.linspace(1, 4, 11)
y = np.linspace(4, 7, 22)
z = np.linspace(7, 9, 33)


# x = np.linspace(0, 1, 3) #  or  0.5*np.arange(3.) works too

# populate the 3D array of values (re-using x because lazy)
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')

vals = np.sin(X) + np.cos(Y) + np.tan(Z)
#print(X)
#data = f(*np.meshgrid(x, y, z, indexing='ij', sparse=True))

#print(np.meshgrid(x, y, z, indexing='ij'))


#my_interpolating_function = RegularGridInterpolator((x, y, z), data)


# print(f([1.2, 4]))

# pts = np.array([[2.1, 6.2, 8.3], [3.3, 5.2, 7.1]])
#print(pts)
#r = my_interpolating_function(pts)
#print(r)