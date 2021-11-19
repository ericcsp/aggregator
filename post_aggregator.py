import geopandas as gpd
import geojson
import pandas as pd

class FullStats:
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        self.superslimcols = self.make_slimcols()
        self.geometry = ''

    def make_slimcols(self):
        vartuple = [(k, v) for k, v in self.slim_variable_props.items()] 
        return [f'{x[1]}_{y}_{x[0]}' for y in self.years for x in vartuple] 

    def make_full_gdf(self):
        gdf = {}
        for yr in self.years:
            gdf[yr] = {}
            for var in self.bands.values():
                with open(f'{kw["stats_dir"]}/Stats_{kw["stats_prefix"]}_{yr}_latlon_{var}.geojson', 'r') as fh:
                    gdf[yr][var] = pd.DataFrame(geojson.load(fh))
                    if not self.geometry:
                        self.geometry = gdf[yr][var]['geometry']
                    for prop in self.properties:
                        gdf[yr][var][prop] = [gdf[yr][var]['properties'][x][prop] for x in range(len(gdf[yr][var]))]
                    gdf[yr][var].drop(columns=['properties', 'type', 'geometry'], inplace=True)
        for var in self.bands.values():
            tmp = gdf[self.years[0]][var].copy()
            if len(self.years) > 1:
                for nyr in self.years[1:]:
                    tmp = tmp.join(gdf[nyr][var].set_index('id'), lsuffix='', rsuffix=f'_{nyr}_{var}', on=['id'])
                    tmp = tmp.loc[:,~tmp.columns.duplicated()]
            tmp.rename(columns={x: f'{x}_{self.years[0]}_{var}' for x in self.properties}, inplace=True)
            gdf[var] = tmp.copy()
            del tmp
        self.fullgdf = pd.concat([gdf[var] for var in self.bands.values()], axis=1)
        self.fullgdf = self.fullgdf.loc[:,~self.fullgdf.columns.duplicated()]

    def write_full_gdf(self):
        self.fullgdf.to_json(f'{kw["stats_dir"]}/{kw["stats_prefix"]}_{kw["region"]}_Statistics_nogeom.json')

    def make_slim_db(self):
        self.slim_db = self.fullgdf[self.superslimcols]
        for col in self.slim_db.columns:
            if 'biomass' in col:
                self.slim_db[col] /= 1000
            self.slim_db[col] = [int(x) if x == x else 0 for x in self.slim_db[col]]

    def write_slim_db(self):
        self.slim_db.to_json(f'{kw["stats_dir"]}/{kw["stats_prefix"]}_{kw["region"]}_Statistics_slim.json')

    def add_geo_to_slim(self):
        self.slim_db['geometry'] = self.geometry

    def write_slim_db_geo(self):
        if 'geometry' in self.slim_db.columns:
            gpd.GeoDataFrame(self.slim_db).to_file('{kw["stats_dir"]}/{kw["stats_prefix"]}_{kw["region"]}_Statistics_slim_withgeo.geojson', driver='GeoJSON')
        else:
            print('geometry not found in slim_db, unable to write GeoDataFrame to GeoJSON')

    def load_original_geojson(self):
        self.original = gpd.read_file(kw["buffered_geojson"])
        self.original.drop(columns='geometry', inplace=True)

    def concat_slim_to_original(self):
        for col in self.slim_db.columns:
            self.original[col] = self.slim_db[col]

    def write_final_geojson(self):
        kw["tiles_dir"] = f'{kw["stats_dir"]}/{kw["stats_prefix"]}_{kw["region"]}_Statistics_{kw["geojson_appendix"]}'
        gpd.GeoDataFrame(self.original).to_file('{kw["tiles_dir"]}.geojson', driver='GeoJSON')
        return kw

def main(**kw):
    my_stats = FullStats(**kw)
    my_stats.make_full_gdf()
    my_stats.make_slim_db()
    my_stats.add_geo_to_slim()
    my_stats.load_original_geojson()
    my_stats.concat_slim_to_original()
    return my_stats.write_final_geojson()
