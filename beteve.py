from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import PlayerProfileV2
import streamlit as st
from nba_api.stats.static import players
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
st.sidebar.success(" ")
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
    "FG3A",
    "FTA",
    "MIN"
]
st.title("ANÁLISE DE JOGADORES")
st.divider()
jogador_input = st.text_input("De que jogador você quer ver as estatísticas?")

###################
# Obtendo id do jogador
try:
    jogador_dict = players.find_players_by_full_name(jogador_input)
except Exception as e:
    st.write("## Confira o nome do jogador.")
try:
    jogador_id = jogador_dict[0]["id"]
except Exception as e:
    st.write("## Confira o nome do jogador.")

if jogador_dict:
    try:
        #####
        # puxando dados das bibliotecas
        nome = jogador_dict[0]["full_name"]
        stats_carreira = playercareerstats.PlayerCareerStats(player_id=jogador_id)   # stats de todas as temporadas
        stats_temporada = PlayerProfileV2(player_id=jogador_id)
        #stats_temporada = stats_temporada.season_totals_regular_season
        # stats dessa temporada
        ##########
        # construindo dataframes:

        # CARREIRA
        df_carreira = stats_carreira.season_totals_regular_season.get_data_frame()
        df_carreira = pl.from_pandas(df_carreira)
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
            (pl.col("FG_PCT")*100).alias("FG%"),
            (pl.col("FG3_PCT")*100).alias("3 FG%"),
            (pl.col("FT_PCT")*100).alias("FT%"),
            (pl.col("FGA") / pl.col("GP")).round(1),
            (pl.col("FG3A") / pl.col("GP")).round(1).alias("FG 3"),
            (pl.col("FTA") / pl.col("GP")).round(1),
            (pl.col("MIN") / pl.col("GP")).round(1)
        )

        #### TEMPORADA
        max_ano = df_carreira.select(pl.col("ano").max()).item()
        df_temporada = df_carreira.filter(pl.col("ano") == max_ano)
        df_temporada = df_temporada.select(
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
            pl.col("FG3A"),
            pl.col("FTA"),
            pl.col("MIN"),
            pl.col("temporada"))
        ppg = df_temporada.item(0, 0)
        rpg = df_temporada.item(0, 1)
        apg = df_temporada.item(0, 2)
        spg = df_temporada.item(0, 3)
        bpg = df_temporada.item(0, 4)
        tpg = df_temporada.item(0, 5)
        fg = df_temporada.item(0, 6)

        fg3 = df_temporada.item(0, 7)

        ft = df_temporada.item(0, 8)

        fga = df_temporada.item(0, 9)
        fg3a = df_temporada.item(0, 10)
        fta = df_temporada.item(0, 11)
        mpg = df_temporada.item(0, 12)
        temporada = df_temporada.item(0, 13)

        dados_carreira_tela = df_carreira.select(
            pl.col("temporada"),
            pl.col("time"),
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
            pl.col("FG3A"),
            pl.col("FTA"),
            pl.col("MIN")
        )

        ##### carreer high
        career_high = stats_temporada.career_highs.get_data_frame()
        career_high = pl.from_pandas(career_high)

    except Exception as e:
        st.write("")
else:
    st.write(" ")


if jogador_dict and jogador_input:
    st.write(f"# {nome}: {temporada}")
    cols = st.columns(5)
    stats_visual = [
        (f"{ppg}", "pts"),
        (f"{rpg}", "reb"),
        (f"{apg}", "ast"),
        (f"{spg}", "stl"),
        (f"{bpg}", "blk")
    ]

    # Iterando pelas colunas e adicionando estatísticas
    for col, (value, label) in zip(cols, stats_visual):
        with col:
            st.markdown(f"""
            <div style="text-align: center; background-color: #091836; padding: 10px; border-radius: 10px;">
                <p style="margin: 0; font-size: 24px; font-weight: bold; color: white;">{value}</p>
                <p style="margin: 0; font-size: 14px; color: gray;">{label}</p>
            </div>
            """, unsafe_allow_html=True)

    # Exibindo as porcentagens com formatação adicional
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p style="font-size: 28px; font-weight: bold; color: #333;">
            {fg:.1f}% FG / {fg3:.1f}% 3 PTS / {ft:.1f}% FT
        </p>
    </div>
    """.format(fg=fg, fg3=fg3, ft=ft), unsafe_allow_html=True)
    #st.write(f"# stats por temporada")
    #st.dataframe(dados_carreira_tela)
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        stat = st.selectbox(
            'Qual estatística quer analisar?',
            stats, key='stats')
    fig = px.line(df_carreira, x="ano", y=stat)
    st.plotly_chart(fig)

