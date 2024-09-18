import os
from nCDF_reader import compile
from nCDF_processor import process
# from nCDF_locations import get_location_data
from nCDF_filters import filter
from nCDF_averages import average_values
from nCDF_plots import visualize
#import mhkit as mhk

def main():
    # Step 1: Set the file directory and list NetCDF files
    file_directory = './Data/'
    flist = compile(file_directory)

    if not flist:
        print("No NetCDF files found. Exiting.")
        return

    # Step 2: Process the NetCDF files to extract necessary data
    lonc, latc, depth_ec, bath_ec = process(file_directory, flist)

    #Step 3: Apply restricting filters
    max_vel = 4 # m/s
    min_depth = 12 #m
    min_clearance = 5 # m
    sites = filter(file_directory,flist,max_vel,min_depth,min_clearance,depth_ec, bath_ec)

    #Step 4: Calculate mean values
    annual_MPD, avg_vel, vel_dir = average_values(file_directory,flist,sites)

    #Step 5: Plot figures
    visualize(lonc,latc,depth_ec,bath_ec,annual_MPD, sites, avg_vel, vel_dir)


if __name__ == "__main__":
    main()
