import subprocess

def main(**kw):
    result = subprocess.run(['tippecanoe', '-pk', '-e', tile_file, '-z', '14', '-ae', '-l', kw["tile_file"], f'{kw["tile_file"]}.geojson'], stdout=subprocess.PIPE)
