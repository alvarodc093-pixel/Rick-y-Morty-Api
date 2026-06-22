# Rick y Morty Api
# MortyDex 🛸

Aplicación interactiva en Streamlit para explorar el universo de Rick & Morty a partir de un CSV local con 826 personajes.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://TU-URL-DE-STREAMLIT)

## Demo

- **App desplegada:** https://TU-URL-DE-STREAMLIT

## Captura

> Sustituye esta imagen por una captura real de tu app.

![Captura de MortyDex](assets/screenshot.png)

## Qué incluye

- Portada con métricas generales.
- Galería de cartas con imagen, nombre y estado.
- Filtros por especie, estado y género.
- Buscador por nombre.
- Ficha detallada de cada personaje.
- Gráficos interactivos con Plotly.
- Tabla completa del dataset.

## Estructura del proyecto

```bash
mortydex/
├── app.py
├── rick_and_morty_characters.csv
├── requirements.txt
├── .gitignore
├── README.md
└── assets/
    └── screenshot.png
```

## Instalación local

1. Clona el repositorio:
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

2. Crea y activa un entorno virtual.

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
streamlit run app.py
```

## Fuente de datos

El proyecto utiliza la API pública de Rick & Morty para generar el CSV con los personajes.  
Más información en: [rickandmortyapi.com](https://rickandmortyapi.com/)

## Tecnologías

- Python
- Streamlit
- Pandas
- Plotly

## Objetivo del proyecto

Este dashboard fue creado como ejercicio educativo para practicar:
- preparación de datos,
- diseño de dashboards,
- visualización interactiva,
- despliegue en Streamlit Cloud,
- y publicación en GitHub.

## Autor

Alvaro Domingo
