import streamlit as st

from nba_api.stats.endpoints import playercareerstats

st.write("Iniciando")

stats = playercareerstats.PlayerCareerStats(
    player_id='2544'
)

st.write("Resposta recebida")

df = stats.season_totals_regular_season.get_data_frame()

st.write(df.head())
