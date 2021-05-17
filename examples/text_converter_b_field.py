"""Convert field quantities from text files to matlab file.
"""
import os
import csv
import numpy as np
import scipy.io as spio
from scipy.constants import mu_0

accepted_power = [2.67479e-19, 2.53509e-19, 2.57445e-19, 2.70529e-19, 3.02819e-19, 2.92014e-19, 2.88874e-19, 3.21899e-19, 2.61459e-19, 3.390277e-19, 3.27098e-19, 1.98715e-19, 3.48907e-19, 2.557820e-19, 2.42046e-19, 2.81527e-19]

field_prefix = os.path.join('F:\\', 'KU_ten_32_Tx_MRT', 'Export', '3d')
hfield_file_names = ["h-field (f=447) [Tran" + str(i+1) + "].txt" for i in range(16)]
hfield_file_paths = [os.path.join(field_prefix, filename) for filename in hfield_file_names]
for path in hfield_file_paths:
    print(path, ": ", os.path.exists(path))

# get xdim, ydim, zdim from first first e-field_file
xdim = np.empty((0,), dtype = np.float)
ydim = np.empty((0,), dtype = np.float)
zdim = np.empty((0,), dtype = np.float)

with open(hfield_file_paths[0], 'r', newline='\r\n') as csvfile:
    field_reader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
    print(next(field_reader))
    print(next(field_reader))
    for row in field_reader:
        if row[0] not in xdim:
            xdim = np.append(xdim, row[0])
        if row[1] not in ydim:
            ydim = np.append(ydim, row[1])
        if row[2] not in zdim:
            zdim = np.append(zdim, row[2])

xdim = [float(x) for x in xdim]
ydim = [float(y) for y in ydim]
zdim = [float(z) for z in zdim]

print(np.shape(xdim)[0], np.shape(ydim)[0], np.shape(zdim)[0])
print(len(hfield_file_paths))
hxre = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(hfield_file_paths)), dtype = np.float)
hyre = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(hfield_file_paths)), dtype= np.float)
hzre = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(hfield_file_paths)), dtype = np.float)
hxim = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(hfield_file_paths)), dtype = np.float)
hyim = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(hfield_file_paths)), dtype = np.float)
hzim = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(hfield_file_paths)), dtype = np.float)

for i in range(len(hfield_file_names)):
    print('processing ', hfield_file_names[i])
    with open(hfield_file_paths[i], 'r', newline='\r\n') as csvfile:
        print(hfield_file_paths[i])
        field_reader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
        next(field_reader)
        next(field_reader)
        row_count = 0
        for row in field_reader:
            # P ~ 1/2|H|*|H|
            hxre[row_count, i] = float(row[3])*2.0/np.sqrt(accepted_power[i])
            hyre[row_count, i] = float(row[4])*2.0/np.sqrt(accepted_power[i])
            hzre[row_count, i] = float(row[5])*2.0/np.sqrt(accepted_power[i])
            hxim[row_count, i] = float(row[6])*2.0/np.sqrt(accepted_power[i])
            hyim[row_count, i] = float(row[7])*2.0/np.sqrt(accepted_power[i])
            hzim[row_count, i] = float(row[8])*2.0/np.sqrt(accepted_power[i])
            row_count += 1

save_dict = {}
save_dict['xdim'] = xdim
save_dict['ydim'] = ydim
save_dict['zdim'] = zdim
save_dict['bxre'] = mu_0*hxre
save_dict['byre'] = mu_0*hyre
save_dict['bzre'] = mu_0*hzre
save_dict['bxim'] = mu_0*hxim
save_dict['byim'] = mu_0*hyim
save_dict['bzim'] = mu_0*hzim
print('saving mat file')
spio.savemat('hfields_norm.mat', save_dict, oned_as='column')
#exre = np.reshape(exre, (len(xdim), len(ydim), len(zdim)))
