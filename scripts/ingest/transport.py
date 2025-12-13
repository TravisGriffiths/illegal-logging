import json
import pandas as pd
import sqlite3
import os
from sqlite3 import Error
from ..SQL import transport_sql, tables

def sql_connection(db: str):
    try:
      conn = sqlite3.connect(db)
      return conn
    except Error:
      print(Error)

index = 0
# Create Transport Record 56 Columns 
def create_record(row):
    global index
    index += 1
    return (
        index + 1,    
        row.get("Nr_da_DI"), # Nº da DI: Número da declaração de importação (apenas para origens do tipo DI). Formato: Texto;
        row.get("Nr_da_Autesp"),  # Nº da Autesp: Número identificador da autorização especial (apenas para origens do tipo AUTESP). Formato: Texto;
        row.get("Validade_Inicial_do_DOF"), # Validade Inicial do DOF: Data de validade inicial do DOF. Formato: Texto formatado em DD/MM/AAAA;
        row.get("Codigo_de_Controle_do_DOF"), # Código de Controle do DOF: Código de controle de 16 dígitos utilizados para verificar a validade do DOF. Formato: Texto;
        row.get("Data_da_Homologacao"), # Data da Homologação: Data de homologação da origem. Formato: Texto formatado em DD/MM/AAAA;
        row.get("ValorConsolidadoDOFmaisR$"), # Valor Consolidado DOF+ (R$): Valor comercial consolidado declarado do item transportado. Formato: Número decimal.
        row.get("Nome_Razao_Social_do_Remetente"), # Nome/Razão Social do Remetente: Nome do detentor do empreendimento de origem da carga, podendo ser pessoa física ou jurídica. Para pessoa física apenas as iniciais dos nomes são exibidas. Formato: Texto;
        row.get("CTF_do_Destinatario"), # CTF do Destinatário: Número identificador do detentor do empreendimento de destino da carga, na base do IBAMA. Formato: Texto;
        row.get("CPF_CNPJ_do_Destinatario"), # CPF/CNPJ do Destinatário: Número do CPF ou CNPJ do detentor do empreendimento de destino da carga. Para pessoa física apenas os três primeiros dígitos do CPF são exibidos. Formato: Texto;
        row.get("Unidade"), # Unidade: Unidade de medida utilizada para o volume do item informado, de acordo com o tipo de produto do item. Formato: Texto;
        row.get("Data_de_Validade_da_Autex"), # Data de Validade da Autex: Data de validade da autorização de exploração (para empreendimentos do tipo AUTEX e PATIOAUTEX vinculado). Formato: Texto formatado em DD/MM/AAAA;
        row.get("Pais_de_Origem"), # País de Origem: Nome do país de origem da importação (apenas para origens do tipo DI). Formato: Texto;
        row.get("Nr_de_Serie_do_DOF"), # Nº de Série do DOF: Número de série identificador do DOF, gerado pelos sistemas. Formato: Texto;
        row.get("UF_de_Origem"), # UF de Origem: Sigla da unidade federativa onde localiza-se o empreendimento de origem da carga. Formato: Texto;
        row.get("Nome_do_Patio_de_Origem"), # Nome do Pátio de Origem: Nome do empreendimento de origem da carga. Formato: Texto;
        row.get("Latitude_de_Origem"), # Latitude de Origem: Coordenada da latitude do empreendimento de origem da carga, em graus decimais. Formato: número decimal separador ponto;
        row.get("Municipio_de_Destino"), # Município de Destino: Nome do município onde localiza-se o empreendimento de destino da carga. Formato: Texto;
        row.get("Municipio_do_Porto"), # Município do Porto: Nome do município onde localiza-se o porto de entrada nacional de destino da carga para operações de exportação registradas nos estados Rondônia, Pará, Maranhão, Minas Gerais, Mato Grosso. É exibida a mesma informação do porto de entrada para as origens do tipo DI (independente da UF). Formato: Texto;
        row.get("Longitude_de_Origem"), # Longitude de Origem: Coordenada da longitude do empreendimento de origem da carga, em graus decimais. Formato: número decimal separador ponto;
        row.get("Produto"), # Produto: Tipo de produto madeireiro do item transportado. Formato: Texto;
        row.get("Pais_de_Destino"), # País de Destino: Nome do país destino da carga para operações de exportação registradas nos estados Rondônia, Pará, Maranhão, Minas Gerais, Mato Grosso. É exibida a mesma informação do porto de entrada para as origens do tipo DI. Formato: Texto;
        row.get("SistemaOriginario"), # Sistema Originário: Sistema Originário do DOF. Formato: Texto;
        row.get("Municipio_de_Origem"),  # Município de Origem: Nome do município onde localiza-se o empreendimento de origem da carga. Formato: Texto;
        row.get("UF_de_Destino"), # UF de Destino: Sigla da unidade federativa onde localiza-se o empreendimento de destino da carga. Formato: Texto;
        row.get("Nome_Porto_de_Entrada_no_Pais"), # Nome Porto de Entrada no País: Nome do porto nacional (ou equivalente) de entrada indicado na declaração de importação (apenas para origens do tipo DI). Formato: Texto;
        row.get("Data_de_Emissao_do_DOF"), # Data de Emissão do DOF: Data da emissão do DOF. Formato: Texto formatado em DD/MM/AAAA;
        row.get("Nome_Porto_de_Saida_do_Pais"), # Nome Porto de Saída do País: Nome do porto nacional (ou equivalente) de destino da carga para operações de exportação registradas nos estados Rondônia, Pará, Maranhão, Minas Gerais, Mato Grosso. É exibida a mesma informação do porto de entrada para as origens do tipo DI (independente da UF). Formato: Texto;
        row.get("CTF_do_Remetente"), # CTF do Remetente: Número identificador do detentor do empreendimento de origem da carga, na base do IBAMA. Formato: Texto;
        row.get("Ultima_Transacao_do_DOF"),  # No docs, example "Forçada entrega", 
        row.get("Volume"), # Volume: Quantidade de volume informada do item transportado. Formato: Número decimal;
        row.get("CodigoRastreio"), # Código de rastreio: Código de rastreio do produto presente no DOF+. Formato: Texto;
        row.get("Nome_do_Patio_de_Destino"), # Nome do Pátio de Destino: Nome do empreendimento de destino da carga. Formato: Texto;
        row.get("UF_do_Porto"), # UF do Porto: Sigla da unidade federativa onde localiza-se o porto de entrada nacional de destino da carga para operações de exportação registradas nos estados Rondônia, Pará, Maranhão, Minas Gerais, Mato Grosso. É exibida a mesma informação do porto de entrada para as origens do tipo DI (independente da UF). Formato: Texto;
        row.get("Ano"), # Ano: Ano da data de emissão do DOF. Formato: Texto no formato AAAA;
        row.get("Data_da_Ultima_Transacao_do_DOF"), # Data da Última Transação: Descrição da última transação no DOF que tenha alterado seu status. Formato: Texto formatado em DD/MM/AAAA;
        row.get("Latitude_do_Destino"), # Latitude do Destino: Coordenada da latitude do empreendimento de destino da carga, em graus decimais. Formato: Número decimal;
        row.get("UltimaAtualizacaoDorelatorio"), # No Docs, timestamp example: "2025-12-07 01:15",
        row.get("Longitude_do_Destino"), # Longitude do Destino: Coordenada da longitude do empreendimento de destino da carga, em graus decimais. Formato: Número decimal;
        row.get("Validade_Final_do_DOF"), # Validade Final do DOF: Data de validade final atual do DOF. Formato: Texto formatado em DD/MM/AAAA;
        row.get("Orgao_Homologador"), # Órgão Homologador: Órgão homologador da origem. Formato: Texto;
        row.get("Orgao_Emissor_da_DI"), # Órgão Emissor da DI: Órgão emissor da declaração de importação (apenas para origens do tipo DI). Formato: Texto;
        row.get("Nome_Razao_Social_Destinatario"), # Nome/Razão Social Destinatário: Nome do detentor do empreendimento de destino da carga, podendo ser pessoa física ou jurídica. Para pessoa física apenas as iniciais dos nomes são exibidas. Formato: Texto;
        row.get("Nr_de_Serie_da_Autex"), # Nº de Série da Autex: Número de série identificador da autorização de exploração (para empreendimentos do tipo AUTEX e PATIOAUTEX vinculado) de origem da carga. Formato: Texto;
        row.get("Rota_do_Transporte"), # Rota do Transporte: Municípios que formam a rota do transporte, incluindo possíveis trechos de transbordo. Formato: Texto;
        row.get("NomePopular"), # Nome Popular: Nome popular da espécie matéria-prima do item transportado. Formato: Texto;
        row.get("Nr_da_Oferta"), # Nº da Oferta: Identificador interno do IBAMA da oferta a partir da qual o DOF foi gerado (se houver). Formato: Texto;
        row.get("Data_de_Validade_da_Autesp"), # Data de Validade da Autesp: Data de validade da autorização especial (apenas para origens do tipo AUTESP). Formato: Texto formatado em DD/MM/AAAA;
        row.get("CPF_CNPJ_do_Remetente"), # CPF/CNPJ do Remetente: Número do CPF ou CNPJ do detentor do empreendimento de origem da carga. Para pessoa física apenas os três primeiros dígitos do CPF são exibidos. Formato: Texto;
        row.get("Nr_da_Autorizacao_Original"), # Nº da Autorização Original: Número da autorização original da autorização de exploração (para empreendimentos do tipo AUTEX). Formato: Texto;
        row.get("Tipo_de_Origem"), # Tipo de Origem: Tipo do empreendimento de origem da carga (e descrição do tipo de autorização, se houver). Formato: Texto;
        row.get("NomeCientifico"), # Nome Científico: Nome Científico da espécie da matéria-prima do item transportado. Formato: Texto;
        row.get("Orgao_Emissor_da_Autesp"),  # Órgão Emissor da Autesp: Órgão emissor da autorização especial (apenas para origens do tipo AUTESP). Formato: Texto;
        row.get("Tipo_de_Autex"), # Tipo de Autex: Descrição do tipo da autorização de exploração (para empreendimentos do tipo AUTEX e PATIOAUTEX vinculado). Formato: Texto;
        row.get("Data_de_Validade_da_DI"), # Data de Validade da DI: Data de validade da declaração de importação (apenas para origens do tipo DI). Formato: Texto formatado em DD/MM/AAAA;
        row.get("Valor_UnitarioR$"), # Valor Unitário (R$): Valor comercial individual declarado do item transportado. Formato: Número decimal.
    )

