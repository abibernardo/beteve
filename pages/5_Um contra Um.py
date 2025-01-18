from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import PlayerProfileV2
from nba_api.stats.endpoints import LeagueLeaders
import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd
import polars as pl
import polars.selectors as cs
import plotly.express as px
import plotly.graph_objects as go

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

def achar_jogo(jogador_id):
    try:
        # Busca jogos associados ao jogador
        jogo = LeagueGameFinder(player_id_nullable=jogador_id, season_type_nullable = 'Regular Season')
        df = jogo.league_game_finder_results.get_data_frame()
    except Exception as e:
        st.write(f"Erro ao buscar dados: {e}")
        df = pd.DataFrame()  # DataFrame vazio em caso de erro
    if not df.empty:
        df_jogos = pl.from_pandas(df)
        df_jogos = df_jogos.with_columns(
            pl.col("GAME_DATE").alias("DATA"),
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
            (pl.col("SEASON_ID").str.slice(1).cast(pl.Int32) + 1).alias("SEASON_ID")
        )

        return df_jogos
    else:
        st.write("Nenhum dado disponível para exibir.")

def media_por_temporada(df_carreira):
    df_carreira = df_carreira.with_columns(
        pl.col("SEASON_ID").alias("temporada"),
        pl.col("SEASON_ID").str.extract(r"^(\d+)", 1).cast(pl.Int32).alias("ano"),
        pl.col("TEAM_ABBREVIATION").alias("time"),
        (pl.col("PTS") / pl.col("GP")).round(1),
        (pl.col("REB") / pl.col("GP")).round(1),
        (pl.col("AST") / pl.col("GP")).round(1),
        (pl.col("STL") / pl.col("GP")).round(1),
        (pl.col("BLK") / pl.col("GP")).round(1),
        (pl.col("TOV") / pl.col("GP")).round(1),
        (pl.col("FG_PCT") * 100).alias("FG%"),
        (pl.col("FG3_PCT") * 100).alias("3 FG%"),
        (pl.col("FT_PCT") * 100).alias("FT%"),
        (pl.col("FGA") / pl.col("GP")).round(1),
        (pl.col("FGM") / pl.col("GP")).round(1),
        (pl.col("FG3A") / pl.col("GP")).round(1),
        (pl.col("FG3M") / pl.col("GP")).round(1),
        (pl.col("FTA") / pl.col("GP")).round(1),
        (pl.col("FTM") / pl.col("GP")).round(1),
        (pl.col("MIN") / pl.col("GP")).round(1),
        pl.col("GP").alias("Jogos")
    )

    return df_carreira

def total_por_temporada(df_carreira):
    df_total_carreira = df_carreira.with_columns(
        pl.col("SEASON_ID").alias("temporada"),
        pl.col("SEASON_ID").str.extract(r"^(\d+)", 1).cast(pl.Int32).alias("ano"),
        pl.col("TEAM_ABBREVIATION").alias("time"),
        pl.col("PTS").round(1),
        pl.col("REB").round(1),
        pl.col("AST").round(1),
        pl.col("STL").round(1),
        pl.col("BLK").round(1),
        pl.col("TOV").round(1),
        (pl.col("FG_PCT") * 100).alias("FG%"),
        (pl.col("FG3_PCT") * 100).alias("3 FG%"),
        (pl.col("FT_PCT") * 100).alias("FT%"),
        pl.col("FGA").round(1),
        pl.col("FGM").round(1),
        pl.col("FG3A").round(1),
        pl.col("FG3M").round(1),
        pl.col("FTA").round(1),
        pl.col("FTM").round(1),
        pl.col("MIN").round(1),
        pl.col("GP").alias("Jogos")
    )
    return df_total_carreira


def total_carreira(df_medias):
    df_totais_carreira = df_medias.with_columns(
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
        pl.col("MIN")
    )

    df_totais_carreira = df_totais_carreira.select(
        pl.col("PTS"),
        pl.col("REB"),
        pl.col("AST"),
        pl.col("STL"),
        pl.col("BLK"),
        pl.col("TOV"),
        pl.col("FG%"),
        pl.col("3 FG%"),
        pl.col("FT%"),
        pl.col("FGA"),
        pl.col("FGM"),
        pl.col("FG3A"),
        pl.col("FG3M"),
        pl.col("FTA"),
        pl.col("FTM"),
        pl.col("MIN")
    )
    return df_totais_carreira


