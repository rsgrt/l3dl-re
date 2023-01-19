L3DL-REscripted widevine downloader

This script was modified from the base L3 module and named as such because it depends on N_m3u8DL-RE instead of yt-dlp/aria2c/ffmpeg/mkvmerge. This project is more of vinebatch's successor that is faster and better.

Since most big VODs have their dedicated downloaders, this is aimed for smaller sites that have no custom payload needed. This is initial release and will likely contain bugs that will either be fixed in the future or not.

Requirements:
- These should be on your PATH (use latest): mkvtoolnix/mkvmerge, shaka-packager.exe
- python3 (tested on python 3.10.xx)
- Working L3 CDM inside \pywidevine_\L3\cdm\devices\android_generic
```
Usage:

l3dl.py [-h] [-m] [-l] [-o] [--select] [--keys] [--batch BATCH]

  -m , --manifest   your mpd/m3u8 link
  -l , --license    license url link
  -o , --output     output file name
  --select          manually pick what to download
  --keys            keys only, don't download
  --batch BATCH     batch download mode. what file to open?
```
There are two modes here, single video version and batch mode. For single version, you need to supply the manifest link, the license link, and the output file name. For batch version, just include --batch and the text file with the following format: name;manifest_link;license_url

If you want to only get keys, add the --keys flag. By default, the settings will download all of the subs and best audio/video. If you know that your manifest has more than one audio, you can add --select flag which will provide you with an interactive menu before downloading.

The PSSH, KID:KEY, manifest link, license URL, are all added on the local db file for reference/review. If you want to view it, you can use sqlitebrowser or similar tools.

The code is self-documenting so browse and read it.
