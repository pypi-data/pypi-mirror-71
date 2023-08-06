#!/bin/bash

vortexfitting -i data/example_Ub_planeZ_0.01.raw -ft openfoam -o results/example_openfoam -rmax 0

vortexfitting -i data/example_Ub_planeZ_0.01.raw -ft openfoam -xy 20 50

vortexfitting -i data/example_adim_vel_{:06d}.dat -ft piv_tecplot -o results/example_adim_vel_000010 -first 10 -t 5 -b 20

vortexfitting -i data/example_dataHIT.nc -ft dns -o results/example_dataHIT 

vortexfitting -i data/example_dataPIV.nc -ft piv_netcdf -o results/example_dataPIV -t 1.5

vortexfitting -i data/example_dim_vel_{:06d}.dat -ft piv_tecplot -o results/example_dim_vel_000010 -first 10 -mf data/example_mean.dat -t 50 -rmax 2

vortexfitting -i data/example_adim_vel_{:06d}.dat -ft piv_tecplot -o results/example_adim_vel_000010 -first 10 -last 10 -t 5  

vortexfitting -i data/example_vel_{:06d}.dat -ft piv_tecplot -o results/example_temporal_series -mf data/example_mean.dat -first 5 -last 6 -t 50 -ct 0.5  

