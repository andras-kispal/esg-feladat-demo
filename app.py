import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

hide_menu_style = """
    <style>
    /* A felső menü és eszköztár eltüntetése */
    #MainMenu {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    header {visibility: hidden;}
    
    /* Az alsó vízjel eltüntetése */
    footer {visibility: hidden;}
    
    /* A "Hosted with Streamlit" lebegő ikon eltüntetése */
    div[class^="viewerBadge"] {display: none !important;}
    [data-testid="stViewerBadge"] {display: none !important;}
    
    /* A GitHub profilkép (Creator Badge) eltüntetése */
    div[class^="creatorBadge"] {display: none !important;}
    [data-testid="stCreatorBadge"] {display: none !important;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)



st.title("Interaktív Függvény (Plotly)")
st.write("A grafikon a következő függvényt ábrázolja: $y = a \cdot \\frac{\\sin(x)}{x}$")

# X értékek generálása
x = np.linspace(-10, 10, 400)

# Előre kiszámoljuk az összes lehetséges 'a' értéket -5 és 5 között
a_values = np.arange(-5.0, 5.5, 0.5)

fig = go.Figure()

# Minden lehetséges görbét hozzáadunk az ábrához, de alapból elrejtjük őket
for a in a_values:
    y = a * np.where(x == 0, 1.0, np.sin(x) / x)
    fig.add_trace(go.Scatter(x=x, y=y, visible=False, name=f"a={a}"))

# A 12. indexű elem az a=1.0, ezt tesszük alapból láthatóvá induláskor
default_idx = 12
fig.data[default_idx].visible = True

# A Plotly beépített böngészős csúszkájának (slider) létrehozása
steps = []
for i, a in enumerate(a_values):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)}],
        label=f"{a:.1f}"
    )
    # Csak az aktuális csúszka-érték görbéje látszódjon
    step["args"][0]["visible"][i] = True  
    steps.append(step)

sliders = [dict(
    active=default_idx,
    currentvalue={"prefix": "Az 'a' szorzó értéke: "},
    pad={"t": 50},
    steps=steps
)]

# Fixáljuk az Y tengelyt, hogy az ábra ne "ugráljon" a csúszka húzásakor
fig.update_layout(
    sliders=sliders,
    yaxis_range=[-1.5, 5.5],
    margin=dict(l=0, r=0, t=30, b=0)
)

# Megjelenítés a Streamlitben
st.plotly_chart(fig, use_container_width=True)