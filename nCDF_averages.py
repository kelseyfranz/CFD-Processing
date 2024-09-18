##---------------------------------------------------------------------------------
## Working modules to read and pull from netCDF files (3 of #)
##---------------------------------------------------------------------------------

import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import os


def average_values(file_directory, flist, sites):
    """
    Calculates the annual depth-averaged power density for the entire domain and saves the results to an Excel file.

    Args:
        file_directory (str): Path to the directory containing NetCDF files.
        flist (list): List of NetCDF file names.
        sites (np.ndarray): Binary grid to implement filter.
    
    Returns:
        
    """
    try:
        # Initialize variables
        elements = np.sum(sites,axis=1) #array of number of bins used in averages
        elements[elements == 0.0] = np.nan # to get rid of no divide by 0 error
        annual_MPD = np.zeros((sites.shape[0]), dtype=np.float64)
        count = 0  # count total number of file records

        # # Process each file
        for f in flist[0:10]:  # Use the first 10 day files for testing
            print(f"Processing file: {f}")

            count = count + 1

            # Open NetCDF file
            fname = Dataset(file_directory + f, mode='r')

            # Read velocity components
            u = np.array(fname['u']).astype(np.float64).transpose()*sites[:,:,np.newaxis] # Read u(east) within filtered domain
            v = np.array(fname['v']).astype(np.float64).transpose()*sites[:,:,np.newaxis] # Read v(north) within filtered domain

            #need to adjust, make sure averaging correctly
            vel = np.sqrt(np.square(u)+np.square(v)) #filtered velocity magnitude
            depth_vel_avg = np.sum(vel,axis=1)/elements[:,np.newaxis] #depth averaged velocity magnitude
            avg_vel = np.average(depth_vel_avg,axis=1) #get daily average

            #depth averaged flow direction
            ## revist: do we want at each viable site? depth averaged? daily average?
            vel_dir = np.arctan(v,u)
            vel_dir = np.sum(vel_dir,axis=1)/elements[:,np.newaxis]

            #Calculate over how many days (files)
            daily_MPD = 0.5 * 1025.0 * np.power(avg_vel,3) / 1000 #daily avg mean power density
            annual_MPD = np.add(annual_MPD,daily_MPD)/count #will be annual when all data processed

            fname.close()

            ##can probably add quite a few more calculations into here
            #might want to compile into a dataframe with all the wanted information

        return annual_MPD, avg_vel, vel_dir  # Return data for further analysis
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None
