import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter


def formatar_como_moeda(valor, divisor_casas):
    # Ajuste da formatação de moeda
    return f'US$ {valor/divisor_casas:,.2f}{"MM" if valor >= 1000000 else "M"}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def formatar_como_quantidade(valor, divisor_casas):
    # Ajuste da formatação de moeda
    return f'{valor/divisor_casas:,.2f}{"MM" if valor >= 1000000 else "M"}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def billion_formatter(x, pos):
    bilao = 1000000000
    milao = 1000000
    # return f'R${x/bilao if x >= bilao else milao:.1f}{"B" if x >= bilao else "MM"}'
    return f'US${x/milao:,.2f}{"B" if x >= 1000000000 else "MM"}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def grafico_pais_valortotal(df, ultimos15anos_geral):
    
    if ultimos15anos_geral:
        data_titulo = '(2008-2022)'
    else:    
        data_titulo = '(1970-2022)'

    # Criando o gráfico de mapa com uma escala de cores contínua
    fig = px.choropleth(
        df,
        locations='pais_ing',  
        locationmode='country names',
        color='valor_total', 
        hover_name='pais',
        hover_data={'valor_total': ':$.2f'},
        labels={'valor_total': 'Preço'},
        color_continuous_scale=['#4682A9', '#F9B572', '#F45050'], 
        title=f'Preço Exportação (US$) por Região {data_titulo} ',
        color_discrete_sequence=['#910A67'],
    )

    # tamanho do gráfico
    fig.update_layout(
        width=1200,
        height=800,
        
        # Configurar o tamanho da fonte do título
        title_font=dict(size=20),
        
        # Configurar o tamanho da linha
        showlegend=True, 
        legend=dict(font=dict(size=20)),  # Tamanho da fonte na legenda

    )

    fig.update_traces(
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#146C94',  
            font=dict(family='Arial', size=12, color='white'),  
        ),
    )

    st.plotly_chart(fig)


def grafico_ano_barra(df, ultimos15anos_geral):

    # Constantes para bilhão e milhão
    bilhao = 1000000000
    milao = 1000000

    try:
        if ultimos15anos_geral:
            df = df[df['classe'] == 'valor'].tail(15)
        else:
            df = df[df['classe'] == 'valor']
        # Filtrando por 'classe' e garantindo que 'total_geral' é numérico
        df = df[df['classe'] == 'valor'][['total_geral']].astype(int)

        # Calculando a média dos gastos
        media_gastos = df['total_geral'].mean()

        # Criando o gráfico com a linha de média e rótulos de valor
        plt.figure(figsize=(10, 3))
        sns.barplot(x=df.index, y=df['total_geral'], palette="viridis")

        if len(df) > 1:
            plt.text(len(df) - 1, media_gastos, f'Média: {formatar_como_moeda(media_gastos, milao)}', 
                    color='red', ha="right", va="bottom")
            plt.axhline(media_gastos, color='red', linestyle='--')

        plt.title('Total de Exportação por Ano', fontsize=10)
        plt.xlabel('Ano', fontsize=8)
        plt.ylabel('Total', fontsize=8)
        plt.xticks(rotation=45)

        # Alterando o tamanho dos rótulos nos eixos X e Y
        plt.tick_params(axis='both', which='major', labelsize=7)
        
        # Alterando a cor de fundo do grid
        # plt.grid(True, color='#f0f0f0')

        # Alterando a cor de fundo do espaço do gráfico
        # plt.gca().set_facecolor('#F3F8FF')
        plt.gca().set_facecolor('white')

        plt.grid(True, axis='y', linestyle='--', linewidth=0.7, color='gray')
        
        # Função para formatar
        plt.gca().yaxis.set_major_formatter(FuncFormatter(billion_formatter))

        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        st.pyplot(plt)
    except:
        st.warning('Atualizar a página!')


