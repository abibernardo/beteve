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
import requests
import time
from nba_api.stats.library.http import NBAStatsHTTP

# Wrapper que substitui TODAS as requisições internas da nba_api
class StableNBA(NBAStatsHTTP):
    def send_api_request(self, endpoint, params):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://www.nba.com/",
            "Origin": "https://www.nba.com",
            "Accept": "application/json, text/plain, */*",
        }

        for tentativa in range(4):  # tenta até 4 vezes
            try:
                resp = requests.get(
                    self.BASE_URL.format(endpoint),
                    params=params,
                    headers=headers,
                    timeout=8
                )
                if resp.status_code == 200:
                    return resp
            except Exception:
                pass
            time.sleep(1.2)

        raise Exception("Falha ao acessar a API da NBA após múltiplas tentativas.")

# Substitui o cliente nativo
NBAStatsHTTP = StableNBA


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


@st.cache_data(ttl=3600)
def achar_jogador(jogador_input):
    if not jogador_input:
        return None, None

    try:
        # timeout evita travamento infinito
        jogador_dict = players.find_players_by_full_name(jogador_input)
    except Exception:
        st.write("⚠️ Não foi possível consultar o jogador. Verifique o nome.")
        return None, None

    # se a API retornar lista vazia (caso comum quando dá rate limit)
    if not jogador_dict:
        st.write("⚠️ Jogador não encontrado ou API não respondeu.")
        return None, None

    # evita IndexError
    jogador_id = jogador_dict[0].get("id", None)
    if jogador_id is None:
        st.write("⚠️ Não foi possível obter o ID do jogador.")
        return None, None

    return jogador_dict, jogador_id

@st.cache_data(ttl=3600)
def get_career(jogador_id):
    from nba_api.stats.endpoints import playercareerstats
    return playercareerstats.PlayerCareerStats(player_id=jogador_id)

@st.cache_data(ttl=3600)
def get_games(jogador_id):
    from nba_api.stats.endpoints import LeagueGameFinder
    jogo = LeagueGameFinder(player_id_nullable=jogador_id, season_type_nullable='Regular Season')
    return jogo.league_game_finder_results.get_data_frame()


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


st.title("ANÁLISE DE JOGADORES")
jogador_input = st.text_input("De que jogador você quer ver as estatísticas?", placeholder="Michael Jordan")
show = st.radio(" ", ["POR TEMPORADA", "CARREIRA"], horizontal=True)

if jogador_input:
    try:
        ### PUXANDO DADOS
        jogador_dict, jogador_id = achar_jogador(jogador_input)
        stats_carreira = get_career(jogador_id)
        df_carreira = stats_carreira.season_totals_regular_season.get_data_frame()
        df_carreira = pl.from_pandas(df_carreira)
        df_medias = stats_carreira.career_totals_regular_season.get_data_frame()
        df_medias = pl.from_pandas(df_medias)
        df_jogos = pl.from_pandas(get_games(jogador_id))


        ### TRATANDO DADOS:  df_carreira = media por temporada
        df_total_carreira = total_por_temporada(df_carreira)
        df_carreira = media_por_temporada(df_carreira)

        ### totais carreira
        totais_carreira = total_carreira(df_medias)
        ### medias da carreira
        df_medias = medias_carreira(df_medias)
        ppg_carreira = df_medias.item(0, 0)
        rpg_carreira = df_medias.item(0, 1)
        apg_carreira = df_medias.item(0, 2)
        spg_carreira = df_medias.item(0, 3)
        bpg_carreira = df_medias.item(0, 4)
        tpg_carreira = df_medias.item(0, 5)
        fg_carreira = df_medias.item(0, 6)
        fg3_carreira = df_medias.item(0, 7)
        ft_carreira = df_medias.item(0, 8)



    except Exception as e:
        st.write(" ")
else:
    st.write(" ")



