import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Lab5_Toolbox"
        self.alias = "Lab5_Toolbox"

        self.tools = [Lab5_Tool]


class Lab5_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Lab5_Tool"
        self.description = "This tool creates a buffer around a selected garage."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        param_GDB_folder = arcpy.Parameter(
            displayName="GDB Folder",
            name="gdbfolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )

        param_GDB_Name = arcpy.Parameter(
            displayName="GDB Name",
            name="gdbname",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param_Garage_CSV_File = arcpy.Parameter(
            displayName="Garage CSV File",
            name="garage_csv_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        param_Campus_GDB = arcpy.Parameter(
            displayName="Campus GDB",
            name="campus_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        param_Selected_Garage_Name = arcpy.Parameter(
            displayName="Selected Garage Name",
            name="selected_garage_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        param_Buffer_Radius = arcpy.Parameter(
            displayName="Buffer Radius",
            name="buffer_radius",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )

        params = [
            param_GDB_folder,
            param_GDB_Name,
            param_Garage_CSV_File,
            param_Campus_GDB,
            param_Selected_Garage_Name,
            param_Buffer_Radius
        ]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal validation is performed.
        This method is called whenever a parameter has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter.
        This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        GDB_Folder = parameters[0].valueAsText
        GDB_Name = parameters[1].valueAsText
        Garage_CSV_File = parameters[2].valueAsText
        Campus_GDB = parameters[3].valueAsText
        Selected_Garage_Name = parameters[4].valueAsText
        Buffer_Radius = parameters[5].valueAsText

        arcpy.AddMessage("User Input:")
        arcpy.AddMessage(f"GDB Folder: {GDB_Folder}")
        arcpy.AddMessage(f"GDB Name: {GDB_Name}")
        arcpy.AddMessage(f"Garage CSV File: {Garage_CSV_File}")
        arcpy.AddMessage(f"Campus GDB: {Campus_GDB}")
        arcpy.AddMessage(f"Selected Garage Name: {Selected_Garage_Name}")
        arcpy.AddMessage(f"Buffer Radius: {Buffer_Radius}")

        GDB_Full_Path = os.path.join(GDB_Folder, GDB_Name)
        if not arcpy.Exists(GDB_Full_Path):
            arcpy.management.CreateFileGDB(GDB_Folder, GDB_Name)

        garages_layer = os.path.join(GDB_Full_Path, "garages_layer")

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
            arcpy.AddError(f"Error: CSV file not found at {Garage_CSV_File}")
            return

        garage_points_layer = os.path.join(Campus_GDB, "GaragePoints")
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

            arcpy.AddMessage("Success: Buffer and clip completed.")
        else:
            arcpy.AddError("Error: Could not find the garage name you entered.")

        return




