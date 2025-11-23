# app.py (substitua seu arquivo atual por este)
import time
import requests
import streamlit as st

# ---------- Stable NBA wrapper (MUST be defined before nba_api imports) ----------
try:
    from nba_api.stats.library.http import NBAStatsHTTP
    class StableNBA(NBAStatsHTTP):
        def send_api_request(self, endpoint, params):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://www.nba.com/",
                "Origin": "https://www.nba.com",
                "Accept": "application/json, text/plain, */*",
            }
            for attempt in range(4):
                try:
                    resp = requests.get(self.BASE_URL.format(endpoint), params=params, headers=headers, timeout=8)
                    if resp.status_code == 200:
                        return resp
                except Exception:
                    pass
                time.sleep(1.2)
            raise Exception("Falha ao acessar API da NBA após múltiplas tentativas.")
    NBAStatsHTTP = StableNBA
except Exception:
    # se falhar, continuamos (biblioteca pode já expor algo compatível)
    pass

# ---------- imports da nba_api e demais libs (após wrapper) ----------
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, LeagueGameFinder, LeagueLeaders
import pandas as pd
import polars as pl
import plotly.express as px

# ---------- configurações / constantes ----------
STATS = ["PTS","REB","AST","STL","BLK","TOV","FG%","3 FG%","FT%","FGA","FGM","FG3A","FG3M","FTA","FTM","MIN"]
LEADER_STATS = ["PTS","REB","AST","STL","BLK","TOV","FGA","FGM","FG3A","FG3M","FTA","FTM","MIN","EFF","OREB","DREB"]

# ---------- cache wrappers para chamadas pesadas ----------
@st.cache_data(ttl=600)  # 10 minutos
def find_players(name: str):
    if not name:
        return []
    try:
        return players.find_players_by_full_name(name)
    except Exception:
        return []

@st.cache_data(ttl=600)
def get_career_dfs(player_id: int):
    if not player_id:
        return None, None
    try:
        pc = playercareerstats.PlayerCareerStats(player_id=player_id)
        df_season = pc.season_totals_regular_season.get_data_frame()
        df_career = pc.career_totals_regular_season.get_data_frame()
        return df_season, df_career
    except Exception:
        return None, None

@st.cache_data(ttl=600)
def get_games_df(player_id: int):
    if not player_id:
        return None
    try:
        lg = LeagueGameFinder(player_id_nullable=player_id, season_type_nullable='Regular Season')
        return lg.league_game_finder_results.get_data_frame()
    except Exception:
        return None

@st.cache_data(ttl=600)
def get_league_leaders(stat):
    if not stat:
        return None
    try:
        ll = LeagueLeaders(per_mode48='PerGame', season_type_all_star='Regular Season', stat_category_abbreviation=stat)
        return ll.league_leaders.get_data_frame()
    except Exception:
        return None

# ---------- UI simples ----------
st.title("ANÁLISE DE JOGADORES (versão simplificada & robusta)")

# busca por formulário (evita requisições em cada tecla)
with st.form("buscar"):
    nome_input = st.text_input("Nome do jogador", placeholder="Michael Jordan")
    buscar_btn = st.form_submit_button("Buscar")

show = st.radio("Visão", ["POR TEMPORADA", "CARREIRA"], horizontal=True)
st.divider()

if not buscar_btn:
    st.info("Digite um nome e clique em Buscar.")
    st.stop()

# ---------- achar jogador (cacheado) ----------
players_list = find_players(nome_input)
if not players_list:
    st.warning("Jogador não encontrado ou API indisponível. Tente outro nome.")
    st.stop()

jogador = players_list[0]
jogador_id = jogador.get("id")
nome = jogador.get("full_name", nome_input)

# ---------- buscar dados (cacheados) ----------
df_season_raw, df_career_raw = get_career_dfs(jogador_id)
df_games_raw = get_games_df(jogador_id)

if df_season_raw is None or df_career_raw is None:
    st.error("Não foi possível obter estatísticas de carreira. Tente novamente mais tarde.")
    st.stop()

# converte pra polars e aplica transformações (mantive sua lógica essencial)
df_carreira = pl.from_pandas(df_season_raw)
df_medias_raw = pl.from_pandas(df_career_raw)  # totais de carreira

def safe_to_percent(col):
    return (col * 100).round(1)

