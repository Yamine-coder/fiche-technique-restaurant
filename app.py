import streamlit as st

col1, col2 = st.columns(2)
with col1:
    st.markdown("Colonne 1")
with col2:
    st.markdown("Colonne 2")

cols = st.columns(5)
for i, kpi in enumerate([10,20,30,40,50]):
    cols[i].metric(f"KPI {i+1}", str(kpi))
