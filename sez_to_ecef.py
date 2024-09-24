# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts latitude, longitude, height above ellipsoid, s position, e position, z position to position in ECEF coordinates (ecef_x_km,ecef_y_km,ecef_z_km) 
# Parameters:
#  lat_deg: latitude in degrees
#  lon_deg: longitude in degrees
#  hae_km: height above ellipsoid in km
#  s_km: south position in km
#  e_km: east position in km
#  z_km: z position in km
# Output:
#  Print the ECEF coordinates (rx,ry,rz) in km
#
# Written by Erika Ashley
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import sys # argv
import math

# "constants"
R_E_KM = 6378.1363
E_E    = 0.081819221456
# helper functions

## calc_denom
##
def calc_denom(ecc,lat_rad):
    return math.sqrt(1.0-ecc**2.0*math.sin(lat_rad)**2.0)
## function description
# def calc_something(param1, param2):
#   pass

# initialize script arguments
o_lat_deg=float('nan') # latitude in degrees
o_lon_deg=float('nan') # longitude in degrees
o_hae_km=float('nan') # height above ellipsoid in km
s_km=float('nan')  # south position in km
e_km=float('nan') # east position in km
z_km=float('nan') # z position in km

# parse script arguments
if len(sys.argv)==7:
    o_lat_deg=float(sys.argv[1])
    o_lon_deg=float(sys.argv[2])
    o_hae_km=float(sys.argv[3])
    s_km=float(sys.argv[4])
    e_km=float(sys.argv[5])
    z_km=float(sys.argv[6])
else:
   print(\
   'Usage: '\
   'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
   exit()

# write script below this line
lat_rad=o_lat_deg*math.pi/180.0
lon_rad=o_lon_deg*math.pi/180.0
denom=calc_denom(E_E,lat_rad)
c_E=R_E_KM/denom
s_E=R_E_KM*(1.0-E_E*E_E)/denom
r_x_km=(c_E+o_hae_km)*math.cos(lat_rad)*math.cos(lon_rad)
r_y_km=(c_E+o_hae_km)*math.cos(lat_rad)*math.sin(lon_rad)
r_z_km=(s_E+o_hae_km)*math.sin(lat_rad)
recef_vect=[r_x_km,r_y_km,r_z_km]

sez_vect=[s_km, e_km, z_km]
rotation_1=[[math.sin(lat_rad), 0, math.cos(lat_rad)],[0, 1, 0],[-math.cos(lat_rad),0,math.sin(lat_rad)]]
rotation_2=[[math.cos(lon_rad),-math.sin(lon_rad),0],[math.sin(lon_rad),math.cos(lon_rad),0],[0,0,1]]

rotationcalc_1=[0,0,0]
rotationcalc_2=[0,0,0]

for i in range(3):
    for j in range(3):
        rotationcalc_1[i]+=rotation_1[i][j]*sez_vect[j]

for i in range(3):
    for j in range(3):
        rotationcalc_2[i]+=rotation_2[i][j]*rotationcalc_1[j]

ecef_vect=[]

for i,j in zip(rotationcalc_2,recef_vect):
    ecef_vect.append(i + j)

ecef_x_km=ecef_vect[0]
ecef_y_km=ecef_vect[1]
ecef_z_km=ecef_vect[2]
print('ecef_x_km:  '+str(ecef_x_km))
print('ecef_y_km:  '+str(ecef_y_km))
print('ecef_z_km:  '+str(ecef_z_km))
