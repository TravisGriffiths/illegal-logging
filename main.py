#!/usr/bin/env python3

from scripts.download.pmfs import downloadPMFS, unzipPMFS
from scripts.download.cnpj import downloadCNPJ
from scripts.download.transport import downloadTransport, unzipTransport 
from scripts.ingest.plans import ingestPlans
from scripts.download.plans import downloadPlans, unzipPlans
from scripts.config import AUTEX_DIR, DATA_DIR, DATABASE_DIR, SQL_DATABASE, PMFS_DIR, PLANS_DIR, PLANS_AMAZON_URL, PLANS_OTHER_URL, CNPJ_DIR, TRANSPORT_DIR
from cli import cli
import os
import sys

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
DATABASE = f"{ROOT_DIR}/{DATABASE_DIR}/{SQL_DATABASE}"
AUTEX_ROUTE = f"{ROOT_DIR}/{DATA_DIR}/{AUTEX_DIR}"
PLANS_ROUTE = f"{ROOT_DIR}/{DATA_DIR}/{PLANS_DIR}"
PMFS_ROUTE = f"{ROOT_DIR}/{DATA_DIR}/{PMFS_DIR}"
CNPJ_ROUTE = f"{ROOT_DIR}/{DATA_DIR}/{CNPJ_DIR}"
TRANSPORT_ROUTE = f"{ROOT_DIR}/{DATA_DIR}/{TRANSPORT_DIR}"

def plans(action: str):
    if action == 'download':
        downloadPlans(PLANS_ROUTE)
        unzipPlans(PLANS_ROUTE)
    if action == 'ingest':
        ingestPlans(PLANS_ROUTE, DATABASE)

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
        downloadTransport(TRANSPORT_ROUTE)
        unzipTransport(TRANSPORT_ROUTE)

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
    if noun == 'plans':
        plans(verb)

if __name__ == '__main__':
    main()