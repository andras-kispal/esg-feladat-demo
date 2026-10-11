import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Oldal beállítások (Széles nézet)
st.set_page_config(page_title="ESG Portfólió Modell", layout="wide", page_icon="🌱")

# 2. Vízjelek eltüntetése
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

# 3. Oldalsáv (Sidebar) létrehozása a vezérlőknek
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/1024px-GitHub_Invertocat_Logo.svg.png", width=50) # Egy kis GitHub ikon díszítésnek
st.sidebar.title("Vezérlőpult")

# ITT VAN A STREAMLIT CSÚSZKA, ami most az oldalsávon jelenik meg, és felveszi a zöld színt
a_val = st.sidebar.slider(
    "Átmeneti kockázati szorzó (Sokk erőssége):",
    min_value=-5.0,
    max_value=5.0,
    value=1.0,
    step=0.5
)

st.sidebar.markdown("---")
st.sidebar.info("A csúszka mozgatásával azonnal frissül a jobb oldali modell. A negatív értékek kedvező szabályozási környezetet, a pozitívak szigorítást jelentenek.")

# 4. Főoldal: Fejléc
st.title("🌱 Klímakockázati Sokk és Stabilizációs Modell")
st.markdown("---")

# 5. Kétoszlopos elrendezés a főoldalon
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Vezetői Összefoglaló")
    st.info("Ez a dashboard egy hirtelen fellépő **átmeneti klímakockázati sokk** hatását szimulálja a banki portfólióra.")
    st.write("**Módszertan:**")
    st.write("A modell egy csillapodó rezgés ($y = a \cdot \\frac{\\sin(x)}{x}$) segítségével mutatja be, hogyan árazza be a piac a kezdeti sokkot (EU Taxonómia szigorítás), és hogyan stabilizálódik a hitelezési portfólió az idő múlásával.")

with col2:
    # A grafikon generálása az oldalsávból kapott 'a_val' alapján
    x = np.linspace(-10, 10, 400)
    y = a_val * np.where(x == 0, 1.0, np.sin(x) / x)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, line=dict(color='#00875A', width=3), name="Portfólió RWA"))

    fig.update_layout(
        yaxis_range=[-5.5, 5.5], # Fixáljuk az Y tengelyt, hogy mozgatható legyen ugrálás nélkül
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Idő (Évek a szabályozási sokk után)",
        yaxis_title="Portfólió volatilitás / RWA kilengés (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    st.plotly_chart(fig, use_container_width=True)

