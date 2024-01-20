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


st.markdown("""# **Tech Challenge: :violet[Exportação de Vinho]**

**:blue[Quem somos]:** 

Somos Expert em Data Analytics em uma empresa de exportação de vinhos, responsável por apresentar relatórios iniciais em uma reunião de investidores e acionistas.
            
**:blue[Objetivo]:**
            
Apresentar o montante de exportação nos últimos 15 anos, destacando análises por país, e fornecer perspectivas futuras com ações recomendadas para aprimorar as exportações. Utilizando de gráficos para facilitar a compreensão, permitindo que investidores e acionistas tomem decisões informadas para impulsionar a empresa.    
               
""")

st.markdown('**Fonte** - [Dados da Vitivinicultura](https://www.cnpuv.embrapa.br/vitibrazil/index.php?opcao=opt_02)')

aba1, aba2, aba3 = st.tabs(['🚢 Exportação', '📁 Tabela Origem e Destino','💳 Comércio'])


with aba1:
    st.header('Exportação de vinhos', divider='violet')

    # lendo as tabelas
    df_exp_vinho_tab = mod_abrir_arquivo.exportacao()[0]
    df_pais_valor = mod_abrir_arquivo.pais_geral_funcao(df_exp_vinho_tab, mod_abrir_arquivo.df_pais)

    st.markdown('📊 Gráfico de Países com maior **:blue[exportação]** de **:violet[vinhos]:**')

    st.markdown("""
        **Tendências de Faturamento**:
        - 🌍 Países com tonalidades :orange[avermelhadas] no mapa apresentam **maiores** faturamentos com a exportação de vinho enquanto os :blue[azulados] **menos**.

        **Crescimento da Exportação**:
        - 🍷 O valor da exportação de :violet[vinhos] tem aumentado mundialmente, indicando um crescimento geral no mercado durante o período de 2012 a 2022.

        **Principais Exportadores**:
        - 🔍 Paraguai, Rússia e Estados Unidos lideram em valor de exportações de vinho.
        """)
    

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

        pais = st.selectbox('**Selecione o País:**', df_pais_valor_maioresV1['País'].unique())

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

    st.header('Tabela de Exportação de vinhos', divider='violet') 
    st.write('- Exporação de vinho, origem (Brasil) e Países de destino.')

    st.markdown('**Exportação**: O dados da tabela contem todas as informações sobre a exportação de vinho e os paises de destino.')

    df_populacao_geral = mod_abrir_arquivo.populacao_geral_media()
    df_destino_tabela = mod_abrir_arquivo.destino_origem(df_populacao_geral, mod_abrir_arquivo.df_pais)

    st.dataframe(df_destino_tabela, hide_index=True,
                 column_config={'Litros_por_populacao': st.column_config.NumberColumn('Litros_por_populacao', format="U$ %.2f"),
                                'Preco_por_litro': st.column_config.NumberColumn('Preco_por_litro', format="U$ %.2f"),
                           "Ano": st.column_config.TextColumn("Ano")})
                        #    "Ano": st.column_config.TextColumn("Ano"),

    # teste = df_destino_tabela[df_destino_tabela['Pais_Ing'].isnull()]['Destino'].unique()
    # st.table(teste)

    st.header(f"Total exportação {df_destino_tabela['Valor'].sum()}")
    st.header(f"Total quantidade {df_destino_tabela['Litros'].sum()}")

    # df_destino_tabela['Ano'] = df_destino_tabela['Ano'].astype(int)
    # teste = df_destino_tabela[(df_destino_tabela['Preco_por_litro'] >= 0) & (df_destino_tabela['Ano'] == 2020)].groupby('Ano')[['Preco_por_litro']].mean()
    # st.dataframe(teste)




with aba3:
    st.header('Comércio de vinhos', divider='violet')
    
    # st.markdown('#### **Comércio**:')


    st.markdown("""#### 💵 :green[**Dados econômicos**]: Exploração dos fatores econômicos que influenciam as exportações de vinho.
                """)
    
    df_cotacaov2 = mod_abrir_arquivo.cotacao_dolar(mod_abrir_arquivo.df_cotacao)

    mod_graficos.grafico_cotacao(df_cotacaov2)

    st.markdown('#### 🍷 :violet[**Comercio de vinho**]: Preço mediano por litro.')
    
    grafico = st.radio('**Selecione a visualização do preço mediano:**', ('Ano', 'Região'))

    if grafico == 'Ano':
        mod_graficos.grafico_linha_preco_mediano(df_destino_tabela)
    elif grafico == 'Região':
        mod_graficos.grafico_barra_preco_mediano(df_destino_tabela)

    st.divider()

    st.markdown('#### **Avaliações de vinhos**:')


    st.markdown("""🗺️ :blue[**Exportação de vinho globalmente**]: Os países que tem o maior mercado de vinhos e de varejo do mundo.
                Demonstrando os países que exportaram o maior valor (US$) de vinhos.""")
    
    mod_graficos.grafico_mapa_geral(df_destino_tabela)

    st.markdown("""🍇 :violet[**Tipos de vinhos mais comercializados**]: Consideração das avaliações para entender preferências e tendências de mercado.""")

    dfcomercio = mod_abrir_arquivo.comercializacao()

    # dfcoluna = dfcomercio.drop(columns=['Ano'])
    dfcoluna = dfcomercio

    # st.dataframe(dfcoluna.columns)

    coluna = grafico = st.radio('**Selecione o Tipo de Vinho:**', (dfcoluna.columns))

    mod_graficos.grafico_linha_comercio(dfcomercio, coluna)

    st.divider()

    mod_graficos.grafico_barra_comercio(dfcomercio)
    




