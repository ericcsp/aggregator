import os

def main(**kw):
    result = subprocess.run(['az',
                          'storage',
                          'blob',
                          'upload-batch',
                          '-s',
                          kw['tiles_dir'],
                          '--account-name',
                          kw['account'],
                          '-d',
                          f'{kw["src_container"]}/{kw["tiles_dir"]}',
                          '--content-type',
                          'application/vnd.mapbox-vector-tile',
                          '--content-encoding',
                          'gzip',
                          '--account-key',
                          os.environ['AZURE_ACCOUNT_KEY']], stdout=subprocess.PIPE)
