import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuración de la página ---
st.set_page_config(
    page_title="Dashboard Spotify",
    #page_icon="🎵",
    layout="wide"
)

# Paleta de colores
COLOR_PRINCIPAL = "#1DB954"
COLOR_SECUNDARIO = "#191414"

# --- CSS personalizado ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #191414;
        border: 1px solid #1DB954;
        border-radius: 10px;
        padding: 15px;
    }
    div[data-testid="stMetricLabel"] {
        color: #1DB954;
    }
    h1, h2, h3 {
        color: #1DB954;
    }
    </style>
""", unsafe_allow_html=True)

# --- Cargar datos ---
dataframe = pd.read_csv("https://raw.githubusercontent.com/JesusAndres765/datasets/refs/heads/main/playlist.csv")
dataframe["duracion_min"] = dataframe["track_duration_ms"] / 60000

# --- Encabezado ---
st.title("Dashboard de mi Playlist de Spotify")
st.write("Análisis de canciones, artistas y popularidad")

# BARRA LATERAL: BÚSQUEDA Y FILTROS
st.sidebar.header("Búsqueda y filtros")

busqueda = st.sidebar.text_input("Buscar canción, artista o álbum")

artistas_disponibles = sorted(dataframe["name_of_artists"].unique())
artista_seleccionado = st.sidebar.selectbox(
    "Filtrar por artista específico",
    options=["Todos"] + artistas_disponibles
)

pop_min, pop_max = st.sidebar.slider(
    "Rango de popularidad",
    0, 100, (0, 100)
)

solo_explicitas = st.sidebar.checkbox("Solo canciones explícitas")

# --- Aplicar filtros ---
df_filtrado = dataframe.copy()

if busqueda:
    mask = (
        df_filtrado["track_name"].str.contains(busqueda, case=False, na=False)
        | df_filtrado["name_of_artists"].str.contains(busqueda, case=False, na=False)
        | df_filtrado["album_name"].str.contains(busqueda, case=False, na=False)
    )
    df_filtrado = df_filtrado[mask]

if artista_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["name_of_artists"] == artista_seleccionado]

df_filtrado = df_filtrado[
    (df_filtrado["track_popularity"] >= pop_min) &
    (df_filtrado["track_popularity"] <= pop_max)
]

if solo_explicitas:
    df_filtrado = df_filtrado[df_filtrado["track_explicit"] == True]

st.sidebar.write(f"**{len(df_filtrado)} canciones encontradas**")

st.divider()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de canciones", len(df_filtrado))
col2.metric("Popularidad promedio", round(df_filtrado["track_popularity"].mean(), 1) if len(df_filtrado) > 0 else 0)
col3.metric("Canciones explícitas", int(df_filtrado["track_explicit"].sum()))
col4.metric("Artistas distintos", df_filtrado["name_of_artists"].nunique())

st.divider()

# TABLA DE DATOS
st.subheader("Resultados de la búsqueda")
st.dataframe(
    df_filtrado[["track_name", "name_of_artists", "album_name", "track_popularity", "track_explicit"]],
    use_container_width=True
)

# GRÁFICAS
if len(df_filtrado) == 0:
    st.warning("No se encontraron canciones con esos filtros.")
else:
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("Distribución de popularidad")
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        ax1.hist(df_filtrado["track_popularity"], color=COLOR_PRINCIPAL, edgecolor="white")
        ax1.set_xlabel("Popularidad")
        ax1.set_ylabel("Cantidad de canciones")
        ax1.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig1)

    with col_der:
        st.subheader("Canciones explícitas")
        explicitas = df_filtrado["track_explicit"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        ax2.pie(
            explicitas,
            labels=explicitas.index,
            autopct="%1.1f%%",
            colors=[COLOR_PRINCIPAL, COLOR_SECUNDARIO],
            startangle=90
        )
        st.pyplot(fig2)

    st.divider()

    st.subheader("Top 10 artistas con más canciones")
    top_artistas = df_filtrado["name_of_artists"].value_counts().head(10)
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.bar(top_artistas.index, top_artistas.values, color=COLOR_PRINCIPAL)
    ax3.set_xticklabels(top_artistas.index, rotation=45, ha="right")
    ax3.set_ylabel("Cantidad de canciones")
    ax3.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig3)

    st.divider()

    col_izq2, col_der2 = st.columns(2)

    with col_izq2:
        st.subheader("Canciones por década de lanzamiento")
        decada = (df_filtrado["album_release_date"].str[:3] + "0").value_counts().sort_index()
        fig4, ax4 = plt.subplots(figsize=(5, 4))
        ax4.plot(decada.index, decada.values, marker="o", color=COLOR_PRINCIPAL, linewidth=2)
        ax4.set_xlabel("Década")
        ax4.set_ylabel("Cantidad de canciones")
        ax4.spines[["top", "right"]].set_visible(False)
        st.pyplot(fig4)

    with col_der2:
        st.subheader("Popularidad según duración")
        df_filtrado["rango_duracion"] = pd.cut(
            df_filtrado["duracion_min"],
            bins=[0, 2, 3, 4, 5, 100],
            labels=["<2 min", "2-3 min", "3-4 min", "4-5 min", ">5 min"]
        )
        fig5, ax5 = plt.subplots(figsize=(5, 4))
        df_filtrado.boxplot(column="track_popularity", by="rango_duracion", ax=ax5)
        ax5.set_xlabel("Duración")
        ax5.set_ylabel("Popularidad")
        ax5.set_title("")
        plt.suptitle("")
        st.pyplot(fig5)

    st.divider()
