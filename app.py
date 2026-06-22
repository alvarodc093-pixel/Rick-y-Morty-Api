import streamlit as st
import pandas as pd
import plotly as pt
import plotly.express as px

st.set_page_config(
    page_title="Rick y Morty Dex | Rick & Morty Dashboard",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    df = pd.read_csv("rick_and_morty_characters.csv")
    for c in ["status", "species", "gender", "origin", "location", "name", "type"]:
        if c in df.columns:
            df[c] = df[c].fillna("unknown")
    if "n_episodes" not in df.columns and "episode" in df.columns:
        df["n_episodes"] = 0
    return df

df = load_data()

def badge_class(v):
    v = str(v).lower()
    if v == "alive":
        return "alive"
    if v == "dead":
        return "dead"
    return "unknown"

st.markdown("""
<div class="hero">
    <h1> 🛸Rick y Morty Dex🛸<h1>
    <p>Dashboard interactivo de Rick & Morty con exploración visual, filtros avanzados y ficha detallada.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🔎 Filtros")
    species_options = sorted(df["species"].dropna().unique())
    status_options = sorted(df["status"].dropna().unique())
    gender_options = sorted(df["gender"].dropna().unique())

    selected_species = st.multiselect("Especie", species_options)
    selected_status = st.multiselect("Estado", status_options)
    selected_gender = st.multiselect("Género", gender_options)
    search_name = st.text_input("Buscar por nombre")

    st.markdown("---")
    st.caption("Tip: combina filtros para encontrar personajes concretos.")

filtered = df.copy()

if selected_species:
    filtered = filtered[filtered["species"].isin(selected_species)]
if selected_status:
    filtered = filtered[filtered["status"].isin(selected_status)]
if selected_gender:
    filtered = filtered[filtered["gender"].isin(selected_gender)]
if search_name:
    filtered = filtered[filtered["name"].str.contains(search_name, case=False, na=False)]

total = len(filtered)
species_count = filtered["species"].nunique()
alive_pct = filtered["status"].eq("Alive").mean() * 100 if total else 0
dead_pct = filtered["status"].eq("Dead").mean() * 100 if total else 0

st.write("")
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Personajes</div>
        <div class="kpi-value">{total}</div>
        <div class="kpi-sub">Resultados visibles</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Especies distintas</div>
        <div class="kpi-value">{species_count}</div>
        <div class="kpi-sub">Diversidad biológica</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">% vivos</div>
        <div class="kpi-value">{alive_pct:.1f}%</div>
        <div class="kpi-sub">Sobre el subconjunto filtrado</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">% muertos</div>
        <div class="kpi-value">{dead_pct:.1f}%</div>
        <div class="kpi-sub">Sobre el subconjunto filtrado</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Portada", "🖼️ Galería", "📊 Análisis", "👤 Ficha"])

with tab1:
    c1, c2 = st.columns([1.25, 1])
    with c1:
        st.markdown('<div class="section-title">Resumen ejecutivo</div>', unsafe_allow_html=True)
        st.write("Este panel resume el universo de personajes filtrado por especie, estado, género y búsqueda por nombre.")
        st.write("La app está diseñada para que parezca un proyecto de portfolio: limpieza visual, jerarquía clara y componentes reutilizables.")
        st.write("Todo se alimenta del CSV local, sin llamar a la API al abrir la app.")
   
with c2:
    status_dist = filtered["status"].value_counts().reset_index()
    status_dist.columns = ["status", "count"]

    color_map = {
        "Alive": "#22c55e",
        "Dead": "#ef4444",
        "unknown": "#000000"
    }

    fig = px.bar(
        status_dist,
        x="status",
        y="count",
        color="status",
        color_discrete_map=color_map,
        title="Distribución por estado"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown('<div class="section-title">Galería de cartas</div>', unsafe_allow_html=True)
    if total == 0:
        st.warning("No hay resultados con los filtros actuales.")
    else:
        page_size = 12
        page_count = max(1, (total + page_size - 1) // page_size)
        page = st.number_input("Página", min_value=1, max_value=page_count, value=1, step=1)
        start = (page - 1) * page_size
        end = start + page_size
        page_df = filtered.sort_values("name").iloc[start:end]

        rows = [page_df.iloc[i:i+4] for i in range(0, len(page_df), 4)]
        for row_df in rows:
            cols = st.columns(4)
            for idx, (_, r) in enumerate(row_df.iterrows()):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="card">
                        <img src="{r['image']}" alt="{r['name']}">
                        <div class="card-body">
                            <div class="card-name">{r['name']}</div>
                            <div class="badge {badge_class(r['status'])}">{r['status']}</div>
                            <div class="meta"><b>Species:</b> {r['species']}</div>
                            <div class="meta"><b>Gender:</b> {r['gender']}</div>
                            <div class="meta"><b>Origin:</b> {r['origin']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

with tab3:
    a, b = st.columns([1.15, 0.85])
    with a:
        top_species = filtered["species"].value_counts().head(10).reset_index()
        top_species.columns = ["species", "count"]
        fig_species = px.bar(
            top_species,
            x="species",
            y="count",
            color="species",
            title="Top 10 especies"
        )
        st.plotly_chart(fig_species, use_container_width=True)
    with b:
        gender_dist = filtered["gender"].value_counts().reset_index()
        gender_dist.columns = ["gender", "count"]
        fig_gender = px.pie(
            gender_dist,
            names="gender",
            values="count",
            hole=0.5,
            title="Distribución por género"
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    c, d = st.columns(2)
    with c:
        st.markdown('<div class="section-title">Top ubicaciones</div>', unsafe_allow_html=True)
        st.dataframe(filtered["location"].value_counts().head(10).reset_index(), use_container_width=True)
    with d:
        st.markdown('<div class="section-title">Top orígenes</div>', unsafe_allow_html=True)
        st.dataframe(filtered["origin"].value_counts().head(10).reset_index(), use_container_width=True)

with tab4:
    st.markdown('<div class="section-title">Ficha del personaje</div>', unsafe_allow_html=True)
    if total == 0:
        st.info("Selecciona otros filtros para mostrar una ficha.")
    else:
        selected_name = st.selectbox("Selecciona un personaje", filtered["name"].sort_values().tolist())
        person = filtered[filtered["name"] == selected_name].iloc[0]
        l, r = st.columns([1, 1.8])
        with l:
            st.image(person["image"], use_container_width=True)
        with r:
            st.markdown(f"## {person['name']}")
            st.markdown(f"<span class='badge {badge_class(person['status'])}'>{person['status']}</span>", unsafe_allow_html=True)
            st.write(f"**Species:** {person['species']}")
            st.write(f"**Type:** {person['type']}")
            st.write(f"**Gender:** {person['gender']}")
            st.write(f"**Origin:** {person['origin']}")
            st.write(f"**Location:** {person['location']}")
            st.write(f"**Episodes:** {int(person['n_episodes']) if 'n_episodes' in person else 'N/A'}")
            st.write(f"**URL:** {person['url']}")
            st.write(f"**Created:** {person['created']}")

st.write("")
st.markdown('<div class="section-title">Dataset filtrado</div>', unsafe_allow_html=True)
st.dataframe(filtered, use_container_width=True)