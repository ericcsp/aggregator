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

def main(input):
    tifname = f'/home/cspadmin/data/{input}.tif'
    shapefile = '/home/cspadmin/data/PLACER_fire_bounds_2016_2018.geojson'
    statsfile = f'{input}_stats.geojson'
    my_stats = Stats(shapefile, tifname, statsfile) 
    my_stats.main()
    return my_stats

if __name__ == "__main__":
    main('2005_ba')
