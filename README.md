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

# Post Aggregator
This is a script that distills the statistics into a form suitable for tiling, keeping the original geojson data and combining it with the statistics data for variables of interest.

# Tippecanoe
Tippecanoe creates vector tiles from a geojson

## Installation Instructions
```sh
$ git clone https://github.com/mapbox/tippecanoe.git
$ cd tippecanoe
$ make -j
$ make install
```

## Upload Tiles
Use the upload\_tiles.sh script to upload the tiles to Azure Blob Storage. Note you will need to have Azure Command Line Installed (az cli), and you will need to populate the script with the appropriate variables, including the storage key.
