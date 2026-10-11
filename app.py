import streamlit as st
import numpy as np
import pandas as pd

# Oldal címe és leírása
st.title("Interaktív Függvény")
st.write("A grafikon a következő függvényt ábrázolja: $y = a \cdot \\frac{\\sin(x)}{x}$")

# Csúszka (slider) létrehozása az 'a' változóhoz
a = st.slider(
    "Állítsd be az 'a' szorzó értékét:", 
    min_value=-5.0,   # Minimum érték
    max_value=5.0,    # Maximum érték
    value=1.0,        # Alapértelmezett kezdőérték
    step=0.5          # Lépésköz
)

# X értékek generálása -10 és 10 között
x = np.linspace(-10, 10, 400)

# Y értékek kiszámítása, a sliderből jövő 'a' értékkel szorozva
# np.where-t használunk, hogy x=0 esetén ne kapjunk hibaüzenetet
y = a * np.where(x == 0, 1.0, np.sin(x) / x)

# Adatok formázása a beépített ábrázolóhoz
chart_data = pd.DataFrame({'x': x, 'y': y}).set_index('x')

# Vonaldiagram megjelenítése
st.line_chart(chart_data)