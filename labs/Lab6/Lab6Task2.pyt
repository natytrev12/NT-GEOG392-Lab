import arcpy
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Lab6_Toolbox"
        self.alias = "Lab6_Toolbox"
        # Add the tools to the toolbox
        self.tools = [Lab6Task2_Tool]

class Lab6Task2_Tool(object):
    def __init__(self):
        """Define the tool for Task 2."""
        self.label = "Lab6_Task2_Tool"
        self.description = "Perform buffer analysis for Task 2"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions."""
        param_input_features = arcpy.Parameter(
            displayName="Input Features",
            name="input_features",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        param_buffer_distance = arcpy.Parameter(
            displayName="Buffer Distance",
            name="buffer_distance",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_output_path = arcpy.Parameter(
            displayName="Output Path",
            name="output_path",
            datatype="DEFolder",
            parameterType="Required",
            direction="Output"
        )
        return [param_input_features, param_buffer_distance, param_output_path]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def execute(self, parameters, messages):
        """Execute the analysis."""
        input_features = parameters[0].valueAsText
        buffer_distance = parameters[1].valueAsText
        output_path = parameters[2].valueAsText
        
        # Create a buffer
        arcpy.AddMessage(f"Creating buffer around {input_features} with distance {buffer_distance}...")
        buffer_output = os.path.join(output_path, "buffer_output.shp")
        arcpy.analysis.Buffer(input_features, buffer_output, buffer_distance)

        arcpy.AddMessage(f"Buffer created successfully at: {buffer_output}")

        return
