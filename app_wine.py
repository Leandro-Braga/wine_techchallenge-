import warnings

import pandas as pd
import pretty_errors
import streamlit as st
from PIL import Image

from data.function import mod_abrir_arquivo, mod_graficos

## --- ignorar avisos Pandas --- ##
warnings.filterwarnings('ignore')

### ---- GRUPO 16 ---- ###

# LEANDRO BRAGA ALVES
# leandro.bsbdf10@gmail.com

# Beatriz Lamarca Costa Camargo
# be.lamarcacc@gmail.com

# NADJO LISBOA DOS SANTOS JUNIOR
# nadjo.junior@ambevtech.com.br

# Rodrigo Mitsuo Yoshida
# rod.yoshida@gmail.com

# Roberto Yukio Ihara
# rihara@gmail.com

## --- Formatação de valores --- ##
pd.options.display.float_format = "{:.2f}".format

# -- imagens e logos -- #
img_wine = './data/img/vinho.png'
img_wine = Image.open(img_wine)

# --- Configurações da página 'Geral' --- #
st.set_page_config(
    page_title='EXPORTA VINHOS - BR',
    page_icon=img_wine,
    layout='wide',
    initial_sidebar_state='expanded',
    # initial_sidebar_state='collapsed',
    menu_items={
        'Get Help': 'https://www.google.com.br/',
        'Report a bug': "https://www.google.com.br/",
        'About': "Esse app foi desenvolvido pelo Grupo 16."
    }
)

# sidebar filtro dos paises

# criar abas de Exportação - Comércio - Produção - Processamento - Importação

aba1, aba2, aba3, aba4, aba5 = st.tabs(['Exportação', 'Comércio', 'Produção', 'Processamento', 'Importação'])

with aba1:
    st.header('Dados de Exportação avaliações de vinhos', divider='violet')
    st.markdown('**Exportação**: Todos os países que exportaram vinhos.')

    # lendo as tabelas
    df_exp_vinho_tab = mod_abrir_arquivo.exportacao()[0]
    df_pais_valor = mod_abrir_arquivo.pais_geral(df_exp_vinho_tab)


    st.markdown('**Gráfico de Países com maior :blue[exportação] de :violet[vinhos]:**')
    mod_graficos.grafico_pais_valortotal(df_pais_valor)

    df_pais_valor_maiores = df_pais_valor[['pais', 'valor_total']].sort_values(by='valor_total', ascending=False).head(10)
    df_pais_valor_maiores = df_pais_valor_maiores.rename(columns={'pais':'País', 'valor_total':'Valor Total'})
    df_pais_valor_maiores = df_pais_valor_maiores.set_index('País')
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('- **Gráfico de :blue[exportação] de :violet[vinhos] por ano:**')
        mod_graficos.grafico_ano_barra(df_exp_vinho_tab)
    with col2:
        st.markdown('- **10 Países com maior :blue[exportação] de :violet[vinhos]:**')
        st.table(df_pais_valor_maiores.style.format({'Valor Total': 'US$ {:.2f}'}))



with aba2:
    st.header('Dados de Comércio avaliações de vinhos', divider='violet')
    st.markdown('**Comércio**: Todos os países que vendem vinhos.')

with aba3:
    st.header('Dados de Produção avaliações de vinhos', divider='violet')
    st.markdown('**Produção**: Todos os países que produzem vinhos.')

with aba4:
    st.header('Dados de Processamento avaliações de vinhos', divider='violet')
    st.markdown('**Processamento**: Todos os países que processam vinhos.')

with aba5:
    st.header('Dados de Importação avaliações de vinhos', divider='violet')
    st.markdown('**Importação**: Todos os países que importam vinhos.')


