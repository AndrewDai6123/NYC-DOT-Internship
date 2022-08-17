import pandas as pd
import geopandas as gpd
from geopandas import GeoSeries, GeoDataFrame
from shapely import wkt

#Read new geocoded CSV file
d = pd.read_csv('output CSV files/accessible-pedestrian-signals-Geo.csv')

#CSV to geoJSON
df = pd.DataFrame(d)
gs = gpd.GeoSeries.from_wkt(df['geometry'])
gdf = gpd.GeoDataFrame(df, geometry=gs, crs="EPSG:4326")
gdf.to_file(filename='output geoJSON files/accessible-pedestrian-signals-Geo.geojson', driver="GeoJSON")