def grafico_linha_pais_qtd(df_exp_vinho_tab, coluna, ultimos15anos_geral):

    if ultimos15anos_geral:
        df_qtd = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'quantidade'][[coluna]].tail(15)
        data_titulo = '(2008-2022)'
    else:
        df_qtd = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'quantidade'][[coluna]]
        data_titulo = '(1970-2022)'

    df_qtd = df_qtd.reset_index()
    df_qtd = df_qtd.rename(columns={'index':'Ano'})

    # Criar o gráfico de linha com Plotly Express
    fig = px.line(
        df_qtd,
        x='Ano',
        y=coluna,
        hover_data=coluna,
        markers=True,
        labels={coluna: coluna},
        title=f'Exportações por Quantidade de Vinhos do {coluna} {data_titulo}',
        line_shape='spline',  # curvatura da linha (linear, spline, hv, vh, hvh, vhl)
        line_dash_sequence=['solid'],  # estilo da linha
        color_discrete_sequence=['#910A67'], # cor da linha
        # text='cotacao_dolar' ## - Rotulos por coluna 
    )


    # Adicionar título e rótulos dos eixos
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title=coluna,
        yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar
        plot_bgcolor="white",

        # Configurar o tamanho da fonte do título
        title_font=dict(size=18),
        
        # Configurar o tamanho da linha
        showlegend=True,  
        legend=dict(font=dict(size=16)),  # Tamanho da fonte na legenda

        # Configurar a cor de fundo
        # paper_bgcolor='#DCF2F1',
        # paper_bgcolor='#000000',
        
        # Configurar a cor das linhas do grid no eixo X e Y
        # xaxis=dict(gridcolor='red'),
        # yaxis=dict(gridcolor='#3B3486'),
        
        # Tamanho do gráfico
        width=1100,
        height=500,

        # Configurar cor e tamanho da fonte dos rótulos dos eixos

        xaxis=dict( # xaxis=dict(gridcolor='red'), 
            title=dict(text='Ano', font=dict(size=16, color='#3B3486')), 
            tickfont=dict(size=14, color='#3B3486')
        ),

        yaxis=dict(gridcolor='#3B3486',
            title=dict(text="Quantidade", font=dict(size=16, color='#3B3486')), 
            tickfont=dict(size=14, color='#3B3486'),
            tickprefix='US$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        line=dict(width=4),  
        marker=dict(size=8), 
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#3C0753',  
            font=dict(family='Arial', size=16, color='white'),
        ),
    )

    st.plotly_chart(fig)


