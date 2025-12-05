from ..SQL import dof_sql
from ..SQL import tables
import config
import os
import json
import pandas as pd
import sqlite3
from sqlite3 import Error

base_path = '../..'

sql_database = f"{base_path}/{config.DATABASE_DIR}/{config.SQL_DATABASE}"

def sql_connection():
    try:
      conn = sqlite3.connect(sql_database)
      return conn
    except Error:
      print(Error)

index = 0
def create_record(row):
    try:
        year = int(row['ANO'])
    except ValueError:
        year = 0
    global index
    index += 1
    return (
    index,
    year,
    row['DATA_DE_CADASTRO_DA_AUTEX'],
    row['LONGITUDE'],
    row['DATA_DE_LIBERACAO_DA_AUTEX'],
    row['SITUACAO_ATUAL'],
    row['NOME_RAZAO_SOCIAL_DO_DETENTOR'],
    row['NOME_POPULAR'],
    row['VOLUME_REMANESCENTE'],
    row['NOME_DA_ORIGEM'],
    row['UF'],
    row['AREA'],
    row['NRO_DA_AUTORIZACAO_ORIGINAL'],
    row['VOLUME_ORIGINAL_AUTORIZADO'],
    row['NUMERO_DE_SERIE_DA_AUTEX'],
    row['NOME_CIENTIFICO'],
    row['ULTIMA_ATUALIZACAO_RELATORIO'],
    row['CTF_DO_DETENTOR'],
    row['TIPO_DE_AUTEX'],
    row['CPF_CNPJ_DO_DETENTOR'],
    row['UNIDADE_DE_MEDIDA'],
    row['MUNICIPIO'],
    row['DATA_DE_VALIDADE_DA_AUTEX'],
    row['TIPO_DE_PRODUTO'],
    row['ORGAO_EMISSOR_DA_AUTORIZACAO'],
    row['LATITUDE']
    )

dir_path = f"{base_path}/{config.AUTEX_DIR}"
files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

connection = sql_connection()
cursor = connection.cursor()
cursor.execute(dof_sql.rm_table_sql)
connection.commit()
cursor.execute(dof_sql.create_table_sql)
connection.commit()

for file in files:
    file_path = f"{dir_path}/{file}"
    print(f"Ingesting: {file_path}:\n")
    with open(file_path) as dof_json_file:
        data = json.load(dof_json_file)
        records = data['data']
        df = pd.DataFrame.from_dict(records, orient='columns')
        records = [create_record(record) for _, record in df.iterrows() ]
        cursor.executemany(dof_sql.sql, records)
        connection.commit()

results = cursor.execute(f"select * from {tables.DOF};")
print(f"Results: {len(results.fetchall())}")
if (connection):
   connection.close()