"""Convert field quantities from text files to matlab file.
"""
import os
import csv
import numpy as np
import scipy.io as spio

accepted_power = [2.67479e-19, 2.53509e-19, 2.57445e-19, 2.70529e-19, 3.02819e-19, 2.92014e-19, 2.88874e-19, 3.21899e-19, 2.61459e-19, 3.390277e-19, 3.27098e-19, 1.98715e-19, 3.48907e-19, 2.557820e-19, 2.42046e-19, 2.81527e-19]
field_prefix = os.path.join('F:\\', 'KU_ten_32_Tx_MRT', 'Export', '3d')
efield_file_names = ["e-field (f=447) [Tran" + str(i+1) + "].txt" for i in range(16)]
efield_file_paths = [os.path.join(field_prefix, filename) for filename in efield_file_names]
for path in efield_file_paths:
    print(path, ": ", os.path.exists(path))

# get xdim, ydim, zdim from first first e-field_file
xdim = np.empty((0,), dtype = np.float)
ydim = np.empty((0,), dtype = np.float)
zdim = np.empty((0,), dtype = np.float)

with open(efield_file_paths[0], 'r', newline='\r\n') as csvfile:
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
print(len(efield_file_paths))
exre = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(efield_file_paths)), dtype = np.float)
eyre = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(efield_file_paths)), dtype= np.float)
ezre = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(efield_file_paths)), dtype = np.float)
exim = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(efield_file_paths)), dtype = np.float)
eyim = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(efield_file_paths)), dtype = np.float)
ezim = np.empty((np.shape(xdim)[0]*np.shape(ydim)[0]*np.shape(zdim)[0], len(efield_file_paths)), dtype = np.float)

for i in range(len(efield_file_names)):
    print('processing ', efield_file_names[i])
    with open(efield_file_paths[i], 'r', newline='\r\n') as csvfile:
        print(efield_file_paths[i])
        field_reader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
        next(field_reader)
        next(field_reader)
        row_count = 0
        for row in field_reader:
            # P ~ 1/2|E|*|E|
            exre[row_count, i] = float(row[3])*2.0/np.sqrt(accepted_power[i]) 
            eyre[row_count, i] = float(row[4])*2.0/np.sqrt(accepted_power[i])
            ezre[row_count, i] = float(row[5])*2.0/np.sqrt(accepted_power[i])
            exim[row_count, i] = float(row[6])*2.0/np.sqrt(accepted_power[i])
            eyim[row_count, i] = float(row[7])*2.0/np.sqrt(accepted_power[i])
            ezim[row_count, i] = float(row[8])*2.0/np.sqrt(accepted_power[i])
            row_count += 1

save_dict = {}
save_dict['xdim'] = xdim
save_dict['ydim'] = ydim
save_dict['zdim'] = zdim
save_dict['exre'] = exre
save_dict['eyre'] = eyre
save_dict['ezre'] = ezre
save_dict['exim'] = exim
save_dict['eyim'] = eyim
save_dict['ezim'] = ezim
print('saving mat file')
spio.savemat('efields_norm.mat', save_dict, oned_as='column')
#exre = np.reshape(exre, (len(xdim), len(ydim), len(zdim)))
