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


st.title("GRÁFICO COMPARATIVO")
show = st.radio("Quais dados deseja utilizar?", ["Carreira", "Última temporada ativa"], horizontal=True)
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    stat_1 = st.selectbox("Eixo X", stats)
with col2:
    stat_2 = st.selectbox("Eixo Y", stats)
with col3:
    jogador_input = st.text_input("Adicione jogadores ao gráfico", placeholder="Lebron James")


if jogador_input:
    try:
        ### PUXANDO DADOS
        jogador_dict, jogador_id = achar_jogador(jogador_input)
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
        df_carreira = df_carreira.reverse().head(1)

        ### medias da carreira
        df_medias = medias_carreira(df_medias)
    except Exception as e:
        st.write(" ")
else:
    st.write(" ")


# Inicializa o DataFrame vazio no session_state, se ainda não existir
if show == "Carreira":
    if "dados" not in st.session_state:
        st.session_state["dados"] = pl.DataFrame(
            {
                "nome": pl.Series([], dtype=pl.Utf8),
                "PTS": pl.Series([], dtype=pl.Float64),
                "REB": pl.Series([], dtype=pl.Float64),
                "AST": pl.Series([], dtype=pl.Float64),
                "STL": pl.Series([], dtype=pl.Float64),
                "BLK": pl.Series([], dtype=pl.Float64),
                "TOV": pl.Series([], dtype=pl.Float64),
                "FG%": pl.Series([], dtype=pl.Float64),
                "3 FG%": pl.Series([], dtype=pl.Float64),
                "FT%": pl.Series([], dtype=pl.Float64),
                "FGA": pl.Series([], dtype=pl.Float64),
                "FGM": pl.Series([], dtype=pl.Float64),
                "FG3A": pl.Series([], dtype=pl.Float64),
                "FG3M": pl.Series([], dtype=pl.Float64),
                "FTA": pl.Series([], dtype=pl.Float64),
                "FTM": pl.Series([], dtype=pl.Float64),
                "MIN": pl.Series([], dtype=pl.Float64),
            }
        )

    colunas_a_manter = [
        "nome", "PTS", "REB", "AST", "STL", "BLK", "TOV",
        "FG%", "3 FG%", "FT%", "FGA", "FGM", "FG3A", "FG3M", "FTA", "FTM", "MIN"
    ]

    # Entrada do jogador
    if jogador_input:
        try:
            nome = jogador_dict[0]["full_name"]
        except Exception as e:
            st.write(" ")
        if 'nome' in locals():
            try:
                dados_novos = df_medias.with_columns(pl.lit(nome).alias("nome"))
                dados_novos = dados_novos.select(colunas_a_manter)
                nova_linha_df = pl.DataFrame([dados_novos.row(0)], schema=colunas_a_manter)
                st.session_state["dados"] = st.session_state["dados"].vstack(nova_linha_df)
            except Exception as e:
                st.write("Erro:", e)

    # Exibe o DataFrame atualizado
    df = st.session_state["dados"]
    df = df.to_pandas()

    fig = px.scatter(df, x=stat_1, y=stat_2, text='nome', log_x=True, size_max=60)
    fig.update_traces(textposition='top center')

    fig.update_layout(
        height=400,
        title_text='Comparação de jogadores'
    )

    st.plotly_chart(fig)

elif show == "Última temporada ativa":
    if "dados_temporada" not in st.session_state:
        st.session_state["dados_temporada"] = pl.DataFrame(
            {
                "nome": pl.Series([], dtype=pl.Utf8),
                "PTS": pl.Series([], dtype=pl.Float64),
                "REB": pl.Series([], dtype=pl.Float64),
                "AST": pl.Series([], dtype=pl.Float64),
                "STL": pl.Series([], dtype=pl.Float64),
                "BLK": pl.Series([], dtype=pl.Float64),
                "TOV": pl.Series([], dtype=pl.Float64),
                "FG%": pl.Series([], dtype=pl.Float64),
                "3 FG%": pl.Series([], dtype=pl.Float64),
                "FT%": pl.Series([], dtype=pl.Float64),
                "FGA": pl.Series([], dtype=pl.Float64),
                "FGM": pl.Series([], dtype=pl.Float64),
                "FG3A": pl.Series([], dtype=pl.Float64),
                "FG3M": pl.Series([], dtype=pl.Float64),
                "FTA": pl.Series([], dtype=pl.Float64),
                "FTM": pl.Series([], dtype=pl.Float64),
                "MIN": pl.Series([], dtype=pl.Float64),
            }
        )

    colunas_a_manter = [
        "nome", "PTS", "REB", "AST", "STL", "BLK", "TOV",
        "FG%", "3 FG%", "FT%", "FGA", "FGM", "FG3A", "FG3M", "FTA", "FTM", "MIN"
    ]

    # Entrada do jogador
    if jogador_input:
        try:
            nome = jogador_dict[0]["full_name"]
        except Exception as e:
            st.write(" ")
        if 'nome' in locals():
            try:
                dados_novos = df_carreira.with_columns(pl.lit(nome).alias("nome"))
                dados_novos = dados_novos.select(colunas_a_manter)
                nova_linha_df = pl.DataFrame([dados_novos.row(0)], schema=colunas_a_manter)
                st.session_state["dados_temporada"] = st.session_state["dados_temporada"].vstack(nova_linha_df)
            except Exception as e:
                st.write("Erro:", e)

    # Exibe o DataFrame atualizado
    df = st.session_state["dados_temporada"]
    df = df.to_pandas()

    fig = px.scatter(df, x=stat_1, y=stat_2, text='nome', log_x=True, size_max=60)
    fig.update_traces(textposition='top center')

    fig.update_layout(
        height=400,
        title_text='Comparação de jogadores'
    )

    st.plotly_chart(fig)

if st.button("Limpar dados"):
    for key in st.session_state.keys():
        del st.session_state[key]
