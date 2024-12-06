import arcpy
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


INPUT_DB_PATH = os.path.join(BASE_DIR, "Lab4_Data", "Campus.gdb")
CSV_PATH = os.path.join(BASE_DIR, "Lab4_Data", "garages.csv")
OUTPUT_DB_PATH = os.path.join(BASE_DIR, "Lab4_Data", "Campus_Output.gdb")

# Set the workspace to the input geodatabase
arcpy.env.workspace = INPUT_DB_PATH


if not arcpy.Exists(OUTPUT_DB_PATH):
    arcpy.management.CreateFileGDB(os.path.dirname(OUTPUT_DB_PATH), os.path.basename(OUTPUT_DB_PATH))

# Load the CSV file and create a point feature class
csv_feature_class = os.path.join(OUTPUT_DB_PATH, 'garage_points')
arcpy.management.XYTableToPoint(
    CSV_PATH, csv_feature_class, "X", "Y", coordinate_system=arcpy.SpatialReference(4326)
)


print("Before Re-Projection...")
print(f"Garage Points Layer spatial reference: {arcpy.Describe(csv_feature_class).spatialReference.name}")


reprojected_garages = os.path.join(OUTPUT_DB_PATH, "GaragePoints_Reprojected")
target_ref = arcpy.SpatialReference("NAD 1983 StatePlane Texas Central FIPS 4203 (US Feet)")
arcpy.management.Project(
    csv_feature_class, reprojected_garages, target_ref
)

# Buffer analysis on the garage points
buffered_garages = os.path.join(OUTPUT_DB_PATH, "Garage_Buffer_150m")
arcpy.analysis.Buffer(reprojected_garages, buffered_garages, "150 meters")


structures_layer = os.path.join(INPUT_DB_PATH, "Structures")
intersected_layer = os.path.join(OUTPUT_DB_PATH, "Garage_Structures_Intersect")
arcpy.analysis.Intersect([buffered_garages, structures_layer], intersected_layer)

# Export layers to output GDB
arcpy.management.CopyFeatures(reprojected_garages, os.path.join(OUTPUT_DB_PATH, "garage_layer"))
arcpy.management.CopyFeatures(structures_layer, os.path.join(OUTPUT_DB_PATH, "structure_layer"))
arcpy.management.CopyFeatures(buffered_garages, os.path.join(OUTPUT_DB_PATH, "buffered_layer"))
arcpy.management.CopyFeatures(intersected_layer, os.path.join(OUTPUT_DB_PATH, "intersected_layer"))

print("Lab 4 completed successfully.")

