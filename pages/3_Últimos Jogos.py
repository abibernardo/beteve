from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import PlayerProfileV2
from nba_api.stats.endpoints import LeagueLeaders
import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import BoxScoreTraditionalV2
from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd
import polars as pl
import plotly.express as px
import plotly.graph_objects as go

# objetos
nba_teams_abbreviations = [
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
            st.write("## Confira o nome do jogador.")

def achar_time(time_input):
    if time_input:
        try:
            time_dict = teams.find_team_by_abbreviation(time_input)
        except Exception as e:
            st.write("## Confira o nome do jogador.")
        try:
            time_id = time_dict["id"]
            return time_id
        except Exception as e:
            st.write("## Confira o nome do jogador.")



def achar_jogo_jogador(jogador_id):
    try:
        # Busca jogos associados ao jogador
        jogo = LeagueGameFinder(player_id_nullable=jogador_id)
        df = jogo.league_game_finder_results.get_data_frame()
    except Exception as e:
        st.write(f"Erro ao buscar dados: {e}")
        df = pd.DataFrame()  # DataFrame vazio em caso de erro
    if not df.empty:
        df_jogos = pl.from_pandas(df)
        return df_jogos
    else:
        st.write("Nenhum dado disponível para exibir.")

def achar_jogo_time(time):
    try:
        # Busca jogos associados ao jogador
        jogo = LeagueGameFinder(team_id_nullable=time)
        df = jogo.league_game_finder_results.get_data_frame()
    except Exception as e:
        st.write(f"Erro ao buscar dados: {e}")
        df = pd.DataFrame()  # DataFrame vazio em caso de erro
    if not df.empty:
        df_jogos = pl.from_pandas(df)
        return df_jogos
    else:
        st.write("Nenhum dado disponível para exibir.")


st.title("Estatísticas dos últimos jogos")
filtro = st.radio(" ", ["Time", "Jogador"])

st.divider()

col1, col2 = st.columns(2)
with col1:
    if filtro=='Jogador':
        input = st.text_input("De que jogador você quer ver as estatísticas?")
        if input:
            jogador_dict, jogador_id = achar_jogador(input)
        else:
            jogador_dict, jogador_id = achar_jogador('harden')
        nome = jogador_dict[0]["full_name"]

        df_jogos = achar_jogo_jogador(jogador_id)
    elif filtro =='Time':
        input = st.selectbox("De que time você quer ver as estatísticas?", nba_teams_abbreviations)
        time_id = achar_time(input)
        df_jogos = achar_jogo_time(time_id)

with col2:
    ultimos_jogos = st.number_input("Há quantos jogos?", min_value=1, step=1)


df_jogos = df_jogos.head(ultimos_jogos)
df_jogos = df_jogos.with_row_count(name="jogo").with_columns((pl.col("jogo") + 1).alias("jogo"))


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
        pl.col("MIN")
    )


#### Médias
# Calculando médias com apenas uma casa decimal
ppg = round(df_jogos["PTS"].mean(), 1)
rpg = round(df_jogos["REB"].mean(), 1)
apg = round(df_jogos["AST"].mean(), 1)
spg = round(df_jogos["STL"].mean(), 1)
bpg = round(df_jogos["BLK"].mean(), 1)

# Calculando porcentagens FG, FG3, e FT com apenas uma casa decimal
fg = round((df_jogos["FGM"].sum() / df_jogos["FGA"].sum()) * 100, 1)
fg3 = round((df_jogos["FG3M"].sum() / df_jogos["FG3A"].sum()) * 100, 1)
ft = round((df_jogos["FTM"].sum() / df_jogos["FTA"].sum()) * 100, 1)

# Configuração dos valores para exibição

stats_visual = [
    (f"{ppg}", "pts"),
    (f"{rpg}", "reb"),
    (f"{apg}", "ast"),
    (f"{spg}", "stl"),
    (f"{bpg}", "blk")
]

# Exibindo os valores no layout do Streamlit

if filtro == "Jogador":
    st.write(f'## Últimos {ultimos_jogos} jogos de {nome}')

if filtro == "Jogador":
    cols = st.columns(5)
    for col, (value, label) in zip(cols, stats_visual):
        with col:
            st.markdown(f"""
                <div style="text-align: center; background-color: #091836; padding: 10px; border-radius: 10px;">
                    <p style="margin: 0; font-size: 24px; font-weight: bold; color: white;">{value}</p>
                    <p style="margin: 0; font-size: 14px; color: gray;">{label}</p>
                </div>""", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            <p style="font-size: 28px; font-weight: bold; color: #333;">
                {fg:.1f}% FG / {fg3:.1f}% 3 PTS / {ft:.1f}% FT
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.divider()
    for row in df_jogos.iter_rows(named=True):
        data = row["DATA"]
        matchup = row["MATCHUP"]
        win_loss = row["W/L"]

        # Customizando o layout para cada linha
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 10px;">
                <p style="margin: 0; font-size: 18px; color: #555;"><b>Data:</b> {data}</p>
                <p style="margin: 0; font-size: 18px; color: #555;"><b>Matchup:</b> {matchup}</p>
                <p style="margin: 0; font-size: 18px; color: {'green' if win_loss == 'W' else 'red'};"><b>Resultado:</b> {win_loss}</p>
            </div>
        """, unsafe_allow_html=True)



st.divider()

col11, col12 = st.columns(2)
if ultimos_jogos > 1:
    with col11:
        stat = st.selectbox(
                    'Estatística de interesse',
                    stats, key='stats')
    st.write(f"## {stat} ao longo dos últimos {ultimos_jogos} jogos")
    fig = px.line(df_jogos, x="jogo", y=stat)
    fig.update_layout(
            xaxis=dict(
            tickmode="array",  # Define os ticks manualmente
            tickvals=df_jogos["jogo"].to_list(),))  # Usa os valores únicos da coluna 'ano'
    st.plotly_chart(fig)

st.divider()
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
st.dataframe(df_jogos_display)
