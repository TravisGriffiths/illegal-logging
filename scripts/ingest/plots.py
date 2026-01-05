import geopandas as gpd
import os
import re 



def ingest_plots(dir: str):
    print('Ingesting Plots...')
    gpkg_files = [f'{dir}/{f}' for f in os.listdir(dir) if os.path.isfile(f'{dir}/{f}') and f.endswith('gpkg')]
    for file in gpkg_files:
        data = gpd.read_file(file)
        print(f'Showing file: {file}')
        data.head()  # Prints the first 5 rows of the loaded data to see what it looks lik
