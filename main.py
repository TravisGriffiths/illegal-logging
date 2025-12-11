#!/usr/bin/env python3

from scripts.download.pmfs import downloadPMFS, unzipPMFS
from scripts.download.cnpj import downloadCNPJ
from scripts.config import PMFS_DIR, CNPJ_DIR
from cli import cli
import os
import sys

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
PMFS_ROUTE = f"{ROOT_DIR}/data-files/{PMFS_DIR}"
CNPJ_ROUTE = f"{ROOT_DIR}/data-files/{CNPJ_DIR}"

def cnpj(action: str):
    if action == 'download':
        print(f'This action can take several *HOURS* all files are multiple Gb in size. Continue? Y/N')
        response = input()
        if response.startswith(('Y', 'y')):
            downloadCNPJ(CNPJ_ROUTE)
        else:
            print('Cancelling')
    if action == 'ingest':
        print('TODO: Build CNPJ ingest')

def transport(action: str):
    if action == 'download':
        print('TODO: build download transport')
    if action == 'ingest':
        print('TODO: build ingest transport')

def main():
    noun, verb = None, None
    if len(sys.argv) > 1:
        noun, verb = cli(sys.argv[1:])
    else:
        noun, verb = cli(None)
    if noun == 'cnpj':
        cnpj(verb)
    if noun == 'transport':
        transport(verb)
    #downloadCNPJ(CNPJ_ROUTE)

    # downloadPMFS(PMFS_ROUTE)
    # unzipPMFS(PMFS_ROUTE)

if __name__ == '__main__':
    main()