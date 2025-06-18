import streamlit as st

col1, col2 = st.columns(2)
with col1:
    st.markdown("Colonne 1")
with col2:
    st.markdown("Colonne 2")
