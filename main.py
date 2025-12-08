#!/usr/bin/env python3

from scripts.download.pmfs import downloadPMFS, unzipPMFS
from scripts.download.cnpj import downloadCNPJ
from scripts.config import PMFS_DIR, CNPJ_DIR
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '.'))
PMFS_ROUTE = f"{ROOT_DIR}/data-files/{PMFS_DIR}"
CNPJ_ROUTE = f"{ROOT_DIR}/data-files/{CNPJ_DIR}"

def main():
    downloadCNPJ(CNPJ_ROUTE)

    # downloadPMFS(PMFS_ROUTE)
    # unzipPMFS(PMFS_ROUTE)

if __name__ == '__main__':
    main()