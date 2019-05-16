"""
Extract fields from a magnetostatic simulation.
"""
import os
import numpy as np
import scipy.io as spio
import matplotlib.pyplot as plt
import cstmod

project_path = os.path.normpath(os.path.join(os.path.realpath(__file__), r'..', r'..', 'Test_Data','TLR_5cm_B0.cst'))
print(project_path)
print("Exits?", os.path.exists(project_path))
rr = cstmod.CSTResultReader('2018')
rr.open_project(project_path)
result_tree_name = rr.query_result_names("2D/3D Results\\B-Field [Ms]")


print(result_tree_name)
xdim, ydim, zdim = rr.load_grid_data()
xdim = np.array(xdim)
ydim = np.array(ydim)
zdim = np.array(zdim)
nx = len(xdim)
ny = len(ydim)
nz = len(zdim)
n_vals = len(xdim) * len(ydim) * len(zdim)

print(result_tree_name[0])
b_field = rr.load_data_3d("2D/3D Results\\B-Field [Ms]")

rr.close_project()

print(b_field)
print(len(b_field)/(len(xdim)*len(ydim)*len(zdim)))
bxr = b_field[0:2*n_vals-1:2]
bxi = b_field[1:2*n_vals:2]
byr = b_field[2*n_vals:4*n_vals-1:2]
byi = b_field[2*n_vals+1:4*n_vals:2]
bzr = b_field[4*n_vals:6*n_vals-1:2]
bzi = b_field[4*n_vals+1:6*n_vals:2]

#np.reshape(bxr, (nx, ny, nz)) + 
#np.reshape(bxi, (nx, ny, nz))
#np.reshape(byr, (nx, ny, nz))
#np.reshape(byi, (nx, ny, nz))
bz = np.reshape(bzr, (nx, ny, nz), order='F') + 1j*np.reshape(bzi, (nx, ny, nz), order='F')
bzr = np.reshape(bzr, (nx, ny, nz), order='F')
bzi = np.reshape(bzi, (nx, ny, nz), order='F')
XU, YU = np.meshgrid(xdim, zdim)
fig1 = plt.figure()
#plt.plot(xdim, 'b')
#plt.plot(ydim, 'r')
#plt.plot(zdim, 'c')

mycmap = plt.cm.get_cmap('jet')

y_slice = 0.0
y_slice_ind = np.argmin(abs(ydim - y_slice))
plt.pcolormesh(np.transpose(XU), np.transpose(YU), bzr[:,y_slice_ind,:], cmap = mycmap, vmin=-3e-6, vmax=3e-6)
plt.colorbar()

plt.savefig('bz0_coronal.png')

#plt.show()