def grafico_linha_pais_valor(df_exp_vinho_tab, coluna, ultimos15anos_geral):

    if ultimos15anos_geral:
        df_valor = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'valor'][[coluna]].tail(15)
        data_titulo = '(2008-2022)'
    else:
        df_valor = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'valor'][[coluna]]
        data_titulo = '(1970-2022)'

    # df_qtd = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'quantidade'][[coluna]]

    df_valor = df_valor.reset_index()
    df_valor = df_valor.rename(columns={'index':'Ano'})

    # st.dataframe(df_valor)

    # Criar o gráfico de linha com Plotly Express
    fig = px.line(
        df_valor,
        x='Ano',
        y=coluna,
        hover_data=coluna,
        markers=True,
        labels={coluna: coluna},
        title=f'Exportações por Valor de Vinhos do {coluna} {data_titulo}',
        line_shape='spline',  # curvatura da linha (linear, spline, hv, vh, hvh, vhl)
        line_dash_sequence=['solid'],  # estilo da linha
        color_discrete_sequence=['#910A67'], # cor da linha
        # text='cotacao_dolar'  
    )

    # Adicionar título e rótulos dos eixos
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title=coluna,
        yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar 
        plot_bgcolor="white",

        # Configurar o tamanho da fonte do título
        title_font=dict(size=18),
        
        # Configurar o tamanho da linha
        showlegend=True,  # mostre a correta
        legend=dict(font=dict(size=16)),  # Tamanho da fonte na legenda

        # Configurar a cor de fundo
        # paper_bgcolor='#DCF2F1',  
        # paper_bgcolor='#000000',  
        
        # Configurar a cor das linhas do grid no eixo X e Y
        # xaxis=dict(gridcolor='red'),  
        # yaxis=dict(gridcolor='#3B3486'),  
        
        # Tamanho do gráfico
        width=1100,
        height=500,

        # Configurar cor e tamanho da fonte dos rótulos dos eixos

        xaxis=dict( # xaxis=dict(gridcolor='red'),  
            title=dict(text='Ano', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486')
        ),

        yaxis=dict(gridcolor='#3B3486',
            title=dict(text='Exportações', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486'),
            tickprefix='US$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        line=dict(width=4),  
        marker=dict(size=8),

        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#3C0753',
            font=dict(family='Arial', size=16, color='white'),
        ),
    )

    st.plotly_chart(fig)


def grafico_cotacao(df_cotacao, ultimos15anos_geral):

    if ultimos15anos_geral:
        df_cotacao = df_cotacao.sort_values(by='Data').tail(15)
        titulo_data = '2009 - 2023'
    else:
        df_cotacao = df_cotacao.sort_values(by='Data')
        titulo_data = '1994 - 2023'


    fig = px.line(
        df_cotacao,
        x='Data',
        y='Cotação Dólar',
        hover_data={'Cotação Dólar': ':$.2f'},
        markers=True,
        labels={'Cotação Dólar': 'Cotação do Dólar'},
        title=f'Variação da Cotação do Dólar ao Longo dos Anos entre {titulo_data}',
        line_shape='spline',  # a curvatura da linha (linear, spline, hv, vh, hvh, vhl)
        line_dash_sequence=['solid'],  # o estilo da linha
        color_discrete_sequence=['#910A67'], # a cor da linha
        # text='Cotação Dólar'  
    )

    # Adicionar título e rótulos dos eixos
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Cotação do Dólar',
        yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar
        plot_bgcolor="white",

        # Configurar o tamanho da fonte do título
        title_font=dict(size=18),
        
        # Configurar o tamanho da linha
        showlegend=True,  # a legenda mostre a correta
        legend=dict(font=dict(size=16)),  # Tamanho da fonte na legenda

        # Configurar a cor de fundo
        # paper_bgcolor='#DCF2F1',  
        # paper_bgcolor='#000000',  
        
        # Configurar a cor das linhas do grid no eixo X e Y
        # xaxis=dict(gridcolor='red'),  
        # yaxis=dict(gridcolor='#3B3486'),  
        
        # Tamanho do gráfico
        # width=1200,
        width=1100,
        height=500,

        # Configurar cor e tamanho da fonte dos rótulos dos eixos

        xaxis=dict( # xaxis=dict(gridcolor='red'),  
            title=dict(text='Ano', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486')
        ),

        yaxis=dict(gridcolor='#3B3486',
            title=dict(text='Cotação do Dólar', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486'),
            tickprefix='US$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        line=dict(width=4),  
        marker=dict(size=8), 
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#3C0753', 
            font=dict(family='Arial', size=16, color='white'), 
        ),
    )

    # Exibir o gráfico
    # fig.show()

    st.plotly_chart(fig)


def grafico_linha_preco_mediano(df_destino_tabela, ultimos15anos_geral):

    if ultimos15anos_geral:
        ultimos15 = df_destino_tabela[(df_destino_tabela['Preco_por_litro'] > 0) & (df_destino_tabela['Ano'] >= 2008)].sort_values(by='Ano')
        titulo_texto = '2008 - 2022'
    else:
        ultimos15 = df_destino_tabela[df_destino_tabela['Preco_por_litro'] > 0]
        titulo_texto = '1970 - 2022'

    # st.dataframe(ultimos15)

    df_aux19 = ultimos15.groupby(['Ano'])[['Preco_por_litro']].mean().reset_index().sort_values(by='Ano', ascending=False)
    # df_aux19 = df_destino_tabela[df_destino_tabela['Preco_por_litro'] > 0].groupby(['Ano'])[['Preco_por_litro']].mean().reset_index().sort_values(by='Ano', ascending=False)

    df_aux19 = df_aux19.rename(columns={'Preco_por_litro': 'Preço por Litro'})

    # st.dataframe(df_aux19)

    fig = px.line(df_aux19, 
                  x="Ano", 
                  y="Preço por Litro",
                  hover_data={'Preço por Litro': ':$.2f'},
                  markers=True,
                  labels={'Preço por Litro': 'Preço por Litro'},
                  title=f'Preço por Litro Mediano por Ano entre {titulo_texto}',
                  line_shape='spline',
                  line_dash_sequence=['solid'],
                  color_discrete_sequence=['#910A67']
                  )


 # Adicionar título e rótulos dos eixos
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Preço por Litro',
        yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar
        plot_bgcolor="white",

        # Configurar o tamanho da fonte do título
        title_font=dict(size=18),
        
        # Configurar o tamanho da linha
        showlegend=True,  
        legend=dict(font=dict(size=16)),  # Tamanho da fonte na legenda

        # Configurar a cor de fundo
        # paper_bgcolor='#DCF2F1',  
        # paper_bgcolor='#000000',  
        
        # Configurar a cor das linhas do grid no eixo X e Y
        # xaxis=dict(gridcolor='red'),  
        # yaxis=dict(gridcolor='#3B3486'),  
        
        # Tamanho do gráfico
        width=1100,
        height=500,

        # Configurar cor e tamanho da fonte dos rótulos dos eixos

        xaxis=dict( # xaxis=dict(gridcolor='red'),  
            title=dict(text='Ano', font=dict(size=16, color='#3B3486')), 
            tickfont=dict(size=14, color='#3B3486')
        ),

        yaxis=dict(gridcolor='#3B3486',
            title=dict(text='Preço por Litro', font=dict(size=16, color='#3B3486')), 
            tickfont=dict(size=14, color='#3B3486'),
            tickprefix='US$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        line=dict(width=4),  
        marker=dict(size=8),  
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#3C0753',
            font=dict(family='Arial', size=16, color='white'),  
        ),
    )

    st.plotly_chart(fig)


def grafico_barra_preco_mediano(df_destino_tabela, ultimos15anos_geral):

    if ultimos15anos_geral:
        ultimos15 = df_destino_tabela[(df_destino_tabela['Preco_por_litro'] > 0) & (df_destino_tabela['Ano'] >= 2008)].sort_values(by='Ano')
        titulo_texto = '2008 - 2022'
    else:
        ultimos15 = df_destino_tabela[df_destino_tabela['Preco_por_litro'] > 0]
        titulo_texto = '1970 - 2022'

    df_aux20 = ultimos15.groupby(['Continente'])[['Preco_por_litro']].mean().reset_index().sort_values(by='Preco_por_litro', ascending=False)
    # df_aux20 = df_destino_tabela[df_destino_tabela['Preco_por_litro'] > 0].groupby(['Continente'])[['Preco_por_litro']].mean().reset_index().sort_values(by='Preco_por_litro', ascending=False)

    df_aux20 = df_aux20.rename(columns={'Preco_por_litro': 'Preço por Litro'})

    fig = px.bar(df_aux20, 
                 x="Continente", 
                 y="Preço por Litro",
                 hover_data={'Preço por Litro': ':$.2f'},
                 labels={'Preço por Litro': 'Preço por Litro'},
                 title=f'Preço por Litro (US$) Mediano por Região entre {titulo_texto}',
                 color_discrete_sequence=['#910A67'],
                                 
                 )
    
    
 # Adicionar título e rótulos dos eixos
    fig.update_layout(
        xaxis_title='Continente',
        yaxis_title='Preço por Litro',
        yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar
        plot_bgcolor="white",

        # Configurar o tamanho da fonte do título
        title_font=dict(size=18),
        
        # Configurar o tamanho da linha
        showlegend=True,  
        legend=dict(font=dict(size=16)),  # Tamanho da fonte na legenda

        # Configurar a cor de fundo
        # paper_bgcolor='#DCF2F1',  
        # paper_bgcolor='#000000',  
        
        # Configurar a cor das linhas do grid no eixo X e Y
        # xaxis=dict(gridcolor='red'), 
        # yaxis=dict(gridcolor='#3B3486'), 
        
        # Tamanho do gráfico
        width=1100,
        height=500,

        # Configurar cor e tamanho da fonte dos rótulos dos eixos
        xaxis=dict( # xaxis=dict(gridcolor='red'), 
            title=dict(text='Continente', font=dict(size=16, color='#3B3486')), 
            tickfont=dict(size=14, color='#3B3486')
        ),

        yaxis=dict(gridcolor='#3B3486',
            title=dict(text='Preço por Litro', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486'),
            tickprefix='US$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#3C0753', 
            font=dict(family='Arial', size=16, color='white'), 
        ),
    )

    st.plotly_chart(fig)


def grafico_layout_mapa(
    fig: px,
    template: str = "seaborn",
    width: int = 1300,
    height: int = 500,
    margin: dict = {"l": 10, "r": 10, "b": 10, "t": 85, "pad": 5},
    legend: dict = {
        "orientation": "v",
        "yanchor": "middle",
        "xanchor": "center",
        "x": 1,
        "y": 0.5,
        "title": "",
        "itemsizing": "constant",
    },
        
    xaxis: dict = {"title": ""},
    yaxis: dict = {"title": ""},
    hovertemplate: str = "<b>%{x}</b><br>%{y}",
    title_text = "-",
    title_sup = "--",
    marker_color = '',
    line_color = '',
    other: dict = dict(),
) -> None:
    dic = dict(
        template=template,
        width=width,
        height=height,
        margin=margin,
        legend=legend,
        xaxis=xaxis,
        yaxis=yaxis,
        title={
            'text': f'{title_text}<br><sup style="color: #3B3486; font-weight: normal;">{title_sup}</sup>',
            'xanchor': 'left',
            'xref': 'paper',
            'yanchor': 'auto',
            'x': 0,
            'y': .95,
            'font': {
                'size': 20,
                'color': '#3B3486'
            }
        },
    )

    fig.update_layout(dic | other)
    
    if marker_color != '':
        fig.update_traces(marker_color = marker_color)
    if line_color != '':
        fig.update_traces(line_color = line_color)
    
    fig.update_traces(hovertemplate=hovertemplate)

    return st.plotly_chart(fig)


def grafico_mapa_geral(df_destino_tabela,var_valor_litros, ultimos15anos_geral):

    if var_valor_litros:
        var = "Valor"
    else:
        var = "Litros"

    if ultimos15anos_geral:
        ultimos15 = df_destino_tabela[(df_destino_tabela["Ano"] > 0) & (df_destino_tabela['Ano'] >= 2008)].sort_values(by='Ano')
        titulo_texto = '2008 - 2022'
    else:    
        ultimos15 = df_destino_tabela[df_destino_tabela["Ano"] > 0]
        titulo_texto = '1970 - 2022'

    # st.dataframe(ultimos15)

    df_aux5v2 = ultimos15.groupby(['Continente','ISO_code', 'Destino'])[[var]].sum().reset_index().sort_values(by='Continente', ascending=False)

    # df_aux5v2 = df_destino_tabela[df_destino_tabela["Ano"] > 0].groupby(['Continente','ISO_code', 'Destino'])[[var]].sum().reset_index().sort_values(by='Continente', ascending=False)

    fig = px.scatter_geo(
            df_aux5v2,
            locations="ISO_code",
            size=var,
            color="Continente",
            projection="natural earth",
            size_max=30,
            custom_data=["Destino", var],
            color_discrete_map={
                "Oceania": "#636EFA",
                "América Central e Caribe": "#C70039",
                "América do Norte": "#362FD9",
                "África": "#AB63FA",
                "Europa": "#CD5C08",
                "Oriente Médio": "#19D3F3",
                "América do Sul": "#1B4242",
                "Ásia": "#FF6692",
            },
        )
    
    fig.update_layout(
    legend=dict(
        font=dict(size=18, color="#3C0753"),  # Configurar tamanho e cor da fonte da legenda
    )
    )

    # Configurar o tamanho do texto do hover_data
    fig.update_traces(
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#146C94',  
            font=dict(family='Arial', size=12, color='white'),  
        ),
    )

    grafico_layout_mapa(
            fig,
            yaxis={"title":f"Total Exportado em {var} - (US$)"},
            xaxis={"title":"Continente"},
            hovertemplate="<b>%{customdata[0]}</b><br>Total: U$ %{customdata[1]}",
            legend={
                "orientation": "h",
                "yanchor": "middle",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.1,
                "title": "",
                "itemsizing": "constant",
            },
            title_text=f"Total Exportado em {var} - (US$) por Continente entre {titulo_texto}",
            title_sup=f"Mapa exibindo o {var} total de vinho exportado (em US$) para cada Continente"
    )


def grafico_linha_comercio(dfcomercio, coluna, ultimos15anos_geral):

    # dfcomercio = dfcomercio

    if ultimos15anos_geral:
        dfcomercio['Ano'] = dfcomercio['Ano'].astype(int)
        ultimos15 = dfcomercio[dfcomercio['Ano'] >= 2007]
        titulo_ano = '2007 - 2021'
    else:
        dfcomercio['Ano'] = dfcomercio['Ano'].astype(int)
        ultimos15 = dfcomercio[dfcomercio['Ano'] > 0]
        titulo_ano = '1970 - 2021'

    if coluna == 'Ano':
        fig = px.line(
            ultimos15,
            x="Ano",
            y=ultimos15.columns[1:],
            title=f'Vendas por Ano entre {titulo_ano}',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            markers=True,
        )
        # Adicionar título e rótulos dos eixos
        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title='Vendas por Ano',
            yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar 
            plot_bgcolor="white",

            # Configurar o tamanho da fonte do título
            title_font=dict(size=18),
            
            # Configurar o tamanho da linha
            showlegend=True, 

            legend=dict(
            title=dict(text="Tipos de Vinhos", font=dict(size=16, color="#3B3486")),  # Configurar título da legenda
            font=dict(size=14, color="#3B3486"),  # Configurar tamanho e cor da fonte da legenda
            ),
            
            # Tamanho do gráfico
            width=1100,
            height=500,

            # Configurar cor e tamanho da fonte dos rótulos dos eixos
            xaxis=dict( # xaxis=dict(gridcolor='red'),  
                title=dict(text='Ano', font=dict(size=16, color='#3B3486')),  
                tickfont=dict(size=14, color='#3B3486')
            ),

            yaxis=dict(gridcolor='#3B3486',
                title=dict(text='Vendas por Ano', font=dict(size=16, color='#3B3486')),  
                tickfont=dict(size=14, color='#3B3486'),
                tickprefix='US$ ',
            ),
        )

        # Configurar o tamanho da linha
        fig.update_traces(
            line=dict(width=4),  
            marker=dict(size=8),  
            # Configurar a cor e a fonte do hover_data
            hoverlabel=dict(
                bgcolor='#3C0753',  
                font=dict(family='Arial', size=16, color='white'), 
            ),
        )
    else:
        # Gráfico de Linha por Ano
        fig = px.line(ultimos15, 
                            x='Ano', 
                            y=coluna, 
                            title=f'Vendas de {coluna} por Ano entre {titulo_ano}',
                            hover_data={coluna: ':$.2f'},
                            markers=True,
                            line_shape='spline',
                            line_dash_sequence=['solid'],
                            color_discrete_sequence=['#910A67']
                            
                            )

        # Adicionar título e rótulos dos eixos
        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title='Vendas por Ano',
            yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar 
            plot_bgcolor="white",

            # Configurar o tamanho da fonte do título
            title_font=dict(size=18),
            
            # Configurar o tamanho da linha
            showlegend=True,  
            legend=dict(font=dict(size=16)),  # Tamanho da fonte na legenda
            
            # Tamanho do gráfico
            width=1100,
            height=500,

            # Configurar cor e tamanho da fonte dos rótulos dos eixos
            xaxis=dict( # xaxis=dict(gridcolor='red'),  # ajustar para a cor desejada
                title=dict(text='Ano', font=dict(size=16, color='#3B3486')),  
                tickfont=dict(size=14, color='#3B3486')
            ),

            yaxis=dict(gridcolor='#3B3486',
                title=dict(text='Vendas por Ano', font=dict(size=16, color='#3B3486')),  
                tickfont=dict(size=14, color='#3B3486'),
                tickprefix='US$ ',
            ),
        )

        # Configurar o tamanho da linha
        fig.update_traces(
            line=dict(width=4),  
            marker=dict(size=8),  
            # Configurar a cor e a fonte do hover_data
            hoverlabel=dict(
                bgcolor='#3C0753',  
                font=dict(family='Arial', size=16, color='white'), 
            ),
        )

    st.plotly_chart(fig)


