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
escolha = st.radio(" ", ["Geral", "Por Time"], horizontal=True)
st.divider()
times_abr = [
    "ATL",  # Atlanta Hawks
    "BOS",  # Boston Celtics
    "BKN",  # Brooklyn Nets
    "CHA",  # Charlotte Hornets
    "CHI",  # Chicago Bulls
    "CLE",  # Cleveland Cavaliers
    "DAL",  # Dallas Mavericks
    "DEN",  # Denver Nuggets
    "DET",  # Detroit Pistons
    "GSW",  # Golden State Warriors
    "HOU",  # Houston Rockets
    "IND",  # Indiana Pacers
    "LAC",  # Los Angeles Clippers
    "LAL",  # Los Angeles Lakers
    "MEM",  # Memphis Grizzlies
    "MIA",  # Miami Heat
    "MIL",  # Milwaukee Bucks
    "MIN",  # Minnesota Timberwolves
    "NOP",  # New Orleans Pelicans
    "NYK",  # New York Knicks
    "OKC",  # Oklahoma City Thunder
    "ORL",  # Orlando Magic
    "PHI",  # Philadelphia 76ers
    "PHX",  # Phoenix Suns
    "POR",  # Portland Trail Blazers
    "SAC",  # Sacramento Kings
    "SAS",  # San Antonio Spurs
    "TOR",  # Toronto Raptors
    "UTA",  # Utah Jazz
    "WAS"   # Washington Wizards
]
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

def achar_jogador(jogador_input):
    if jogador_input:
        try:
            jogador_dict = players.find_players_by_full_name(jogador_input)
        except Exception as e:
            st.write("## Confira o nome do jogador.")
        try:
            jogador_id = jogador_dict[0]["id"]
            return jogador_dict, jogador_id
        except Exception as e:
            st.write(" ")



with col01:
    stat_lider = st.selectbox(
                'Quer ver o ranking de qual stat?',
                stats2, key='stats_lider')
    with col02:
        if escolha == "Geral":
            jogador_input = st.text_input("Quer ver o ranking de qual jogador?", placeholder="James Harden")
            if jogador_input:
                try:
                    jogador_dict, jogador_id = achar_jogador(jogador_input)
                except Exception as e:
                    st.write(" ")
        else:
            time = st.selectbox("Ver ranking em qual time?", times_abr)

lideres = LeagueLeaders(per_mode48='PerGame', season_type_all_star='Regular Season', stat_category_abbreviation=stat_lider)
df_lider = lideres.league_leaders.get_data_frame()
df_lider = pl.from_pandas(df_lider)

if escolha == "Por Time":
    df_lider = df_lider.filter(pl.col('TEAM') == time)
else:
    if jogador_input:
        try:
            df_lider_jogador = df_lider.filter(pl.col("PLAYER_ID") == jogador_id)
            df_lider_jogador = df_lider_jogador.select(pl.col('RANK'), pl.col('PLAYER'), pl.col('TEAM'), pl.col(stat_lider)).head(10)
        except Exception as e:
            st.write(" ")
df_lider_tela = df_lider.select(pl.col('RANK'), pl.col('PLAYER'), pl.col('TEAM'), pl.col(stat_lider)).head(10)

col01, col02 = st.columns(2)
with col01:
    for row in df_lider_tela.iter_rows():
        rank, player, team, stat = row  # Supondo que as colunas sejam 'rank', 'player', 'team', e 'stat'
        st.markdown(f"""
        <div style="margin: 5px 0; padding: 8px; border-radius: 5px; border: 1px solid #ddd;">
            <strong>#{rank}</strong> {player} 
            <span style="color: #7a0b11;">({team})</span> — 
            <strong>{stat_lider}: {stat}</strong>
        </div>
        """, unsafe_allow_html=True)


if escolha == 'Geral':
    with col02:
        if jogador_input:
            try:
                for row in df_lider_jogador.iter_rows():
                    rank, player, team, stat = row  # Supondo que as colunas sejam 'rank', 'player', 'team', e 'stat'
                    st.markdown(f"""
                                    <div style="margin: 5px 0; padding: 8px; border-radius: 5px; border: 1px solid #444; background-color: #ffffff;">
                                        <strong style="color: #0056b3;">#{rank}</strong> 
                                        <span style="font-weight: bold; color: #222;">{player}</span> — 
                                        <span style="color: #555;">{team}</span>
                                        <span style="float: right; font-weight: bold; color: #d9534f;">{stat_lider}: {stat}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
            except Exception as e:
                st.write("### Confira o nome do jogador.")
