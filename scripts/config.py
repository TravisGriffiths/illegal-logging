# These are the settings for all the scripts. Behavior and targets can be easily changed by changing values here

# Autex are the authorizations for forest exploration, logging permits, 
AUTEX_DIR       = 'Autex'
AUTEX_URL       = 'https://dadosabertos.ibama.gov.br/dados/DOF/DOFAutorizacoes/DOFAutorizacoes_json.zip'
DATA_DIR        = 'data-files'
DATABASE_DIR    = 'databases'
SQL_DATABASE    = 'forestry.db'
PMFS_DIR        = 'PMFS'
PMFS_URL        = 'https://dadosabertos.ibama.gov.br/dados/SINAFLOR/pmfs/AmazoniaLegal/pmfsAmazoniaLegal_json.zip'
# CNPJ is the Brazian Tax ID on a company, every legal company has one for tax purposes, these are published monthly 
CNPJ_URL        = 'https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj'
CNPJ_DIR        = 'CNPJ'
# Plans corrispond to Plano Operacional Anual (POA) - Annual Operating Plans 
PLANS_DIR       = 'plans'
PLANS_AMAZON_URL = "https://dadosabertos.ibama.gov.br/dados/SINAFLOR/poa/poaAmazoniaLegal/poaAmazoniaLegal_json.zip"
PLANS_OTHER_URL = "https://dadosabertos.ibama.gov.br/dados/SINAFLOR/poa/poaOutrosBiomas/poaOutrosBiomas_json.zip"
# Transport are the transportation records against Documento de Origem Florestal (DOF), Forest Origin Documentation system
TRANSPORT_DIR   = 'transport'
TRANSPORT_URL   = 'https://dadosabertos.ibama.gov.br/dados/DOF/DOFTransportes/DOFTransportes_json.zip'
PLOTS_DIR       = 'CAR'