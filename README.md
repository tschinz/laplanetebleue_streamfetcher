[La Planète Bleue Streamfetcher](https://github.com/tschinz/laplanetebleue_streamfetcher)
================================

This Python script let your download the latest La Planète Bleue Episodes from the [La Planète Bleue Website](https://laplanetebleue.com/podcast).

Requirements
---
* ``Python 3.0`` but should be compatible with ``Python 2.x``
  * ``pycurl``
  * ``xml.dom``
* ``mid3v2.py`` - For create the id3 tags

On a Debian based Linux:
```bash
sudo apt-get install python3 python3-pycurl mid3v2
```

Features
---
* Lets you download all current episodes as MP3
* Lets you download only the last episodes as MP3
* Creates ID3 tags for the episode
* Checks for duplicated episodes
* Checks for folders
* Creates a folder per Year

Usage
---

```bash
python lpb_streamfetcher.py -h

Usage: lpb_streamfetcher.py [options]

Options:
  -h, --help            show this help message and exit
  -a, --all             Download all 500 last Maloney episodes. Does not work
                        for the newest one or two, use -l instead.
  -l, --latest          Download the last 10 Maloney episodes, works also for
                        the newest ones ;-).
  -o OUTDIR, --outdir=OUTDIR
                        Specify directory to store episodes to.
  -v, --verbose         Enable verbose.
```

* Execute script
```bash
python lpb_streamfetcher.py -l -o /location/to/musicfiles
```

* Use Cronjob for automatically execute the script every Monday at 24:00.
```bash
crontab -e
```
```bash
0 * * * 1 python /location/to/lpb_streamfetcher.py -l -o /location/to/musicfiles
```

![La Planète Bleue](https://laplanetebleue.com/images/lpb5-moebius.jpg)

Versions Log
---
- `v1.0`
  * Initial Release

Thanks
---
  * Yves Blanc for an awesome Podcast since so many years.
  * Thanks for all who streams and contributes to La Planète Bleue

Licensing
---
This document is under the [CC BY-NC-ND 3-0 License, Attribution-NonCommercial-NoDerivs 3.0 Unported](http://creativecommons.org/licenses/by-nc-nd/3.0/). Use this script at your own risc!

The La Planète Bleue streams are copyright by [Yves Blanc](https://laplanetebleue.com). It is against the law to distribute the generated mp3 files!
