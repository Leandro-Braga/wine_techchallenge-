import pandas as pd
import streamlit as st

# from streamlit_extras.dataframe_explorer import dataframe_explorer

## -- Arquivos base -- ##

# Exportação
exp_vinho = './data/doc/ExpVinho.csv'
exp_espumante = './data/doc/ExpEspumantes.csv'
exp_suco = './data/doc/ExpSuco.csv'
exp_uva = './data/doc/ExpUva.csv'

# importação
imp_espumante = './data/doc/ImpEspumantes.csv'
imp_frescas = './data/doc/ImpFrescas.csv'
imp_passas = './data/doc/ImpPassas.csv'
imp_suco = './data/doc/ImpSuco.csv'
imp_vinhos = './data/doc/ImpVinhos.csv'

# Processamento
processa_americanas = './data/doc/ProcessaAmericanas.csv'
processa_mesa = './data/doc/ProcessaMesa.csv'
processa_sem_class = './data/doc/ProcessaSemclass.csv'
processa_viniferas = './data/doc/ProcessaViniferas.csv'

# produção
producao = './data/doc/Producao.csv'

# Comercialização
comercio = './data/doc/Comercio.csv'

# paises e continentes
pais = './data/doc/pais.csv'
pais_geral = './data/doc/info_geral_paises.csv'

# cotacao dolar análise
cotacao = './data/doc/cotacao_dolar_ano.xlsx'

# demográfico da população
populacao = './data/doc/WPP2022_Demographic_Indicators_Medium.csv'


## -- Dataframes -- ##
df_exp_vinho = pd.read_csv(exp_vinho, delimiter=';')
df_exp_espumante = pd.read_csv(exp_espumante, delimiter=';')
df_exp_suco = pd.read_csv(exp_suco, delimiter=';')
df_exp_uva = pd.read_csv(exp_uva, delimiter=';')

# base país
# global df_pais
df_pais = pd.read_csv(pais, delimiter=';', encoding='latin-1')
df_pais_geral = pd.read_csv(pais_geral, delimiter=';', encoding='latin-1')

# df demográfico da população
df_populacao = pd.read_csv(populacao, delimiter=',')

# base cotação dolar
df_cotacao = pd.read_excel(cotacao)

# Exportação
@st.cache_data
def exportacao():

    # -- tratand a base df_exp_vinho -- #
    
    # Função para classificar com base no índice
    def classificar(index):
        if str(index).endswith('.1'):
            return 'valor'
        else:
            return 'quantidade'

    df_exp_vinho_qtde = df_exp_vinho.drop(columns={'Id'})

    # Filtrar colunas de quantidade e valor
    colunas_qtde = [col for col in df_exp_vinho_qtde.columns if not col.endswith('.1')]
    colunas_valor = [col for col in df_exp_vinho_qtde.columns if col.endswith('.1')]

    # Assegurar que 'País' não seja incluído nas somas
    colunas_qtde.remove('País')

    # Calcular a soma das quantidades e valores
    df_exp_vinho_qtde['qtde_total'] = df_exp_vinho_qtde[colunas_qtde].sum(axis=1)
    df_exp_vinho_qtde['valor_total'] = df_exp_vinho_qtde[colunas_valor].sum(axis=1)

    df_exp_vinho_tab = df_exp_vinho_qtde
    # filtro das colunas sem total 
    df_exp_vinho_tab = df_exp_vinho_tab.iloc[:, :-2]
    # renomeis o índice para Ano
    df_exp_vinho_tab = df_exp_vinho_tab.rename(columns={'País':'Ano'})
    # seta o índice para o ano
    df_exp_vinho_tab = df_exp_vinho_tab.set_index('Ano')
    # faz o transpose da tabela
    df_exp_vinho_tab = df_exp_vinho_tab.T

    # criação da coluna 'total_geral'
    df_exp_vinho_tab['total_geral'] = df_exp_vinho_tab.sum(axis=1)
    # cria uma classificação para 'quantidade' e para 'valor'
    df_exp_vinho_tab['classe'] = df_exp_vinho_tab.index.map(classificar)
    # alteração do índice do tipo string retirando o '.1'
    df_exp_vinho_tab.index = df_exp_vinho_tab.index.map(lambda x: x.replace('.1', ''))

    return df_exp_vinho_tab, df_exp_espumante, df_exp_suco, df_exp_uva


def populacao_geral_media():

    ### --- tabela populacao --- ##

    filtro_tab = ['Time','ISO3_code', 'TPopulation1Jan', 'MedianAgePop', 'PopDensity', 'PopSexRatio']
    df_populacao_filtro = df_populacao[filtro_tab]

    # renomeando colunas
    df_populacao_filtro.columns = 'ano', 'iso_code', 'populacao', 'idade_mediana', 'densidade_populacional', 'sexo_populacional'

    # filtro e tratamento dos dados
    df_populacao_geral = df_populacao_filtro[(df_populacao_filtro['iso_code'].notnull()) & (df_populacao_filtro['ano'] < 2023)]

    # renomeando colunas
    df_populacao_geral.columns = ['Ano', 
                                'iso_code',
                                'populacao', 
                                'idade_mediana', 
                                'densidade_populacional', 
                                'sexo_populacional']
    
    return df_populacao_geral


