##-----------------------------------------------------------------------------
## Working modules to read and pull from netCDF files (2 of #)
##---------------------------------------------------------------------------------

import numpy as np
from netCDF4 import Dataset
import pandas as pd

def process(file_directory, flist):
    """
    Processes the specified file in the given list of NetCDF files to extract variables longitude, latitude, 
    and depth at element centers, and returns array, assuming all files the same mesh.

    Args:
        file_directory (str): Path to the directory containing NetCDF files.
        flist (list): List of NetCDF file names.

    Returns:
        tuple: Four numpy arrays for the longitude, latitude, depth of element centers.
    """
    try:

        # Pull information from first NetCDF file
        f = flist[0]
        file_path = file_directory + f
        print(f"---Pulling spacial information from {f}---")

        # Read in node, element center, and sigma layers location information
        loc = Dataset(file_path, mode='r') # Open the NetCDF file

        lon = np.array(loc['lon']) - 360.0  # longitude for each node
        lat = np.array(loc['lat'])  # latitude for each node
        h = np.array(loc['h'])      # bathymetry for each node

        lonc = np.array(loc['lonc']) - 360.0  # longitude for each element center
        latc = np.array(loc['latc'])  # latitude for each element center

        nv = np.array(loc['nv']).transpose()  # node connectivity info, 3 nodes per element

        sig_lay = -1*np.array(loc['siglay']).transpose()/10.0 #sigma layer information (sigma layers (20 layers at 7907 nodes))
            ###error -- should add to 1, adding to 10 for some reason, interm fix to divide by 10, -1 to be positive       
        sig_lev = np.array(loc['siglev']).transpose() #sigma levels, where nodes are 
        
        # Calculate depth of nodes and element centers through water column
        depth_n = sig_lev*h[:,np.newaxis] #array of all depths for each node through sigma levels
        depth_ec = -1* (depth_n[nv[:,0] - 1] + depth_n[nv[:,1] - 1] + depth_n[nv[:,2] - 1]) / 3.0 # not adjusted for surface elevation (MSL)
        depth_ec = (depth_ec[:,:-1] + depth_ec[:,1:])/2 #midpoint between sigma layers (should be midpoint of sigma layers??)

        bath_ec = (h[nv[:, 0] - 1] + h[nv[:, 1] - 1] + h[nv[:, 2] - 1]) / 3.0 # Calculate bathymetry of element centers (total depth)
    
        if len(lonc)!=len(latc)!=len(depth_ec[:]!=len(bath_ec)):
            print(f"Spatial dimensions error for file: {f}")

        return lonc, latc, depth_ec, bath_ec

    except Exception as e:
        print(f"An error occurred while processing the files: {e}")
        return None, None, None