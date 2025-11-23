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
import time
import requests
from requests.exceptions import Timeout

# Tenta forçar headers usados por navegadores (ajuda a reduzir bloqueios)
try:
    from nba_api.stats.library.http import NBAStatsHTTP
    NBAStatsHTTP.headers = {
        "Host": "stats.nba.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://www.nba.com/",
        "x-nba-stats-origin": "stats",
        "x-nba-stats-token": "true",
    }
except Exception:
    # se não for possível sobrescrever, não quebra — apenas segue
    pass

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

# -----------------------
# CACHEADAS (API calls)
# -----------------------

@st.cache_data(ttl=3600)
def cached_find_players_by_name(name: str):
    """Busca jogadores estático (pode retornar lista vazia). Cacheada para evitar múltiplas requisições."""
    if not name:
        return []
    try:
        # players.find_players_by_full_name é um lookup estático, mas cache evita chamadas repetidas
        return players.find_players_by_full_name(name)
    except Exception as e:
        # Retorna lista vazia em caso de erro (tratado depois)
        return []

@st.cache_data(ttl=3600)
def cached_player_career_stats(player_id: int):
    """Busca career stats (totais por temporada e totais de carreira)."""
    if not player_id:
        return None, None
    try:
        t0 = time.time()
        stats_obj = playercareerstats.PlayerCareerStats(player_id=player_id)
        df_season_totals = stats_obj.season_totals_regular_season.get_data_frame()
        df_career_totals = stats_obj.career_totals_regular_season.get_data_frame()
        # apenas para debug, não escreve no app porque cache roda antes em alguns casos
        _ = time.time() - t0
        return df_season_totals, df_career_totals
    except Exception:
        return None, None

@st.cache_data(ttl=3600)
def cached_player_games(player_id: int):
    """Busca jogos do jogador via LeagueGameFinder."""
    if not player_id:
        return None
    try:
        t0 = time.time()
        finder = LeagueGameFinder(player_id_nullable=player_id, season_type_nullable='Regular Season')
        df = finder.league_game_finder_results.get_data_frame()
        _ = time.time() - t0
        return df
    except Exception:
        return None

# -----------------------
# Funções de transformação (mantive sua lógica)
# -----------------------

def achar_jogador(jogador_input):
    """Wrapper que usa cache e retorna (jogador_dict, jogador_id) ou (None, None)."""
    if not jogador_input:
        return None, None

    jogador_list = cached_find_players_by_name(jogador_input)

    if not jogador_list:
        st.warning("Jogador não encontrado ou a API não respondeu. Verifique o nome.")
        return None, None

    jogador = jogador_list[0]
    jogador_id = jogador.get("id")
    if not jogador_id:
        st.warning("Não foi possível obter o ID do jogador.")
        return None, None

    return jogador_list, jogador_id

def achar_jogo(jogador_id):
    """Retorna um DataFrame polars com os jogos ou None."""
    df = cached_player_games(jogador_id)
    if df is None or df.empty:
        return None

    df_jogos = pl.from_pandas(df)
    # manter apenas colunas úteis e renomear
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
        pl.col("MIN"),
        pl.col("SEASON_ID")
    )
    # Ajuste da coluna SEASON_ID para formato que você usa
    # Alguns SEASON_IDs vêm como '22020' etc; seu anterior fazia slice e +1 — mantive semelhante
    try:
        df_jogos = df_jogos.with_columns(
            (pl.col("SEASON_ID").str.slice(1).cast(pl.Int32) + 1).alias("SEASON_ID")
        )
    except Exception:
        # se falhar, deixa a coluna como está
        pass

    return df_jogos

