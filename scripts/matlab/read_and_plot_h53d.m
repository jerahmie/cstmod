% load 3 component (fx, fy, fz) field data from hdf5 file exported with CST
% The HDF5 h5dump utility lists all the available fields in a given hdf5 file.
% h5dump --header file.h5

h5file = 'h-field (f=) [AC1].h5'; key='/H-Field';
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

% read h data from h5 into struct
field = h5read(h5file, key);
field_units = strsplit(h5readatt(h5file, key, 'unit'),'\0');
display(strcat('field units: ', field_units(1)));

% collapse struct to complex b1+ matrix
b1px = field.x.re + i*field.x.im;  % x component
b1py = field.y.re + i*field.y.im;  % y component
b1pz = field.z.re + i*field.z.im;  % z component

save('b1plus.mat', b1px, b1py, b1pz);

% plotting
% |F|
b1pmag = sqrt(fx.*conj(fx) + fy.*conj(fy) + fz.*conj(fz));


% plot the results
zval = 0;  % z position to plot
[zc, zi] = min(abs(zdim - zval));  % index of z_val

[X,Y] = meshgrid(xdim, ydim);

h = pcolor(X', Y', abs(fmag(:,:,zi)));
set(h, 'EdgeColor', 'none');
title(strcat("Field Magnitude: (", field_units(1), ')'))
colorbar
