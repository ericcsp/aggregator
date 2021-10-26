# Aggregator
Repository to calculate statistics of a raster array within one or more geographic vector layers, using the rasterstats package.

## Requirements
The rasterstats and geojson packages for Python, a raster array, and a shapefile of vector layers.

## Statistics Generated
The statistics generated are in the Stats class attribute `mystats`, and are currently as follows:
- mean
- std
- median
- count
- percentile\_10
- percentile\_90
- min
- max
- sum

Note that these can be adjusted as necessary.

## Notes
As it stands, the values are hardcoded to the locations of the raster array `tifname`, the shapefile `shapefile`, and the output statistics file `statsfile`. These can be adjusted as necessary in a branch for your needs.
