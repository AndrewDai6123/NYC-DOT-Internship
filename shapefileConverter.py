import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
from shapely import wkt

#Read new geocoded CSV file
d = pd.read_csv('output CSV files/accessible-pedestrian-signals-Geo.csv')

#CSV geometry types to shapefile
df = pd.DataFrame(d)
gs = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry=gs, crs="EPSG:4326")

#separating the different geometry types
gdfPoints = gdf.loc[gdf.geometry.type == "Point"]
gdfLineString = gdf.loc[gdf.geometry.type == "LineString"]

#creating shapefile for different geometry types
gdfPoints.to_file(filename='output shapefiles/accessible-pedestrian-signals-Geo-Points.shp', driver="ESRI Shapefile")
gdfLineString.to_file(filename='output shapefiles/accessible-pedestrian-signals-Geo-LineString.shp', driver="ESRI Shapefile")