import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container


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
