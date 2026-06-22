import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Rick and Morty Word🛸",page_icon=":🛸:", layout = "wide")
st.title("Rick and Morty World 🛸")
st.write("Bienvenido al mundo de Rick y Morty, aqui podrás ver la información de todos los personajes del mundo de Rick y Morty.")

@st.cache_data
def cargar():
    return pd.read_csv(Path(__file__).parent / "rick_and_morty_characters.csv")

df = cargar ()

st.sidebar.title("Personajes")
busca = st.sidebar.text_input("Busca nombres", placeholder= "ejemplo: Rick Sánchez")

