from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

import streamlit as st
import pandas as pd
import polars as pl
import plotly.express as px

from nba_api.stats.library.http import NBAStatsHTTP

NBAStatsHTTP.TIMEOUT = 10
st.set_page_config(layout="wide")

# =========================================================
# CONFIG
# =========================================================

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

# =========================================================
# CACHE
# =========================================================

@st.cache_data(ttl=3600)
def achar_jogador(nome):
    jogador = players.find_players_by_full_name(nome)

    if not jogador:
        return None, None

    return jogador[0], jogador[0]["id"]


@st.cache_data(ttl=3600)
def puxar_stats_carreira(jogador_id):

    stats_carreira = playercareerstats.PlayerCareerStats(
        player_id=jogador_id
    )

    # TEMPORADAS
    df_carreira = stats_carreira.season_totals_regular_season.get_data_frame()

    # TOTAIS CARREIRA
    df_totais = stats_carreira.career_totals_regular_season.get_data_frame()

    return (
        pl.from_pandas(df_carreira),
        pl.from_pandas(df_totais)
    )


@st.cache_data(ttl=3600)
def puxar_jogos(jogador_id, temporada):

    gamelog = playergamelog.PlayerGameLog(
        player_id=jogador_id,
        season=temporada
    )

    df = gamelog.get_data_frames()[0]

    return pl.from_pandas(df)


# =========================================================
# TRATAMENTO
# =========================================================

def media_por_temporada(df):

    df = df.with_columns(
        pl.col("SEASON_ID").alias("temporada"),

        pl.col("SEASON_ID")
        .str.extract(r"^(\d+)", 1)
        .cast(pl.Int32)
        .alias("ano"),

        (pl.col("PTS") / pl.col("GP")).round(1).alias("PTS"),
        (pl.col("REB") / pl.col("GP")).round(1).alias("REB"),
        (pl.col("AST") / pl.col("GP")).round(1).alias("AST"),
        (pl.col("STL") / pl.col("GP")).round(1).alias("STL"),
        (pl.col("BLK") / pl.col("GP")).round(1).alias("BLK"),
        (pl.col("TOV") / pl.col("GP")).round(1).alias("TOV"),

        ((pl.col("FG_PCT")) * 100).round(1).alias("FG%"),
        ((pl.col("FG3_PCT")) * 100).round(1).alias("3 FG%"),
        ((pl.col("FT_PCT")) * 100).round(1).alias("FT%"),

        (pl.col("FGA") / pl.col("GP")).round(1).alias("FGA"),
        (pl.col("FGM") / pl.col("GP")).round(1).alias("FGM"),
        (pl.col("FG3A") / pl.col("GP")).round(1).alias("FG3A"),
        (pl.col("FG3M") / pl.col("GP")).round(1).alias("FG3M"),
        (pl.col("FTA") / pl.col("GP")).round(1).alias("FTA"),
        (pl.col("FTM") / pl.col("GP")).round(1).alias("FTM"),

        (pl.col("MIN") / pl.col("GP")).round(1).alias("MIN")
    )

    return df


def tratar_jogos(df):

    df = df.with_columns(

        pl.col("GAME_DATE").alias("DATA"),

        pl.col("WL").alias("W/L"),

        ((pl.col("FG_PCT")) * 100).round(1).alias("FG%"),

        ((pl.col("FG3_PCT")) * 100)
        .fill_nan(0)
        .round(1)
        .alias("3 FG%"),

        ((pl.col("FT_PCT")) * 100)
        .fill_nan(0)
        .round(1)
        .alias("FT%")
    )

    return df


