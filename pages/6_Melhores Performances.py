from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import PlayerProfileV2
from nba_api.stats.endpoints import LeagueLeaders
import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

# objetos
stats = [
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "FG%",
    "3 FG%",
    "FT%",
    "FGA",
    "FGM",
    "FG3A",
    "FG3M",
    "FTA",
    "FTM",
    "MIN"
]
stats2 = [
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PLUS_MINUS",
    "FG%",
    "3 FG%",
    "FT%",
    "FGA",
    "FGM",
    "FG3A",
    "FG3M",
    "FTA",
    "FTM",
    "MIN"
]


def achar_jogador(jogador_input):
    if jogador_input:
        try:
            jogador_dict = players.find_players_by_full_name(jogador_input)
        except Exception as e:
            st.divider()
            st.write("# Confira o nome do jogador.")
        try:
            jogador_id = jogador_dict[0]["id"]
            return jogador_dict, jogador_id
        except Exception as e:
            st.write("## Confira o nome do jogador.")

def achar_jogo(jogo, nome):
    try:
        df = jogo.league_game_finder_results.get_data_frame()
    except Exception as e:
        st.write(f"Erro ao buscar dados: {e}")
        df = pd.DataFrame()  # DataFrame vazio em caso de erro
    if not df.empty:
        df_jogos = pl.from_pandas(df)
        df_jogos = df_jogos.with_columns(
            pl.col("GAME_DATE").alias("DATA"),
            (pl.col("TEAM_NAME")).alias("TIME"),
            pl.col("WL").alias("W/L"),
            pl.col("PTS"),
            pl.col("REB"),
            pl.col("AST"),
            pl.col("STL"),
            pl.col("BLK"),
            pl.col("TOV"),
            (pl.col("FG_PCT") * 100).alias("FG%"),
            (pl.col("FG3_PCT") * 100).alias("3 FG%"),
            (pl.col("FT_PCT") * 100).alias("FT%"),
            pl.col("FGA"),
            pl.col("FGM"),
            pl.col("FG3A"),
            pl.col("FG3M"),
            pl.col("FTA"),
            pl.col("FTM"),
            pl.col("MIN"))
        df_jogos = df_jogos.with_columns(
            (pl.col("SEASON_ID").str.slice(1).cast(pl.Int32) + 1).alias("TEMPORADA")
        )
        df_jogos = df_jogos.select(
            ["DATA", "MATCHUP", "W/L", "PTS", "REB", "AST", "STL", "BLK", "FG%", "3 FG%", "FT%", "FGM",
             "FGA", "FG3M", "FG3A", "FTM", "FTA", "MIN"]
        )

        return df_jogos
    else:
        st.write(f'{nome} nunca teve um jogo com essas estatísticas.')



st.title("Melhores Performances")
jogador_input = st.text_input("De que jogador você quer ver as estatísticas?", placeholder="James Harden")
temporada = st.radio(" ", ["Temporada Regular", "Playoffs"], horizontal=True)
st.divider()
st.write("### Buscar jogos em que o jogador teve pelo menos:")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    pts = st.number_input("PTS", 0)
with col2:
    ast = st.number_input("AST", 0)
with col3:
    reb = st.number_input("REB", 0)
with col4:
    stl = st.number_input("STL", 0)
with col5:
    blk = st.number_input("BLK", 0)
with col1:
    fm3 = st.number_input("Bolas de 3", 0)
with col2:
    fg_pct = st.number_input("FG %", 0)
with col3:
    fg3_pct = st.number_input("FG 3%", 0)

estatisticas = [pts, ast, reb, stl, blk, fm3, fg_pct, fg3_pct]
tipos_estatisticas = ["pontos", "assistências", "rebotes", "roubos de bola", "tocos", "bolas de 3", "% de aproveitamento de quadra", "% de aproveitamento de 3"]

if jogador_input:
    try:
        jogador_dict, jogador_id = achar_jogador(jogador_input)
    except Exception as e:
        st.write(" ")
    try:
        if jogador_id:
            nome = jogador_dict[0]["full_name"]
            if temporada in "Temporada Regular":
                jogo = LeagueGameFinder(player_id_nullable=jogador_id, season_type_nullable = "Regular Season", gt_pts_nullable = pts, gt_ast_nullable = ast, gt_reb_nullable = reb, gt_stl_nullable=stl, gt_blk_nullable=blk, gt_fg3m_nullable = fm3, gt_fg_pct_nullable = fg_pct/100, gt_fg3_pct_nullable = fg3_pct/100)
            else:
                jogo = LeagueGameFinder(player_id_nullable=jogador_id, season_type_nullable="Playoffs", gt_pts_nullable = pts, gt_ast_nullable = ast, gt_reb_nullable = reb, gt_stl_nullable = stl, gt_blk_nullable = blk, gt_fg3m_nullable = fm3, gt_fg_pct_nullable = fg_pct / 100, gt_fg3_pct_nullable = fg3_pct / 100)
            df = achar_jogo(jogo, nome)
            qtd = df.height

            st.divider()

            if any(valor > 0 for valor in estatisticas):
                if temporada in "Temporada Regular":
                    st.write(f'### Na temporada regular, {nome} teve {qtd} jogos com pelo menos:')
                elif temporada in "Playoffs":
                    st.write(f'### Nos Playoffs, {nome} teve {qtd} jogos com pelo menos:')
                for estatistica, tipos_estatisticas in zip(estatisticas, tipos_estatisticas):
                    if estatistica > 0:
                        st.write(f' ### **{estatistica} {tipos_estatisticas}**')
                st.divider()
                st.dataframe(df)
                count_w = df.filter(pl.col("W/L") == "W").height
                vitorias = round((count_w/qtd) * 100, 1)
                st.write(f'**{nome} venceu {vitorias}% dos jogos em que alcançou essas estatísticas.**')
    except Exception as e:
        st.write(' ')
