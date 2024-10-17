import os
import geopandas as gpd

#Set up directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = BASE_DIR

# Define CensusTract class
class CensusTract:
    def __init__(self, geoid, population, geometry):
        self.geoid = geoid
        self.population = population
        self.geometry = geometry

    def calculate_population_density(self):
        """
        """
        area = self.geometry.area 
        if area > 0:  
            population_density = self.population / area
        else:
            population_density = 0
        return population_density

if __name__ == "__main__":
    file_path = os.path.join(DATA_DIR, 'data.geojson')
    #Load data into GeoDataFrame
    gdf = gpd.read_file(file_path)

    print(gdf.head())
    print(gdf.columns)
    print(gdf.shape)
    print(gdf.dtypes)

    #Calculation of Population Density using apply and lambda
    def calculate_density(row):
        
        tract = CensusTract(
            geoid=row['GeoId'],
            population=row['Pop'],
            geometry=row['geometry']
        )
        return tract.calculate_population_density()

    #Apply the function to calculate the population density for each row
    gdf['Pop_Den_new'] = gdf.apply(lambda row: calculate_density(row), axis=1)

    print(gdf.head())






