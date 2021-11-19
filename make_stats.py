from rasterstats import zonal_stats
import geojson

class Stats:
    def __init__(self, shapefile, tifname, statsfile, **kw):
        self.shapefile = shapefile
        self.tifname = tifname 
        self.statsfile = statsfile
        self.mystats = kw["properties"]

    def make_vector_summary(self):
        self.stats = zonal_stats(self.shapefile, self.tifname, stats=self.mystats, geojson_out=True)
        with open(self.statsfile, 'w') as fh:
            geojson.dump(self.stats, fh)

    def main(self):
        self.make_vector_summary()

def main(vrt_file, **kw):
    yr = kw["this_yr"]
    var = kw["this_var"]
    tifname = vrt_file
    shapefile = kw["buffered_geojson"]
    statsfile = f'{kw["stats_dir"]}/Stats_{kw["stats_prefix"]}_{yr}_{kw["region"]}_{var}.geojson'
    my_stats = Stats(shapefile, tifname, statsfile, **kw) 
    my_stats.main()
    return my_stats
