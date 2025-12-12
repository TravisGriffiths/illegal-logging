### Download and save the Annual Operation Plans JSON data
# file currently saved in 2 files, 
# One for the Amazon - here: https://dadosabertos.ibama.gov.br/dados/SINAFLOR/poa/poaAmazoniaLegal/poaAmazoniaLegal_json.zip
# The other for everything else - here: https://dadosabertos.ibama.gov.br/dados/SINAFLOR/poa/poaOutrosBiomas/poaOutrosBiomas_json.zip
# Information for
# Amazon here: https://dadosabertos.ibama.gov.br/en/dataset/sinaflor-poa-amazonia-legal/resource/e1c34194-677f-4f9a-9192-01a1fbafa55f
# Other biomes here: https://dadosabertos.ibama.gov.br/en/dataset/sinaflor-poa-outros-biomas/resource/16a06598-3eee-44cb-89a6-ea80f384b59d
from ..config import PLANS_AMAZON_URL, PLANS_OTHER_URL
from .fetch import fetch
from .unzip import unzip
import os

def downloadPlans(dir: str):
    amazon_file = f'{dir}/POA_Amazon.zip'
    other_file = f'{dir}/POA_Other.zip'
    downloads = [{
        'url': PLANS_AMAZON_URL,
        'file': amazon_file
    }, {
       'url': PLANS_OTHER_URL,
        'file': other_file
    }]
    for download in downloads:
        if os.path.exists(download.get('file')):
            print(f'Plans file found, skipping download')
            continue
        else:
            print(f'Fetching plans from {download.get('url')} to place in {download.get('file')}')
            # create the directory if needed
            if not os.path.exists(dir):
                os.makedirs(dir)
                print(f'Created directory: {dir}')
            else:
                print(f'Found directory: {dir} ready for download')
            # Directory built/found, download
            fetch(download.get('url'), download.get('file'))

def unzipPlans(dir: str):
    zip_files = [f'{dir}/{f}' for f in os.listdir(dir) if os.path.isfile(f'{dir}/{f}') and f.endswith('zip')]
    print(f'Found {len(zip_files)} to unzip in directory {dir}')
    for file in zip_files:
        unzip(file, dir)