if jogador_input:
    try:
        nome = jogador_dict[0]["full_name"]
        if show == "POR TEMPORADA":
            df_jogos = df_jogos.with_columns(
                pl.concat_str(
                    [
                        (pl.col("SEASON_ID") - 1).cast(pl.Utf8),  # Subtrai 1 e converte para string
                        pl.lit("-"),  # Adiciona o separador "-"
                        pl.col("SEASON_ID").cast(pl.Utf8)  # Mantém o valor original como string
                    ]
                ).alias("SEASON_ID")  # Renomeia a nova coluna
            )
            st.divider()

            # criando e ordenando temporadas
            temporadas = df_jogos["SEASON_ID"].unique().to_list()
            temporadas = [t for t in temporadas if "-" in t and len(t.split("-")) == 2]
            def extrair_ano_inicial(temporada):
                return int(temporada.split("-")[0])
            temporadas = sorted(temporadas, key=extrair_ano_inicial, reverse=True)

            col7, col8 = st.columns(2)
            with col7:
                temp = st.selectbox("Selecione uma temporada", temporadas)
            df_jogos = df_jogos.filter(pl.col("SEASON_ID") == temp)
            ppg = round(df_jogos["PTS"].mean(), 1)
            rpg = round(df_jogos["REB"].mean(), 1)
            apg = round(df_jogos["AST"].mean(), 1)
            spg = round(df_jogos["STL"].mean(), 1)
            bpg = round(df_jogos["BLK"].mean(), 1)
            fg = round((df_jogos["FGM"].sum() / df_jogos["FGA"].sum()) * 100, 1)
            fg3 = round((df_jogos["FG3M"].sum() / df_jogos["FG3A"].sum()) * 100, 1)
            ft = round((df_jogos["FTM"].sum() / df_jogos["FTA"].sum()) * 100, 1)

            st.write(f"# {nome}: {temp}")
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

            df_jogos_display = df_jogos.select(
                pl.col("DATA"),
                pl.col("MATCHUP"),
                pl.col("W/L"),
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
            df_jogos = (
                df_jogos
                    .with_row_count(name="jogos")
                    .with_columns((pl.lit(df_jogos.height) - pl.col("jogos")).alias("jogos"))
            )

            st.divider()
            col11, col12 = st.columns(2)
            if jogador_input:
                with col11:
                    stat = st.selectbox(
                        'Estatística de interesse',
                        stats, key='stats')
                fig = px.line(df_jogos, x="jogos", y=stat)
                st.plotly_chart(fig)
                if stat not in ["FG%", "3 FG%", "FT%"]:
                    media = round(df_jogos_display[stat].mean(), 1)
                    st.markdown(
                        f"<p style='font-size:18px; font-weight:bold; text-align:center;'>Média de {media}</p>",
                        unsafe_allow_html=True)

        elif show == "CARREIRA":
            st.divider()
            st.write(f"# Carreira de {nome}")
            cols = st.columns(5)
            stats_visual = [
                (f"{ppg_carreira}", "pts"),
                (f"{rpg_carreira}", "reb"),
                (f"{apg_carreira}", "ast"),
                (f"{spg_carreira}", "stl"),
                (f"{bpg_carreira}", "blk")
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
                           """.format(fg=fg_carreira, fg3=fg3_carreira, ft=ft_carreira), unsafe_allow_html=True)
            st.divider()
            st.write("## Estatísticas ao longo da carreira")
            col1, col15, col2 = st.columns(3)
            with col1:
                stat = st.selectbox(
                    'Estatística de interesse',
                    stats, key='stats')
            with col2:
                tipo_stat = st.radio("Forma da estatística", ["Por jogo", "Total"])
            media_carreira = df_medias.select(pl.col(stat).first()).item()
            total_carreira_stat = totais_carreira.select(pl.col(stat).first()).item()

            if tipo_stat == "Por jogo":
                fig = px.line(df_carreira, x="ano", y=stat)
                fig.update_layout(
                    xaxis=dict(
                        tickmode="array",  # Define os ticks manualmente
                        tickvals=df_carreira["ano"].to_list(),  # Usa os valores únicos da coluna 'ano'
                    )
                )
                st.plotly_chart(fig)
                st.markdown(
                    f"<p style='font-size:18px; font-weight:bold; text-align:center;'>{media_carreira:.1f} {stat} de média na carreira</p>",
                    unsafe_allow_html=True)
                st.divider()
            elif tipo_stat == "Total":
                fig = px.line(df_total_carreira, x="ano", y=stat)
                fig.update_layout(
                    xaxis=dict(
                        tickmode="array",  # Define os ticks manualmente
                        tickvals=df_total_carreira["ano"].to_list(),  # Usa os valores únicos da coluna 'ano'
                    )
                )
                st.plotly_chart(fig)
                st.markdown(
                    f"<p style='font-size:18px; font-weight:bold; text-align:center;'>{total_carreira_stat} {stat} na carreira</p>",
                    unsafe_allow_html=True)
                st.divider()
    except Exception as e:
        st.write(" ")