def medias_carreira(df_medias):
    df_medias = df_medias.with_columns(
        (pl.col("PTS") / pl.col("GP")).round(1),
        (pl.col("REB") / pl.col("GP")).round(1),
        (pl.col("AST") / pl.col("GP")).round(1),
        (pl.col("STL") / pl.col("GP")).round(1),
        (pl.col("BLK") / pl.col("GP")).round(1),
        (pl.col("TOV") / pl.col("GP")).round(1),
        (pl.col("FG_PCT") * 100).alias("FG%"),
        (pl.col("FG3_PCT") * 100).alias("3 FG%"),
        (pl.col("FT_PCT") * 100).alias("FT%"),
        (pl.col("FGA") / pl.col("GP")).round(1),
        (pl.col("FGM") / pl.col("GP")).round(1),
        (pl.col("FG3A") / pl.col("GP")).round(1),
        (pl.col("FG3M") / pl.col("GP")).round(1),
        (pl.col("FTA") / pl.col("GP")).round(1),
        (pl.col("FTM") / pl.col("GP")).round(1),
        (pl.col("MIN") / pl.col("GP")).round(1)
    )
    df_medias = df_medias.select(
        pl.col("PTS"),
        pl.col("REB"),
        pl.col("AST"),
        pl.col("STL"),
        pl.col("BLK"),
        pl.col("TOV"),
        pl.col("FG%"),
        pl.col("3 FG%"),
        pl.col("FT%"),
        pl.col("FGA"),
        pl.col("FGM"),
        pl.col("FG3A"),
        pl.col("FG3M"),
        pl.col("FTA"),
        pl.col("FTM"),
        pl.col("MIN"))
    return df_medias


st.title("Um contra Um")
show = st.radio("Quais dados deseja utilizar?", ["Carreira", "Última temporada ativa"], horizontal=True)
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    jogador_1 = st.text_input("Jogador A", placeholder="Anthony Edwards", key='um')
with col2:
    jogador_2 = st.text_input("Jogador B", placeholder="Ja Morant", key='dois')



if jogador_1:
    try:
        ### PUXANDO DADOS
        jogador_dict, jogador_id = achar_jogador(jogador_1)
        jogador_1 = jogador_dict[0]["full_name"]
        stats_carreira = playercareerstats.PlayerCareerStats(player_id=jogador_id)   # stats de todas as temporadas
        df_carreira = stats_carreira.season_totals_regular_season.get_data_frame()
        df_carreira = pl.from_pandas(df_carreira)
        df_medias = stats_carreira.career_totals_regular_season.get_data_frame()
        df_medias = pl.from_pandas(df_medias)
        df_jogos = achar_jogo(jogador_id)

        ### TRATANDO DADOS:  df_carreira = media por temporada
        df_total_carreira = total_por_temporada(df_carreira)
        df_carreira = media_por_temporada(df_carreira)

        # média temporada atual
        df_carreira_1 = df_carreira.reverse().head(1)
        df_carreira_1 = df_carreira_1.with_columns(pl.lit(jogador_1).alias("nome"))
        df_carreira_1 = total_carreira(df_carreira_1)
        df_medias_1 = df_carreira_1.with_columns(
            pl.lit(jogador_1).alias("nome"))
        ### medias da carreira
        df_medias_1 = medias_carreira(df_medias)
        df_medias_1 = df_medias_1.with_columns(
            pl.lit(jogador_1).alias("nome"))
    except Exception as e:
        st.write(" ")
else:
    st.write(" ")

if jogador_2:
    try:
        ### PUXANDO DADOS
        jogador_dict, jogador_id = achar_jogador(jogador_2)
        jogador_2 = jogador_dict[0]["full_name"]
        stats_carreira = playercareerstats.PlayerCareerStats(player_id=jogador_id)  # stats de todas as temporadas
        df_carreira = stats_carreira.season_totals_regular_season.get_data_frame()
        df_carreira = pl.from_pandas(df_carreira)
        df_medias = stats_carreira.career_totals_regular_season.get_data_frame()
        df_medias = pl.from_pandas(df_medias)
        df_jogos = achar_jogo(jogador_id)

        ### TRATANDO DADOS:  df_carreira = media por temporada
        df_total_carreira = total_por_temporada(df_carreira)
        df_carreira = media_por_temporada(df_carreira)

        # média temporada atual
        df_carreira_2 = df_carreira.reverse().head(1)
        df_carreira_2 = df_carreira_2.with_columns(pl.lit(jogador_2).alias("nome"))
        df_carreira_2 = total_carreira(df_carreira_2)
        ### medias da carreira
        df_medias_2 = medias_carreira(df_medias)
        df_medias_2 = df_medias_2.with_columns(
            pl.lit(jogador_2).alias("nome"))
    except Exception as e:
        st.write(" ")
else:
    st.write(" ")

# ultima_ativa = pl.concat([df_carreira_1, df_carreira_2], how="vertical_relaxed")
# carreira = pl.concat([df_medias_1, df_medias_2], how="vertical_relaxed")

