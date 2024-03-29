#!/usr/bin/python
# coding=utf-8
#-------------------------------------------------------------------------------
# Import modules
#
import pycurl
from xml.dom import minidom
import os, io, re, math
import argparse
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import mutagen.mp3
import mutagen.id3


class lpb_download:
  ''' Downloads La Planète Bleue Episodes '''
  verbose = False

  def __init__(self, verbose=False, outdir = None, download_all = True):
    # Change to script location
    path,file=os.path.split(os.path.realpath(__file__))
    os.chdir(path)
    self.path    = path
    self.verbose = verbose
    self.all     = download_all
    self.lpb_url = "https://laplanetebleue.com/podcast"
    self.cover_image = "assets/lpb.png"

    if outdir == None:
      self.outdir = "./../out"
    else:
      self.outdir = outdir
    if not(os.path.isdir(self.outdir)):
      os.mkdir(self.outdir)

    # Get page info
    page = self.curl_page(self.lpb_url)
    mp3_urls = self.parse_html(page)
    today = date.today().strftime("%d.%m.%Y %Hh%M")

    self.log("#######################################################")
    self.log("# La Planète Bleue Streamfetcher - BEGIN")
    self.log("#   " + today)
    if self.all:
      self.log("#   Download all episodes")
      self.log("#")
      for mp3_url in mp3_urls:             # Download all
        self.download_episode(self.outdir, mp3_url, self.cover_image)
    else:                                  # Download only last
      self.log("#   Download only latest episodes")
      self.log("#")
      self.download_episode(self.outdir, mp3_urls[0], self.cover_image)

    self.log("#")
    self.log("#   " + today)
    self.log("# La Planète Bleue Streamfetcher - END")
    self.log("#######################################################")


  def download_episode(self, outdir, mp3_url, cover_image):
    '''Download and save mp3 file from url location'''
    # Get new episode data
    (filename_old, filename, date, nbr) = self.get_fileinfo(mp3_url)
    path = outdir + "/" + date[:4]
    filepath = path + "/" + filename
    episode_data = {"mp3_name": filename, "album": "La Planète Bleue", "genre": "Chillout", "title": mp3_url[0], "artist": "Yves Blanc", "year":date[:4], "date":date, "nbr":nbr}

    # Check if fodler or file already exists
    download = False
    if not(os.path.isdir(path)):
      os.mkdir(path)

    if os.path.isfile(filepath):
      filesize_local = int(os.path.getsize(filepath))
      filesize_web   = int(urllib.request.urlopen(mp3_url[1]).getheader('content-length'))
      filesize_delta = 1000000
      #print("Filesize local {} <=> net {}".format(filesize_local, filesize_web))
      if ((filesize_local < (filesize_web+filesize_delta)) and (filesize_local > (filesize_web-filesize_delta))):
        self.log(" Skipping Episode \"{}\" already exists in the output folder {}".format(filename, path))
      else:
        #download = True
        self.log("  Episode {} was not correctly downloaded. Deleting and trying again.".format(filename))
        #os.remove(filepath)
    else:
      download = True
    if download:
      self.log("Downloading Episode: {}".format(mp3_url[0]))
      self.log("  Save Directory: {}".format(filepath))
      dlmp3 = urllib.request.urlopen(mp3_url[1])
      length = dlmp3.getheader('content-length')
      if length:
        length = int(length)
        blocksize = max(4096, length//100)
      else:
        blocksize = 100000000//100 # just made something up (100MB/100)

      blocknumber = 1
      with open(filepath, 'wb') as file:
        while True:
          percent = int(((blocksize*blocknumber)/length*100))
          percentbar = math.floor(percent/10)
          print("\r Downloading {}% [".format(percent)+(percentbar-1)*"="+">"+(10-percentbar)*" "+"]",end="")
          chunk = dlmp3.read(blocksize)
          if not chunk:
            break
          file.write(chunk)
          blocknumber += 1
        print() ## Just add newline at the end

      # Write the ID3 Tags
      self.write_id3(filepath, episode_data, cover_image)

  def write_id3(self, filepath, episode_data, cover_image):
    '''
    Write Basic ID3 Tags
    '''
    # Read ID3 tag or create it if not present
    try:
      tags = mutagen.id3.ID3(filepath)
    except mutagen.id3.ID3NoHeaderError:
      tags = mutagen.id3.ID3()

    self.log("  Adding ID3 Tags...")
    tags["TIT2"] = mutagen.id3.TIT2(encoding=3, text=episode_data["mp3_name"][:-4])
    tags["TALB"] = mutagen.id3.TALB(encoding=3, text=episode_data["album"])
    tags["TPE1"] = mutagen.id3.TPE1(encoding=3, text=episode_data["artist"])
    tags["TCON"] = mutagen.id3.TCON(encoding=3, text=episode_data["genre"])
    tags["TDRC"] = mutagen.id3.TDRC(encoding=3, text=episode_data["year"])
    tags["TRCK"] = mutagen.id3.TRCK(encoding=3, text=episode_data["nbr"])
    self.log("  Adding Album Cover...")
    cover_image_data = open(cover_image, 'rb').read()

    tags["APIC"] = mutagen.id3.APIC(3, 'image/png', 3, 'Front cover', cover_image_data)

    tags.save(filepath)

  def get_fileinfo(self, mp3_url):
    '''
    Get Filename from URL and split into useful data, construct new filename
    '''
    title = mp3_url[0]
    url = urlparse(mp3_url[1])
    filename_orig = os.path.basename(url.path)
    date = filename_orig[:11].replace("-", "").replace("_","")
    nbr = re.search(".*planete_(\d+)_.*", filename_orig).group(1)
    filename_new = "{} - La Planète Bleue - no {}.mp3".format(date, nbr)
    #self.log("Filename found: {}".format(filename_orig))
    #self.log("=> New Filename constructed: {}".format(filename_new))
    return (filename_orig, filename_new, date, nbr)

  def curl_page(self, url, decode=True):
    '''
    Get Webpage HTML file
    '''
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    if decode:
      return buffer.getvalue().decode("utf-8")
    else:
      return buffer.getvalue()

  def parse_html(self, html):
    '''
    Parse Webpage HTML file
    '''
    mp3_urls = []
    soup = BeautifulSoup(html, "lxml")
    #self.log(soup)
    for ul in soup.find_all('ul', {"id": "playlist"}):
      for li in ul.find_all('li'):
        a = li.find('a')
        mp3_urls.append((a.get_text().strip(), a['href'].strip()))

    if False:
      if mp3_urls:
        self.log("Found episodes to download:")
        for mp3_url in mp3_urls:
          self.log("    * {}: {}".format(mp3_url[0], mp3_url[1]))
      else:
        self.log("no Episodes found")
    return(mp3_urls)

  def system_command(self, command):
    self.log(command)
    os.system(command)

  def log(self, message):
    if self.verbose:
      print(message)

#-------------------------------------------------------------------------------
# Execute
#
if __name__ == "__main__":

  parser = argparse.ArgumentParser(description = 'Options for laplanetebleue_streamfetcher script')
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

  lpb_downloader = lpb_download(verbose=args.verbose, outdir=args.outdir, download_all=download_all)
