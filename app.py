import base64
import copy
import datetime
import json
import math
import os
import sys
import subprocess
import time
import unicodedata
from functools import lru_cache
from typing import Any, Dict
from urllib.parse import quote
import html

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import pulp
import streamlit as st
import streamlit.components.v1 as components
from scipy.optimize import linprog

# Configuration
from config import TVA_MP, TVA_VENTE

# Modules métier
from modules.business import calculate_margin_rate, calculer_cout, get_dough_cost
from modules.business.optimization import (
    optimize_grammages_balanced,
    optimize_grammages_linprog,
    optimize_grammages_exact,
    optimize_top2_ingredients
)
from modules.business.decision_helper import build_decision_playbook
from modules.utils import (
    load_data, load_drafts, save_drafts, autosave_plat,
    get_plat_image_filename, get_plat_image_path, get_image_data_uri,
    normalize_label, generer_detailed_breakdown
)
from modules.data import PRIX_VENTE_DICT, IMAGES_PLATS, COUT_PATE
from modules.styles import inject_all_styles, ensure_css_once
from modules.components import (
    render_view_header, render_overview_insights,
    render_global_simulator, render_decision_simulator,
    afficher_image_plat,
)
# from modules.components.chatbot import render_floating_chatbot  # TODO: Ajouter dossier chatbot/ au repo

# Vues principales
from modules.views import (
    render_overview_view,
    render_dish_analysis_view,
    render_comparative_view,
    render_edit_dish_view
)

EDIT_VIEW_AVAILABLE = True


# Injection des styles CSS globaux
inject_all_styles()


# ─── ENTÊTE CRÉATIVE ET RAFFINÉE ─────────────────────────────────────────────────────────

# ─── STYLES CSS CRÉATIFS ─────────────────────────────────────────────────────────



# ============== ALIASES POUR RÉTROCOMPATIBILITÉ ==============
# Les fonctions et données ont été déplacées vers les modules
# Création d'alias pour éviter de casser le code existant
prix_vente_dict = PRIX_VENTE_DICT
images_plats = IMAGES_PLATS
images_plats_lookup = {normalize_label(name): filename for name, filename in IMAGES_PLATS.items()}


# ============== FONCTIONS DE VISUALISATION ==============

# Alias pour rétrocompatibilité
_ensure_css_once = ensure_css_once


# Note: build_decision_playbook a été migré vers modules/business/decision_helper.py
# Note: render_floating_chatbot a été migré vers modules/components/chatbot.py


# Note: render_chatbot_decision a été migré vers modules/components/chatbot.py


# Note: generer_detailed_breakdown a été migré vers modules/utils/text_helpers.py

# Note: Les fonctions d'optimisation ont été migrées vers modules/business/optimization.py
# - optimize_grammages_linprog
# - optimize_grammages_balanced  
# - optimize_grammages_exact
# - optimize_top2_ingredients

# ============== PERFORMANCE LOGGING ==============
import time
_perf_start = time.time()
print(f"[PERF] 🚀 Démarrage app à {datetime.datetime.now().strftime('%H:%M:%S')}")

# Chargement des données
_load_start = time.time()
recettes, ingredients = load_data()
_load_time = time.time() - _load_start
print(f"[PERF] 📊 Chargement recettes/ingrédients: {_load_time:.2f}s")

if recettes is None or ingredients is None:
    st.error("Impossible de charger les données. Veuillez réessayer ou contacter le support.")
    st.stop()

# Gestion des paramètres d'URL pour la navigation directe depuis les cartes
query_params = st.query_params
mode_values = query_params.get("mode")
plat_values = query_params.get("plat")
mode_param = ""
plat_param = ""

if isinstance(mode_values, list):
    mode_param = mode_values[0] if mode_values else ""
elif mode_values:
    mode_param = str(mode_values)

if isinstance(plat_values, list):
    plat_param = plat_values[0] if plat_values else ""
elif plat_values:
    plat_param = str(plat_values)

mode_param = mode_param.lower()

if "last_applied_query" not in st.session_state:
    st.session_state.last_applied_query = None

query_signature = (mode_param, plat_param)
if query_signature != st.session_state.last_applied_query:
    if mode_param == "analyse":
        st.session_state.mode_navigation = "Analyse d'un plat"
        if plat_param:
            match_rows = recettes[recettes["plat"].apply(lambda x: normalize_label(x) == normalize_label(plat_param))]
            if not match_rows.empty:
                selected_row = match_rows.iloc[0]
                st.session_state.categorie_analyse = selected_row["categorie"]
                st.session_state.plat_unique = selected_row["plat"]
    st.session_state.last_applied_query = query_signature

# Styles minimalistes pour la sidebar - cohérent avec la charte de l'app