def card(valor, label):

    st.markdown(
        f"""
        <div style="
            text-align:center;
            background-color:#091836;
            padding:12px;
            border-radius:12px;
        ">
            <p style="
                margin:0;
                font-size:28px;
                font-weight:bold;
                color:white;
            ">
                {valor}
            </p>

            <p style="
                margin:0;
                color:gray;
            ">
                {label}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# UI
# =========================================================

st.title("ANÁLISE NBA")

jogador_input = st.text_input(
    "Digite um jogador",
    placeholder="Michael Jordan"
)

show = st.radio(
    "Modo",
    ["POR TEMPORADA", "CARREIRA"]
)

buscar = st.button("Buscar")

# =========================================================
# EXECUÇÃO
# =========================================================

if buscar and jogador_input:

    try:

        # =====================================================
        # JOGADOR
        # =====================================================

        jogador, jogador_id = achar_jogador(jogador_input)

        if jogador_id is None:
            st.error("Jogador não encontrado.")
            st.stop()

        nome = jogador["full_name"]

        # =====================================================
        # CARREIRA
        # =====================================================

        df_carreira_raw, df_totais = puxar_stats_carreira(
            jogador_id
        )

        df_carreira = media_por_temporada(
            df_carreira_raw
        )

        # =====================================================
        # POR TEMPORADA
        # =====================================================

        if show == "POR TEMPORADA":

            temporadas = (
                df_carreira["temporada"]
                .unique()
                .to_list()
            )

            temporadas = sorted(
                temporadas,
                reverse=True
            )

            temporada = st.selectbox(
                "Selecione a temporada",
                temporadas
            )

            df_jogos = puxar_jogos(
                jogador_id,
                temporada
            )

            df_jogos = tratar_jogos(df_jogos)

            # =========================================
            # MÉDIAS
            # =========================================

            ppg = round(df_jogos["PTS"].mean(), 1)
            rpg = round(df_jogos["REB"].mean(), 1)
            apg = round(df_jogos["AST"].mean(), 1)
            spg = round(df_jogos["STL"].mean(), 1)
            bpg = round(df_jogos["BLK"].mean(), 1)

            st.divider()

            st.subheader(f"{nome} — {temporada}")

            cols = st.columns(5)

            with cols[0]:
                card(ppg, "PTS")

            with cols[1]:
                card(rpg, "REB")

            with cols[2]:
                card(apg, "AST")

            with cols[3]:
                card(spg, "STL")

            with cols[4]:
                card(bpg, "BLK")

            st.divider()

            # =========================================
            # GRÁFICO
            # =========================================

            stat = st.selectbox(
                "Estatística",
                stats
            )

            df_jogos = (
                df_jogos
                .with_row_count("jogo")
            )

            fig = px.line(
                df_jogos.to_pandas(),
                x="jogo",
                y=stat,
                title=f"{stat} por jogo"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =========================================
            # TABELA
            # =========================================

            st.dataframe(
                df_jogos.select(
                    [
                        "DATA",
                        "MATCHUP",
                        "W/L",
                        "PTS",
                        "REB",
                        "AST",
                        "STL",
                        "BLK",
                        "FG%",
                        "3 FG%",
                        "FT%"
                    ]
                ).to_pandas(),
                use_container_width=True
            )

        # =====================================================
        # CARREIRA
        # =====================================================

        elif show == "CARREIRA":

            st.divider()

            st.subheader(f"Carreira de {nome}")

            media_pts = df_carreira["PTS"].mean()
            media_reb = df_carreira["REB"].mean()
            media_ast = df_carreira["AST"].mean()
            media_stl = df_carreira["STL"].mean()
            media_blk = df_carreira["BLK"].mean()

            cols = st.columns(5)

            with cols[0]:
                card(round(media_pts, 1), "PTS")

            with cols[1]:
                card(round(media_reb, 1), "REB")

            with cols[2]:
                card(round(media_ast, 1), "AST")

            with cols[3]:
                card(round(media_stl, 1), "STL")

            with cols[4]:
                card(round(media_blk, 1), "BLK")

            st.divider()

            stat = st.selectbox(
                "Estatística",
                stats
            )

            fig = px.line(
                df_carreira.to_pandas(),
                x="ano",
                y=stat,
                title=f"{stat} ao longo da carreira"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                df_carreira.select(
                    [
                        "temporada",
                        "PTS",
                        "REB",
                        "AST",
                        "STL",
                        "BLK",
                        "FG%",
                        "3 FG%",
                        "FT%"
                    ]
                ).to_pandas(),
                use_container_width=True
            )

    except Exception as e:
        st.error(e)
