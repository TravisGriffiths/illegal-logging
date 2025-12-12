### Download and save the Annual Operation Plans JSON data
# file currently saved in 2 files, 
# One for the Amazon - here: https://dadosabertos.ibama.gov.br/dados/SINAFLOR/poa/poaAmazoniaLegal/poaAmazoniaLegal_json.zip
# The other for everything else - here: https://dadosabertos.ibama.gov.br/dados/SINAFLOR/poa/poaOutrosBiomas/poaOutrosBiomas_json.zip
# Information for
# Amazon here: https://dadosabertos.ibama.gov.br/en/dataset/sinaflor-poa-amazonia-legal/resource/e1c34194-677f-4f9a-9192-01a1fbafa55f
# Other biomes here: https://dadosabertos.ibama.gov.br/en/dataset/sinaflor-poa-outros-biomas/resource/16a06598-3eee-44cb-89a6-ea80f384b59d
from ..config import PMFS_URL, PMFS_DIR
from .fetch import fetch
from .unzip import unzip
import os

def downloadPMFS(dir: str):
    save_file = f'{dir}/PMFS_ALL.zip'
    if os.path.exists(save_file):
        print(f'PMFS file found, skipping download')
        return
    print(f'Fetching PMFS from {PMFS_URL} to place in {save_file}')
    # First create the directory
    if not os.path.exists(dir):
        os.makedirs(dir)
        print(f'Created directory: {PMFS_DIR}')
    else:
        print(f'Found directory: {dir} ready for download')
    fetch(PMFS_URL, save_file)

def unzipPMFS(dir: str):
    zip_file = f'{dir}/PMFS_ALL.zip'
    if not os.path.exists(zip_file):
        print(f'PMFS zip file not found')
        return
    else:
        unzip(zip_file, dir)