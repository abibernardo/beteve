import streamlit as st

glossario = {
    "PTS": "Pontos marcados pelo jogador.",
    "REB": "Rebotes capturados.",
    "AST": "Assistências realizadas.",
    "STL": "Roubos de bola.",
    "BLK": "Tocos dados.",
    "TOV": "Turnovers (erros de posse).",
    "FG%": "Percentual de acertos nos arremessos de quadra.",
    "3 FG%": "Percentual de acertos nos arremessos de três pontos.",
    "FT%": "Percentual de acertos nos lances livres.",
    "FGA": "Tentativas de arremessos de quadra.",
    "FGM": "Arremessos de quadra convertidos.",
    "FG3A": "Tentativas de arremessos de três pontos.",
    "FG3M": "Arremessos de três pontos convertidos.",
    "FTA": "Tentativas de lances livres.",
    "FTM": "Lances livres convertidos.",
    "MIN": "Minutos jogados.",
}



st.title("Glossário de Estatísticas da NBA")
st.divider()

col1, col2 = st.columns(2)


with col1:
    for i, (sigla, descricao) in enumerate(glossario.items()):
        if i % 2 == 0:  # Mostra itens em col1
            st.markdown(f"**{sigla}:** {descricao}")

with col2:
    for i, (sigla, descricao) in enumerate(glossario.items()):
        if i % 2 != 0:  # Mostra itens em col2
            st.markdown(f"**{sigla}:** {descricao}")