## Documented, but not found in records
# Órgão Emissor da Autex: Órgão emissor da autorização de exploração (para empreendimentos do tipo AUTEX). Formato: Texto;

def ingestTransport(dir: str, db: str):
    json_files = [f'{dir}/{f}' for f in os.listdir(dir) if os.path.isfile(f'{dir}/{f}') and f.endswith('json')]
    if len(json_files) > 0:
        file_count = len(json_files)
        print(f'{file_count} files  found for ingestion, starting database init')
        connection = sql_connection(db)
        cursor = connection.cursor()
        print('Removing any old records')
        cursor.execute(transport_sql.rm_table_sql)
        connection.commit()
        print('Re-creating table')
        cursor.execute(transport_sql.create_table_sql)
        connection.commit()
        file_count = len(json_files) 
        print('Ingesting files...')
        for index, file in enumerate(json_files):
            with open(file) as json_file:
                print(f'Processing {file}...')
                data = json.load(json_file)
                records = data['data']
                df = pd.DataFrame.from_dict(records, orient='columns')
                records = [create_record(record) for _, record in df.iterrows() ]
                cursor.executemany(transport_sql.sql, records)
                connection.commit()
                print(f'Processed {len(records)} from {file}')
                print(f'{index + 1} files of {file_count} ingested')
        else:
            print('Ingest completed, verifing record counts...')
            count = cursor.execute(f'select count(*) from {tables.TRANSPORT};')
            print(f"Records Ingested: {count.fetchall()}")
            if (connection):
              connection.close()

    else:
        print(f'No files found for Annual Plan ingest at: {dir}') 
   

916.67