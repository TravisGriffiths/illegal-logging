import requests
import re

# url = 'https://example.com/file.zip'


# response = requests.get(url, stream=True, headers=headers)

# if response.status_code == 200:
#     with open('file.zip', 'wb') as file:
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 file.write(chunk)
#     print("File downloaded successfully!")
# else:
#     print(f"Failed to download file. Status code: {response.status_code}")   

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
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        print('.', end='')
                        file.write(chunk)
                else:
                    print(f"\nDownload complete - file at: {filename} named as: {file.name}")
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
    else:
        print(f"URL: {url} not found to have usable origin (http://)")
        return
