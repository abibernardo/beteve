from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import PlayerProfileV2
from nba_api.stats.endpoints import LeagueLeaders
import streamlit as st
from nba_api.stats.static import players
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

st.title("Líderes da Liga")
#### Lideres da temporada
col01, col02 = st.columns(2)
stats2 = [
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "FGA",
    "FGM",
    "FG3A",
    "FG3M",
    "FTA",
    "FTM",
    "MIN",
    "EFF",
    "OREB",
    "DREB"
]
with col01:
    stat_lider = st.selectbox(
                'Quer ver o ranking de qual stat?',
                stats2, key='stats_lider')

lideres = LeagueLeaders(per_mode48='PerGame', season_type_all_star='Regular Season', stat_category_abbreviation=stat_lider)
df_lider = lideres.league_leaders.get_data_frame()
st.dataframe(df_lider)
df_lider = pl.from_pandas(df_lider)
df_lider = df_lider.select(pl.col('RANK'), pl.col('PLAYER'), pl.col('TEAM'), pl.col(stat_lider)).head(10)

# Iterar pelas linhas do DataFrame
col01, col02 = st.columns(2)
with col01:
    for row in df_lider.iter_rows():
        rank, player, team, stat = row  # Extrair valores na ordem das colunas

        st.markdown(f"""
        <div style="background-color: #edc2c5; color: #333; margin: 5px 0; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
            <strong>#{rank}</strong> {player} <span style="color: #7a0b11;">({team})</span> — <strong>{stat_lider}: {stat}</strong>
        </div>
        """, unsafe_allow_html=True)