def media_por_temporada(df_carreira):
    if df_carreira is None:
        return None
    df = df_carreira.with_columns(
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
    return df

def total_por_temporada(df_carreira):
    if df_carreira is None:
        return None
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
    if df_medias is None:
        return None
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
    if df_medias is None:
        return None
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

# -----------------------
# UI / fluxo principal
# -----------------------

st.title("ANÁLISE DE JOGADORES")
jogador_input = st.text_input("De que jogador você quer ver as estatísticas?", placeholder="Michael Jordan")
show = st.radio(" ", ["POR TEMPORADA", "CARREIRA"], horizontal=True)

if not jogador_input:
    st.write(" ")  # nada por enquanto
    st.stop()

# Pegando jogador (cacheado)
jogador_dict, jogador_id = achar_jogador(jogador_input)

if jogador_id is None:
    # Já mostramos aviso dentro de achar_jogador; interrompe execução para evitar chamadas subsequentes
    st.stop()

# Puxa career stats e jogos (cacheados)
df_season_totals_raw, df_career_totals_raw = cached_player_career_stats(jogador_id)
df_jogos_raw = cached_player_games(jogador_id)

# Verifica retornos
if df_season_totals_raw is None or df_career_totals_raw is None:
    st.warning("Não foi possível obter estatísticas de carreira. Tente novamente mais tarde.")
    st.stop()

# Converte para polars e aplica transformações
df_carreira = pl.from_pandas(df_season_totals_raw)
df_medias = pl.from_pandas(df_career_totals_raw)

# Processa jogos (pode ser None)
df_jogos = None
if df_jogos_raw is not None and not df_jogos_raw.empty:
    df_jogos = pl.from_pandas(df_jogos_raw)

# TRATANDO DADOS:  df_carreira = media por temporada
df_total_carreira = total_por_temporada(df_carreira)
df_carreira = media_por_temporada(df_carreira)

# totais carreira
totais_carreira = total_carreira(df_medias)
# medias da carreira
df_medias_proc = medias_carreira(df_medias)

# proteção contra DataFrames vazios
if df_medias_proc is None or df_medias_proc.height == 0:
    st.warning("Dados de média de carreira indisponíveis.")
    st.stop()

# extrai métricas de carreira com fallback
def safe_item(df, row, col_idx, default=0.0):
    try:
        return df.item(row, col_idx)
    except Exception:
        return default

ppg_carreira = safe_item(df_medias_proc, 0, 0, 0.0)
rpg_carreira = safe_item(df_medias_proc, 0, 1, 0.0)
apg_carreira = safe_item(df_medias_proc, 0, 2, 0.0)
spg_carreira = safe_item(df_medias_proc, 0, 3, 0.0)
bpg_carreira = safe_item(df_medias_proc, 0, 4, 0.0)
tpg_carreira = safe_item(df_medias_proc, 0, 5, 0.0)
fg_carreira = safe_item(df_medias_proc, 0, 6, 0.0)
fg3_carreira = safe_item(df_medias_proc, 0, 7, 0.0)
ft_carreira = safe_item(df_medias_proc, 0, 8, 0.0)

# -----------------------
# Exibição (mantive sua lógica)
# -----------------------

try:
    nome = jogador_dict[0]["full_name"]
except Exception:
    nome = jogador_input

if show == "POR TEMPORADA":
    if df_jogos is None:
        st.info("Nenhum jogo encontrado para exibir essa visualização.")
        st.stop()

    # Construção de SEASON_ID no formato 'XXXX-YYYY' para seleção
    try:
        df_jogos = df_jogos.with_columns(
            pl.concat_str(
                [
                    (pl.col("SEASON_ID") - 1).cast(pl.Utf8),
                    pl.lit("-"),
                    pl.col("SEASON_ID").cast(pl.Utf8)
                ]
            ).alias("SEASON_ID")
        )
    except Exception:
        # se a transformação falhar, segue sem modificar
        pass

    st.divider()

    temporadas = df_jogos["SEASON_ID"].unique().to_list()
    temporadas = [t for t in temporadas if isinstance(t, str) and "-" in t and len(t.split("-")) == 2]
    def extrair_ano_inicial(temporada):
        return int(temporada.split("-")[0])
    temporadas = sorted(temporadas, key=extrair_ano_inicial, reverse=True)

    col7, col8 = st.columns(2)
    with col7:
        temp = st.selectbox("Selecione uma temporada", temporadas)
    if not temp:
        st.info("Selecione uma temporada.")
        st.stop()

    df_jogos = df_jogos.filter(pl.col("SEASON_ID") == temp)

    # cálculos seguros com fallback
    def safe_mean(col):
        try:
            return round(df_jogos[col].mean(), 1)
        except Exception:
            return 0.0

    ppg = safe_mean("PTS")
    rpg = safe_mean("REB")
    apg = safe_mean("AST")
    spg = safe_mean("STL")
    bpg = safe_mean("BLK")

    def safe_pct(numer_col, denom_col):
        try:
            num = df_jogos[numer_col].sum()
            den = df_jogos[denom_col].sum()
            if den == 0:
                return 0.0
            return round((num / den) * 100, 1)
        except Exception:
            return 0.0

    fg = safe_pct("FGM", "FGA")
    fg3 = safe_pct("FG3M", "FG3A")
    ft = safe_pct("FTM", "FTA")

    st.write(f"# {nome}: {temp}")
    cols = st.columns(5)
    stats_visual = [
        (f"{ppg}", "pts"),
        (f"{rpg}", "reb"),
        (f"{apg}", "ast"),
        (f"{spg}", "stl"),
        (f"{bpg}", "blk")
    ]

    for col, (value, label) in zip(cols, stats_visual):
        with col:
            st.markdown(f"""
                    <div style="text-align: center; background-color: #091836; padding: 10px; border-radius: 10px;">
                        <p style="margin: 0; font-size: 24px; font-weight: bold; color: white;">{value}</p>
                        <p style="margin: 0; font-size: 14px; color: gray;">{label}</p>
                    </div>
                    """, unsafe_allow_html=True)

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
        pl.col("MIN")
    )

    df_jogos = (
        df_jogos
            .with_row_count(name="jogos")
            .with_columns((pl.lit(df_jogos.height) - pl.col("jogos")).alias("jogos"))
    )

    st.divider()
    col11, col12 = st.columns(2)
    with col11:
        stat = st.selectbox('Estatística de interesse', stats, key='stats')

    fig = px.line(df_jogos.to_pandas(), x="jogos", y=stat)
    st.plotly_chart(fig)

    if stat not in ["FG%", "3 FG%", "FT%"]:
        try:
            media = round(df_jogos_display[stat].mean(), 1)
        except Exception:
            media = 0.0
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

    for col, (value, label) in zip(cols, stats_visual):
        with col:
            st.markdown(f"""
                           <div style="text-align: center; background-color: #091836; padding: 10px; border-radius: 10px;">
                               <p style="margin: 0; font-size: 24px; font-weight: bold; color: white;">{value}</p>
                               <p style="margin: 0; font-size: 14px; color: gray;">{label}</p>
                           </div>
                           """, unsafe_allow_html=True)

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
        stat = st.selectbox('Estatística de interesse', stats, key='stats_career')
    with col2:
        tipo_stat = st.radio("Forma da estatística", ["Por jogo", "Total"])

    # valores seguros para médias e totais
    try:
        media_carreira = df_medias_proc.select(pl.col(stat).first()).item()
    except Exception:
        media_carreira = 0.0
    try:
        total_carreira_stat = totais_carreira.select(pl.col(stat).first()).item()
    except Exception:
        total_carreira_stat = 0.0

    if tipo_stat == "Por jogo":
        try:
            fig = px.line(df_carreira.to_pandas(), x="ano", y=stat)
            fig.update_layout(
                xaxis=dict(
                    tickmode="array",
                    tickvals=df_carreira["ano"].to_list(),
                )
            )
            st.plotly_chart(fig)
            st.markdown(
                f"<p style='font-size:18px; font-weight:bold; text-align:center;'>{media_carreira:.1f} {stat} de média na carreira</p>",
                unsafe_allow_html=True)
            st.divider()
        except Exception:
            st.info("Não foi possível plotar a estatística por jogo.")
    elif tipo_stat == "Total":
        try:
            fig = px.line(df_total_carreira.to_pandas(), x="ano", y=stat)
            fig.update_layout(
                xaxis=dict(
                    tickmode="array",
                    tickvals=df_total_carreira["ano"].to_list(),
                )
            )
            st.plotly_chart(fig)
            st.markdown(
                f"<p style='font-size:18px; font-weight:bold; text-align:center;'>{total_carreira_stat} {stat} na carreira</p>",
                unsafe_allow_html=True)
            st.divider()
        except Exception:
            st.info("Não foi possível plotar a estatística total.")

# fim do script
