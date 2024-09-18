import numpy as np
import pandas as pd
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import os

##plotting various 

def visualize(lonc,latc,depth_ec,bath_ec,annual_MPD, sites, avg_vel, vel_dir):
    try:

        ##Plot 1 - bathymetry of element centers/viable locations
        # plt.figure(figsize=(10,6))
        # bathymetry = plt.contourf(lonc,latc,bath_ec)
        # cbar = plt.colorbar(bathymetry)
        # cbar.set_label('Depth [m]')
        # plt.title("Bathymetry ([m], MSL)")
        # plt.xlabel('Longitude')
        # plt.ylabel('Latitude')

        #plt.savefig('Bathymetry.png',format='png',dpi=240)

        plt.show()

        ##plot 2 - average velocity/viable locations

        ##plot 3 - annual mean power density/viable locations

        ##plot 4 - rose diagram of velocity direction (for what locations?)

        ##....any other plots
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None