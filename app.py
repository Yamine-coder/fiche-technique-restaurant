import streamlit as st
import time

st.set_page_config(
    page_title="Test Layout Resize",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🚨 Forcer un resize initial
st.write("<script>window.dispatchEvent(new Event('resize'));</script>", unsafe_allow_html=True)

# ➖ SIDEBAR - interactions classiques
option = st.sidebar.radio("Choisir une option", ["A", "B"])
# On force un petit délai puis un redraw après action
time.sleep(0.05)
st.write("<script>window.dispatchEvent(new Event('resize'));</script>", unsafe_allow_html=True)

slider_val = st.sidebar.slider("Slide", 0, 100, 50)
time.sleep(0.05)
st.write("<script>window.dispatchEvent(new Event('resize'));</script>", unsafe_allow_html=True)

# ➖ CONTENU PRINCIPAL - deux colonnes pour tester le layout
col1, col2 = st.columns(2)
with col1:
    st.markdown("### Colonne 1")
    st.write(f"Option sélectionnée : {option}")
with col2:
    st.markdown("### Colonne 2")
    st.write(f"Valeur du slider : {slider_val}")

# 🚨 Forcer un dernier redraw à la fin
st.write("<script>window.dispatchEvent(new Event('resize'));</script>", unsafe_allow_html=True)
