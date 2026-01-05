import json
import pandas as pd 
from pandas import Series
import sqlite3
import os
import re
import geopandas as gpd
# from sqlite3 import Error
# from ..SQL import transport_sql, tables

def make_origin(lat: float, long: float):
    return f'lat:{round(lat, 5)}-long:{round(long, 5)}'

## Convience for cutting down the number of years
def hasYear(name: str, years: list[str]):
    # ex: DOFTransportes_ano_2025_uf_SC.json
    tokens = name.split('_')
    year = tokens[2]
    if year in years:
        return True 
    return False

# This is hardcoded for now, this list are the states that have POA records 
def includedState(name: str):
    #states_with_plans = {'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'BA', 'MG', 'SC', 'RO','PA', 'AM', 'AC','AP','RR','TO','MT'}
    states = {'AM'}
    # ex: DOFTransportes_ano_2025_uf_SC.json
    tokens = name.split('_')
    last = tokens[4]
    state, _ = last.split('.')
    return state in states

class Origin:

    def add_series(self, row):
        series = row.get("Nr_de_Serie_do_DOF")
        if series:
            self.series.add(series)

    def add_year(self, row):
        year = row.get("Ano")
        if year:
            self.years.add(year)

    def add_volume(self, row):
        vol: float = row.get("Volume", 0.0)
        if type(vol) in (float, int):
            self.volume += vol

    # Tally of how many ans which DOF systems are using this area
    def add_system(self, row):
        sys = row.get("SistemaOriginario")
        if sys:
            self.systems.add(sys)

    def add_shipment(self, row):
        self.shipments += 1
        self.add_series(row)
        self.add_volume(row)
        self.add_system(row)

    def add_plot(selt, plot: gpd.GeoDataFrame):
        self.cad = 

    def __init__(self, row):
        self.cad: str | None = None
        self.area: float = -1.0
        self.state: str = row.get("UF_de_Origem")
        self.city: str = row.get("Municipio_de_Origem")
        self.lat: float = row.get("Latitude_de_Origem")
        self.long: float = row.get("Longitude_de_Origem")
        self.origin = make_origin(self.lat, self.long)
        self.point = gpd.points_from_xy([self.lat], [self.long])[0]
        self.shipments: int = 0
        self.volume: float = 0.0
        self.systems: set[str] = set()
        self.series: set[str] = set()
        self.years: set[str] = set()
        self.add_shipment(row)

all_origins: dict[str, Origin] = {}
destinations: set[str] = set()
origins: dict[str, Origin] = {}
# units: set[str] = set()
# volumes: dict[str, float] = {}
# shipments: dict[str, int] = {}

def get_volumes(m: dict[str, Origin]):
    return [o.volume for o in m.values()]

# This removes any origins that are also a destination, i.e. logs were shipped raw to that point
# as any point that is gathering and reshipping logs is causp.ing double counting as the logs were 
# merely shipped multiple times in raw form. 
def clear_transhipment_points():
    transhipment_points = 0
    for origin in all_origins.keys():
        if not origin in destinations:
            orig = all_origins.get(origin)
            if orig:
                origins[origin] = orig
        else:
            transhipment_points += 1
    else:
        return transhipment_points


def output_total():
    transhipment_points = clear_transhipment_points()
    final_volumes = get_volumes(origins)
    total_volume = sum(final_volumes)
    print(f'Found {transhipment_points} transhipment points')
    print(f'Total cubic meters shipped: {format(round(total_volume, 3), ',')}')
    print(f'Total Hectares cleared (approx): {format(round(total_volume/150, 3), ',')}')
    print(f'Top origins by volume: {sorted(final_volumes, reverse=True)[0:10]}')
    print(f'Total Origins: {len(origins)}')


def process_shipment(row: Series):
    lat = row.get("Latitude_de_Origem")
    long = row.get("Longitude_de_Origem")
    if lat != None and long != None:
        id = make_origin(lat, long)
        # Record destinations in order to identify transhipment points to prevent double counting
        dest_lat = row.get("Latitude_do_Destino")
        dest_long = row.get("Longitude_do_Destino")
        if dest_lat != None and dest_long != None:
            destination = make_origin(dest_lat, dest_long)
            destinations.add(destination)

        orig = all_origins.get(id, Origin(row))
        if id in all_origins:
            orig.add_shipment(row)
        all_origins[id] = orig 

