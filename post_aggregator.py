import geopandas as gpd
import geojson
import pandas as pd

config = {}
config['properties'] = ['min', 'max', 'mean', 'std', 'sum']
config['years'] = [2016,2018]
config['variables'] = ['biomass', 'basalarea', 'canopycover']
config['slim_variable_props'] = ['sum', 'mean', 'mean']

class FullStats:
    def __init__(self, cfg):
        for k, v in cfg.items():
            setattr(self, k, v)
        self.superslimcols = self.make_slimcols()

    def make_slimcols(self):
        vartuple = [(v, p) for v, p in zip(self.variables, self.slim_variable_props)] 
        return [f'{x[1]}_{y}_{x[0]}' for y in self.years for x in vartuple] 

    def make_full_gdf(self):
        gdf = {}
        for yr in self.years:
            gdf[yr] = {}
            for var in self.variables:
                with open(f'aggregator/New_Fire_{yr}_conuslatlon_{var}.geojson', 'r') as fh:
                    gdf[yr][var] = pd.DataFrame(geojson.load(fh))
                    if yr == self.years[0] and self.variables[0] in var:
                        self.geometry = gdf[yr][var]['geometry']
                    for prop in self.properties:
                        gdf[yr][var][prop] = [gdf[yr][var]['properties'][x][prop] for x in range(len(gdf[yr][var]))]
                    gdf[yr][var].drop(columns=['properties', 'type', 'geometry'], inplace=True)
        for var in self.variables:
            gdf[var] = gdf[2016][var].join(gdf[2018][var].set_index('id'), lsuffix=f'_2016_{var}', rsuffix=f'_2018_{var}', on=['id'])
        self.fullgdf = pd.concat([gdf[var] for var in self.variables], axis=1)
        self.fullgdf = self.fullgdf.loc[:,~self.fullgdf.columns.duplicated()]

    def write_full_gdf(self):
        self.fullgdf.to_json(f'data/Fire_Region_Statistics_nogeom2.json')

    def make_slim_db(self):
        self.slim_db = self.fullgdf[self.superslimcols]
        for col in self.slim_db.columns:
            if 'biomass' in col:
                self.slim_db[col] /= 1000
            self.slim_db[col] = [int(x) if x == x else 0 for x in self.slim_db[col]]

    def write_slim_db(self):
        self.slim_db.to_json(f'data/Fire_Region_Statistics_slim.json')

    def add_geo_to_slim(self):
        self.slim_db['geometry'] = self.geometry

    def write_slim_db_geo(self):
        if 'geometry' in self.slim_db.columns:
            gpd.GeoDataFrame(self.slim_db).to_file('data/Fire_Region_Statistics_slim_withgeo.geojson', driver='GeoJSON')
        else:
            print('geometry not found in slim_db, unable to write GeoDataFrame to GeoJSON')

    def load_original_geojson(self):
        self.original = gpd.read_file('data/buffer0.geojson')
        self.original.drop(columns='geometry', inplace=True)

    def concat_slim_to_original(self):
        for col in self.slim_db.columns:
            self.original[col] = self.slim_db[col]

    def write_final_geojson(self):
        gpd.GeoDataFrame(self.original).to_file('data/Fire_Region_Statistics_viascript.geojson', driver='GeoJSON')

def main():
    my_stats = FullStats(config)
    my_stats.make_full_gdf()
    my_stats.make_slim_db()
    my_stats.add_geo_to_slim()
    my_stats.load_original_geojson()
    my_stats.concat_slim_to_original()
    my_stats.write_final_geojson()
