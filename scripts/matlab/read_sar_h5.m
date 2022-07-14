% load complex field data from hdf5 file exported with CST
% The HDF5 h5dump utility lists all the available fields in a given hdf5 file.
% h5dump --header file.h5

h5file = 'SAR (f=297) [AC1] (Point).h5'; key='/SAR';
%h5file = 'e-field (f=45.6) [AC1].h5'; key='/E-Field';


% read x, y, and z export mesh data
xdim = h5read(h5file, '/Mesh line x');
ydim = h5read(h5file, '/Mesh line y');
zdim = h5read(h5file, '/Mesh line z');

% units are hdf5 'attributes' and read with h5readatt
% units are null terminated strings
xunit = strsplit(h5readatt(h5file, '/Mesh line x','unit'),'\0');
disp(strcat('physical units: ', xunit(1)));

field_shape = [length(xdim), length(ydim), length(zdim)];

% read SAR data from h5 into struct
data = h5read(h5file, key);
data_units = strsplit(h5readatt(h5file, key, 'unit'),'\0');
display(strcat('SAR units: ', data_units(1)));

% collapse struct to complex b1+ matrix
%b1p = field.z.re + i*field.z.im;  % complex field
save('sar_point.mat', 'data');

% plotting
% |F|

% plot the results
zval = 0;  % z position to plot
[zc, zi] = min(abs(zdim - zval));  % index of z_val

[X,Y] = meshgrid(xdim, ydim);

h = pcolor(X', Y', data(:,:,zi));
set(h, 'EdgeColor', 'none');
title(strcat("Field Magnitude: (", data_units(1), ')'))
colorbar
