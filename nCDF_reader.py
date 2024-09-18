##---------------------------------------------------------------------------------
## Working modules to post-process netCDF files (1 of #)
##---------------------------------------------------------------------------------
import os
from netCDF4 import Dataset
import numpy as np

def compile(file_directory):
    """
    Compiles all NetCDF files in the specified directory into a sorted list,
    lists individual file names, and prints the variables and dimensions for a user specified file.

    Args:
        file_directory (str): The path to the directory containing NetCDF files.

    Returns:
        flist: A sorted list of NetCDF file.
    """
    try:
        # Create list of files in the given directory that match the NetCDF extension
        file_extension = '.nc'
        flist = [
            f for f in os.listdir(file_directory)
            if os.path.isfile(os.path.join(file_directory, f))
            and f.endswith(file_extension)
        ]

        # Check for no NetCDF file error
        if not flist:
            print(f"No NetCDF files found in {file_directory}.")
            return []

        # Sort by name
        flist.sort()

        print(f"\n--- Found {len(flist)} NetCDF file(s) ---\n")
        for idx, fname in enumerate(flist, start=1):
            print(f"{idx}.{fname}")

        # Print variables and dimensions in NetCDF file(s) in the directory
        try:

            fnum = 0
            fname = flist[fnum]
            file_path = os.path.join(file_directory, fname)
            fdv = Dataset(file_path, mode = "r")

            print(f"\n--- Dimensions and Variables in {fname} ---")

            print("\n--- Dimensions ---")
            for dim_name, dim in fdv.dimensions.items():
                print(f"{dim_name}: {dim.size}")

            print("\n--- Variables ---")
            for var_name, var in fdv.variables.items():
                print(f"{var_name}: {var.shape}")

        except Exception as e:
            print(f"Error reading file {fname}: {e}")        

        return flist  # Returns sorted list of NetCDF files

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
print("Done reading NetCDF files")
    


