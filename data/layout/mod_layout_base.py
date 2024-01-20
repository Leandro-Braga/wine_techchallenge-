import streamlit as st
# from streamlit_extras.metric_cards import style_metric_cards
# from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.row import row


# Configuração do tamanho dos textos principais
def texto_diversos():
        st.markdown(
        """
        <style>

        .st-emotion-cache-1r99xku p {
        word-break: break-word;
        margin-bottom: -1px;
        font-size: 18px;}

        .st-emotion-cache-q4lvki p {
            word-break: break-word;
            margin-bottom: 0px;
            font-size: 18px;
        }
        .css-176rrwg {
            min-height: 1.5rem;
        }

        .css-q4lvki p {
            font-size: 18px;
        }

        .css-atw1qn p {
            font-size: 18px;
        }

        .st-af {
            font-size: 1.1rem;
        }

        </style>
        """,
        unsafe_allow_html=True)


def selecao_dataframe(df):


    row1 = row([2, 4, 1], vertical_align="bottom")
    row2 = row(1)

    continetes = row1.multiselect("Continentes", ['Ásia', 
                                                'Europa', 
                                                'África', 
                                                'América Central e Caribe', 
                                                'América do Sul', 
                                                'Oceania', 
                                                'Oriente Médio', 
                                                'América do Norte'], default=['Europa', 
                                                                            'América do Sul', 
                                                                            'América do Norte'])

    # row1.text_input("País de Destino")
    # row1.text_input("Ano")

    df['Ano Exportação'] = df['Ano Exportação'].astype(str)

    df = df[df['Continente'].isin(continetes)]
    df = df[df['País de Destino'].str.contains(row1.text_input("País de Destino"), case=False)]
    df = df[df['Ano Exportação'].str.contains(row1.text_input("Ano"), case=False)]

    row2.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={'Litros_por_populacao': st.column_config.NumberColumn('Litros_por_populacao', format="U$ %.2f"),
                                'Preco_por_litro': st.column_config.NumberColumn('Preco_por_litro', format="U$ %.2f"),
                                'Ano Exportação': st.column_config.TextColumn('Ano Exportação')})

    # st.table(df['Continente'].unique())

    # row1.dataframe(df, use_container_width=True)
    # row1.line_chart(df, use_container_width=True)

    # row2.button("Send", use_container_width=True)


