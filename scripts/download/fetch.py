import requests
import re
import pycurl
# for displaying the output text
from sys import stderr as STREAM

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
        # headers = {
        #     'Accept-Encoding': 'identity', # Critical, as the Content-Length is WRONG on several sources, the python library will cut the download on that length 
        #     'Accept': '*/*',
        #     'Origin': origin,  # Set the origin to match the expected value
        #     'Connection': 'keep-alive',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        # }
        # Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36

        # headerlist = [
        #     'Accept-Encoding: identity', 
        #     'Accept: */*',
        #     f'Origin: {origin}'
        # ]
        # use kiB's
        kb = 1024

        # callback function for c.XFERINFOFUNCTION
        def status(download_t, download_d, upload_t, upload_d):
            STREAM.write('Downloading: {}/{} kiB ({}%)\r'.format(
                str(int(download_d/kb)),
                str(int(download_t/kb)),
                str(int(download_d/download_t*100) if download_t > 0 else 0)
            ))
            STREAM.flush()

        print(f'Starting download...')
        with open(filename, 'wb') as file:
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(c.WRITEDATA, file)
            c.setopt(c.VERBOSE, 1)
            c.setopt(c.NOPROGRESS, False)
            c.setopt(c.FOLLOWLOCATION, 1)
            c.setopt(c.XFERINFOFUNCTION, status)
            c.perform()
            c.close()

    else:
        print(f"URL: {url} not found to have usable origin (http://)")
        return

# This is just for fetching individual web pages
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