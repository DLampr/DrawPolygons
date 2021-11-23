# Copyright © 2020 Dimitris Lampropoulos
# Licensed under the terms of the MIT License

import os
import csv
import pandas as pd
from shapely.geometry import Point, LineString, Polygon
from shapely import geometry
import geopandas as gpd
from pyproj import CRS

def loadTxts():
    """
    Input: a directory (folder) containing the txts
    Returns a list of the txts in the specified folder.
    """
    directory = input('Enter the folder path of the txts here: ')
    print("Searching for txts in folder...", end="\n\n")

    file_lst = []

    # Iterate through all the files in directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"): 
            file = (os.path.join(directory, filename))
            file_lst.append(file)
    
    return file_lst
    
def check_Txts(file_lst):
    """
    Input: the list of the txts' paths
    Checks if all the coordinates can convert to float and raises ValueError if not
    """
    if len(file_lst) == 0:
        print(f'There are {len(file_lst)} txts in the specified folder. Check again.', end = "\n\n")
    
    else:
        for i in file_lst:
            exampleFile = open(i, encoding='cp1252')
            exampleReader = csv.reader(exampleFile)
            exampleData = list(exampleReader)
            for y in range(len(exampleData)):
                try:
                    exampleData[y][1] = float(exampleData[y][1]) 
                    exampleData[y][2] = float(exampleData[y][2])
                    
                except ValueError as err:
                    print(err.args, end="\n\n")
                    print(f"The error is in the file {i} in row {exampleData[y][0],exampleData[y][1],exampleData[y][2]}")
                    break
        
def DrawPolygons(file_lst):
    """
    Input: the list of the txts' paths
    Writes a shapefile on the specified path and all the Polygons of the txts in it.
    """
    try:        
        poly_lst = []
        outfp = input('Enter the output file path of the .shp file here: ')                    

        for file in file_lst:
                # Read the txts (as csvs) and create pandas DataFrame
                x = pd.read_csv(file, header = None)
                #Create GeoDataFrame from pandas DataFrame with Points(coordinates) as geometry
                gdf = gpd.GeoDataFrame(x, geometry=gpd.points_from_xy(x[1],x[2]))
                # Iterate through all the rows of the GeoDataFrame and append a new list with all the x,y sets of one whole txt
                y = []
                for idx, row in x.iterrows():
                    y.append(row['geometry'])

                # Transform every list of x,y of one polygon to a Polygon and append this polygon to the list of Polygons
                f = Polygon(y)
                poly_lst.append(f)

        # Create the final GeoDataFrame with the list of Polygons as geometry
        newdata = gpd.GeoDataFrame(geometry = poly_lst)

        # Set the GeoDataFrame's coordinate system to GreekGrid (epsg 2100)
        newdata.crs = CRS.from_epsg(2100).to_wkt()

        # Add 'area' and 'file' columns to the final GeoDataFrame
        newdata['area'] = round(newdata.area, 2)
        y = []
        for i in file_lst:
            y.append(i.split(sep = "\\")[-1])
        newdata['file'] = y
        
        # Write the data into that Shapefile
        newdata.to_file(outfp)

        print(f"There were {len(file_lst)} files converted to Polygons.\n\nThe list of files is:")
        for file in file_lst:
            print(file)
        print(f"\nThe output shapefile is:\n{outfp}")

    except ValueError:
        check_Txts(file_lst)
        
def main():
    file_lst = loadTxts()
    DrawPolygons(file_lst)
    
if __name__ == "__main__":
    main()