from .fetch import fetch
from .unzip import unzip
from ..config import TRANSPORT_URL
import os


def downloadTransport(dir: str):
    save_file = f'{dir}/Transport_ALL.zip'
    if os.path.exists(save_file):
        print(f'Transport zip file found, skipping download')
        return
    print(f'Fetching Transport data from {TRANSPORT_URL} to place in {save_file}')
    # First create the directory
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f'Created directory: {dir}')
    else:
        print(f'Found directory: {dir} ready for download')
    fetch(TRANSPORT_URL, save_file)

def unzipTransport(dir: str):
    zip_file = f'{dir}/Transport_ALL.zip'
    if not os.path.exists(zip_file):
        print(f'PMFS zip file not found')
        return
    else:
        unzip(zip_file, dir)