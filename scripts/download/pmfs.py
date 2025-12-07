### Download and save the PMFS JSON data
# file currently saved here: https://dadosabertos.ibama.gov.br/dados/SINAFLOR/pmfs/AmazoniaLegal/pmfsAmazoniaLegal_json.zip
# Information here: https://dadosabertos.ibama.gov.br/en/dataset/sinaflor-pmfs-amazonia-legal/resource/6a756194-3bb4-4149-8348-0ff457ed45ff
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