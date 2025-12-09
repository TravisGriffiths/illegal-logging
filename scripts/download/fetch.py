import requests
import re
import shutil
import os

def stringifyKbs(kbs: int):
    units = ['kb', 'mb', 'gb', 'tb', 'pb']
    divisor = 1000
    unit_idx = 0
    while kbs > 1000:
        kbs = kbs / divisor
        unit_idx += 1
    return f'{round(kbs, 2)} {units[unit_idx]}'

def have_full_file(filename: str, total: int):
    if not os.path.exists(filename):
        return False
    size = os.path.getsize(filename)
    if size < total:
        print(f'{round(size / 1024)} of {round(total / 1024)} kb downloaded')
        return False 
    return True

def fetch(url: str, filename: str):
    if filename == None:
        print(f"No filename passed to save {url} to")
        return
    urlScan = re.match(r"http[s]*://[\w\.]+", url)
    if urlScan == None:
        print(f"URL: {url} not found to have usable origin (http://)")
        return
    origin = urlScan.group(0)
    if origin:
        headers = {
            'Accept-Encoding': 'identity, deflate, compress, gzip', 
            'Accept': '*/*',
            'Origin': origin,  # Set the origin to match the expected value
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
        total_content_size = int(requests.get(url, stream=True).headers['Content-Length'])
        range = 0
        print(f'Starting download...')
        while not have_full_file(filename, total_content_size):
            headers['Range'] = 'bytes=%d-' % range
            with requests.get(url, stream=True, headers=headers) as response:
                response.raise_for_status()
                with open(filename, 'ab') as file:
                    shutil.copyfileobj(response.raw, file, length=16*1024*1024)
                    file.flush()
            range = os.path.getsize(filename)
            print(f'Fetch complete file size: {range} total content: {total_content_size}')
    else:
        print(f"URL: {url} not found to have usable origin (http://)")
        return

def get(url):
    urlScan = re.match(r"http[s]*://[\w\.]+", url)
    if urlScan == None:
        print(f"URL: {url} not found to have usable origin (http://)")
        return
    origin = urlScan.group(0)
    if origin:
        headers = {
            'Origin': origin,  # Set the origin to match the expected value
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed fetch from {url}. Status code: {response.status_code}")