def destino_origem(df_populacao_geral, df_pais):

    # -- inicio da tabela de destino e origem com o 'df_exp_vinho' exportação -- #

    df_exp_vinho_qtde = df_exp_vinho.drop(columns={'Id'})

    # Filtrar colunas de quantidade e valor
    colunas_qtde = [col for col in df_exp_vinho_qtde.columns if not col.endswith('.1')]
    colunas_valor = [col for col in df_exp_vinho_qtde.columns if col.endswith('.1')]

    # Assegurar que 'País' não seja incluído nas somas
    colunas_qtde.remove('País')

    # Calcular a soma das quantidades e valores
    df_exp_vinho_qtde['qtde_total'] = df_exp_vinho_qtde[colunas_qtde].sum(axis=1)
    df_exp_vinho_qtde['valor_total'] = df_exp_vinho_qtde[colunas_valor].sum(axis=1)

    ########## Tabela destino e Origem #################

    # Lista de colunas que não são 'País', 'qtde_total' ou 'valor_total'
    colunas_anos = [col for col in df_exp_vinho_qtde.columns if col not in ['País', 'qtde_total', 'valor_total']]

    # Aplicando o melt
    df_melted = df_exp_vinho_qtde.melt(id_vars='País', value_vars=colunas_anos, var_name='Ano', value_name='Valor')

    # # Separando 'Ano' em 'Ano' e 'Tipo'
    df_melted['Tipo'] = df_melted['Ano'].str.endswith('.1')

    ## Removendo os .1 das colunas dos anos
    df_melted['Ano'] = df_melted['Ano'].astype(str).str.replace(r'\.1$', '', regex=True)

    # # Pivotando o DataFrame para ter colunas separadas para quantidade e valor total
    df_pivot = df_melted.pivot_table(index=['País', 'Ano'], columns='Tipo', values='Valor').reset_index()

    df_pivot.fillna(0.0, inplace=True) # alterando os dados NaN no dataframe

    ## Renomeando as colunas
    df_pivot.columns = ['País', 'Ano', 'Litros', 'Valor']

    ## Exibindo o DataFrame resultante
    df_pivot['Origem'] = 'Brasíl'
    filtro = ['Origem', 'País', 'Ano', 'Litros', 'Valor']
    df_filtrado = df_pivot[filtro]
    df_filtrado.columns = ['Origem', 'Destino', 'Ano', 'Litros', 'Valor']


    ############ Tratamento da base de pais geral com pais continente e iso3 ############

    df_pais_geral.columns = ['pais', 'iso_code', 'pais_ing', 'continent', 'cod_iso3']

    filtro_paisgeral = ['pais', 'continent']
    df_pais_geralv1 = df_pais_geral[filtro_paisgeral]
        
    filtro_pais = ['NO_PAIS', 'NO_PAIS_ING', 'CO_PAIS_ISOA3']

    df_pais = df_pais[filtro_pais]
    df_pais = df_pais.rename(columns={'NO_PAIS':'pais', 'NO_PAIS_ING':'pais_ing', 'CO_PAIS_ISOA3':'iso_code'})
    df_pais_continet = pd.merge(df_pais, df_pais_geralv1, how='left', on='pais')
    
    df_pais_continet.fillna('Não Definido', inplace=True) # Retira os NaN da coluna ISO_CODE

    # ajuste de nomes dos paises

    df_pais_continet.loc[df_pais_continet['pais'] == 'Alemanha', 'pais'] =  'Alemanha, República Democrática'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Belize', 'pais'] = 'Belice'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Coreia do Sul', 'pais'] = 'Coreia, Republica Sul'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Dubai', 'pais'] = 'Emirados Arabes Unidos'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Eslováquia', 'pais'] = 'Eslovaca, Republica'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Guiné-Bissau', 'pais'] = 'Guine Bissau'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Guiné Equatorial', 'pais'] = 'Guine Equatorial'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Virgens, Ilhas (Britânicas)', 'pais'] = 'Ilhas Virgens'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Índia', 'pais'] = 'India'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Namíbia', 'pais'] = 'Namibia'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Nicarágua', 'pais'] = 'Nicaragua'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Países Baixos (Holanda)', 'pais'] = 'Países Baixos'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Taiwan (Formosa)', 'pais'] = 'Taiwan (FORMOSA)'
    df_pais_continet.loc[df_pais_continet['pais'] == 'Trinidad e Tobago', 'pais'] = 'Trinidade Tobago'

    ## dataframe para adicionar outa linha
    df_singapura_col = ['pais','pais_ing','iso_code','continent'] 
    df_singapura_dado = ['Singapura','Singapore','SGP','Ásia']

    df_singapura = pd.DataFrame(columns=df_singapura_col, data=[df_singapura_dado])

    # Adicionando a linha ao DataFrame existente
    df_pais_continet = df_pais_continet.append(df_singapura, ignore_index=True)

    df_pais_continet.columns = ['Destino', 'pais_ing', 'iso_code', 'continent']
    df_exporta_paisv1 = pd.merge(df_filtrado, df_pais_continet, how='left', on='Destino')
    df_exporta_paisv1['Ano'] = df_exporta_paisv1['Ano'].astype('int64')
    
    df_exporta_paisv2 = pd.merge(df_exporta_paisv1, df_populacao_geral, how='left', on=['Ano', 'iso_code'])
    
    # Criando as colunas de 'litros por populacao' e 'preco por litro'
    df_exporta_paisv2['Litros_por_populacao'] = df_exporta_paisv2['Litros'] / df_exporta_paisv2['populacao']
    df_exporta_paisv2['Preco_por_litro'] = df_exporta_paisv2['Valor'] / df_exporta_paisv2['Litros']

    df_exporta_paisv2['Preco_por_litro'].fillna(0.0, inplace=True)

    # Renomeando as colunas e deixando na ordem correta
    df_exporta_paisv2.columns = ['Origem', 'Destino', 'Ano', 'Litros', 'Valor', 'Pais_Ing', 'ISO_code',
                             'Continente', 'Populacao', 'Idade_media', 'Densidade_populacional',
                             'Sexo_populacional', 'Litros_por_populacao', 'Preco_por_litro']
    

    # Lista de colunas em que você deseja substituir NaN por 0.0
    colunas_substituir_nan = ['Populacao', 'Idade_media', 'Densidade_populacional', 'Sexo_populacional',
                              'Litros_por_populacao', 'Preco_por_litro']

    # Substituir NaN por 0.0 nas colunas especificadas
    df_exporta_paisv2[colunas_substituir_nan] = df_exporta_paisv2[colunas_substituir_nan].fillna(0.0)

    return df_exporta_paisv2


