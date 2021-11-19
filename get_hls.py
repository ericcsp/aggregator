import os
import subprocess

def list_hls_files(**kw):
  result = subprocess.run(['az',
                         'storage',
                         'blob',
                         'list',
                         '--prefix',
                         f'{kw["src_folder"]}/{kw["src_var"]}/{kw["this_yr"]}{kw["src_prefix"]}',
                         '--output',
                         'yaml',
                         '--account-name',
                         kw['account'],
                         '-c',
                         kw['src_container'],
                         '--account-key',
                         os.environ['AZURE_ACCOUNT_KEY']], stdout=subprocess.PIPE)
  return [fil["name"] for fil in yaml.safe_load(result.stdout)]

def main(**kw):
  files = list_hls_files(**kw)
  for fil in files:
    result = subprocess.run(['az',
                              'storage',
                              'blob',
                              'download',
                              '-f',
                              fil.replace(f'{kw["src_folder"]}/{kw["src_var"]}/{kw["this_yr"]}/', f'{kw["this_bnd_yr"]}/{kw["this_yr"]}_').replace('.tif', f'_{kw["this_var"]}.tif'),
                              '-n',
                              fil,
                              '--account-name',
                              kw['account'],
                              '-c',
                              kw['src_container'],
                              '--account-key',
                              os.environ['AZURE_ACCOUNT_KEY']], stdout=subprocess.PIPE)
