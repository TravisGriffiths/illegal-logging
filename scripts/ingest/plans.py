import json
import pandas as pd
import sqlite3
import os
from sqlite3 import Error
from ..SQL import poa_sql, tables

## NOTE: in SQL and some vars plans are referred to as POA, Plano Operacional Anual (POA) - Annual Operating Plans 

def sql_connection(db: str):
    try:
      conn = sqlite3.connect(db)
      return conn
    except Error:
      print(Error)

index = 0
def create_record(row):
    global index
    index += 1
    return (
    index,    
    row.get('PRODUTO'),    # product, 
    row.get('NOME_POPULAR'),    # common_name, 
    row.get('NOME_CIENTIFICO'),    # scientific_name, 
    row.get('VOLUME'),    # volume, 
    row.get('ORGAO_AMBIENTAL_RESP_ANALISE'),    # analyst_institution, 
    row.get('DATA_DE_VALIDADE'),        # date_valid, 
    row.get('NRO_CAR_IMOVEL_RURAL'),        # plot_car_id,
    row.get('UF'),        # state,
    row.get('MUNICIPIO'),        # city,
    row.get('LATITUDE_UPA'),        # unit_latitude,
    row.get('LONGITUDE_UPA'),        # unit_longitude,
    row.get('AREA_UPA'),        # unit_area,
    row.get('LATITUDE_EMPREENDIMENTO'),        # operation_latitude,
    row.get('LONGITUDE_EMPREENDIMENTO'),        # operation_longitude,
    row.get('NRO_UPA'),        # production_unit,
    row.get('DATA_DE_EMISSAO'),        # date_issued,
    row.get('DATA_DA_SITUACAO'),        # date_effective,
    row.get('NRO_AUTORIZACAO_PMFS_VINCULADO'),        # authorization,
    row.get('NRO_REGISTRO'),        # registration,
    row.get('NRO_AUTORIZACAO_PMFS_VINCULADO'),        # pmfs_authorization_boundry, 
    row.get('NOME_DO_RT'),        # technician_name,
    row.get('NRO_ART'),        # technician_number,
    row.get('ATIVIDADE_RT'),        # technician_grade,
    row.get('NOME_DETENTOR'),        # operator_name,
    row.get('CPF_CNPJ_DETENTOR'),        # operator_id,
    row.get('AREA_MANEJO_FLORESTAL'),        # managed_area,
    row.get('EQUACAO_VOLUME'),        # volume_equation,
    row.get('METODO_INVENTARIO'),        # inventory_method,
    row.get('DATA_DO_TRAMITE'),        # last_referenced,
    row.get('ULTIMA_ATUALIZACAO_RELATORIO'),        # last_updated,
    row.get('NATUREZA_JURIDICA'),        # legal_status,
    row.get('IMOVEL_RURAL_VINCULADO'),        # boundry,
    row.get('SITUACAO'),        # situation,
    row.get('TIPO_DE_EMPREENDIMENTO'),        # business_type,
    row.get('NOME_EMPREENDIMENTO_VINC'),        # business_name,
    row.get('COMPETENCIA_AVALIACAO'),        # assessment,
    row.get('NRO_AUTORIZACAO_ORIGINAL'),        # origninal_authorization,
    row.get('ULTIMO_TRAMITE')        # last_processed
    )

def ingestPlans(dir: str, db: str):
    json_files = [f'{dir}/{f}' for f in os.listdir(dir) if os.path.isfile(f'{dir}/{f}') and f.endswith('json')]
    if len(json_files) > 0:
        connection = sql_connection(db)
        cursor = connection.cursor()
        cursor.execute(poa_sql.rm_table_sql)
        connection.commit()
        cursor.execute(poa_sql.create_table_sql)
        index = 0
        for file in json_files:
            with open(file) as poa_json_file:
                data = json.load(poa_json_file)
                records = data['data']
                df = pd.DataFrame.from_dict(records, orient='columns')
                records = [create_record(record) for _, record in df.iterrows() ]
                cursor.executemany(poa_sql.sql, records)
                connection.commit()
        else:
            results = cursor.execute(f'select * from {tables.POA};')
            print(f"Records Ingested: {len(results.fetchall())}")
            if (connection):
              connection.close()

    else:
        print(f'No files found for Annual Plan ingest at: {dir}') 
   

