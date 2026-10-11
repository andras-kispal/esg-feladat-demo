import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. Oldal beállítások (Széles nézet és böngészőfül címe)
st.set_page_config(page_title="ESG Portfólió Modell", layout="wide", page_icon="🌱")

# 2. Vízjelek és ikonok eltüntetése (a korábbi kód)
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[class^="viewerBadge"] {display: none !important;}
    [data-testid="stViewerBadge"] {display: none !important;}
    div[class^="creatorBadge"] {display: none !important;}
    [data-testid="stCreatorBadge"] {display: none !important;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# 3. Fejléc
st.title("🌱 Klímakockázati Sokk és Stabilizációs Modell")
st.markdown("---")

# 4. Kétoszlopos elrendezés létrehozása (1/4 és 3/4 arányban)
col1, col2 = st.columns([1, 3])

# Bal oszlop: Szakmai kontextus és magyarázat
with col1:
    st.subheader("Vezetői Összefoglaló")
    st.info("Ez a dashboard egy hirtelen fellépő **átmeneti klímakockázati sokk** (pl. NGFS 'Disorderly Transition' forgatókönyv) hatását szimulálja a banki portfólióra.")
    
    st.write("**Módszertan:**")
    st.write("A modell egy csillapodó rezgés ($y = a \cdot \\frac{\\sin(x)}{x}$) segítségével mutatja be, hogyan árazza be a piac a kezdeti sokkot (EU Taxonómia szigorítás), és hogyan stabilizálódik a hitelezési portfólió az idő múlásával.")
    
    st.write("**Használat:**")
    st.write("A grafikon alatti csúszkával állítható a szabályozói szigorítás (sokk) induló ereje, amely azonnali RWA (kockázattal súlyozott eszközérték) kilengést eredményez.")

# Jobb oszlop: A gyors, akadásmentes Plotly grafikon
with col2:
    x = np.linspace(-10, 10, 400)
    a_values = np.arange(-5.0, 5.5, 0.5)
    fig = go.Figure()

    # Görbék generálása (Streamlit zöld színnel)
    for a in a_values:
        y = a * np.where(x == 0, 1.0, np.sin(x) / x)
        fig.add_trace(go.Scatter(x=x, y=y, visible=False, name=f"Sokk: {a}", line=dict(color='#00875A', width=3)))

    default_idx = 12
    fig.data[default_idx].visible = True

    # Plotly belső csúszka logikája
    steps = []
    for i, a in enumerate(a_values):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)}],
            label=f"{a:.1f}"
        )
        step["args"][0]["visible"][i] = True  
        steps.append(step)

    sliders = [dict(
        active=default_idx,
        currentvalue={"prefix": "Átmeneti kockázati szorzó (Sokk erőssége): "},
        pad={"t": 50},
        steps=steps
    )]

    # Tengelyek és háttér formázása a letisztult kinézetért
    fig.update_layout(
        sliders=sliders,
        yaxis_range=[-1.5, 5.5],
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Idő (Évek a szabályozási sokk után)",
        yaxis_title="Portfólió volatilitás / RWA kilengés (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    # Halvány rácsvonalak hozzáadása
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    st.plotly_chart(fig, use_container_width=True)