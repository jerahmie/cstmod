"""plot_3d_fields.py

Plot field results form hdf5 file.
"""
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from cstmod.field_reader import FieldReaderCST2019

def plot_results(axs, data):
    """
    Args: 
        axs - figure axes
        data - data to plot
    """
    pass

if __name__ == "__main__":
    result_files = [os.path.join('D:\\','Temp_CST','field3d.hdf5'), 
                    os.path.join('D:\\','workspace','cstmod','test_data',
                                 'Simple_Cosim','Simple_Cosim','Export','3d',
                                 'h-field (f=63.65) [1].h5')]
    for f in result_files:
        print(f + ': ' , os.path.exists(f))

    z0 = 76.2
    with h5py.File(result_files[0],'r') as dataf0:
        xdim0 = dataf0['Mesh line x'][()]
        ydim0 = dataf0['Mesh line y'][()]
        zdim0 = dataf0['Mesh line z'][()]
        zind0 = np.argmin(abs(zdim0-z0))
        fxre0 = dataf0['H-Field']['x']['re']
        fxim0 = dataf0['H-Field']['x']['im']
        fyre0 = dataf0['H-Field']['y']['re']
        fyim0 = dataf0['H-Field']['y']['im']
        fzre0 = dataf0['H-Field']['z']['re']
        fzim0 = dataf0['H-Field']['z']['im']

    with h5py.File(result_files[1],'r') as dataf1:
        xdim1 = dataf1['Mesh line x'][()]
        ydim1 = dataf1['Mesh line y'][()]
        zdim1 = dataf1['Mesh line z'][()]
        zind1 = np.argmin(abs(zdim1-z0))
        print('zind1: ', zind1)
        fxre1 = np.transpose(dataf1['H-Field']['x']['re'], (2,1,0))
        fxim1 = np.transpose(dataf1['H-Field']['x']['im'], (2,1,0))
        fyre1 = np.transpose(dataf1['H-Field']['y']['re'], (2,1,0))
        fyim1 = np.transpose(dataf1['H-Field']['y']['im'], (2,1,0))
        fzre1 = np.transpose(dataf1['H-Field']['z']['re'], (2,1,0))
        fzim1 = np.transpose(dataf1['H-Field']['z']['im'], (2,1,0))
        fabs1 = np.sqrt(np.abs(np.multiply(fxre1, np.conj(fxim1)) + 
                        np.multiply(fyre1, np.conj(fyim1)) +
                        np.multiply(fzre1, np.conj(fzim1))))
    fig, axs = plt.subplots(1,2)
    pc0 = axs[0].pcolormesh(fxre0[:,:,zind0])
    axs[0].set_aspect('equal','box')
    fig.colorbar(pc0, ax=axs[0])
    pcm = axs[1].pcolormesh(fxre1[:,:,zind1],vmin=0, vmax=0.5)
    axs[1].set_aspect('equal','box')
    fig.colorbar(pcm, ax=axs[1])
    plt.show()