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

pais = './data/doc/pais.csv'

## -- Dataframes -- ##

# Exportação
@st.cache_data
def exportacao():
    df_exp_vinho = pd.read_csv(exp_vinho, delimiter=';')
    df_exp_espumante = pd.read_csv(exp_espumante, delimiter=';')
    df_exp_suco = pd.read_csv(exp_suco, delimiter=';')
    df_exp_uva = pd.read_csv(exp_uva, delimiter=';')

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


# importação
@st.cache_data
def importacao():
    df_imp_vinhos = pd.read_csv(imp_vinhos, delimiter=';')
    df_imp_espumante = pd.read_csv(imp_espumante, delimiter=';')
    df_imp_frescas = pd.read_csv(imp_frescas, delimiter=';')
    df_imp_passas = pd.read_csv(imp_passas, delimiter=';')
    df_imp_suco = pd.read_csv(imp_suco, delimiter=';')
    return df_imp_vinhos, df_imp_espumante, df_imp_frescas, df_imp_passas, df_imp_suco


# Processamento
@st.cache_data
def processamento():
    df_processa_viniferas = pd.read_csv(processa_viniferas, delimiter='\t')
    df_processa_americanas = pd.read_csv(processa_americanas, delimiter=';')
    df_processa_mesa = pd.read_csv(processa_mesa, delimiter=';')
    df_processa_sem_class = pd.read_csv(processa_sem_class, delimiter=';')
    return df_processa_viniferas, df_processa_americanas, df_processa_mesa, df_processa_sem_class


# produção
@st.cache_data
def producao_geral():
    df_producao = pd.read_csv(producao, delimiter=';')
    return df_producao


# Comercialização
@st.cache_data
def comercializacao():
    df_comercio = pd.read_csv(comercio, delimiter=';')
    return df_comercio


# base país
@st.cache_data
def pais_geral(df_exp_vinho_tab):

    df_pais = pd.read_csv(pais, delimiter=';', encoding='latin-1')

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
    filtro_paistotal = ['pais_ing', 'pais','valor_total']
    # filtro_paistotal = ['pais_ing', 'pais','valor_total', 'norm', 'cor']
    df_pais_valortotal_nomes = df_pais_valortotal_nomes[filtro_paistotal]


    return df_pais_valortotal_nomes




