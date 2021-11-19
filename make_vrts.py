import os
import subprocess

def main(**kw):
    yr = kw["this_yr"]:
    var = kw["this_var"]
    thisdir = os.path.join(kw["local_folder"], yr, var)
    files_in_dir = [os.path.join(thisdir, x) for x in os.listdir(thisdir) if f'{yr}_1' in x]
    for fil in files_in_dir:
        make_gdal_warp(fil)
    latlon_files_in_dir = [f'latlon_{x}' for x in files_in_dir]
    vrt_file = os.path.join(thisdir, f'{yr}_{kw["region"]}_{var}.vrt')
    make_gdal_vrt(vrt_file, latlon_files_in_dir)
    return vrt_file

def make_gdal_warp(in_fil, proj='EPSG:4326'):
    result = subprocess.run(['gdalwarp',
                             '-t_srs',
                             proj,
                             in_fil,
                             f'latlon_{in_fil}'], stdout=subprocess.PIPE)

def make_gdal_vrt(in_vrt_file, in_files):
    result = subprocess.run(['gdalbuildvrt',
                             in_vrt_file] + in_files, stdout=subprocess.PIPE)
