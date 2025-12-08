import requests
import re

def stringifyKbs(kbs: int):
    units = ['kb', 'mb', 'gb', 'tb', 'pb']
    divisor = 1000
    unit_idx = 0
    while kbs > 1000:
        kbs = kbs / divisor
        unit_idx += 1
    return f'{round(kbs, 2)} {units[unit_idx]}'

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
            'Origin': origin,  # Set the origin to match the expected value
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, stream=True, headers=headers)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                print(f'Starting download...')
                kbs = 0
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        kbs += 1
                        file.write(chunk)
                else:
                    print(f"\nDownload complete - {stringifyKbs(kbs)} - file at: {filename} named as: {file.name}")
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
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