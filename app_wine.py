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

# Análise - Problema – Conclusão.
# Qual é o mercado que podemos explorar nos próximos anos?


#########################

## --- Formatação de valores --- ##
pd.options.display.float_format = "{:.2f}".format 

# -- imagens e logos -- #
img_wine = './data/img/vinho.png'
img_us = './data/img/estados-unidos.png'
img_rusia = './data/img/russia.png'
img_parag = './data/img/paraguai.png'
img_geral = './data/img/vinho_geral.png'
img_geralv2 = './data/img/vinho_geral_v2.jpg'

img_wine = Image.open(img_wine)
img_usa = Image.open(img_us)
img_ru = Image.open(img_rusia)
img_pa = Image.open(img_parag)
img_uva = Image.open(img_geral)
img_uvav2 = Image.open(img_geralv2)

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

**:violet[Quem Somos:]** 

- Somos Expert em Data Analytics em uma empresa de exportação de vinhos, responsável por apresentar relatórios iniciais em uma reunião de investidores e acionistas.
            
**:violet[Objetivo:]**
            
- Apresentar o montante de exportação nos últimos 15 anos, destacando análises por países, e fornecer perspectivas futuras com ações recomendadas para aprimorar as exportações. Utilizando de gráficos para facilitar a compreensão, permitindo que investidores e acionistas tomem decisões informadas para impulsionar a empresa.          
""")

st.markdown('**:violet[Data Base de Exportação:]**')
ultimos15anos_geral = st.toggle('**1970-2022 / últimos 15 anos**', ['1970-2022, últimos 15 anos'], help='Se marcado os gráficos irão exibir os **últimos 15 anos** de exportação, desmarcado exibem os anos entre **1970-2022**.')

# st.header(ultimos15anos_geral)

st.markdown('**Fonte** - [Dados da Vitivinicultura](https://www.cnpuv.embrapa.br/vitibrazil/index.php?opcao=opt_02)')

aba1, aba2, aba3, aba4 = st.tabs(['🚢 Exportação', '📁 Tabela Origem e Destino','💳 Comércio', '💡 Análise'])


with aba1:
    st.header('Exportação de vinhos', divider='violet')

    df_exp_vinho_tab = mod_abrir_arquivo.exportacao()
    # df_exp_vinho_tab = mod_abrir_arquivo.exportacao()[0]
    df_pais_valor = mod_abrir_arquivo.pais_geral_funcao(df_exp_vinho_tab, mod_abrir_arquivo.df_pais, ultimos15anos_geral)

    st.markdown('📊 Gráfico de Países com maior **:blue[exportação]** de **:violet[vinhos]:**')
    st.markdown("""
        **Tendências de Faturamento**:
        - 🌍 Países com as tonalidades :orange[avermelhadas] no mapa apresentam **maiores** faturamentos com a exportação de vinho enquanto os :blue[azulados] **menos**.

        **Crescimento da Exportação**:
        - 🍷 O valor da exportação de :violet[vinhos] tem aumentado mundialmente, indicando um crescimento geral no mercado durante o período de análise.

        **Principais Exportadores**:
        - 🔍 Paraguai, Rússia e Estados Unidos lideram em valor de exportações de vinho.
        """)
        
    mod_graficos.grafico_pais_valortotal(df_pais_valor, ultimos15anos_geral)

    # Mostrando os 10 países com maior exportação de vinhos + Brasil
    df_pais_valor_maiores = df_pais_valor[['pais', 'valor_total']].sort_values(by='valor_total', ascending=False).head(10)
    brasil_total = df_pais_valor[df_pais_valor['pais'] == 'Brasil'][['pais', 'valor_total']]
    df_pais_valor_maiores = pd.concat([df_pais_valor_maiores, brasil_total], axis=0) 
    df_pais_valor_maiores = df_pais_valor_maiores.rename(columns={'pais':'País', 'valor_total':'Valor Total'})
    df_pais_valor_maiores = df_pais_valor_maiores.set_index('País')

    col1, col2 = st.columns(2)

    if ultimos15anos_geral:
        valor_paraquai = 'US$ 38.719.031,00'
    else:
        valor_paraquai = 'US$ 85.606.168,00'

    with col1:
        st.markdown(f"""
        🔝 **Principais Exportadores**:
        - Paraguai, Rússia e Estados Unidos lideram em valor de exportações de vinho.

        💵 **Economia do Paraguai**:
        - Conforme tabela de países com o Paraguai à frente, exportando um total de {valor_paraquai}, seguido pelos Estados Unidos e Rússia.
        - A análise dos valores de exportação mostra que o Paraguai teve um maior valor de exportação, superando os Estados Unidos. Esse fenômeno pode ser explicado por vários fatores relacionados ao desempenho econômico e às relações comerciais entre os países.
        - Crescimento Econômico do Paraguai: A economia do Paraguai também registrou um crescimento significativo entre 2022 e 2023. O setor agrícola, particularmente a produção de soja, arroz, cana-de-açúcar e mandioca, foi um fator-chave nesse crescimento. O Paraguai experimentou um aumento na demanda externa por seus produtos.

        🗽 **Mercado dos EUA**:
        - Os EUA representam o maior mercado de varejo de vinhos e são um dos que mais crescem em consumo e produção. O mercado americano é majoritariamente ocupado por produtores locais. Algumas das maiores empresas produtoras de vinho do mundo estão localizadas nos Estados Unidos.
         """)
        
    with col2:
        st.markdown('- **Brasil em comparação com os 10 Países com maior :blue[exportação] de :violet[vinhos]:**')
        st.table(df_pais_valor_maiores.style.format({'Valor Total': 'US$ {:.2f}'}))
    
    st.divider()
    
    if ultimos15anos_geral:
        st.markdown('- 📈 **O crescimento da exportação geral no mundo por período entre 2008 e 2022.**')
    else:
        st.markdown('- 📈 **O crescimento da exportação geral no mundo por período entre 1970 e 2022.**')
    
    mod_graficos.grafico_ano_barra(df_exp_vinho_tab, ultimos15anos_geral)

    st.markdown('- 📈 As exportações têm apresentado crescimento nos últimos 7 anos. A oscilação nas exportações, não tem correlação com a produção de uvas no país, pois segunda a Embrapa a produção é crescente. Portanto, podemos buscar esse crescimento.')

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
        
        if pais == 'Paraguai':
            st.markdown("""* As exportações ao Paraguai representam 65,4% das exportações. Precisamos manter o relacionamento com nosso principal parceiro comercial, porém expandir para novos mercados potenciais.""")

        elif pais == 'Estados Unidos':
            st.markdown("""* Para entender melhor porque os EUA estão entre os maiores parceiros comerciais de vinhos em toda série histórica, precisamos analisar o comportamento ao longo de muitos anos.""")
        elif ultimos15anos_geral:
            st.markdown("""**1970 - 2022: As exportações aos Estados Unidos caíram muito no final da década de 90.**""")
            
    with col4:

        if ultimos15anos_geral:
            data_resumo = '2008 - 2022'
            data_resumo2 = 'A partir do ano de 2012 no geral'
        else:
            data_resumo = '1970 - 2022'
            data_resumo2 = 'A partir da década de 1980'

        st.markdown(f"""
            📋 **Resumo do Gráfico de Quantidade:**
            - **Período:** {data_resumo}
            - **Dados Representados:** Exportações de vinhos global.
            - **Crescimento Significativo:** {data_resumo2}, observa-se um aumento significativo nas exportações, atingindo picos notáveis em determinados anos.
            - **Variações Acentuadas:** Há variações acentuadas na quantidade de exportações ao longo do período analisado, indicando flutuações no mercado de vinhos ou na capacidade de exportação do país.
            - **Picos de Exportação:** Notam-se picos expressivos de exportação em alguns anos específicos, sugerindo eventos ou mudanças no mercado que impactaram positivamente as exportações.

            📶 **Gráfico de Exportação por Valor:** Complementa a análise, mostrando o valor monetário dessas exportações ao longo do mesmo período. Isso permiti avaliar não apenas o volume exportado, mas também como o valor das exportações de vinhos variou ao longo do tempo, oferecendo uma visão mais abrangente da importância econômica do setor para o país.
                    """)
        

    mod_graficos.grafico_linha_pais_qtd(df_exp_vinho_tab, pais, ultimos15anos_geral)
    mod_graficos.grafico_linha_pais_valor(df_exp_vinho_tab, pais, ultimos15anos_geral)


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
    mod_layout_base.selecao_dataframe(df_destino_tabela_config, ultimos15anos_geral)


with aba3:
    st.header('Comércio de vinhos', divider='violet')
    st.markdown("""#### 💵 :green[**Dados econômicos:**]""")
    
    df_destino_tabela = mod_abrir_arquivo.destino_origem(df_populacao_geral, mod_abrir_arquivo.df_pais)
    df_cotacaov2 = mod_abrir_arquivo.cotacao_dolar(mod_abrir_arquivo.df_cotacao)

    st.markdown("""📈 A cotação do dólar desempenha um papel crucial nas exportações de vinhos em escala global. A variação na taxa de câmbio afeta diretamente o **custo dos vinhos exportados**, influenciando sua competitividade nos mercados internacionais.                             
    Quando a moeda do país produtor se **desvaloriza em relação ao dólar**, os vinhos tornam-se **mais acessíveis e atraentes para os compradores estrangeiros**, impulsionando as exportações.""")

    grafico = mod_graficos.grafico_cotacao(df_cotacaov2, ultimos15anos_geral)

    st.markdown("""- Custo médio em Dólar sofrendo oscilação, mas em média se mantendo estável. Com a valorização do Dólar frente ao Real, a exportação fica mais atrativa.""")

    st.divider()

    st.markdown('#### 🍷 :violet[**Comércio de vinho:**]')

    st.markdown("""📈 O preço médio de um vinho é uma **medida de acompanhamento e indicação do valor unitário do vinho**. Ao examinar o comércio de vinhos, é essencial observar a flutuação do preço mediano por litro ao longo dos anos, bem como a variação regional nesse aspecto.  Observar a variação regional no preço por litro é crucial para entender como **fatores como clima**, **solo** e técnicas de produção podem **influenciar os custos** e, consequentemente, os preços dos vinhos em diferentes partes do mundo.""")
    
    grafico = st.radio('**Selecione a visualização do preço mediano:**', ('Ano', 'Região'))

    if grafico == 'Ano':
        mod_graficos.grafico_linha_preco_mediano(df_destino_tabela, ultimos15anos_geral)
    elif grafico == 'Região':
        mod_graficos.grafico_barra_preco_mediano(df_destino_tabela, ultimos15anos_geral)
    
    st.divider()

    st.markdown("""#### 🗺️ :blue[**Exportação de vinho globalmente:**] """)
    st.markdown("""Os países que tem o maior mercado de vinhos e de varejo do mundo.
                Demonstrando os países que exportaram o maior valor (US$) de vinhos.""")
    
    var_valor_litros = st.toggle('**Litros / Valor**', ['Valor, Litros'], help='Se marcado o mapa irá exibir os **valores** totais de exportação, desmarcado exibe os **litros**.')
    
    mod_graficos.grafico_mapa_geral(df_destino_tabela, var_valor_litros, ultimos15anos_geral)

    st.divider()

    if ultimos15anos_geral:
        vinho_mesa = '234 milhões'
        vinho_mesa_barra = '3.0 bilhões'
        Fino_Mesa_barra = '327 milhões'
        frizante = '25 milhões'
        especiais = '124 mil'
        organico = '18 mil'
    else:
        vinho_mesa = '271 milhões'
        vinho_mesa_barra = '9.3 bilhões'
        Fino_Mesa_barra = '1.4 bilhões'
        frizante = '31 milhões'
        especiais = '163 milhões'
        organico = '20 mil'

    st.markdown("""#### 🍇 :violet[**Tipos de vinhos mais comercializados:**]""")

    st.markdown(f"""📉 Ao analisar os tipos de vinhos mais comercializados, notamos uma tendência de crescimento no faturamento do **vinho de mesa** ao longo dos anos. Em **2005**, atingiu seu pico com **:blue[{vinho_mesa}]**, enquanto em **2021**, embora tenha reduzido para **:blue[210 milhões]**, ainda mantém uma posição significativa. (**:blue[Vendas em US dólar]**)""")

    dfcomercio = mod_abrir_arquivo.comercializacao()
    
    dfcoluna = dfcomercio

    coluna = st.radio('**Selecione o Tipo de Vinho:**', (dfcoluna.columns))
    # coluna = grafico = st.radio('**Selecione o Tipo de Vinho:**', (dfcoluna.columns))

    mod_graficos.grafico_linha_comercio(dfcomercio, coluna, ultimos15anos_geral)

    st.markdown(f"""- Nos últimos 15 anos queda na comercialização, mas que vem se recuperando fortemente nos últimos 2 anos analisados.""")
    st.markdown(f"""- Os vinhos orgânicos são bem novos no mercado, mas a procura cresce exponencialmente.""")
    st.markdown(f"""- Percebemos que a produção de orgânicos no mundo também vem crescendo, o que indica a aceitação desse tipo de produto em nível global.""")
    
    st.divider()
    
    st.markdown(f"""📊 As vendas totais durante esse período foram lideradas pelo **vinho de mesa**, com **:blue[{vinho_mesa_barra}]**, seguido pelo **vinho fino de mesa** com **:blue[{Fino_Mesa_barra}]**. Além disso, os **frizantes**, **vinhos especiais** e **orgânicos** contribuíram com valores de **:blue[{frizante}]**, **:blue[{especiais}]** e **:blue[{organico}]**, respectivamente. Avaliações detalhadas desses tipos de vinhos oferecem insights sobre as preferências e tendências do mercado.
    (**:blue[Vendas em US dólar]**)""")

    mod_graficos.grafico_barra_comercio(dfcomercio, ultimos15anos_geral)
    
