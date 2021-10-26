from rasterstats import zonal_stats
import geojson

class Stats:
    def __init__(self, shapefile, tifname, statsfile):
        self.shapefile = shapefile
        self.tifname = tifname 
        self.statsfile = statsfile
        self.mystats = ["std", "count", "mean", "median", "percentile_10", "percentile_90", "min", "max", "sum"]

    def make_vector_summary(self):
        self.stats = zonal_stats(self.shapefile, self.tifname, stats=self.mystats, geojson_out=True)
        with open(self.statsfile, 'w') as fh:
            geojson.dump(self.stats, fh)

    def main(self):
        self.make_vector_summary()

def main(yr, var, region):
    tifname = f'/big/hls_output_2021-05-13/{yr}/{var}/{yr}_latlon_{var}.vrt'
    shapefile = f'/home/cspadmin/data/buffer0.geojson'
    statsfile = f'New_Fire_{yr}_{region}_{var}.geojson'
    my_stats = Stats(shapefile, tifname, statsfile) 
    my_stats.main()
    return my_stats

if __name__ == "__main__":
    my_region = 'conuslatlon'
    for my_yr in [2016, 2018]:
        for my_var in ['biomass', 'basalarea', 'canopycover']:
            main(my_yr, my_var, my_region)
