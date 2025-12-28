import geopandas as gpd
import fiona
import numpy as np
import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
      conn = sqlite3.connect('../forestry.db')
      return conn
    except Error:
      print(Error)

unique_cad_codes_sql = """select DISTINCT plot_car_id from poa where plot_car_id NOT NULL and state = 'AM';"""

with sql_connection() as connection:
    # connection = sql_connection()
    cursor = connection.cursor()
    unique_cad = cursor.execute(unique_cad_codes_sql).fetchall()
    cads = set(np.concatenate(unique_cad).ravel().tolist())      
    cursor.close()


#print(cads)
path = './AM/AREA_IMOVEL/AREA_IMOVEL_1.shp'

gdf = gpd.read_file(path)

filtered = gdf.loc[gdf['cod_imovel'].isin(cads)]
filtered.to_file('AM_planned_cads.shp', driver='ESRI Shapefile')
filtered.to_file('AM_planned_cads.kml', driver='KML')

# for index, row in gdf.iterrows():  # AM-1303403-659B5651334F4BB5BB4955C4EBEB0D92
#    if row['cod_imovel'] in cads:
#       print(row['cod_imovel'])
#with fiona.open('./AM/AREA_IMOVEL/AREA_IMOVEL_1.shp') as source:
#    print(source.schema)
#    '''
#    {'properties': {'cod_tema': 'str:254', 'nom_tema': 'str:254', 'cod_imovel': 'str:254', 'mod_fiscal': 'float:33.31', 'num_area': 'float:33.31', 'ind_status': 'str:254', 'ind_tipo': 'str:254', 'des_condic': 'str:254', 'municipio': 'str:254', 'cod_estado': 'str:254', 'dat_criaca': 'str:254', 'dat_atuali': 'str:254'}, 'geometry': 'Polygon'}
#    '''