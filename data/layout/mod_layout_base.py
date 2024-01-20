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
    row3 = row(2, vertical_align="center")

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

    df['Ano Exportação'] = df['Ano Exportação'].astype(str)

    df = df[df['Continente'].isin(continetes)]
    df = df[df['País de Destino'].str.contains(row1.text_input("País de Destino"), case=False)]
    df = df[df['Ano Exportação'].str.contains(row1.text_input("Ano Exportação"), case=False)]

    row2.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={'Litros por População': st.column_config.NumberColumn('Litros por População', format="U$ %.2f"),
                                'Preço do Vinho (US$/Litro)': st.column_config.NumberColumn('Preço do Vinho (US$/Litro)', format="U$ %.2f"),
                                'Valor Exportado (US$)': st.column_config.NumberColumn('Valor Exportado (US$)', format="U$ %.2f"),
                                'Ano Exportação': st.column_config.TextColumn('Ano Exportação')})

    with row3.expander("Definição das Colunas p1:"):
          st.markdown("""
                        1. **Pais de Origem:**
                            - Representa o país de onde o vinho é exportado.
                        
                        2. **País de Destino:**
                            - Indica o país para o qual o vinho é exportado.

                        3. **Ano Exportação:**
                            - Refere-se ao ano em que a exportação do vinho ocorreu.

                        4. **Vinho Exportado (Litros):**
                            - Quantidade de vinho exportado, por Pessoa (em Litros).

                        5. **Valor Exportado (US$):**
                            - Valor monetário total do vinho exportado em dólares americanos.

                        6. **Pais de Destino Inglês:**
                            - Nome do país de destino em inglês.

                        7. **Continente:**
                            - Indica a região continental do país de destino.
                        """)
          
    with row3.expander("Definição das Colunas p2:"):
        st.markdown("""
                        8. **População do País:**
                            - Número total de habitantes no país de destino.

                        9. **Idade Média do País:**
                            - A média de idade da população do país de destino.

                        10. **Densidade Populacional:**
                            - Número de habitantes por unidade de área do país de destino.

                        11. **Razão de Sexo do País:**
                            - Proporção entre homens e mulheres na população.

                        12. **Litros por População:**
                            - A média de litros de vinho exportados por habitante.

                        13. **Preço do Vinho (US$/Litro):**
                            - O custo médio do vinho por litro em dólares americanos.
                        """)
        


