## Download and save CNPJ Data
# files currently updated montly and are posted here: https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/

from bs4 import BeautifulSoup
from ..config import CNPJ_URL, CNPJ_DIR
from .fetch import fetch, get
from .unzip import unzip
import re
import os

def mostRecent(a: str | None, b: str | None):
    if a == None and b == None:
        return None
    if a == None and b:
        return b 
    if b == None and a:
        return a 
    aTokens = a.rstrip('/').split('-')
    bTokens = b.rstrip('/').split('-')
    YEAR = 0
    MONTH = 1
    if aTokens[YEAR] == bTokens[YEAR]:
        if aTokens[MONTH] > bTokens[MONTH]:
            return a 
        else: 
            return b 
    if aTokens[YEAR] > bTokens[YEAR]:
        return a 
    else:
        return b

# "2025-05/"?
def isDownloadLink(href: str):
    tokens = href.rstrip('/').split('-')
    return len(tokens) == 2 and tokens[0].isdigit() and tokens[1].isdigit()

def downloadCNPJ(dir: str):
    current_html = get(CNPJ_URL)
    if not current_html:
        print(f'Unable to get existing data from {CNPJ_URL}')
    dom = BeautifulSoup(current_html, 'html.parser')
    most_recent: str | None = None
    for link in dom.find_all('a'):
        href = link.get('href')
        if isDownloadLink(href):
            most_recent = mostRecent(most_recent, href)
    else:
        if most_recent:
            current_url = f'{CNPJ_URL}/{most_recent}'
            print(f'Most recent month found at: {current_url}')
            recent_html = get(current_url)
            if not recent_html:
                print('Unable to get most recent month from {current_url}')
            else:
                recent_dom = BeautifulSoup(recent_html, 'html.parser')
                zips: list[str] = []
                for link in recent_dom.find_all('a'):
                    href = link.get('href')
                    if href.endswith('zip'):
                        print(f'Link Found: {href}')
                        zips.append(href)
                else:
                    zip_routes = [ { 'file': f'{dir}/{zip}', 'url': f'{current_url}{zip}' } for zip in zips  ]
                    print(f'Grab zip File: {zip_routes[0].get('file')}')
                    print(f'Zip URL: {zip_routes[0].get('url')}')
                    fetch(zip_routes[0].get('url'), zip_routes[0].get('file'))

        else:
            print(f'Failed to find the most recent link')