if jogador_1 and jogador_2:
    if show == "Carreira":
        ppg_carreira_1 = df_medias_1.item(0, 0)
        rpg_carreira_1 = df_medias_1.item(0, 1)
        apg_carreira_1 = df_medias_1.item(0, 2)
        spg_carreira_1 = df_medias_1.item(0, 3)
        bpg_carreira_1 = df_medias_1.item(0, 4)
        tpg_carreira_1 = df_medias_1.item(0, 5)
        fg_carreira_1 = df_medias_1.item(0, 6)
        fg3_carreira_1 = df_medias_1.item(0, 7)
        ft_carreira_1 = df_medias_1.item(0, 8)
        ppg_carreira_2 = df_medias_2.item(0, 0)
        rpg_carreira_2 = df_medias_2.item(0, 1)
        apg_carreira_2 = df_medias_2.item(0, 2)
        spg_carreira_2 = df_medias_2.item(0, 3)
        bpg_carreira_2 = df_medias_2.item(0, 4)
        tpg_carreira_2 = df_medias_2.item(0, 5)
        fg_carreira_2 = df_medias_2.item(0, 6)
        fg3_carreira_2 = df_medias_2.item(0, 7)
        ft_carreira_2 = df_medias_2.item(0, 8)
    elif show == "Última temporada ativa":
        ppg_carreira_1 = df_carreira_1.item(0, 0)
        rpg_carreira_1 = df_carreira_1.item(0, 1)
        apg_carreira_1 = df_carreira_1.item(0, 2)
        spg_carreira_1 = df_carreira_1.item(0, 3)
        bpg_carreira_1 = df_carreira_1.item(0, 4)
        tpg_carreira_1 = df_carreira_1.item(0, 5)
        fg_carreira_1 = df_carreira_1.item(0, 6)
        fg3_carreira_1 = df_carreira_1.item(0, 7)
        ft_carreira_1 = df_carreira_1.item(0, 8)
        ppg_carreira_2 = df_carreira_2.item(0, 0)
        rpg_carreira_2 = df_carreira_2.item(0, 1)
        apg_carreira_2 = df_carreira_2.item(0, 2)
        spg_carreira_2 = df_carreira_2.item(0, 3)
        bpg_carreira_2 = df_carreira_2.item(0, 4)
        tpg_carreira_2 = df_carreira_2.item(0, 5)
        fg_carreira_2 = df_carreira_2.item(0, 6)
        fg3_carreira_2 = df_carreira_2.item(0, 7)
        ft_carreira_2 = df_carreira_2.item(0, 8)

    if jogador_1 and jogador_2:
        metrics = ["PTS", "REB", "AST", "STL", "BLK", "TOV", "FG%", "3P%", "FT%"]
        player_1_stats = [ppg_carreira_1, rpg_carreira_1, apg_carreira_1, spg_carreira_1, bpg_carreira_1, tpg_carreira_1,
                          fg_carreira_1, fg3_carreira_1, ft_carreira_1]
        player_2_stats = [ppg_carreira_2, rpg_carreira_2, apg_carreira_2, spg_carreira_2, bpg_carreira_2, tpg_carreira_2,
                          fg_carreira_2, fg3_carreira_2, ft_carreira_2]

        st.markdown("<hr style='border: 2px solid #0056b3; margin: 20px 0;'>", unsafe_allow_html=True)

        # Layout das colunas
        col1, col2 = st.columns(2)

        # Estilo de cada bloco de métricas
        metric_style = """
            <div style="
                margin: 10px 0; 
                padding: 15px; 
                border-radius: 10px; 
                border: 1px solid #0077b6; 
                background-color: #e0f7fa; 
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            ">
                <strong style="color: #0077b6; font-size: 16px;">{metric}:</strong> 
                <span style="font-weight: bold; color: #333; font-size: 16px;">{value:.1f}</span>
            </div>
        """

        # Jogador 1
        with col1:
            st.markdown(f"<h3 style='text-align: center; color: #0056b3;'>{jogador_1}</h3>", unsafe_allow_html=True)
            for metric, value in zip(metrics, player_1_stats):
                st.markdown(metric_style.format(metric=metric, value=value), unsafe_allow_html=True)

        # Jogador 2
        with col2:
            st.markdown(f"<h3 style='text-align: center; color: #0056b3;'>{jogador_2}</h3>", unsafe_allow_html=True)
            for metric, value in zip(metrics, player_2_stats):
                st.markdown(metric_style.format(metric=metric, value=value), unsafe_allow_html=True)

        # Linha final decorativa
        st.markdown("<hr style='border: 2px solid #0056b3; margin: 20px 0;'>", unsafe_allow_html=True)
