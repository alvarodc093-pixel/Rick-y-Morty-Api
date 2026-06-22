import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from streamlit_autorefresh import st_autorefresh


st.set_page_config(page_title="Rick and Morty Word",page_icon=":🛸:", layout = "wide")
st.title("Rick and Morty World 🛸")
st.write("Bienvenido al mundo de Rick y Morty, aqui podrás ver la información de todos los personajes del mundo de Rick y Morty.")

@st.cache_data
def cargar():
    return pd.read_csv(Path(__file__).parent / "rick_and_morty_characters.csv")

df = cargar ()


st.sidebar.title("🛸 Rick & Morty 🛸")

species_filter = st.sidebar.multiselect(
    "Species",
    options=sorted(df["species"].dropna().unique()),
    default=[]
)

status_filter = st.sidebar.multiselect(
    "Status",
    options=sorted(df["status"].dropna().unique()),
    default=[]
)

gender_filter = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["gender"].dropna().unique()),
    default=[]
)
filtered_df = df.copy()

if species_filter:
    filtered_df = filtered_df[
        filtered_df["species"].isin(species_filter)
    ]

if status_filter:
    filtered_df = filtered_df[
        filtered_df["status"].isin(status_filter)
    ]

if gender_filter:
    filtered_df = filtered_df[
        filtered_df["gender"].isin(gender_filter)
    ]

st.title("🛸 Rick & Morty Análisis de personaje 🛸")

st.markdown("""
Exploración interactiva de personajes del universo Rick & Morty.
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Characters",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Species",
        filtered_df["species"].nunique()
    )

with col3:
    st.metric(
        "Origins",
        filtered_df["origin"].nunique()
    )

with col4:
    st.metric(
        "Locations",
        filtered_df["location"].nunique()
    )

st.divider()

col1, col2 = st.columns(2)

with col1:

    species_count = (
        filtered_df["species"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    species_count.columns = ["Species", "Count"]

    fig_species = px.bar(
        species_count,
        x="Species",
        y="Count",
        title="Top 10 especioes"
    )

    st.plotly_chart(
        fig_species,
        use_container_width=True
    )

with col2:

    status_count = (
        filtered_df["status"]
        .value_counts()
        .reset_index()
    )

    status_count.columns = ["Status", "Count"]

    fig_status = px.pie(
    status_count,
    names="Status",
    values="Count",
    color="Status",
    color_discrete_map={
        "Alive": "green",
        "Dead": "red",
        "unknown": "black"
    }
)

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

gender_count = (
    filtered_df["gender"]
    .value_counts()
    .reset_index()
)

gender_count.columns = ["Gender", "Count"]

fig_gender = px.bar(
    gender_count,
    x="Gender",
    y="Count",
    title="Distribución de géneros",
    color="Gender"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)

st.divider()


st.subheader("🔍 Explorador de personajes")

character = st.selectbox(
    "Choose a character",
    filtered_df["name"].sort_values()
)

selected = filtered_df[
    filtered_df["name"] == character
].iloc[0]

col1, col2 = st.columns([1,2])

with col1:
    st.image(
        selected["image"],
        width=300
    )

with col2:

    st.markdown(f"## {selected['name']}")

    st.write(f"**Status:** {selected['status']}")
    st.write(f"**Species:** {selected['species']}")
    st.write(f"**Gender:** {selected['gender']}")
    st.write(f"**Origin:** {selected['origin']}")
    st.write(f"**Location:** {selected['location']}")

    if selected["type"]:
        st.write(f"**Type:** {selected['type']}")

st.divider()

st.subheader("📋 Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)