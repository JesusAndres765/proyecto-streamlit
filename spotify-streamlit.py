import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard de mi Playlist de Spotify")
st.write("Análisis de canciones, artistas y popularidad")

# Cargar datos
dataframe = pd.read_csv("https://raw.githubusercontent.com/JesusAndres765/datasets/refs/heads/main/playlist.csv")

# --- Gráfica 1: Histograma de popularidad ---
st.subheader("Distribución de popularidad")
fig1, ax1 = plt.subplots()
ax1.hist(dataframe["track_popularity"])
ax1.set_xlabel("Popularidad")
ax1.set_ylabel("Cantidad de canciones")
st.pyplot(fig1)

# --- Gráfica 2: Pastel de explícitas ---
st.subheader("Proporción de canciones explícitas")
explicitas = dataframe["track_explicit"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(explicitas, labels=explicitas.index, autopct="%1.1f%%")
st.pyplot(fig2)

# --- Gráfica 3: Barras top artistas ---
st.subheader("Top 10 artistas con más canciones")
top_artistas = dataframe["name_of_artists"].value_counts().head(10)
fig3, ax3 = plt.subplots()
ax3.bar(top_artistas.index, top_artistas.values)
ax3.set_xticklabels(top_artistas.index, rotation=45, ha="right")
ax3.set_ylabel("Cantidad de canciones")
st.pyplot(fig3)

# --- Gráfica 4: Líneas canciones por año ---
st.subheader("Canciones por año de lanzamiento")
por_anio = dataframe["album_release_date"].str[:4].value_counts().sort_index()
fig4, ax4 = plt.subplots()
ax4.plot(por_anio.index, por_anio.values, marker="o")
ax4.set_xlabel("Año")
ax4.set_ylabel("Cantidad de canciones")
plt.xticks(rotation=45)
st.pyplot(fig4)

# --- Gráfica 5: Dispersión duración vs popularidad ---
st.subheader("Duración vs Popularidad")
fig5, ax5 = plt.subplots()
ax5.scatter(dataframe["track_duration_ms"], dataframe["track_popularity"])
ax5.set_xlabel("Duración (ms)")
ax5.set_ylabel("Popularidad")
st.pyplot(fig5)

# --- Tabla de datos ---
st.subheader("Datos completos")
st.dataframe(dataframe)