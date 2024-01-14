import warnings

import pandas as pd
import pretty_errors
import streamlit as st
from PIL import Image

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

st.header('Dados de avaliações de vinhos', divider='violet')
st.markdown('**Tabela**: País de origem (Brasil).')

