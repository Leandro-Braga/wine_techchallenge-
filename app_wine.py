import warnings

import pandas as pd
import streamlit as st
from PIL import Image

from data.function import mod_abrir_arquivo, mod_graficos
from data.layout import mod_layout_base

## --- ignorar avisos Pandas --- ##
warnings.filterwarnings('ignore')

# URL: https://winetechchallengegrupo16.streamlit.app/

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
    page_title='EXPORTAÇÃO DE VINHOS',
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

# Fonte dos textos das abas
mod_layout_base.texto_diversos()

# sidebar filtro dos paises

# criar abas de Exportação - Comércio - Produção - Processamento - Importação

aba1, aba2, aba3, aba4, aba5 = st.tabs(['Exportação', 'Comércio'])
# aba1, aba2, aba3, aba4, aba5 = st.tabs(['Exportação', 'Comércio', 'Produção', 'Processamento', 'Importação'])

with aba1:
    st.header('Dados de Exportação de vinhos', divider='violet')

    # lendo as tabelas
    df_exp_vinho_tab = mod_abrir_arquivo.exportacao()[0]
    df_pais_valor = mod_abrir_arquivo.pais_geral(df_exp_vinho_tab)

    st.markdown('📊 Gráfico de Países com maior **:blue[exportação]** de **:violet[vinhos]:**')

    st.markdown("""
        **Tendências de Faturamento**:
        - 🌍 Países com tonalidades mais :red[avermelhadas] no mapa apresentaram maiores faturamentos com a exportação de vinho.

        **Crescimento da Exportação**:
        - 🍷 O valor da exportação de :violet[vinhos] tem aumentado mundialmente, indicando um crescimento geral no mercado durante o período de 2012 a 2022.

        **Principais Exportadores**:
        - 🔍 Paraguai, Rússia e Estados Unidos lideram em valor de exportações de vinho.
        """)
    
    st.markdown('Fonte - [Dados da Vitivinicultura](https://www.cnpuv.embrapa.br/vitibrazil/index.php?opcao=opt_02)')

    mod_graficos.grafico_pais_valortotal(df_pais_valor)


    # Mostrando os 10 países com maior exportação de vinhos + Brasil
    df_pais_valor_maiores = df_pais_valor[['pais', 'valor_total']].sort_values(by='valor_total', ascending=False).head(10)
    brasil_total = df_pais_valor[df_pais_valor['pais'] == 'Brasil'][['pais', 'valor_total']]
    df_pais_valor_maiores = pd.concat([df_pais_valor_maiores, brasil_total], axis=0) 
    df_pais_valor_maiores = df_pais_valor_maiores.rename(columns={'pais':'País', 'valor_total':'Valor Total'})
    df_pais_valor_maiores = df_pais_valor_maiores.set_index('País')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        🔝 **Principais Exportadores**:
        - Paraguai, Rússia e Estados Unidos lideram em valor de exportações de vinho.

        💵 **Economia do Paraguai**:
        - Conforme tabela de países com o Paraguai à frente, exportando um total de US$ 85.606.168,00, seguido pelos Estados Unidos e Rússia.
        - A análise dos valores de exportação mostra que o Paraguai teve um maior valor de exportação, superando os Estados Unidos. Esse fenômeno pode ser explicado por vários fatores relacionados ao desempenho econômico e às relações comerciais entre os países.
        - Crescimento Econômico do Paraguai: A economia do Paraguai também registrou um crescimento significativo entre 2022 e 2023. O setor agrícola, particularmente a produção de soja, arroz, cana-de-açúcar e mandioca, foi um fator-chave nesse crescimento. O Paraguai experimentou um aumento na demanda externa por seus produtos.

        🗽 **Mercado dos EUA**:
        - Os EUA representam o maior mercado de varejo de vinhos e são um dos que mais crescem em consumo e produção. O mercado americano é majoritariamente ocupado por produtores locais. Algumas das maiores empresas produtoras de vinho do mundo estão localizadas nos Estados Unidos.
         """)
        
    with col2:
        st.markdown('- **Brasil em comparação com os 10 Países com maior :blue[exportação] de :violet[vinhos]:**')
        st.table(df_pais_valor_maiores.style.format({'Valor Total': 'US$ {:.2f}'}))
    
    st.divider()
    
    st.markdown('- 📈 **O crescimento da exportação geral no mundo por período entre 1970 e 2022.**')
    mod_graficos.grafico_ano_barra(df_exp_vinho_tab)

    st.divider()

    ## Selecionar o pais para verificar o valor de exportação ##

    col3, col4 = st.columns(2)

    df_pais_valor_maioresV1 = df_pais_valor_maiores.reset_index()

    with col3:

        pais = st.selectbox('Selecione o País:', df_pais_valor_maioresV1['País'].unique())

        valor_pais = df_pais_valor_maioresV1[df_pais_valor_maioresV1['País'] == pais]['Valor Total'].astype(int)

        valor_pais = float(valor_pais)

        milao = 1000000

        valor_paisformatado = mod_graficos.formatar_como_moeda(valor_pais, milao)

        st.write(f"🌏 **:violet[{pais}]** tem o valor exportação de **{valor_paisformatado}**.")
        st.markdown("""
            Os gráficos que criamos mostram a variação das exportações de vinhos dos principais paises entre os anos de 1970 e 2022. Este gráfico oferece uma visão detalhada e histórica da evolução da exportação de vinhos do país selecionado, permitindo identificar padrões, picos e quedas ao longo do tempo.
                    """)
    with col4:
        st.markdown("""
            📋 **Resumo do Gráfico de Quantidade:**
            - **Período:** 1970 - 2022
            - **Dados Representados:** Exportações de vinhos global.
            - **Crescimento Significativo:** A partir da década de 1980, observa-se um aumento significativo nas exportações, atingindo picos notáveis em determinados anos.
            - **Variações Acentuadas:** Há variações acentuadas na quantidade de exportações ao longo do período analisado, indicando flutuações no mercado de vinhos ou na capacidade de exportação do país.
            - **Picos de Exportação:** Notam-se picos expressivos de exportação em alguns anos específicos, sugerindo eventos ou mudanças no mercado que impactaram positivamente as exportações.

            📶 **Gráfico de Exportação por Valor:** Complementa a análise, mostrando o valor monetário dessas exportações ao longo do mesmo período. Isso permiti avaliar não apenas o volume exportado, mas também como o valor das exportações de vinhos variou ao longo do tempo, oferecendo uma visão mais abrangente da importância econômica do setor para o país.
                    """)

    #######################################################

    # st.dataframe(df_pais_valor_maioresV1)

    mod_graficos.grafico_linha_pais_qtd(df_exp_vinho_tab, pais)

    st.divider()

    mod_graficos.grafico_linha_pais_valor(df_exp_vinho_tab, pais)




with aba2:
    st.header('Dados de Comércio para avaliações de vinhos', divider='violet')
    st.markdown('**Comércio**: Todos os países que vendem vinhos.')

# with aba3:
#     st.header('Dados de Produção de vinhos', divider='violet')
#     st.markdown('**Produção**: Todos os países que produzem vinhos.')

# with aba4:
#     st.header('Dados de Processamento de vinhos', divider='violet')
#     st.markdown('**Processamento**: Todos os países que processam vinhos.')

# with aba5:
#     st.header('Dados de Importação de vinhos', divider='violet')
#     st.markdown('**Importação**: Todos os países que importam vinhos.')


