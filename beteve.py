import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Dados extraídos das tabelas com as colunas adicionais
dados = [
    # Tabelas 2, 3, 4 (AAS)
    {"ano": 1990, "p": 0.827, "var": 0.0006, "estimador": "p", "plano amostral": "AAS"},
    {"ano": 2000, "p": 0.595, "var": 0.00066, "estimador": "p", "plano amostral": "AAS"},
    {"ano": 2010, "p": 0.426, "var": 0.00067, "estimador": "p", "plano amostral": "AAS"},
    {"ano": 2020, "p": 0.401, "var": 0.00073, "estimador": "p", "plano amostral": "AAS"},

    {"ano": 1990, "p": 0.834, "var": 0.245, "estimador": "pr", "plano amostral": "AAS"},
    {"ano": 2000, "p": 0.597, "var": 0.274, "estimador": "pr", "plano amostral": "AAS"},
    {"ano": 2010, "p": 0.418, "var": 0.257, "estimador": "pr", "plano amostral": "AAS"},
    {"ano": 2020, "p": 0.409, "var": 0.261, "estimador": "pr", "plano amostral": "AAS"},

    {"ano": 1990, "p": 0.826, "var": 0.0006, "estimador": "preg", "plano amostral": "AAS"},
    {"ano": 2000, "p": 0.595, "var": 0.000665, "estimador": "preg", "plano amostral": "AAS"},
    {"ano": 2010, "p": 0.425, "var": 0.000669, "estimador": "preg", "plano amostral": "AAS"},
    {"ano": 2020, "p": 0.401, "var": 0.00073, "estimador": "preg", "plano amostral": "AAS"},

    # Tabelas 5, 6, 7 (AE)
    {"ano": 1990, "p": 0.830, "var": 0.000016, "estimador": "p", "plano amostral": "AE"},
    {"ano": 2000, "p": 0.617, "var": 0.0000018, "estimador": "p", "plano amostral": "AE"},
    {"ano": 2010, "p": 0.418, "var": 0.0000081, "estimador": "p", "plano amostral": "AE"},
    {"ano": 2020, "p": 0.346, "var": 0.00000144, "estimador": "p", "plano amostral": "AE"},

    {"ano": 1990, "p": 0.831, "var": 0.0003, "estimador": "pr", "plano amostral": "AE"},
    {"ano": 2000, "p": 0.620, "var": 0.00016, "estimador": "pr", "plano amostral": "AE"},
    {"ano": 2010, "p": 0.413, "var": 0.000064, "estimador": "pr", "plano amostral": "AE"},
    {"ano": 2020, "p": 0.352, "var": 0.000045, "estimador": "pr", "plano amostral": "AE"},

    {"ano": 1990, "p": 0.828, "var": 0.00059, "estimador": "preg", "plano amostral": "AE"},
    {"ano": 2000, "p": 0.617, "var": 0.000635, "estimador": "preg", "plano amostral": "AE"},
    {"ano": 2010, "p": 0.414, "var": 0.000465, "estimador": "preg", "plano amostral": "AE"},
    {"ano": 2020, "p": 0.346, "var": 0.000354, "estimador": "preg", "plano amostral": "AE"},
]

# Criando o dataframe consolidado
df = pl.DataFrame(dados)
df = df.with_columns(
    pl.col("ano").cast(str)
)

st.title("**ME430**")
st.sidebar.subheader("Escolha o que deseja comparar")
secs = ["Planos amostrais", "Tipos de estimadores"]
tickers = secs
x = st.sidebar.selectbox("Comparação", tickers)


if x == "Planos amostrais":
    y = st.radio(
        "Qual estimador deseja visualizar?",
        ["clássico", "razão", "regressão"])
    if y == "clássico":
        df = df.filter(pl.col("estimador") == "p")
    elif y == "razão":
        df = df.filter(pl.col("estimador") == "pr")
    elif y == "regressão":
        df = df.filter(pl.col("estimador") == "preg")
    col1, col2 = st.columns(2)
    with col1:
        fig_lines = px.line(
            df.to_pandas(),
            x="ano",
            y="p",
            color="plano amostral",
            title="Estimativas da proporção",
            labels={"ano": "Ano", "p": "Estimador p", "plano amostral": "Plano Amostral", "estimador": "Estimador"}
        )
        st.write(fig_lines)
    with col2:
        fig_bar = px.bar(
            df.to_pandas(),  # Convertendo o DataFrame para pandas para uso com plotly
            x="ano",
            y="var",
            color="plano amostral",
            facet_row="estimador",  # Cria uma subtrama para cada estimador
            title="Variância do estimador",
            labels={"var": "Variância", "ano": "Ano", "plano amostral": "Plano Amostral"},
            barmode="group"  # Agrupa as barras por plano amostral
        )
        st.write(fig_bar)
elif x == "Tipos de estimadores":
    z = st.radio(
        "Qual plano amostral deseja visualizar?",
        ["Amostragem Aleatória Simples", "Amostra Estratificada"])
    if z == "Amostragem Aleatória Simples":
        df = df.filter(pl.col("plano amostral") == "AAS")
    elif z == "Amostra Estratificada":
        df = df.filter(pl.col("plano amostral") == "AE")
    col1, col2 = st.columns(2)
    with col1:
        fig_lines = px.line(
            df.to_pandas(),
            x="ano",
            y="p",
            color="estimador",
            title="Estimativas pontuais",
            labels={"ano": "Ano", "p": "Estimador p", "plano amostral": "Plano Amostral", "estimador": "Estimador"}
        )
        st.write(fig_lines)
    with col2:
        fig_bar = px.bar(
            df.to_pandas(),  # Convertendo o DataFrame para pandas para uso com plotly
            x="ano",
            y="var",
            color="estimador",
            title="Variância de cada tipo de estimador",
            labels={"var": "Variância", "ano": "Ano", "plano amostral": "Plano Amostral"},
            barmode="group"  # Agrupa as barras por plano amostral
        )
        st.write(fig_bar)
