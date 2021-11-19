import yaml
import buffer_geojson
import get_hls
import make_vrts
import make_stats
import post_aggregator
import make_tippecanoe_tiles
import upload_tiles

with open('config.yaml', 'r') as fh:
    kw = yaml.safe_load(fh)

kw = buffer_geojson.main(**kw)
Path(kw["local_folder"]).mkdir(parents=True, exist_ok=True)
for yr in kw["years"]:
    kw["this_yr"] = yr
    yr_folder = f'{kw["local_folder"]}/{yr}'
    Path(yr_folder).mkdir(parents=True, exist_ok=True)
    for srcvar, bnd in kw["bands"].items():
        bnd_folder = f'{yr_folder}/{bnd}'
        Path(bnd_folder).mkdir(parents=True, exist_ok=True)
        kw["this_bnd_yr"] = bnd_folder
        kw["this_var"] = bnd
        kw["src_var"] = srcvar
        get_hls.main(**kw)
        vrt_file = make_vrts.main(**kw)
        stats = make_stats.main(**kw)
kw = post_aggregator.main(**kw)
make_tippecanoe_tiles.main(**kw)
upload_tiles(**kw)