with st.sidebar:
    # Logo minimaliste avec charte rouge et blanc
    st.markdown(
        """
        <div style="
            padding: 0.7rem 0.65rem 0.75rem 0.65rem;
            margin-bottom: 1.2rem;
            background: #ffffff;
            border-radius: 5px;
            border-left: 2px solid #D92332;
            border: 1px solid #f1f5f9;
            border-left: 2px solid #D92332;
        ">
            <div style="
                font-size: 0.95rem; 
                font-weight: 700; 
                color: #0f172a;
                letter-spacing: -0.01em;
                margin-bottom: 0.2rem;
            ">Chez Antoine</div>
            <div style="
                font-size: 0.7rem; 
                color: #D92332; 
                font-weight: 600;
                letter-spacing: 0.02em;
            ">Food Cost Control</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Style minimaliste avec charte graphique rouge
    st.markdown(
        """
        <style>
            /* Sidebar background */
            [data-testid="stSidebar"] {
                background: #ffffff;
            }
            
            [data-testid="stSidebar"] > div:first-child {
                background: #ffffff;
                padding-top: 0.75rem;
            }
            
            /* Navigation minimaliste avec accent rouge */
            .nav-group div[role="radiogroup"] label {
                display: flex;
                align-items: center;
                padding: 0.55rem 0.75rem !important;
                border-radius: 5px;
                border: 1px solid transparent;
                margin: 0 0 0.25rem 0 !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                background: #fafbfc;
                position: relative;
            }
            
            .nav-group div[role="radiogroup"] label:hover {
                background: #f8fafc;
                border-color: #fee2e2;
                transform: translateX(2px);
            }
            
            .nav-group div[role="radiogroup"] label[data-checked="true"] {
                background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
                border-color: #D92332;
                border-left: 3px solid #D92332;
                box-shadow: 0 1px 3px rgba(217, 35, 50, 0.1);
                transform: translateX(0);
            }
            
            .nav-group div[role="radiogroup"] label[data-checked="true"]::before {
                content: '';
                position: absolute;
                left: -1px;
                top: 50%;
                transform: translateY(-50%);
                width: 3px;
                height: 60%;
                background: #D92332;
                border-radius: 0 2px 2px 0;
            }
            
            .nav-group div[role="radiogroup"] label[data-checked="true"] p {
                color: #D92332 !important;
                font-weight: 600;
            }
            
            .nav-group div[role="radiogroup"] label p {
                color: #64748b;
                font-size: 0.82rem;
                font-weight: 500;
                transition: all 0.2s ease;
                margin: 0;
            }
            
            .nav-group div[role="radiogroup"] {
                gap: 0;
            }
            
            /* Input fields compacts */
            [data-testid="stSidebar"] input[type="text"] {
                border-radius: 4px !important;
                border: 1px solid #e2e8f0 !important;
                background: #ffffff !important;
                font-size: 0.8rem !important;
                padding: 0.4rem 0.55rem !important;
                min-height: 36px !important;
            }
            
            [data-testid="stSidebar"] input[type="text"]:focus {
                border-color: #D92332 !important;
                box-shadow: 0 0 0 2px rgba(217, 35, 50, 0.08) !important;
            }
            
            /* Selectbox compact */
            [data-testid="stSidebar"] [data-baseweb="select"] > div {
                border-radius: 4px !important;
                border-color: #e2e8f0 !important;
                background: #ffffff !important;
                font-size: 0.8rem !important;
                min-height: 36px !important;
            }
            
            [data-testid="stSidebar"] [data-baseweb="select"]:focus-within > div {
                border-color: #D92332 !important;
                box-shadow: 0 0 0 1px #D92332 !important;
            }
            
            /* Slider rouge */
            [data-testid="stSidebar"] [data-baseweb="slider"] [role="slider"] {
                background-color: #D92332 !important;
                border-color: #D92332 !important;
                width: 14px !important;
                height: 14px !important;
            }
            
            [data-testid="stSidebar"] [data-baseweb="slider"] [data-testid="stTickBar"] > div {
                background-color: #D92332 !important;
            }
            
            /* Labels compacts */
            [data-testid="stSidebar"] label {
                font-size: 0.75rem !important;
                font-weight: 500 !important;
                color: #475569 !important;
                margin-bottom: 0.25rem !important;
            }
            
            /* Checkbox et radio compacts */
            [data-testid="stSidebar"] [data-testid="stCheckbox"],
            [data-testid="stSidebar"] [data-testid="stRadio"] {
                padding: 0.15rem 0 !important;
            }
            
            [data-testid="stSidebar"] [data-testid="stCheckbox"] label,
            [data-testid="stSidebar"] [data-testid="stRadio"] label {
                font-size: 0.8rem !important;
            }
            
            /* Multiselect compact */
            [data-testid="stSidebar"] [data-baseweb="tag"] {
                font-size: 0.72rem !important;
                padding: 0.2rem 0.4rem !important;
            }
            
            /* Réduire l'espacement vertical entre les éléments */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
                gap: 0.4rem !important;
            }
            
            /* Slider compact */
            [data-testid="stSidebar"] [data-testid="stSlider"] {
                padding: 0.3rem 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    nav_options = [
        "Vue d'ensemble",
        "Analyse d'un plat",
        "Analyse comparative",
    ]
    
    # Ajouter "Modifier un plat" seulement si disponible
    if EDIT_VIEW_AVAILABLE:
        nav_options.append("Modifier un plat")

    st.markdown('<div class="nav-group">', unsafe_allow_html=True)
    mode_analysis = st.radio(
        "Navigation",
        nav_options,
        key="mode_navigation",
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if "objectif_marge" not in st.session_state:
        st.session_state["objectif_marge"] = 70

    # L'objectif de marge matière reste disponible via session_state
    # mais n'apparaît plus dans l'interface (suppression du Paramètre patron).

# PRINCIPAL : GESTION DES DIFFÉRENTS MODES 

# Récupération de l'objectif de marge depuis session_state
objectif_marge_actuel = st.session_state.get("objectif_marge", 70)

print(f"[PERF] ⏱️  Temps total chargement: {time.time() - _perf_start:.2f}s")
print(f"[PERF] 🎯 Mode sélectionné: {mode_analysis}")

_render_start = time.time()

if mode_analysis == "Vue d'ensemble":
    print(f"[PERF] 📈 Rendu Vue d'ensemble...")
    render_overview_view(recettes, ingredients, objectif_marge_actuel)

elif mode_analysis == "Analyse d'un plat":
    print(f"[PERF] 🍕 Rendu Analyse d'un plat...")
    render_dish_analysis_view(recettes, ingredients, objectif_marge_actuel)

elif mode_analysis == "Analyse comparative":
    print(f"[PERF] 📊 Rendu Analyse comparative...")
    render_comparative_view(recettes, ingredients, objectif_marge_actuel)

elif mode_analysis == "Modifier un plat":
    if EDIT_VIEW_AVAILABLE:
        print(f"[PERF] ✏️  Rendu Modifier un plat...")
        render_edit_dish_view(recettes, ingredients, objectif_marge_actuel)
    else:
        st.error("⚠️ La vue 'Modifier un plat' est temporairement indisponible")

_render_time = time.time() - _render_start
_total_time = time.time() - _perf_start
print(f"[PERF] 🎨 Temps rendu vue: {_render_time:.2f}s")
print(f"[PERF] ✅ TOTAL: {_total_time:.2f}s")
print(f"[PERF] {'='*60}")

# Préparation des données pour le chatbot avec calculs de marges
df_plats_chatbot = recettes.copy()
if not df_plats_chatbot.empty and "plat" in df_plats_chatbot.columns:
    # Calculer les coûts et marges pour chaque plat
    for idx, row in df_plats_chatbot.iterrows():
        plat_name = row["plat"]
        # Récupérer les ingrédients du plat
        plat_ingredients = ingredients[ingredients["plat"] == plat_name]
        
        if not plat_ingredients.empty:
            # Calculer coût matière avec TVA
            cout_total = 0
            for _, ing_row in plat_ingredients.iterrows():
                quantite_kg = ing_row["quantite_g"] / 1000
                prix_kg_ht = ing_row.get("prix_kg", 0)
                prix_kg_ttc = prix_kg_ht * (1 + TVA_MP)
                cout_total += quantite_kg * prix_kg_ttc
            
            # Récupérer prix de vente
            prix_ttc = PRIX_VENTE_DICT.get(plat_name, 0)
            prix_ht = prix_ttc / (1 + TVA_VENTE)
            
            # Calculer marge
            marge_pct = ((prix_ht - cout_total) / prix_ht * 100) if prix_ht > 0 else 0
            
            # Mettre à jour le DataFrame
            df_plats_chatbot.at[idx, "cout_matiere"] = cout_total
            df_plats_chatbot.at[idx, "prix_ttc"] = prix_ttc
            df_plats_chatbot.at[idx, "prix_ht"] = prix_ht
            df_plats_chatbot.at[idx, "marge_pct"] = marge_pct
            df_plats_chatbot.at[idx, "nom"] = plat_name

# Affichage du chatbot flottant sur toutes les pages
# render_floating_chatbot(df_plats_chatbot, ingredients, objectif_marge_actuel)  # TODO: Ajouter dossier chatbot/ au repo
