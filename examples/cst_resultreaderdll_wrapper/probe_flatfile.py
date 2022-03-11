
import os 
import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt
from cstmod.dllreader import ResultReaderDLL
from PIL import Image, ImageShow


def field_probe(cst_file, field_result, z0 = 76.2/1000):
    with ResultReaderDLL(cst_file, '2020') as results:
        result_size = results._get_3d_hex_result_size(field_result, 0)
        (xdim, ydim, zdim) = results._get_hex_mesh()
        field3d = results._get_3d_hex_result(field_result, 0)
    print(len(xdim), len(ydim), len(zdim))
    print(result_size)
    print(len(field3d))
    setsize = len(xdim)*len(ydim)*len(zdim)
    zind = np.argmin(np.abs(np.array(zdim) - z0))
    print(zind, zdim[zind])
    
    test_field = np.reshape(field3d[0:2*setsize:2],(len(zdim), len(ydim), len(xdim)))
    nrows = 4
    ncols = 4
    fig, axs = plt.subplots(nrows, ncols)
    delta_z = int(len(zdim)/(nrows*ncols+1))
    zind = 0
    XX, YY = np.meshgrid(xdim, ydim)
    for i in range(ncols):
        for j in range(nrows):
            zind += delta_z
            axs[i][j].pcolormesh(XX, YY, test_field[zind,:,:], vmin=0, vmax=0.5)
    plt.show()
    
def materials_probe(cst_file, mat_type=0):
    with ResultReaderDLL(cst_file, '2020') as results:
        (nx, ny, nz) = results._get_hex_mesh_info()
        (xdim, ydim, zdim) = results._get_hex_mesh()
        mesh_materials = results._get_material_matrix_hex_mesh(mat_type)
    
    xmin = -63.5/1000
    xmax = 63.5/1000
    ymin = -63.5/1000
    ymax = 63.5/1000
    zmin = 0.0
    zmax = 152.4/1000
    nsize = nx*ny*nz
    
    mesh_materials = regrid_material_mesh(mesh_materials, (nx, ny, nz))

    
    zind = np.argmin(np.abs(np.array(zdim)-0.0762))
    yind = np.argmin(np.abs(np.array(ydim)))
    xind = np.argmin(np.abs(np.array(xdim)))
    x1 = np.argmin(np.abs(np.array(xdim)-xmin))
    x2 = np.argmin(np.abs(np.array(xdim)-xmax))
    y1 = np.argmin(np.abs(np.array(ydim)-ymin))
    y2 = np.argmin(np.abs(np.array(ydim)-ymax))
    z1 = np.argmin(np.abs(np.array(zdim)-zmin))
    z2 = np.argmin(np.abs(np.array(zdim)-zmax))
    xdim_subset = xdim[x1:x2]
    ydim_subset = ydim[y1:y2]
    zdim_subset = zdim[z1:z2]
    zind_subset = np.argmin(np.abs(np.array(zdim_subset)-0.0762))+1
    #zind_subset = np.argmin(np.abs(np.array(zdim_subset)-0.125))
    
    if False:
        fig1, axs1 = plt.subplots(1,3)
        axs1[0].plot(xdim_subset)
        axs1[1].plot(ydim_subset)
        axs1[2].plot(zdim_subset)
    

    mesh_materials_subset = mesh_materials[x1:x2,y1:y2,z1:z2,:]
    if True:
        XX2, YY2 = np.meshgrid(xdim_subset,ydim_subset)
        fig2, axs2 = plt.subplots(1,3)
        
        #mesh_materials_subset = mesh_materials
        if mat_type == 0:
            vmin_mat = 0.0
            vmax_mat = None
        elif mat_type == 1:
            vmin_mat = 0.0
            vmax_mat = None
        elif mat_type == 2:
            vmin_mat = 0.0
            vmax_mat = None
        elif mat_type == 3:
            vmin_mat = 0.0
            vmax_mat = None
        else:
            vmin_mat = 0.0
            vmax_mat = 1.0
    
        print('mesh_materials_shape: ', np.shape(mesh_materials_subset))
        pcm = axs2[0].pcolormesh(np.transpose(XX2),np.transpose(YY2),
                                (mesh_materials_subset[:,:,zind_subset,0]),vmin=vmin_mat, vmax=vmax_mat)
        fig2.colorbar(pcm, ax=axs2[0])
        pcm = axs2[1].pcolormesh(np.transpose(XX2),np.transpose(YY2),
                                (mesh_materials_subset[:,:,zind_subset,1]),vmin=vmin_mat, vmax=vmax_mat)
        fig2.colorbar(pcm, ax=axs2[1])
        pcm = axs2[2].pcolormesh(np.transpose(XX2),np.transpose(YY2),
                                (mesh_materials_subset[:,:,zind_subset,2]),vmin=vmin_mat, vmax=vmax_mat)
        fig2.colorbar(pcm, ax=axs2[2])

    if True:
        fig3, axs3 = plt.subplots(1,3)
        axs3[0].plot(mesh_materials_subset[:,yind,zind,0])
        axs3[0].set_ylim(0,const.mu_0)
        axs3[1].plot(mesh_materials_subset[:,yind,zind,1])
        axs3[1].set_ylim(0,const.mu_0)
        axs3[2].plot(mesh_materials_subset[:,yind,zind,2])
        axs3[2].set_ylim(0,const.mu_0)
        

#    fig, axs = plt.subplots(nrows, ncols)
#    ncols = 10
#    nrows = 10    
#    delta_z = max(int(nz/(nrows*ncols+1)), 1)
#    for i in range(ncols):
#        for j in range(nrows):
#            zind += delta_z
#            pcm = axs[i][j].pcolormesh(np.transpose(XX), np.transpose(YY), mesh_materials[:,:,zind,0], linewidth=1, vmin=0, vmax=100)
#            fig.colorbar(pcm, ax=axs[i][j])
#            axs[i][j].grid(True)
    plt.show()

def regrid_material_mesh(mesh_materials, mesh_dim):
    """Convert the linear material mesh data to a (xdim x ydim x zdim x 3) matrix
    Args:
        mesh_materials: 1D array of mesh materials
        mesh_dims: tuple of reported mesh dimensions: (nx, ny, nz)
    Returns:
        re-structured material mesh matrix 
    """
    (nx, ny, nz) = (mesh_dim[0], mesh_dim[1], mesh_dim[2])
    regrid_mat = np.empty((nx, ny, nz, 3))
    # todo: this is slow
    for d in range(3):
        for k in range(nz):
            #print("d= ", d, ", k= ", k)
            for j in range(ny):
                #for i in range(nx):
                mind = nx*j + ny*nx*k + nx*ny*nz*d
                regrid_mat[:,j,k,d] = mesh_materials[mind:mind+nx]
    return regrid_mat

if __name__ == "__main__":
    cst_file = os.path.join('D:\\','workspace','cstmod','test_data',
                                 'Simple_Cosim','Simple_Cosim_1.cst')
    field_result = r'2D/3D Results\H-Field\h-field (f=300) [1]'
    #field_probe(cst_file, field_result)
    materials_probe(cst_file, 3)
