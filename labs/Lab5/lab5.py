import arcpy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Campus_GDB = os.path.join(BASE_DIR, "Lab5_data", "Campus.gdb")
Garage_CSV_File = r"C:\Users\natyt\NT-GEOG392-Lab\labs\Lab5\Lab5_data\garages.csv"  # Updated to use a raw string

GDB_Folder = input("Enter the GDB Folder Path: ")
GDB_Name = input("Enter the GDB Name (e.g., Lab5.gdb): ")
Selected_Garage_Name = input("Enter the Garage Name to Select: ")
Buffer_Radius = input("Enter the Buffer Radius (e.g., '150 meters'): ")

GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)
if not arcpy.Exists(GDB_Full_Path):
    arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)

garages_layer = os.path.join(GDB_Full_Path, "garages")

if os.path.exists(Garage_CSV_File):
    arcpy.management.MakeXYEventLayer(
        Garage_CSV_File,
        "X",  # X coordinate field
        "Y",  # Y coordinate field
        "garage_points_layer",
        arcpy.SpatialReference(4326)
    )
    arcpy.management.CopyFeatures("garage_points_layer", garages_layer)
else:
    print(f"Error: CSV file not found at {Garage_CSV_File}")

garage_points_layer = os.path.join(GDB_Full_Path, "garages")
where_clause = f"LotName = '{Selected_Garage_Name}'"
cursor = arcpy.da.SearchCursor(garage_points_layer, ["LotName"], where_clause)

shouldProceed = False
for row in cursor:
    if Selected_Garage_Name in row:
        shouldProceed = True
        break

if shouldProceed:
    
    selected_garage_layer = os.path.join(GDB_Full_Path, "selected_garage")
    arcpy.analysis.Select(garage_points_layer, selected_garage_layer, where_clause)

    buffered_garage = os.path.join(GDB_Full_Path, "garage_buffered")
    arcpy.analysis.Buffer(selected_garage_layer, buffered_garage, Buffer_Radius)

    structures_layer = os.path.join(Campus_GDB, "Structures")

    clipped_structures = os.path.join(GDB_Full_Path, "structures_clipped")
    arcpy.analysis.Clip(structures_layer, buffered_garage, clipped_structures)

    print("Success: Buffer and clip completed.")
else:
    print("Error: Could not find the garage name you entered.")

