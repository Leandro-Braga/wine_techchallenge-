import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
# import pydeck as pdk
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter

# def formatar_como_moeda(valor, divisor_casas):

#     # Ajuste da formatação de moeda em reais
#     # divisor_casas = 1000000000

#     return f'R$ {valor/divisor_casas:,.2f}{"B" if valor >= 1000000000 else "MM"}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def formatar_como_moeda(valor, divisor_casas):
    # Ajuste da formatação de moeda
    return f'US$ {valor/divisor_casas:,.2f}{"B" if valor >= 1000000000 else "MM"}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def formatar_como_quantidade(valor, divisor_casas):
    # Ajuste da formatação de moeda
    return f'{valor/divisor_casas:,.2f}QTD'.replace(',', 'X').replace('.', ',').replace('X', '.')


def billion_formatter(x, pos):
    bilao = 1000000000
    milao = 1000000
    # return f'R${x/bilao if x >= bilao else milao:.1f}{"B" if x >= bilao else "MM"}'
    return f'US${x/milao:,.2f}{"B" if x >= 1000000000 else "MM"}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def grafico_pais_valortotal(df):

    # Normalizando os valores para o intervalo [0, 1]
    df['exportação'] = (df['valor_total'] - 
                df['valor_total'].min()) / (df['valor_total'].max() - 
                                            df['valor_total'].min())

    # Criando o gráfico de mapa com uma escala de cores contínua
    fig = px.choropleth(
        df	,
        locations='pais_ing',  # Esta coluna deve conter nomes de países reconhecíveis por Plotly
        locationmode='country names',
        color='exportação',  # Use a coluna normalizada para o mapeamento de cores
        hover_name='pais',
        hover_data=['valor_total'],
        color_continuous_scale=['green', 'yellow', 'red']  # Define a escala de cor do verde para vermelho
    )

    # Mostrar o gráfico
    # fig.show()

    # tamanho do gráfico
    fig.update_layout(
        width=1400,
        height=800,
    )

    st.plotly_chart(fig)


def grafico_ano_barra(df):

    # Constantes para bilhão e milhão
    bilhao = 1000000000
    milao = 1000000

    # Filtrando por 'classe' e garantindo que 'total_geral' é numérico
    df = df[df['classe'] == 'valor'][['total_geral']].astype(int)

    # Calculando a média dos gastos
    media_gastos = df['total_geral'].mean()

    # Criando o gráfico com a linha de média e rótulos de valor
    plt.figure(figsize=(14, 5))
    sns.barplot(x=df.index, y=df['total_geral'], palette="viridis")

    if len(df) > 1:
        plt.text(len(df) - 1, media_gastos, f'Média: {formatar_como_moeda(media_gastos, milao)}', 
                color='red', ha="right", va="bottom")
        plt.axhline(media_gastos, color='red', linestyle='--')

    plt.title('Total de Exportação por Ano', fontsize=16)
    plt.xlabel('Ano', fontsize=10)
    plt.ylabel('Total', fontsize=10)
    plt.xticks(rotation=45)
    
    # Alterando a cor de fundo do grid
    # plt.grid(True, color='#f0f0f0')

    # Alterando a cor de fundo do espaço do gráfico
    plt.gca().set_facecolor('#f8f8f8')

    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, color='gray')
    

    # Adicionando rótulos de valor nas barras

    # for index, value in df['total_geral'].items():
    #     plt.text(index, value, formatar_como_moeda(value, milao), color='black', ha="center", va="bottom")
    # for index, value in enumerate(df['total_geral']):
    #         plt.text(index, value, f'{formatar_como_moeda(value, milao)}', color='black', ha="center", va="bottom")

    # Função para formatar
    plt.gca().yaxis.set_major_formatter(FuncFormatter(billion_formatter))

    plt.tight_layout()

    st.pyplot(plt)



def grafico_linha_pais_qtd(df_exp_vinho_tab, coluna):

    milao = 1000000

    df_qtd = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'quantidade'][[coluna]]

    # Convertendo os índices para inteiros
    df_qtd.index = df_qtd.index.map(int)

    # Criando o gráfico novamente com a formatação personalizada no eixo Y
    plt.figure(figsize=(14, 5))
    plt.plot(df_qtd.index, df_qtd[coluna], color='darkred', marker='o')

    plt.title(f'Exportações por Quantidade de Vinhos do {coluna} (1970-2022)', fontsize=14)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Exportações', fontsize=12)

    plt.xticks(range(df_qtd.index.min(), df_qtd.index.max()+1, 2), rotation=45)

    # Aplicando a função de formatação ao eixo Y
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: formatar_como_quantidade(x, milao)))

    plt.grid(True)
    # plt.grid(True, axis='x', linestyle='--', linewidth=0.7, color='gray')

    # Alterando a cor de fundo do grid
    plt.grid(True, color='#F5EEE6')

    # Alterando a cor de fundo do espaço do gráfico
    plt.gca().set_facecolor('#f8f8f8')
    # plt.gca().set_facecolor('#E6A4B4')
    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, color='gray')

    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)



def grafico_linha_pais_valor(df_exp_vinho_tab, coluna):

    milao = 1000000

    df_valor = df_exp_vinho_tab.loc[df_exp_vinho_tab['classe'] == 'valor'][[coluna]]

    # Convertendo os índices para inteiros
    df_valor.index = df_valor.index.map(int)

    # Criando o gráfico novamente com a formatação personalizada no eixo Y
    plt.figure(figsize=(14, 5))
    plt.plot(df_valor.index, df_valor[coluna], color='darkred', marker='o')

    plt.title(f'Exportações por Valor de Vinhos do {coluna} (1970-2022)', fontsize=14)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Exportações', fontsize=12)

    plt.xticks(range(df_valor.index.min(), df_valor.index.max()+1, 2), rotation=45)

    # Aplicando a função de formatação ao eixo Y
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: formatar_como_moeda(x, milao)))

    plt.grid(True)
    # plt.grid(True, axis='x', linestyle='--', linewidth=0.7, color='gray')

    # Alterando a cor de fundo do grid
    plt.grid(True, color='#F5EEE6')

    # Alterando a cor de fundo do espaço do gráfico
    plt.gca().set_facecolor('#f8f8f8')
    # plt.gca().set_facecolor('#E6A4B4')
    plt.grid(True, axis='y', linestyle='--', linewidth=0.7, color='gray')

    plt.tight_layout()
    # plt.show()
    st.pyplot(plt)