def grafico_barra_comercio(dfcomercio, ultimos15anos_geral):

    if ultimos15anos_geral:
        dfcomercio['Ano'] = dfcomercio['Ano'].astype(int)
        ultimos15 = dfcomercio[dfcomercio['Ano'] >= 2007]
        titulo_ano = '2007 - 2021'
    else:
        dfcomercio['Ano'] = dfcomercio['Ano'].astype(int)
        ultimos15 = dfcomercio[dfcomercio['Ano'] > 0]
        titulo_ano = '1970 - 2021'
        
    ## ajustes para o gráfico de barras ##
    dfcomerciov5 = ultimos15.drop(columns=['Ano'])
    dfcomerciov6 = dfcomerciov5.T
    dfcomerciov6['Total'] = dfcomerciov6.sum(axis=1)
    dfcomerciov7 = dfcomerciov6.reset_index()
    dfcomerciov7 = dfcomerciov7.rename(columns={'index':'Vinhos'})
    filtro_tab = ['Vinhos', 'Total']
    dfcomerciov8 = dfcomerciov7[filtro_tab].sort_values(by='Total', ascending=False)

    # Gráfico de Barras por Tipo de Vinho
    fig = px.bar(dfcomerciov8, 
                 x='Vinhos', 
                 y='Total', 
                 labels={'Total': 'Preço Total'},
                 title=f'Vendas de Vinho de Mesa por Ano entre {titulo_ano}',
                 color_discrete_sequence=['#910A67'])
    
     
    # Adicionar título e rótulos dos eixos
    fig.update_layout(
        xaxis_title='Vinhos',
        yaxis_title='Preço Total',
        yaxis_tickprefix='US$ ',  # Adicionar prefixo de dólar 
        plot_bgcolor="white",

        # Configurar o tamanho da fonte do título
        title_font=dict(size=18),
        
        # Configurar o tamanho da linha
        showlegend=True,
        legend=dict(font=dict(size=16)),  

        # Tamanho do gráfico
        width=1100,
        height=500,

        # Configurar cor e tamanho da fonte dos rótulos dos eixos

        xaxis=dict(
            title=dict(text='Vinhos', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486')
        ),

        yaxis=dict(gridcolor='#3B3486',
            title=dict(text='Preço Total', font=dict(size=16, color='#3B3486')),  
            tickfont=dict(size=14, color='#3B3486'),
            tickprefix='US$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#3C0753',  
            font=dict(family='Arial', size=16, color='white'), 
        ),
    )

    st.plotly_chart(fig)