def cotacao_dolar():
    print('nada ainda na cotação.')

# importação
# @st.cache_data
def importacao():
    df_imp_vinhos = pd.read_csv(imp_vinhos, delimiter=';')
    df_imp_espumante = pd.read_csv(imp_espumante, delimiter=';')
    df_imp_frescas = pd.read_csv(imp_frescas, delimiter=';')
    df_imp_passas = pd.read_csv(imp_passas, delimiter=';')
    df_imp_suco = pd.read_csv(imp_suco, delimiter=';')
    return df_imp_vinhos, df_imp_espumante, df_imp_frescas, df_imp_passas, df_imp_suco


# Processamento
# @st.cache_data
def processamento():
    df_processa_viniferas = pd.read_csv(processa_viniferas, delimiter='\t')
    df_processa_americanas = pd.read_csv(processa_americanas, delimiter=';')
    df_processa_mesa = pd.read_csv(processa_mesa, delimiter=';')
    df_processa_sem_class = pd.read_csv(processa_sem_class, delimiter=';')
    return df_processa_viniferas, df_processa_americanas, df_processa_mesa, df_processa_sem_class


# produção
# @st.cache_data
def producao_geral():
    df_producao = pd.read_csv(producao, delimiter=';')
    return df_producao


# Comercialização
# @st.cache_data
def comercializacao():
    df_comercio = pd.read_csv(comercio, delimiter=';')
    return df_comercio


# base país
# @st.cache_data
def pais_geral_funcao(df_exp_vinho_tab, df_pais):

    # df_pais = pd.read_csv(pais, delimiter=';', encoding='latin-1')

    # Recebe o df_exp_vinho_tab e cria uma coluna com o 'total_geral'
    # para ter o total por pais
    
    df_pais_valor = df_exp_vinho_tab[df_exp_vinho_tab['classe'] == 'valor']
    df_pais_valor = df_pais_valor.drop(columns={'total_geral','classe'})
    df_pais_valor = df_pais_valor.T
    df_pais_valor['valor_total'] = df_pais_valor.sum(axis=1)
    df_pais_valortotal = df_pais_valor[['valor_total']]
    df_pais_valortotal.reset_index(inplace=True)
    df_pais_valortotal = df_pais_valortotal.rename(columns={'Ano':'pais'})
    df_pais_valortotal.head()

    filtro_pais = ['NO_PAIS', 'NO_PAIS_ING']

    df_pais = df_pais[filtro_pais]

    df_pais = df_pais.rename(columns={'NO_PAIS':'pais', 'NO_PAIS_ING':'pais_ing'})
    df_pais_valortotal_nomes = pd.merge(df_pais_valortotal, df_pais, how='left', on='pais')
    filtro_paistotal = ['pais_ing', 'pais', 'valor_total']
    # filtro_paistotal = ['pais_ing', 'pais','valor_total', 'norm', 'cor']
    df_pais_valortotal_nomes = df_pais_valortotal_nomes[filtro_paistotal]

    return df_pais_valortotal_nomes





