#!/usr/bin/python
# coding=utf-8
# -------------------------------------------------------------------------------
# Import modules
#
import argparse

from src import lpb_streamfetcher

print("-> Starting La Planète Bleue Streamfetcher...")

# -------------------------------------------------------------------------------
# Execute
#
if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Options for laplanetebleue_streamfetcher script')
  parser.add_argument('-a', '--all', action='store_true', dest='all', help='Download all available episodes on La Planète Bleue Website.')
  parser.add_argument('-l', '--latest', action='store_true', dest="latest", help='Download only the last episode.')
  parser.add_argument('-o', '--outdir', dest='outdir', help='Specify directory to store episodes to.')
  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Enable verbosity.')
  args = parser.parse_args()

  if args.latest and args.all or args.all:
    download_all = True
  elif args.latest:
    download_all = False
  else:
    download_all = True

  lpb_downloader = lpb_streamfetcher.lpb_download(verbose=args.verbose, outdir=args.outdir, download_all=download_all)