def ingest_origins(dir: str, plots_dir: str):
    print('Ingesting Origins...')
    years = ['2024']
    #years = ['2025', '2024', '2024', '2023', '2022']
    json_files = [f'{dir}/{f}' for f in os.listdir(dir) if os.path.isfile(f'{dir}/{f}') and f.endswith('json') and hasYear(f, years)]
    if len(json_files) > 0:
        file_count = len(json_files)
        print(f'{file_count} files  found for ingestion, starting database init')
        # connection = sql_connection(db)
        # cursor = connection.cursor()
        # print('Removing any old records')
        # cursor.execute(transport_sql.rm_table_sql)
        # connection.commit()
        # print('Re-creating table')
        # cursor.execute(transport_sql.create_table_sql)
        # connection.commit()
        # file_count = len(json_files) 
        print('Ingesting files...')

        for index, file in enumerate(json_files):
            with open(file) as json_file:
                print(f'Processing {file}...')
                data = json.load(json_file)
                df = pd.DataFrame.from_dict(data['data'], orient='columns')
                # Filter records to only look at shipments of logs specifically (no sawn products) from the federal systems specifically
                [process_shipment(record) for _, record in df.iterrows() if record.get("Produto") == 'Tora']
                # cursor.executemany(transport_sql.sql, records)
                # connection.commit()
                # Grab the file name only for clearer log messages
                file_name = re.split(r'[/\\]', file)[-1]
                #print(f'Now have {format(len(origins), ',')} unique origins after adding {file_name}')
                # print(f'All Units found: {', '.join(units)}')
                vols = get_volumes(all_origins)
                print(f"Top volumes: {sorted(vols, reverse=True)[0:10]}")
                print(f'{index + 1} files of {file_count} ingested')
        
        else:
            print('Ingest completed, checking origins...')
            output_total()
            # print(f'Total Origins: {format(len(origins), ',')}')
            # print(f"Top volumes: {sorted(volumes.values(), reverse=True)[0:10]}")
            # print(f'All Units found: {', '.join(units)}')
            # count = cursor.execute(f'select count(*) from {tables.TRANSPORT};')
            # print(f"Records Ingested: {count.fetchall()}")
            # print('Vacuuming db to clean up space, this may take awhile')
            # cursor.execute('VACUUM;')
            # print('Vacuum cleanup complete..')
            # if (connection):
            #   connection.close()

            # First: seperate all Origins into States and municipalities. This allows the quick query of the Dataframe 
            # to JUST the state and city of interest before doing any expensive matching for location. 

            per_city_origins: dict[str, dict[str, list[Origin]]] = {}
            for origin in origins.values():
                city = origin.city
                state = origin.state 
                origin_state = per_city_origins.get(state, {})
                cities = origin_state.get(city, [])
                cities.append(origin)
                origin_state[city] = cities
                per_city_origins[state] = origin_state

            print('Ingesting Plots...')
            gpkg_files = [f'{plots_dir}/{f}' for f in os.listdir(plots_dir) if os.path.isfile(f'{plots_dir}/{f}') and f.endswith('gpkg')]
            for file in gpkg_files:
                data = gpd.read_file(file)
                print(f'Showing file: {file}')
                print(f'{data.head}')
                # State: sigla_uf
                # City: nm_mun 
                # minx, miny, maxx, maxy = gdf.geometry.total_bounds
                for state, cities in per_city_origins.items():
                    for city, origs in cities.items():
                        print(f'Matching Plots to {city}, {state}, {len(origs)} origins present')
                        city_plots = data.loc[data['sigla_uf'] == state and data['nm_mun'] == city]
                        print(f'{len(city_plots)} found')
                        if not city_plots or len(city_plots) == 0:
                            print(f'No discoverable plots located, moving to next municipality')
                            continue
                        for origin in origins.values():
                            # distances = [ b for b in data.loc[data['nm_mun'] == 'Porto Grande'][0:10].geometry.distance(point) ] 
                            # [ [ b.id, b.geometry.distance(point) ] for i, b in list.iterrows() ][0]
                            # sorted(distances, key=lambda plot: plot[1])
                            if origin.point:
                                distances: list[(str, float)] = sorted([ [ b.id, b.geometry.distance(origin.point) ] for i, b in city_plots.iterrows() ], key=lambda plot: plot[1])
                                closest = distances[0]
                                # TODO: More sanity checks 
                                [id, distance] = closest
                                print(f'Distance found at: {distance}')
                                plot = city_plots.loc[city_plots['id'] == id]
                                # o = [l for [i, l] in plot.iterrows()][0]
                            else:
                                print(f'No origin point found for {origin.origin}')
                                

    else:
        print(f'No files found for Shipping Records ingest at: {dir}') 
   