with aba4:
    st.header('Análise Final', divider='violet')

    df_exp_top_paises = mod_abrir_arquivo.exporta_topn()
    lista_pais_topn = df_exp_top_paises['Pais'].unique()

    st.markdown('* **Selecione o país para visualizar nossa análise.**')

    pais_topn = st.radio('**Selecione o País:**', (lista_pais_topn))
    
    if pais_topn == 'Estados Unidos':
        st.markdown("""Não temos queda nas exportações gerais para esse período do final da década de 90, o que indica não temos problemas comerciais que possam impedir a exportação de vinhos com os **Estados Unidos**.""")

    elif pais_topn == 'Rússia':
        st.markdown("""A **Rússia** vem perdendo relacionamento nas exportações ao longo da ultima década, motivos globais e ainda com cenário atual de conflito, são sinais de receio para fortalecer o relacionamento, pelo menos por enquanto.""")

    else:
        st.markdown("""Temos um sólido relacionamento com o **Paraguai**, no total de exportações, considerando tudo o que é comercializado.""")


    mod_graficos.grafico_linha_topn_exportacao(df_exp_top_paises, pais_topn)


    col8, col9 = st.columns(2)

    with col8:
        if pais_topn == 'Estados Unidos':
            st.markdown("""Não percebemos queda no consumo por habitante, segundo estudo da Apex-Brasil no período do final da década de 90, mostrando inclusive, aumento significativo no consumo da bebida.
            O vinho representa cerca de 14% do mercado de bebidas alcoólicas dos EUA e é uma indústria de $72 bilhões. De acordo com o Wine Institute.
                        """)
            st.markdown('**Fonte** - [apexbrasil](https://www.apexbrasil.com.br/Content/imagens/10235c85-73e5-468d-9643-c2eb53a2be00.pdf)')
            st.markdown('**Fonte** - [www.gov.br](https://www.gov.br/empresas-e-negocios/pt-br/invest-export-brasil/exportar/conheca-os-mercados/pesquisas-de-mercado/estudo-de-mercado.pdf/EUAportuguesVinho.pdf)')

        elif pais_topn == 'Rússia':
            st.markdown("""A **Rússia** é o segundo país que mais importou nossos vinhos, porém, grandes quantidades por um curto período. Mas hoje os números são insignificantes.""")

        else:
            st.markdown("""Apesar de o **Paraguai** ser nosso maior parceiro comercial, ainda podemos observar um crescimento expressivo nas exportações. O que nos leva a concluir que temos alto potencial de crescimento nos parceiros menores. """)
    
    with col9:
        if pais_topn == 'Estados Unidos':
            st.markdown("""Segundo a Forbes, os incêndios na Califórnia, principal zona produtora de vinhos dos EUA, fazem a qualidade de seus vinhos e produtividade caírem. Isso pode apresentar uma oportunidade para oferecermos um pouco da nossa segurança com fornecimento dessa bebida.""")
            st.markdown('**Fonte** - [forbes](https://forbes.com.br/forbesagro/2022/10/como-o-clima-global-esta-mudando-a-producao-local-de-uvas-e-vinhos/)')
            
        elif pais_topn == 'Rússia':
            st.markdown("""O aumento em valor é ainda mais expressivo por conta da valorização do Dólar frente ao Real.""")

        else:
            st.markdown("""O aumento em valor é ainda mais expressivo por conta da valorização do Dólar frente ao Real.""")
            
    st.header('Considerações Finais', divider='violet')

    col10, col11 = st.columns(2)
    with col10:
        st.image(img_pa, width=80)
        st.markdown(f"""**:violet[Conclusão 1:]** Como o relacionamento como Paraguai já está estabelecido nas exportações gerais e a exportação de vinhos está em ascensão, além da proximidade geográfica que gera menos custos de transporte. Precisamos manter esse relacionamento e fortalece-lo ainda mais.""")
        st.image(img_usa, width=80)
        st.markdown(f"""**:violet[Conclusão 2:]** Os EUA já compraram muito dos nossos vinhos no final da década de 90 e como não temos motivos para não nos relacionarmos com eles, precisamos retomar essas exportações. Podemos aproveitar ainda as instabilidades climáticas enfrentadas por sua principal zona produtora de vinho, a Califórnia, que vem sofrendo com queimadas recorrentes ano após ano, afetando sua produção interna.""")
        st.image(img_uva, width=80)
        st.markdown("""**:violet[Conclusão 3:]** Baseando-se no aumento exponencial do consumo interno dos nosso vinhos orgânicos, consideramos também que a exportação desse produto seja uma ótima oportunidade. Já que a tendência de procura por produtos orgânicos é global.""")
    with col11:
        st.image(img_uvav2, width=600)

        





