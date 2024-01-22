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

# LEANDRO
# Beatriz
# NADJO
# Rodrigo
# Roberto

#########################

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

**:violet[Quem somos]:** 

- Somos Expert em Data Analytics em uma empresa de exportação de vinhos, responsável por apresentar relatórios iniciais em uma reunião de investidores e acionistas.
            
**:violet[Objetivo]:**
            
- Apresentar o montante de exportação nos últimos 15 anos, destacando análises por países, e fornecer perspectivas futuras com ações recomendadas para aprimorar as exportações. Utilizando de gráficos para facilitar a compreensão, permitindo que investidores e acionistas tomem decisões informadas para impulsionar a empresa.          
""")

st.markdown('**Fonte** - [Dados da Vitivinicultura](https://www.cnpuv.embrapa.br/vitibrazil/index.php?opcao=opt_02)')

aba1, aba2, aba3 = st.tabs(['🚢 Exportação', '📁 Tabela Origem e Destino','💳 Comércio'])


with aba1:
    st.header('Exportação de vinhos', divider='violet')

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
        
    col5, col6 = st.columns(2)

    with col5:  
        mod_graficos.grafico_linha_pais_qtd(df_exp_vinho_tab, pais)
    with col6:
        mod_graficos.grafico_linha_pais_valor(df_exp_vinho_tab, pais)


with aba2:

    st.header('Tabela de Exportação de vinhos', divider='violet') 
    st.markdown('**Exportação**: A tabela engloba todas as informações acerca da exportação de vinho, incluindo os países de destino.')
    st.write('- Exporação de vinho com origem (**:green[Brasil]**).')

    df_populacao_geral = mod_abrir_arquivo.populacao_geral_media()
    df_destino_tabela = mod_abrir_arquivo.destino_origem(df_populacao_geral, mod_abrir_arquivo.df_pais)

    df_destino_tabela_config = df_destino_tabela
    df_destino_tabela_config = df_destino_tabela_config.drop(columns=['ISO_code'])

    # Renomear colunas para melhorar a legibilidade da tabela
    df_destino_tabela_config.columns = ['País de Origem',
                                        'País de Destino',
                                        'Ano Exportação',
                                        'Vinho Exportado (Litros)',
                                        'Valor Exportado (US$)',
                                        'Pais de Destino Inglês',
                                        'Continente',
                                        'População do País',
                                        'Idade Média do País',
                                        'Densidade Populacional',
                                        'Razão de Sexo do País',
                                        'Litros por População',
                                        'Preço do Vinho (US$/Litro)']
    
    st.markdown('**:violet[**Filtros da tabela:**]**')
    mod_layout_base.selecao_dataframe(df_destino_tabela_config)


with aba3:
    st.header('Comércio de vinhos', divider='violet')
    st.markdown("""#### 💵 :green[**Dados econômicos:**]""")
    
    df_destino_tabela = mod_abrir_arquivo.destino_origem(df_populacao_geral, mod_abrir_arquivo.df_pais)
    df_cotacaov2 = mod_abrir_arquivo.cotacao_dolar(mod_abrir_arquivo.df_cotacao)

    col1, col2 = st.columns(2)

    st.markdown("""📈 A cotação do dólar desempenha um papel crucial nas exportações de vinhos em escala global. A variação na taxa de câmbio afeta diretamente o **custo dos vinhos exportados**, influenciando sua competitividade nos mercados internacionais.                             
    Quando a moeda do país produtor se **desvaloriza em relação ao dólar**, os vinhos tornam-se **mais acessíveis e atraentes para os compradores estrangeiros**, impulsionando as exportações.""")

    grafico = mod_graficos.grafico_cotacao(df_cotacaov2)

    st.divider()

    st.markdown('#### 🍷 :violet[**Comércio de vinho:**]')

    st.markdown("""📈 O preço médio de um vinho é uma **medida de acompanhamento e indicação do valor unitário do vinho**. Ao examinar o comércio de vinhos, é essencial observar a flutuação do preço mediano por litro ao longo dos anos, bem como a variação regional nesse aspecto.  Observar a variação regional no preço por litro é crucial para entender como **fatores como clima**, **solo** e técnicas de produção podem **influenciar os custos** e, consequentemente, os preços dos vinhos em diferentes partes do mundo.""")
    
    grafico = st.radio('**Selecione a visualização do preço mediano:**', ('Ano', 'Região'))

    if grafico == 'Ano':
        mod_graficos.grafico_linha_preco_mediano(df_destino_tabela)
    elif grafico == 'Região':
        mod_graficos.grafico_barra_preco_mediano(df_destino_tabela)
    
    st.divider()

    st.markdown("""#### 🗺️ :blue[**Exportação de vinho globalmente:**] """)
    st.markdown("""Os países que tem o maior mercado de vinhos e de varejo do mundo.
                Demonstrando os países que exportaram o maior valor (US$) de vinhos.""")
    
    var_valor_litros = st.toggle('**Litros / Valor**', ['Valor, Litros'], help='Se marcado o mapa irá exibir os **valores** totais de exportação, desmarcado exibe os **litros**.')
    
    mod_graficos.grafico_mapa_geral(df_destino_tabela, var_valor_litros)

    st.divider()

    st.markdown("""#### 🍇 :violet[**Tipos de vinhos mais comercializados:**]""")

    st.markdown("""📉 Ao analisar os tipos de vinhos mais comercializados, notamos uma tendência de crescimento no faturamento do **vinho de mesa** ao longo dos anos. Em **2005**, atingiu seu pico com **:blue[271 milhões]**, enquanto em **2021**, embora tenha reduzido para **:blue[210 milhões]**, ainda mantém uma posição significativa. (**:blue[Vendas em US dólar]**)""")

    dfcomercio = mod_abrir_arquivo.comercializacao()
    dfcoluna = dfcomercio

    coluna = grafico = st.radio('**Selecione o Tipo de Vinho:**', (dfcoluna.columns))

    mod_graficos.grafico_linha_comercio(dfcomercio, coluna)

    st.markdown("""📊 As vendas totais durante esse período foram lideradas pelo **vinho de mesa**, com **:blue[9.3 bilhões]**, seguido pelo Vinho Fino de Mesa com **:blue[1.4 bilhões]**. Além disso, os **vinhos especiais**, **frizantes** e **orgânicos** contribuíram com valores de **:blue[163 milhões]**, **:blue[31 milhões]** e **:blue[20 mil]**, respectivamente. Avaliações detalhadas desses tipos de vinhos oferecem insights valiosos sobre as preferências e tendências do mercado, fornecendo uma visão abrangente do panorama da indústria vinícola.
    (**:blue[Vendas em US dólar]**)""")

    mod_graficos.grafico_barra_comercio(dfcomercio)
    