# medias / totais por temporada (compacto)
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
df_carreira = df_carreira.with_columns(
    pl.col("SEASON_ID").alias("temporada"),
    pl.col("SEASON_ID").str.extract(r"^(\d+)", 1).cast(pl.Int32).alias("ano"),
    (pl.col("PTS")/pl.col("GP")).round(1).alias("PTS"),
    (pl.col("REB")/pl.col("GP")).round(1).alias("REB"),
    (pl.col("AST")/pl.col("GP")).round(1).alias("AST"),
    (pl.col("STL")/pl.col("GP")).round(1).alias("STL"),
    (pl.col("BLK")/pl.col("GP")).round(1).alias("BLK"),
    (pl.col("TOV")/pl.col("GP")).round(1).alias("TOV"),
    (pl.col("FG_PCT")*100).alias("FG%"),
    (pl.col("FG3_PCT")*100).alias("3 FG%"),
    (pl.col("FT_PCT")*100).alias("FT%"),
    pl.col("GP").alias("Jogos")
)

# processa jogos (se tiver)
df_jogos = None
if df_games_raw is not None and not df_games_raw.empty:
    df_jogos = pl.from_pandas(df_games_raw)
    # renomeia/ajusta colunas básicas
    try:
        df_jogos = df_jogos.with_columns(
            pl.col("GAME_DATE").alias("DATA"),
            pl.col("WL").alias("W/L"),
            (pl.col("FG_PCT")*100).alias("FG%"),
            (pl.col("FG3_PCT")*100).alias("3 FG%"),
            (pl.col("FT_PCT")*100).alias("FT%")
        )
    except Exception:
        pass

# extrai métricas de carreira com segurança
def safe_item(df, r, c, default=0.0):
    try:
        return df.item(r, c)
    except Exception:
        return default

df_medias_proc = medias = df_medias_raw.with_columns(
    (pl.col("PTS")/pl.col("GP")).round(1).alias("PTS"),
    (pl.col("REB")/pl.col("GP")).round(1).alias("REB"),
    (pl.col("AST")/pl.col("GP")).round(1).alias("AST"),
    (pl.col("FG_PCT")*100).alias("FG%"),
) if df_medias_raw.height>0 else df_medias_raw

ppg = safe_item(df_medias_proc, 0, 0, 0.0)

# ---------- Exibição (compacta e segura) ----------
st.header(f"{nome}")

if show == "POR TEMPORADA":
    if df_jogos is None:
        st.info("Nenhum jogo encontrado para esse jogador.")
        st.stop()

    # cria lista de temporadas no formato 'YYYY-YYYY'
    try:
        df_jogos = df_jogos.with_columns(pl.concat_str([(pl.col("SEASON_ID")-1).cast(pl.Utf8), pl.lit("-"), pl.col("SEASON_ID").cast(pl.Utf8)]).alias("SEASON_ID"))
    except Exception:
        pass

    temporadas = [t for t in df_jogos["SEASON_ID"].unique().to_list() if isinstance(t, str) and "-" in t]
    temporadas = sorted(temporadas, key=lambda x: int(x.split("-")[0]), reverse=True)
    if not temporadas:
        st.info("Sem temporadas para exibir.")
        st.stop()

    temporada_sel = st.selectbox("Temporada", temporadas)
    df_sel = df_jogos.filter(pl.col("SEASON_ID")==temporada_sel)

    # mostra KPIs simples
    def safe_mean(col):
        try:
            return round(df_sel[col].mean(),1)
        except Exception:
            return 0.0

    cols = st.columns(5)
    kpis = [safe_mean("PTS"), safe_mean("REB"), safe_mean("AST"), safe_mean("STL"), safe_mean("BLK")]
    labels = ["PTS","REB","AST","STL","BLK"]
    for c, val, lab in zip(cols, kpis, labels):
        with c:
            st.metric(lab, val)

    # plot simples
    stat = st.selectbox("Estatística para o gráfico", STATS, index=0)
    fig = px.line(df_sel.to_pandas(), x=df_sel.to_pandas().index, y=stat, title=f"{stat} por jogo")
    st.plotly_chart(fig, use_container_width=True)

elif show == "CARREIRA":
    st.subheader("Médias de carreira")
    # tabela simplificada
    simples = df_medias_proc.select(["PTS","REB","AST","FG%"]).to_pandas() if df_medias_proc is not None else pd.DataFrame()
    st.table(simples.head(1).T if not simples.empty else simples)

    stat = st.selectbox("Estatística de interesse (carreira)", STATS, index=0, key="career_stat")
    # média por temporada
    try:
        fig = px.line(df_carreira.to_pandas(), x="ano", y=stat, markers=True)
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.info("Não foi possível plotar essa estatística.")

# ---------- Liga - líderes (opcional, compacto) ----------
st.divider()
st.subheader("Líderes da liga (por estatística)")
stat_lider = st.selectbox("Estatística", LEADER_STATS, index=0, key="leader_stat")
df_lider = get_league_leaders(stat_lider)
if df_lider is None:
    st.info("Líderes indisponíveis no momento.")
else:
    df_lider = pl.from_pandas(df_lider).select(["RANK","PLAYER","TEAM",stat_lider]).head(10)
    st.table(df_lider.to_pandas())

# fim
