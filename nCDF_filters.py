import numpy as np
import pandas as pd
from nCDF_processor import process
from netCDF4 import Dataset


def filter(file_directory, flist, max_vel, min_depth, min_clearance, depth_ec,bath_ec):
    
    """
    Filter out locations based on specified limiations, specifically the maximum velocity (magnitude),
    minimum depth, and maximum depth

    Args:
        file_directory (str): Path to the directory containing NetCDF files.
        flist (list): List of NetCDF file names.
        max_vel (float): Maximum velocity magnitude allowed by technology
        min_depth (float): Minimum depth from water surafce in meters
        min_clearance (float): Minimum distance from inlet floor in meters
        depth_ec (np.array): Array of depths of element centers through water column
        bath_ec (np.array): array of bathymetry for each element center

    Returns:
        --->list of locations meeting criteria that we can apply to datasets

    """

    # Define locations within depth limitations
    depth_ec[depth_ec < min_depth] = 0.0 #remove too shallow areas
    depth_ec[np.abs(bath_ec[:,np.newaxis] - depth_ec) < min_clearance] = 0.0 #remove areas too close to bottom
    allowed_depths = np.where(depth_ec > 0, 1.0, 0.0)

    try:
        #Load file and relevant variables
        for f in flist:
            print(f"---Applying filters on {f}---")
            
            file_path = file_directory+f
            fname = Dataset(file_path, mode = "r")

            #Load velocities and apply depth filter   
            u = np.array(fname.variables['u']).astype(np.float64).transpose()
            v = np.array(fname.variables['v']).astype(np.float64).transpose()
            vel = np.sqrt(np.square(u)+np.square(v)) #2D velocity magnitude (no vertical vector??)

            # Create 2D matrix of locations under maximum velocity
            allowable_vel = np.ones(allowed_depths.shape) #initialize np array to match depths array
            for i in range(vel.shape[2]): #goes through 96 time intervals

                vel_time = vel[:,:,i] #creates 2D array

                vel_fil = np.where(vel_time >= max_vel, 0.0, 1.0) #sets vel boundary

                if np.all(vel_fil == 0.0): #error check incase of all zeros time step
                    print(f"Time step {i} has all zeros, skipping")
                    continue

                allowable_vel = np.multiply(allowable_vel,vel_fil) #multiplies all time steps to get master matrix
            
            allowable_vel=allowable_vel*allowable_vel #multiply across multiple days

        sites = np.multiply(allowable_vel,allowed_depths) #get full domain of elements that meet criteria
        if np.all(sites == 0):
            print("No viable sites")

        return sites        

    except Exception as e:
        print(f"An error occurred while processing the files: {e}")
        return None, None, None

