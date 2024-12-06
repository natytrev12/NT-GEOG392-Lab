import arcpy
import os
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox."""
        self.label = "Lab6_Toolbox"
        self.alias = "Lab6_Toolbox"
        self.tools = [Lab6_Tool]


class Lab6_Tool(object):
    def __init__(self):
        """Define the tool."""
        self.label = "Lab6_Tool"
        self.description = "Renders Structures and Trees layer with UniqueValueRenderer and GraduatedColorsRenderer."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param_proj_path = arcpy.Parameter(
            displayName="Project Path (.aprx)",
            name="proj_path",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param_layer_name = arcpy.Parameter(
            displayName="Layer Name",
            name="layer_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param_output_path = arcpy.Parameter(
            displayName="Output Project Path (Optional)",
            name="output_path",
            datatype="DEFile",
            parameterType="Optional",
            direction="Output"
        )

        params = [param_proj_path, param_layer_name, param_output_path]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool parameter."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        readTime = 3
        start = 0
        max_val = 100
        step = 25

        arcpy.SetProgressor("step", "Initializing...", start, max_val, step)
        arcpy.AddMessage("Starting tool...")

 
        aprx_file_path = parameters[0].valueAsText
        layer_name = parameters[1].valueAsText
        output_path = parameters[2].valueAsText if parameters[2].value else aprx_file_path.replace(".aprx", "_updated.aprx")

    
        project = arcpy.mp.ArcGISProject(aprx_file_path)
        map_obj = project.listMaps('Map')[0]  # Assuming only one 'Map' exists

        layers = map_obj.listLayers()
        for layer in layers:
            if layer.isFeatureLayer:
                symbology = layer.symbology
                arcpy.SetProgressorPosition(start + step)
                arcpy.SetProgressorLabel("Finding the layers...")
                arcpy.AddMessage(f"Processing layer: {layer.name}")
                time.sleep(readTime)

                if hasattr(symbology, 'renderer') and layer.name == 'Structures':
                    # Apply UniqueValueRenderer to 'Structures'
                    symbology.updateRenderer('UniqueValueRenderer')
                    symbology.renderer.fields = ["Type"]  # Set renderer field
                    layer.symbology = symbology
                    arcpy.SetProgressorPosition(start + 2 * step)
                    arcpy.SetProgressorLabel("Re-rendering Structures layer...")
                    arcpy.AddMessage("Re-rendering Structures layer with UniqueValueRenderer.")
                    time.sleep(readTime)

                elif hasattr(symbology, 'renderer') and layer.name == 'Trees':
                    # Apply GraduatedColorsRenderer to 'Trees'
                    symbology.updateRenderer('GraduatedColorsRenderer')
                    symbology.renderer.classificationField = "Shape_Area"
                    symbology.renderer.breakCount = 5
                    symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
                    layer.symbology = symbology
                    arcpy.SetProgressorPosition(start + 3 * step)
                    arcpy.SetProgressorLabel("Re-rendering Trees layer...")
                    arcpy.AddMessage("Re-rendering Trees layer with GraduatedColorsRenderer.")
                    time.sleep(readTime)

        project.saveACopy(output_path)
        arcpy.SetProgressorPosition(max_val)
        arcpy.SetProgressorLabel("Saving the project...")
        arcpy.AddMessage("Project saved successfully.")
        time.sleep(readTime)

        return


