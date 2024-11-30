from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import PlayerProfileV2
import streamlit as st
from nba_api.stats.static import players
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
st.sidebar.success("Escolha o que quer explorar!")

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="NBA Stats",
    page_icon="🏀",
    layout="centered",
)

# Estilo personalizado para a página
st.markdown("""
    <style>
        body {
            background-color: #091836;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        .container {
            text-align: center;
            padding: 20px;
        }
        .title {
            font-size: 50px;
            font-weight: bold;
            margin: 10px 0;
            color: #FDB927;
        }
        .subtitle {
            font-size: 18px;
            color: #D1D1D1;
            margin-bottom: 30px;
        }
        .button-container {
            margin-top: 20px;
        }
        .button {
            background-color: #FDB927;
            border: none;
            color: #091836;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
            text-decoration: none;
        }
        .button:hover {
            background-color: #FFB81C;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Estrutura da página
st.markdown("""
<div class="container">
    <img src="https://ih1.redbubble.net/image.4531426106.3746/flat,750x,075,f-pad,750x1000,f8f8f8.jpg" 
         alt="NBA Logo" style="width: 200px; border-radius: 10px; margin-bottom: 20px;">
    <div class="title">NBA Stats Hub</div>
    <div class="subtitle">
        Bem-vindo ao site mais legal de estatísticas básicas e avançadas da NBA!
    </div>
    </div>
</div>
""", unsafe_allow_html=True)

