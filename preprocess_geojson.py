import geopandas as gpd

filename = 'data/Fire_Bounds_US_2017-2018'
newfile = f'{filename}_buffered'
df = gpd.read_file(f'{filename}.geojson')
my_geoms = df['geometry'].buffer(0)
df['geometry'] = my_geoms
df = df[~df['geometry'].isnull()]
df.to_file(f'{newfile}.geojson', driver='GeoJSON')
