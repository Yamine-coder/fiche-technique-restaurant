import streamlit as st

st.set_page_config(layout="wide")

# Colonnes de KPI (exemple)
cols = st.columns(5)
for i, kpi in enumerate([10, 20, 30, 40, 50]):
    cols[i].metric(f"KPI {i+1}", str(kpi))

# Titre principal et sous‑titre
st.title("🍽️ Fiche Technique - Chez Antoine")
st.subheader("🔍 Analyse Comparative")
