"""App minimale pour tester les imports progressivement"""
import streamlit as st

st.title("🔍 Test des imports")

try:
    st.write("✓ Streamlit OK")
    
    st.write("Test 1: Import config...")
    from config import TVA_MP, TVA_VENTE
    st.write("✓ config OK")
    
    st.write("Test 2: Import modules.data.constants...")
    from modules.data.constants import PRIX_VENTE_DICT
    st.write("✓ modules.data.constants OK")
    
    st.write("Test 3: Import modules.business...")
    from modules.business.cost_calculator import calculer_cout
    st.write("✓ modules.business.cost_calculator OK")
    
    st.write("Test 4: Import modules.data.sales_data...")
    from modules.data.sales_data import load_ventes
    st.write("✓ modules.data.sales_data OK")
    
    st.write("Test 5: Import modules.views.overview_view...")
    from modules.views.overview_view import render_overview_view
    st.write("✓ modules.views.overview_view OK")
    
    st.write("Test 6: Import modules.views.dish_analysis_view...")
    from modules.views.dish_analysis_view import render_dish_analysis_view
    st.write("✓ modules.views.dish_analysis_view OK")
    
    st.write("Test 7: Import modules.views.comparative_view...")
    from modules.views.comparative_view import render_comparative_view
    st.write("✓ modules.views.comparative_view OK")
    
    st.write("Test 8: Import modules.views.edit_dish_view...")
    from modules.views.edit_dish_view import render_edit_dish_view
    st.write("✓ modules.views.edit_dish_view OK")
    
    st.success("🎉 Tous les imports fonctionnent !")
    
except SyntaxError as e:
    st.error(f"❌ SYNTAX ERROR ligne {e.lineno}: {e.msg}")
    st.code(f"Fichier: {e.filename}", language="text")
    if e.text:
        st.code(e.text, language="python")
    
except Exception as e:
    st.error(f"❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    st.code(traceback.format_exc(), language="text")
