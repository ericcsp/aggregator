import geopandas as gpd

def main(already_buffered=False, **kw):
    filename = kw["geojson_file"]
    if not already_buffered:
        newfile = f'{filename}_buffered'
        df = gpd.read_file(f'{filename}.geojson')
        my_geoms = df['geometry'].buffer(0)
        df['geometry'] = my_geoms
        df = df[~df['geometry'].isnull()]
        kw["buffered_geojson"] = f'{newfile}.geojson'
        df.to_file(kw["buffered_geojson"], driver='GeoJSON')
    else:
        kw["buffered_geojson"] = f'{filename}.geojson'
    return kw
