# Module: KEYS-L3
# Created on: 11-10-2021, modified 1/17/23 for l3dl-re
# Authors: -∞WKS∞- , r3n

from pywidevine_.L3.decrypt.wvdecryptcustom import WvDecrypt
from pywidevine_.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from getPSSH import get_pssh
import subprocess
import xmltodict
import argparse
import requests
import sqlite3
import headers
import base64
import os
version = '0.1'


def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64,
                          device=deviceconfig.device_android_generic)
    widevine_license = requests.post(
        url=lic_url, data=wvdecrypt.get_challenge(), headers=headers.headers)
    license_b64 = b64encode(widevine_license.content)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt


def insert_table(pssh, keys, license_, mpd_):
    conn = sqlite3.connect('keyVault.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO TBL_KEYS(PSSH,KEYS,LICENSE_URL,MPD_URL) VALUES ('{pssh}','{keys}','{license_}','{mpd_}')")
    conn.commit()
    conn.close()


def find_pssh(pssh):
    conn = sqlite3.connect('keyVault.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM TBL_KEYS WHERE PSSH='{pssh}'")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def fetch_key(pssh):
    conn = sqlite3.connect('keyVault.db')
    conn.text_factory = str
    cursor = conn.cursor()
    fetch = cursor.execute(
        f"SELECT KEYS FROM TBL_KEYS WHERE PSSH='{pssh}'").fetchall()
    # edit this for cases that no pssh can be extracted from MPD
    fetched_keys = fetch[0][0]
    conn.commit()
    conn.close()
    return fetched_keys


def download(keys):
    if mpd_url != None:
        if select_ and not os.path.exists(f'{cd}\\output\\{name}.mkv'):
            os.system(f'N_m3u8DL-RE.exe "{mpd_url}" --log-level ERROR --binary-merge --live-real-time-merge --mp4-real-time-decryption --key {keys} -M format=mkv --del-after-done --save-name "{name}" --save-dir "{cd}\\output" --use-shaka-packager -mt TRUE --thread-count 12')
        elif not select_ and not os.path.exists(f'{cd}\\output\\{name}.mkv'):
            print(
                f'Processing {name} | Download, decrypt, and muxing may take some time.')
            subprocess.call(f'N_m3u8DL-RE.exe "{mpd_url}" --log-level ERROR --binary-merge --live-real-time-merge --mp4-real-time-decryption --key {keys} -M format=mkv --del-after-done -ss all -sa best -sv best --save-name "{name}" --save-dir "{cd}\\output" --use-shaka-packager -mt TRUE --thread-count 12')
        else:
            print(f'{name} already on output folder. Skipped.')
    else:
        print('No MPD URL supplied. Try again.')


def start_():
    if pssh_:
        pssh = pssh_
    else:
        pssh = get_pssh(mpd_url)

    if pssh != 'skip':
        print(f'\nPSSH: {pssh}')
        cached = find_pssh(pssh)
        if cached:
            keys = fetch_key(pssh)
            print(f'Cached key found for {name}: {fetch_key(pssh)}')
            if not keys_:
                download(keys)
        else:
            if lic_url != None:
                correct, keys = WV_Function(pssh.strip(), lic_url.strip())

                if keys:
                    for key in keys:
                        print(f'Key: {key}')
                        insert_table(pssh, key, lic_url, mpd_url)
                    # consider multi-keys scenario, pssh to kid?
                    if keys_:
                        print(f'Done fetching keys for {name}.')
                    else:
                        download(keys)
            else:
                print(f'You have no license URL for {name}. Try again.')
    else:
        print(f'Skipped {name}.')


print(f'''\n
r3n@RSG                                  {version}
██╗     ██████╗ ██████╗ ██╗      ██████╗ ███████╗
██║     ╚════██╗██╔══██╗██║      ██╔══██╗██╔════╝
██║      █████╔╝██║  ██║██║█████╗██████╔╝█████╗  
██║      ╚═══██╗██║  ██║██║╚════╝██╔══██╗██╔══╝  
███████╗██████╔╝██████╔╝███████╗ ██║  ██║███████╗
╚══════╝╚═════╝ ╚═════╝ ╚══════╝ ╚═╝  ╚═╝╚══════╝
                                                 
    -- L3DL REscripted Widevine Downloader --''')

parser = argparse.ArgumentParser(
    description='L3DL-RE widevine downloader - r3n@RSG')
parser.add_argument('-m', '--manifest', type=str,
                    metavar='', help="your mpd/m3u8 link")
parser.add_argument('-l', '--license', type=str,
                    metavar='', help="license url link")
parser.add_argument('-o', '--output', type=str.lower,
                    metavar='', help="output file name")
parser.add_argument('-p', '--pssh', type=str,
                    metavar='', help="supply pssh instead of extracting from manifest")
parser.add_argument('--batch', help="batch download mode. what file to open?")
parser.add_argument('--select', action='store_true',
                    help="manually pick what to download")
parser.add_argument('--keys', action='store_true',
                    help="keys only, don't download")
parser.add_argument('--shut', action='store_true',
                    help="shutdown windows after the process")


args = parser.parse_args()
mpd_url = args.manifest
lic_url = args.license
name = args.output
select_ = args.select
keys_ = args.keys
batch_mode = args.batch
shutdown = args.shut
pssh_ =  args.pssh

cd = os.getcwd()

if not os.path.exists('output'):
    os.makedirs('output')


if batch_mode:
    print('\nBatch mode activated.')
    source_file = open(batch_mode, "r", encoding='latin-1')
    for line in source_file:
        fields = line.split(";")
        name = fields[0]
        mpd_url = fields[1]
        lic_url = fields[2]
        start_()
else:
    start_()


if shutdown:
    os.system(f'shutdown /f /s')

# TODO: support for multi-keys usecase
