from rasterstats import zonal_stats
import geojson

class Stats:
    def __init__(self, shapefile, tifname, statsfile):
        self.shapefile = shapefile
        self.tifname = tifname 
        self.statsfile = statsfile

    def make_vector_summary(self):
        self.stats = zonal_stats(self.shapefile, self.tifname, geojson_out=True)
        with open(self.statsfile, 'w') as fh:
            geojson.dump(self.stats, fh)

    def main(self):
        self.make_vector_summary()

def main(input):
    tifname = f'{input}_remapped.tif'
    shapefile = '/data/placer/shp/AOI'
    statsfile = f'{input}_stats'
    my_stats = Stats(shapefile, tifname, statsfile) 
    my_stats.main()
    return my_stats

if __name__ == "__main__":
    main('2005_ba')
