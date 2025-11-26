"""
Modifier un plat - Interface de gestion et d'optimisation des recettes
"""
import streamlit as st
import pandas as pd
import copy
import math
from urllib.parse import quote

from modules.data.constants import TVA_VENTE, prix_vente_dict
from modules.business.cost_calculator import calculer_cout, get_dough_cost
from modules.business.optimization import optimize_grammages_balanced
from modules.utils.data_manager import load_drafts, save_drafts


def render_edit_dish_view(recettes, ingredients, objectif_marge):
    """
    Affiche l'interface de modification et création de plats.
    
    Args:
        recettes: DataFrame des recettes
        ingredients: DataFrame des ingrédients
        objectif_marge: Objectif de marge en pourcentage
    """
    # === CSS MODERNE ET HARMONISÉ ===
    _render_edit_styles()
    
    # === INITIALISATION ===
    _initialize_session_state()
    
    # === SIDEBAR UNIFIÉE ===
    _render_unified_sidebar()
    
    # Configuration
    taux_tva = TVA_VENTE
    seuil_marge_perso = st.session_state.get("objectif_marge_edit", 70)
    
    # === HEADER ===
    _render_edit_header()
    
    # === NAVIGATION ===
    _render_navigation_tabs()
    
    # === CONTENU SELON LA VUE ===
    if st.session_state.edit_view == "liste":
        _render_list_view(recettes, ingredients, taux_tva, seuil_marge_perso)
    elif st.session_state.edit_view == "creation":
        _render_creation_view(recettes, ingredients, taux_tva, seuil_marge_perso)
    else:
        _render_edition_view(recettes, ingredients, taux_tva, seuil_marge_perso)


def _render_edit_styles():
    """Affiche tous les styles CSS pour le mode édition"""
    st.markdown("""
    <style>
    /* Variables CSS pour cohérence */
    :root {
        --primary: #D92332;
        --primary-light: rgba(217, 35, 50, 0.1);
        --primary-dark: #b41c29;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --neutral-50: #f8fafc;  
        --neutral-100: #f1f5f9;
        --neutral-200: #e2e8f0;
        --neutral-300: #cbd5e1;
        --neutral-400: #94a3b8;
        --neutral-500: #64748b;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1e293b;
        --neutral-900: #0f172a;
        --radius: 8px;
        --radius-lg: 12px;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --transition: all 0.25s cubic-bezier(0.25, 1, 0.5, 1);
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Masquer l'en-tête principal */
    .creative-header {
        display: none !important;
    }
    
    /* Header moderne avec badge */
    div[data-testid="stHorizontalBlock"]:has(.modifier-left) {
        background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
        border: 1px solid #e2e8f0;
        border-left: 3px solid #D92332;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        padding: 0.6rem 0.9rem;
        border-radius: 7px;
        margin-bottom: 0.9rem;
        margin-top: -1rem;
        gap: 1rem !important;
    }
    
    div[data-testid="stHorizontalBlock"]:has(.modifier-left) > div {
        padding: 0 !important;
    }
    
    .modifier-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .modifier-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: rgba(217, 35, 50, 0.08);
        border-radius: 6px;
        flex-shrink: 0;
    }
    
    .modifier-icon svg {
        width: 18px;
        height: 18px;
    }
    
    .modifier-text {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .modifier-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 1rem;
        letter-spacing: -0.01em;
        margin: 0;
        line-height: 1.3;
    }
    
    .modifier-subtitle {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 400;
        margin: 0.15rem 0 0;
        line-height: 1.25;
    }
    
    .modifier-badge {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        padding: 0.5rem 0.75rem;
        font-size: 0.85rem;
        color: #374151;
        font-weight: 600;
        white-space: nowrap;
    }
    
    /* Cards des plats */
    .dish-card-modern {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.5);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    
    .dish-card-modern.excellent {
        border-left: 4px solid var(--success);
    }
    
    .dish-card-modern.good {
        border-left: 4px solid var(--warning);
    }
    
    .dish-card-modern.poor {
        border-left: 4px solid var(--danger);
    }
    
    .dish-card-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
        border-color: rgba(203, 213, 225, 0.9);
    }
    
    .dish-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.2rem;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    
    .dish-card-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 0.35rem 0;
        line-height: 1.3;
        letter-spacing: -0.01em;
    }
    
    .dish-card-base {
        font-size: 0.8rem;
        color: var(--neutral-500);
        font-weight: 400;
    }
    
    .dish-card-status {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .dish-card-status.excellent {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success);
    }
    
    .dish-card-status.good {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
    }
    
    .dish-card-status.poor {
        background: rgba(244, 63, 94, 0.1);
        color: var(--danger);
    }
    
    .dish-card-metrics {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
        padding: 1.25rem;
        background: var(--neutral-50);
        border-radius: var(--radius);
        border: 1px solid var(--neutral-200);
    }
    
    .dish-metric {
        text-align: center;
    }
    
    .dish-metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--neutral-800);
        margin-bottom: 0.25rem;
        line-height: 1;
    }
    
    .dish-metric-label {
        font-size: 0.75rem;
        color: var(--neutral-500);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    /* Formulaires modernes */
    .form-modern {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-sm);
    }
    
    .form-section-modern {
        margin-bottom: 1.5rem;
        margin-top: -0.5rem;
    }
    
    .form-section-modern h3 {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--neutral-200);
    }
    
    .form-section-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: var(--primary-light);
        border-radius: var(--radius);
        color: var(--primary);
    }
    
    /* Métriques de prévisualisation */
    .preview-metrics-modern {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 1rem 0 1.5rem 0;
    }
    
    .preview-metric {
        background: var(--neutral-50);
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius);
        padding: 1.25rem;
        text-align: center;
        transition: var(--transition);
    }
    
    .preview-metric:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-sm);
    }
    
    .preview-metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--neutral-800);
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .preview-metric-label {
        font-size: 0.875rem;
        color: var(--neutral-500);
        font-weight: 500;
    }
    
    /* États vides */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        margin: 2rem 0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        opacity: 0.6;
    }
    
    .empty-state h3 {
        color: var(--neutral-800);
        margin-bottom: 0.75rem;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    .empty-state p {
        color: var(--neutral-500);
        margin: 0;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .dish-card-metrics, .preview-metrics-modern {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        
        .form-modern {
            padding: 1.25rem;
            margin-bottom: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .dish-card-metrics, .preview-metrics-modern {
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }
        
        .form-modern {
            padding: 1rem;
            border-radius: 8px;
        }
    }
    
    /* Animations */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-slide-up {
        animation: slideInUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        will-change: transform, opacity;
    }
    
    .animate-fade-in {
        animation: fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        will-change: transform, opacity;
    }
    </style>
    """, unsafe_allow_html=True)


def _initialize_session_state():
    """Initialise les états de session nécessaires"""
    if "brouillons" not in st.session_state:
        st.session_state.brouillons = load_drafts()
    if "plat_actif" not in st.session_state:
        st.session_state.plat_actif = None
    if "suggestions" not in st.session_state:
        st.session_state.suggestions = None
    if "edit_view" not in st.session_state:
        st.session_state.edit_view = "liste"
    if "show_success" not in st.session_state:
        st.session_state.show_success = False
    if "objectif_marge_edit" not in st.session_state:
        st.session_state.objectif_marge_edit = 70


def _render_unified_sidebar():
    """Affiche une sidebar unifiée et moderne"""
    st.sidebar.markdown("""
    <div style="
        font-size: 0.75rem;
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.5rem;
        padding-left: 0.2rem;
        letter-spacing: 0.02em;
    ">PARAMÈTRES</div>
    """, unsafe_allow_html=True)
    
    # Slider objectif de marge
    st.session_state.objectif_marge_edit = st.sidebar.slider(
        "Objectif de marge (%)", 
        40, 90, 
        st.session_state.get("objectif_marge_edit", 70), 
        1, 
        key="objectif_marge_edit_slider",
        help="Définissez votre objectif de marge pour l'optimisation des grammages"
    )
    
    # Info optimisation
    with st.sidebar.expander("💡 Optimisation grammages"):
        st.markdown("""
        <div style="font-size: 0.8rem; color: #475569; line-height: 1.6;">
        <strong style="color: #334155; font-size: 0.82rem;">Comment ça fonctionne ?</strong><br>
        L'outil ajuste automatiquement les quantités des ingrédients principaux pour atteindre votre objectif de marge.
        <br><br>
        <strong style="color: #334155; font-size: 0.82rem;">Avantages :</strong><br>
        • Préserve l'équilibre de la recette<br>
        • Respecte les proportions entre ingrédients<br>
        • Optimise les coûts sans compromettre la qualité
        <br><br>
        <strong style="color: #334155; font-size: 0.82rem;">Ingrédients optimisables :</strong><br>
        • Viandes, poissons, fromages<br>
        • Légumes et féculents principaux<br>
        • Sauces et garnitures
        </div>
        """, unsafe_allow_html=True)


def _render_edit_header():
    """Affiche le header avec badge"""
    col_left, col_right = st.columns([0.85, 0.15])
    
    with col_left:
        st.markdown(
            """
            <div class="modifier-left">
                <div class="modifier-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" 
                              stroke="#D92332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" 
                              stroke="#D92332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="modifier-text">
                    <div class="modifier-title">Modifier un plat</div>
                    <div class="modifier-subtitle">Créez et optimisez vos recettes</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_right:
        st.markdown(
            f"""
            <div class="modifier-badge">{len(st.session_state.brouillons)} plats</div>
            """,
            unsafe_allow_html=True,
        )


def _render_navigation_tabs():
    """Affiche les onglets de navigation avec style carte"""
    # CSS pour les boutons stylisés en cartes
    _render_navigation_styles()
    
    # Créer trois colonnes pour les boutons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        liste_active = st.session_state.edit_view == "liste"
        if st.button(
            "☰  Liste des plats",
            key="nav_liste",
            type="primary" if liste_active else "secondary",
            use_container_width=True,
            help="Vue d'ensemble de tous vos plats"
        ):
            st.session_state.edit_view = "liste"
            st.rerun()
    
    with col2:
        creation_active = st.session_state.edit_view == "creation"
        if st.button(
            "✚  Créer un plat",
            key="nav_creation",
            type="primary" if creation_active else "secondary",
            use_container_width=True,
            help="Créer une nouvelle recette"
        ):
            st.session_state.edit_view = "creation"
            st.rerun()
    
    with col3:
        edition_active = st.session_state.edit_view == "edition"
        edit_btn_disabled = not st.session_state.plat_actif
        
        if st.session_state.plat_actif:
            plat_name = st.session_state.plat_actif["nom"]
            label = f"✎  {plat_name[:13]}…" if len(plat_name) > 13 else f"✎  {plat_name}"
            help_text = f"Modifier le plat {plat_name}"
        else:
            label = "✎  Modifier un plat"
            help_text = "Sélectionnez d'abord un plat"
        
        if st.button(
            label,
            key="nav_edition",
            type="primary" if edition_active else "secondary",
            disabled=edit_btn_disabled,
            use_container_width=True,
            help=help_text
        ):
            if st.session_state.plat_actif:
                st.session_state.edit_view = "edition"
                st.rerun()
    
    # Message contextuel
    _render_context_message()


def _render_context_message():
    """Affiche le message contextuel selon la vue active"""
    if st.session_state.edit_view == "liste":
        context_title = "Liste des plats"
        context_message = "Consultez et sélectionnez un plat pour le modifier ou créez une nouvelle recette personnalisée."
        step_indicator = "1/3"
    elif st.session_state.edit_view == "creation":
        context_title = "Création de plat"
        context_message = "Configurez votre nouvelle recette en choisissant une base et en ajustant les ingrédients selon vos besoins."
        step_indicator = "2/3"
    else:
        plat_name = st.session_state.plat_actif["nom"] if st.session_state.plat_actif else "plat"
        context_title = f"Édition: {plat_name}"
        context_message = f"Personnalisez les ingrédients et ajustez les coûts pour optimiser la rentabilité de votre recette."
        step_indicator = "3/3"
    
    st.markdown(f"""
    <div class="context-message">
        <div class="step-badge">{step_indicator}</div>
        <div class="context-content">
            <div class="context-title">{context_title}</div>
            <div class="context-text">{context_message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_navigation_styles():
    """CSS pour styliser les boutons en cartes élégantes"""
    st.markdown("""
    <style>
    /* Conteneur des boutons de navigation */
    div[data-testid="stHorizontalBlock"]:has(button[key="nav_liste"]) {
        margin-bottom: 1rem;
        gap: 0.6rem;
    }
    
    /* Style de base des boutons carte */
    button[key^="nav_"] {
        min-height: 64px !important;
        padding: 1rem 1.5rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        border: 1.5px solid rgba(226, 232, 240, 0.6) !important;
        background: white !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        text-align: center !important;
        color: #1e293b !important;
        letter-spacing: 0.01em !important;
        line-height: 1.6 !important;
    }
    
    /* Bouton secondaire (non actif) */
    button[key^="nav_"][kind="secondary"] {
        background: white !important;
        border-color: rgba(226, 232, 240, 0.6) !important;
        color: #1e293b !important;
    }
    
    button[key^="nav_"][kind="secondary"]:hover:not(:disabled) {
        border-color: #D92332 !important;
        box-shadow: 0 2px 8px rgba(217, 35, 50, 0.12) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Bouton primaire (actif) */
    button[key^="nav_"][kind="primary"] {
        background: linear-gradient(135deg, #D92332, #b41c29) !important;
        border-color: transparent !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(217, 35, 50, 0.25) !important;
    }
    
    button[key^="nav_"][kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(217, 35, 50, 0.35) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Bouton désactivé */
    button[key^="nav_"]:disabled {
        opacity: 0.5 !important;
        cursor: not-allowed !important;
        border-color: rgba(226, 232, 240, 0.6) !important;
    }
    
    button[key^="nav_"]:disabled:hover {
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Message contextuel */
    .context-message {
        display: flex;
        align-items: flex-start;
        background: linear-gradient(145deg, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.65rem 0.9rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        animation: fadeIn 0.5s ease;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .step-badge {
        background: #D92332;
        color: white;
        padding: 0.15rem 0.45rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-right: 0.65rem;
        flex-shrink: 0;
        min-width: 2.2rem;
        text-align: center;
    }
    
    .context-content {
        flex: 1;
    }
    
    .context-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.15rem;
    }
    
    .context-text {
        font-size: 0.8rem;
        color: #64748b;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# VUES PRINCIPALES
# ============================================================================

def _render_list_view(recettes, ingredients, taux_tva, seuil_marge_perso):
    """Affiche la vue liste des plats"""
    # CSS pour la grille
    st.markdown("""
    <style>
    .plat-grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
        gap: 1.5rem;
    }
    
    @media (max-width: 768px) {
        .plat-grid-container {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
    
    .plat-card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        overflow: hidden;
        border: 1px solid #e2e8f0;
        animation: fadeIn 0.3s ease-out forwards;
        opacity: 0;
        transition: all 0.2s ease;
        margin-bottom: 0;
    }

    .plat-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card-content {
        padding: 1.25rem;
        padding-bottom: 0.75rem;
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin: 0 0 0.3rem 0;
        line-height: 1.3;
    }
    
    .card-subtitle {
        font-size: 0.8rem;
        color: #64748b;
    }
    
    /* Boutons icônes intégrés dans le header */
    .btn-container-edit-0, .btn-container-edit-1, .btn-container-edit-2, .btn-container-edit-3, .btn-container-edit-4, .btn-container-edit-5, .btn-container-edit-6, .btn-container-edit-7, .btn-container-edit-8, .btn-container-edit-9,
    .btn-container-delete-0, .btn-container-delete-1, .btn-container-delete-2, .btn-container-delete-3, .btn-container-delete-4, .btn-container-delete-5, .btn-container-delete-6, .btn-container-delete-7, .btn-container-delete-8, .btn-container-delete-9 {
        position: absolute;
        width: 0;
        height: 0;
        overflow: visible;
    }
    
    .plat-card button {
        min-width: 32px !important;
        width: 32px !important;
        height: 32px !important;
        padding: 0 !important;
        border-radius: 5px !important;
        font-size: 1rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 1px solid #e2e8f0 !important;
        background: white !important;
        color: #64748b !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    
    .plat-card button:hover {
        background: #f8fafc !important;
        border-color: #D92332 !important;
        color: #D92332 !important;
        transform: scale(1.05) !important;
    }
    
    /* Masquer les colonnes des boutons après le rendu */
    .plat-card + div[data-testid="column"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="plat-grid-container">', unsafe_allow_html=True)
    
    if not st.session_state.brouillons:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">🍽️</div>
            <h3>Aucun plat personnalisé</h3>
            <p>Commencez par créer votre premier plat personnalisé pour optimiser votre menu</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, plat in enumerate(st.session_state.brouillons):
            # Calculs
            ingr = pd.DataFrame(plat["composition"])
            if "Coût (€)" not in ingr.columns:
                ingr["Coût (€)"] = (ingr["prix_kg"] * ingr["quantite_g"]) / 1000
            
            cout_matiere = ingr["Coût (€)"].sum()
            prix = plat.get('prix_affiche', 0)
            prix_ht = prix / (1 + taux_tva)
            prix_ttc = prix
            marge = prix_ht - cout_matiere
            taux_marge = (marge / prix_ht * 100) if prix_ht > 0 else 0

            # Statut
            if taux_marge >= seuil_marge_perso:
                status_class = "excellent"
                status_text = "Excellent"
                status_icon = "✓"
                badge_bg = "#ecfdf5"
                badge_color = "#065f46"
            elif taux_marge >= seuil_marge_perso - 10:
                status_class = "good" 
                status_text = "Correct"
                status_icon = "⚖️"
                badge_bg = "#fffbeb"
                badge_color = "#92400e"
            else:
                status_class = "poor"
                status_text = "À optimiser"
                status_icon = "⚠️"
                badge_bg = "#fef2f2"
                badge_color = "#b91c1c"

            # HTML de la card avec conteneurs pour les boutons
            card_html = f"""
            <div class="plat-card" data-plat-id="{i}">
                <div class="card-content">
                    <div class="card-header">
                        <div style="flex: 1;">
                            <h3 class="card-title">{plat['nom']}</h3>
                            <div class="card-subtitle">{plat['base']}</div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div style="background: linear-gradient(135deg, {badge_bg} 0%, {badge_bg} 100%); color: {badge_color}; padding: 0.35rem 0.7rem; border-radius: 5px; font-size: 0.88rem; font-weight: 700; box-shadow: 0 2px 4px rgba(0,0,0,0.06); border: 1px solid {badge_color}20;">
                                {taux_marge:.0f}%
                                <span style="font-size: 0.68rem; font-weight: 500; opacity: 0.7; margin-left: 0.35rem;">• {status_text}</span>
                            </div>
                            <div class="btn-container-edit-{i}" style="display: inline-block;"></div>
                            <div class="btn-container-delete-{i}" style="display: inline-block;"></div>
                        </div>
                    </div>
                    <div style="background: linear-gradient(to bottom, #ffffff 0%, #fafbfc 100%); border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1rem; display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem; margin: 0.75rem 0; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                        <div style="text-align: center; position: relative;">
                            <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; letter-spacing: -0.01em;">{prix_ht:.2f}€</div>
                            <div style="font-size: 0.66rem; color: #94a3b8; margin-top: 0.25rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.02em;">Prix HT</div>
                        </div>
                        <div style="text-align: center; border-left: 1px solid #e2e8f0;">
                            <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; letter-spacing: -0.01em;">{prix_ttc:.2f}€</div>
                            <div style="font-size: 0.66rem; color: #94a3b8; margin-top: 0.25rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.02em;">Prix TTC</div>
                        </div>
                        <div style="text-align: center; border-left: 1px solid #e2e8f0;">
                            <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; letter-spacing: -0.01em;">{cout_matiere:.2f}€</div>
                            <div style="font-size: 0.66rem; color: #94a3b8; margin-top: 0.25rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.02em;">Coût</div>
                        </div>
                        <div style="text-align: center; border-left: 1px solid #e2e8f0;">
                            <div style="font-size: 1.05rem; font-weight: 700; color: {badge_color}; letter-spacing: -0.01em;">{marge:.2f}€</div>
                            <div style="font-size: 0.66rem; color: #94a3b8; margin-top: 0.25rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.02em;">Marge</div>
                        </div>
                        <div style="text-align: center; border-left: 1px solid #e2e8f0;">
                            <div style="font-size: 1.05rem; font-weight: 700; color: #0f172a; letter-spacing: -0.01em;">{len(ingr)}</div>
                            <div style="font-size: 0.66rem; color: #94a3b8; margin-top: 0.25rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.02em;">Ingréd.</div>
                        </div>
                    </div>
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)

            # Boutons icônes intégrés dans la card
            col_edit, col_delete = st.columns(2)
            
            with col_edit:
                if st.button("✏️", key=f"edit_{i}", help="Modifier", use_container_width=True):
                    plat_modifie = plat.copy()
                    plat_modifie["nom_original"] = plat["nom"]
                    st.session_state.plat_actif = plat_modifie
                    st.session_state.edit_view = "edition"
                    st.rerun()
            
            with col_delete:
                if st.button("🗑️", key=f"delete_{i}", help="Supprimer", use_container_width=True):
                    st.session_state.brouillons = [b for b in st.session_state.brouillons if b["nom"] != plat["nom"]]
                    save_drafts(st.session_state.brouillons)
                    st.toast(f"✓ {plat['nom']} supprimé", icon="🗑️")
                    st.rerun()
            
            st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def _render_creation_view(recettes, ingredients, taux_tva, seuil_marge_perso):
    """Affiche la vue création d'un plat"""
    st.markdown("""
    <div class="form-modern animate-slide-up" style="padding: 0.5rem; margin-bottom: 0.5rem;">
        <div class="form-section-modern" style="margin-bottom: 0.5rem;">
            <h3 style="font-size: 1rem; padding-bottom: 0.3rem; margin-bottom: 0.3rem;">
                <div class="form-section-icon" style="width: 24px; height: 24px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 6v12M6 12h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                Choix de la base
            </h3>
            <p style="color: var(--neutral-500); margin-bottom: 0.5rem; font-size: 0.85rem;">Sélectionnez un plat existant comme base</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sélection plat de base
    col1, col2 = st.columns(2)
    with col1:
        categories = ["Tout"] + sorted(list(recettes["categorie"].unique()))
        categorie_filtre = st.selectbox("🏷️ Catégorie", categories, key="cat_creation")

    with col2:
        if categorie_filtre == "Tout":
            plats_filtres = sorted(recettes["plat"].unique())
        else:
            plats_filtres = sorted(recettes[recettes["categorie"] == categorie_filtre]["plat"].unique())
        plat_selectionne = st.selectbox("🍽️ Plat de base", plats_filtres, key="base_creation")

    # Configuration
    st.markdown("""
    <div class="form-section-modern">
        <h3>
            <div class="form-section-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="1.5"/>
                </svg>
            </div>
            Configuration du plat
        </h3>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        nom_plat = st.text_input("📝 Nom du plat", value=f"{plat_selectionne} personnalisé", key="nom_plat")
    
    # Traitement des ingrédients
    filtered_ingredients = ingredients[ingredients['plat'].str.lower() == plat_selectionne.lower()].copy()
    
    if filtered_ingredients.empty:
        st.error(f"❌ Aucun ingrédient trouvé pour {plat_selectionne}")
        st.stop()

    ingr_base = calculer_cout(filtered_ingredients.copy())
    
    # Traitement spécial panini
    if plat_selectionne.lower() == "panini pizz":
        ingr_base = _render_panini_configuration(filtered_ingredients)
    # Ajout pâte pour pizzas
    elif any(s in plat_selectionne.lower() for s in ["pizza", " s", " m"]):
        pate_cost = get_dough_cost(plat_selectionne)
        if pate_cost > 0:
            pate_row = pd.DataFrame([{
                "ingredient": "Pâte à pizza",
                "quantite_g": 0,
                "prix_kg": 0,
                "Coût (€)": pate_cost
            }])
            ingr_base = pd.concat([ingr_base, pate_row], ignore_index=True)

    cout_initial = ingr_base["Coût (€)"].sum()
    
    # Prix suggéré
    prix_conseille_ht = cout_initial / (1 - seuil_marge_perso/100) if seuil_marge_perso < 100 else None
    prix_ttc_base = prix_vente_dict.get(plat_selectionne, (prix_conseille_ht * (1 + taux_tva)) if prix_conseille_ht else 10.0)
    prix_ht_base = prix_ttc_base / (1 + taux_tva)

    with col2:
        prix_nouveau_ht = st.number_input(
            f"💰 Prix de vente HT",
            min_value=1.0,
            value=prix_ht_base,
            step=0.5,
            key="prix_nouveau",
            help=f"Prix recommandé : {prix_conseille_ht:.2f}€ HT" if prix_conseille_ht else ""
        )
        prix_ttc_correspondant = prix_nouveau_ht * (1 + taux_tva)
        st.markdown(f"<div style='font-size: 0.85rem; color: #64748b; margin-top: -0.5rem;'>Prix carte TTC: <b>{prix_ttc_correspondant:.2f}€</b></div>", unsafe_allow_html=True)

    # Aperçu financier
    marge_estimee = prix_nouveau_ht - cout_initial
    taux_estime = (marge_estimee / prix_nouveau_ht * 100) if prix_nouveau_ht > 0 else 0

    if taux_estime >= seuil_marge_perso:
        preview_color = "#22c55e"
    elif taux_estime >= seuil_marge_perso - 10:
        preview_color = "#f59e0b"
    else:
        preview_color = "#ef4444"

    st.markdown("""
    <div class="form-section-modern" style="margin-top: 1rem !important;">
        <h3>
            <div class="form-section-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" stroke="currentColor" stroke-width="1.5"/>
                </svg>
            </div>
            Aperçu financier
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="preview-metrics-modern">
        <div class="preview-metric">
            <div class="preview-metric-value">{cout_initial:.2f} €</div>
            <div class="preview-metric-label">Coût matière</div>
        </div>
        <div class="preview-metric">
            <div class="preview-metric-value" style="color: {preview_color};">{marge_estimee:.2f} €</div>
            <div class="preview-metric-label">Marge brute</div>
        </div>
        <div class="preview-metric">
            <div class="preview-metric-value" style="color: {preview_color};">{taux_estime:.0f}%</div>
            <div class="preview-metric-label">Taux de marge</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Composition détaillée
    with st.expander("📋 Voir la composition détaillée", expanded=False):
        display_df = ingr_base.copy()
        if 'ingredient_original' in display_df.columns:
            display_df['ingredient'] = display_df['ingredient_original']
            display_df = display_df.drop(columns=['ingredient_original', 'ingredient_id'], errors='ignore')
        st.dataframe(
            display_df[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]],
            use_container_width=True,
            hide_index=True
        )

    # Actions
    st.markdown("<div style='margin: 0.35rem 0 0.6rem 0;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    
    if col1.button("Annuler", use_container_width=True, key="cancel_creation"):
        st.session_state.edit_view = "liste"
        st.rerun()
    
    if col2.button("Créer et personnaliser", use_container_width=True, type="primary", key="create_dish"):
        if any(plat["nom"] == nom_plat for plat in st.session_state.brouillons):
            st.error(f"❌ Un plat nommé '{nom_plat}' existe déjà")
        else:
            prix_ttc_sauvegarde = prix_nouveau_ht * (1 + taux_tva)
            st.session_state.plat_actif = {
                "nom": nom_plat,
                "base": plat_selectionne,
                "composition": ingr_base.to_dict(orient="records"),
                "prix_affiche": prix_ttc_sauvegarde,
                "nom_original": None
            }
            st.session_state.edit_view = "edition"
            st.rerun()
    
    st.markdown('<div style="margin-bottom: 4rem;"></div>', unsafe_allow_html=True)


def _render_panini_configuration(filtered_ingredients):
    """Configuration spéciale pour les paninis"""
    st.markdown("""
    <div style="margin-bottom: 1rem; padding: 0.6rem 0.8rem; border: 1px solid #e5e7eb; border-left: 3px solid #D92332; border-radius: 6px; background-color: #fafafa;">
        <div style="font-weight: 600; color: #334155; font-size: 0.95rem; margin-bottom: 0.5rem;">
            Configuration du panini
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    mode_avance = st.checkbox("Personnaliser les ingrédients", key="mode_avance")
    
    composition = []
    
    if mode_avance:
        # Mode avancé
        base_selection = st.radio("Base", ["Crème", "Sauce Tomate"], horizontal=True, key="base_panini")
        base_key = "crème" if base_selection == "Crème" else "sauce tomate"
        
        base_matches = filtered_ingredients[filtered_ingredients["ingredient"].str.lower() == base_key]
        if not base_matches.empty:
            composition.append(base_matches.iloc[0])
        
        additional = filtered_ingredients[~filtered_ingredients["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
        if not additional.empty and "Coût (€)" not in additional.columns:
            additional = calculer_cout(additional)
        
        if not additional.empty:
            additional_clean = additional.drop_duplicates(subset=["ingredient"])
            all_ingrs = sorted(list(additional_clean["ingredient"].unique()))
            
            col1, col2 = st.columns(2)
            with col1:
                slot1 = st.selectbox("Ingrédient #1", ["Aucun"] + all_ingrs, key="slot1")
            with col2:
                slot2 = st.selectbox("Ingrédient #2", ["Aucun"] + all_ingrs, key="slot2")
            
            for i, slot in enumerate([slot1, slot2]):
                if slot != "Aucun":
                    slot_matches = additional[additional["ingredient"] == slot]
                    if not slot_matches.empty:
                        ingr_row = slot_matches.iloc[0].copy()
                        if slot in [ing.get("ingredient") for ing in composition]:
                            ingr_row["ingredient_id"] = f"{slot}_{i+1}"
                        composition.append(ingr_row)
    else:
        # Mode simple
        st.caption("Configuration standard avec sauce tomate et ingrédients moyens")
        
        base_key = "sauce tomate"
        base_matches = filtered_ingredients[filtered_ingredients["ingredient"].str.lower() == base_key]
        if not base_matches.empty:
            composition.append(base_matches.iloc[0])
        
        additional = filtered_ingredients[~filtered_ingredients["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
        if not additional.empty and "Coût (€)" not in additional.columns:
            additional = calculer_cout(additional)
        
        if not additional.empty:
            avg_qty = additional["quantite_g"].mean()
            avg_price = additional["prix_kg"].mean() 
            avg_cost = additional["Coût (€)"].mean()
        else:
            avg_qty, avg_price, avg_cost = 30, 8.0, 0.24
        
        for _ in range(2):
            composition.append(pd.Series({
                "ingredient": "Moyenne suppl",
                "quantite_g": avg_qty,
                "prix_kg": avg_price,
                "Coût (€)": avg_cost
            }))
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Ajout mozzarella et pâte
    composition.extend([
        pd.Series({"ingredient": "Mozzarella", "quantite_g": 40, "prix_kg": 5.85, "Coût (€)": 0.234}),
        pd.Series({"ingredient": "Pâte à panini", "quantite_g": 0, "prix_kg": 0, "Coût (€)": 0.12})
    ])
    
    ingr_base = pd.DataFrame(composition)
    
    if 'ingredient_id' in ingr_base.columns:
        ingr_base['ingredient_original'] = ingr_base['ingredient']
        ingr_base.loc[ingr_base['ingredient_id'].notna(), 'ingredient'] = ingr_base.loc[ingr_base['ingredient_id'].notna(), 'ingredient_id']
    
    return calculer_cout(ingr_base)


def _render_edition_view(recettes, ingredients, taux_tva, seuil_marge_perso):
    """Affiche la vue édition d'un plat"""
    # Vérification plat actif
    if "plat_actif" not in st.session_state or st.session_state.plat_actif is None:
        st.error("❌ Aucun plat sélectionné")
        if st.button("🔄 Retour à la liste"):
            st.session_state.edit_view = "liste"
            st.rerun()
        st.stop()
    
    plat_data = st.session_state.plat_actif
    
    # Copie initiale pour détection de modifications
    if "plat_initial" not in st.session_state:
        st.session_state.plat_initial = copy.deepcopy(plat_data)
    
    # Traitement des données
    try:
        ingr_modifie = pd.DataFrame(plat_data["composition"])
        if "Coût (€)" not in ingr_modifie.columns:
            ingr_modifie["Coût (€)"] = (ingr_modifie["prix_kg"] * ingr_modifie["quantite_g"]) / 1000
        ingr_modifie = calculer_cout(ingr_modifie)
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
        if st.button("🔄 Retour"):
            st.session_state.edit_view = "liste"
            st.session_state.plat_actif = None
            st.rerun()
        st.stop()
    
    # Prix et métriques
    prix_ttc = plat_data.get("prix_affiche", 10.0)
    prix_ht = prix_ttc / (1 + taux_tva)
    cout_matiere = ingr_modifie["Coût (€)"].sum()
    marge_brute = prix_ht - cout_matiere
    taux_marge = (marge_brute / prix_ht * 100) if prix_ht > 0 else 0
    
    # Statut
    if taux_marge >= seuil_marge_perso:
        status_class, status_text, status_icon, status_color = "excellent", "Excellente rentabilité", "🟢", "#22c55e"
    elif taux_marge >= seuil_marge_perso - 10:
        status_class, status_text, status_icon, status_color = "good", "Rentabilité correcte", "🟠", "#f59e0b"
    else:
        status_class, status_text, status_icon, status_color = "poor", "À optimiser", "🔴", "#ef4444"
    
    # Interface d'édition
    _render_edition_styles()
    
    # Champs principaux
    col1, col2 = st.columns(2)
    
    with col1:
        nouveau_nom = st.text_input("Nom du plat", value=plat_data["nom"], key="edit_nom")
        if nouveau_nom != plat_data["nom"]:
            plat_data["nom"] = nouveau_nom
            st.session_state.plat_actif = plat_data
    
    with col2:
        prix_ht_edit = st.number_input(
            "Prix de vente HT",
            min_value=1.0,
            value=prix_ht,
            step=0.5,
            key="edit_prix"
        )
        prix_ttc_edit = prix_ht_edit * (1 + taux_tva)
        st.markdown(f"<div style='font-size: 0.75rem; color: #64748b; margin-top: -0.6rem;'>TTC: <b>{prix_ttc_edit:.2f}€</b></div>", unsafe_allow_html=True)
        
        if prix_ttc_edit != plat_data.get("prix_affiche", 0):
            plat_data["prix_affiche"] = prix_ttc_edit
            st.session_state.plat_actif = plat_data
    
    # Métriques
    _render_edition_metrics(prix_ht_edit, prix_ttc_edit, cout_matiere, taux_marge, seuil_marge_perso, status_text, status_icon)
    
    # Composition
    _render_composition_editor(ingr_modifie, ingredients)
    
    # Assistant rentabilité
    _render_optimization_assistant(ingr_modifie, prix_ht_edit, seuil_marge_perso, taux_marge)
    
    # Actions finales
    _render_edition_actions(nouveau_nom, prix_ttc_edit, ingr_modifie, plat_data)
    
    # Espacement après les actions
    st.markdown('<div style="margin-bottom: 4rem;"></div>', unsafe_allow_html=True)


def _render_edition_styles():
    """Styles pour l'édition"""
    st.markdown("""
    <style>
    .section-block {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 0.4rem 0.6rem;
        margin-bottom: 0.5rem;
    }
    .section-title-inline {
        font-size: 0.8rem;
        font-weight: 600;
        color: #0f172a;
    }
    .section-divider {
        height: 1px;
        background: #e2e8f0;
        margin: 0.3rem 0 0.5rem 0;
    }
    .metrics-wrapper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.4rem;
        margin: 0.5rem 0;
    }
    .metric-card-min {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 0.4rem 0.5rem;
    }
    .metric-label {
        font-size: 0.65rem;
        color: #64748b;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.05rem;
        font-weight: 600;
        color: #0f172a;
    }
    .status-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 0.75rem;
        padding: 0.3rem 0.55rem;
        border-radius: 999px;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def _render_edition_metrics(prix_ht, prix_ttc, cout, taux, objectif, status_text, status_icon):
    """Affiche les métriques d'édition"""
    marge = prix_ht - cout
    ecart = taux - objectif
    trend_icon = "↗" if ecart >= 0 else "↘"
    trend_color = "#16a34a" if ecart >= 0 else "#dc2626"
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    metrics_html = f"""
    <div class="metrics-wrapper">
        <div class="metric-card-min">
            <span class="metric-label">Coût ingréd.</span>
            <div class="metric-value">{cout:.2f}€</div>
        </div>
        <div class="metric-card-min">
            <span class="metric-label">Prix HT</span>
            <div class="metric-value">{prix_ht:.2f}€</div>
            <span style="font-size: 0.65rem; color: #94a3b8;">TTC: {prix_ttc:.2f}€</span>
        </div>
        <div class="metric-card-min">
            <span class="metric-label">Marge brute</span>
            <div class="metric-value">{marge:.2f}€</div>
        </div>
        <div class="metric-card-min">
            <span class="metric-label">Taux de marge</span>
            <div class="metric-value">{taux:.1f}%</div>
            <span style="font-size: 0.65rem; color:{trend_color};">{trend_icon} {abs(ecart):.1f} pts</span>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)
    
    status_bg = "#dcfce7" if status_icon == "🟢" else "#fef3c7" if status_icon == "🟠" else "#fee2e2"
    status_fg = "#166534" if status_icon == "🟢" else "#92400e" if status_icon == "🟠" else "#b91c1c"
    
    st.markdown(f"""
    <div class="status-chip" style="background:{status_bg}; color:{status_fg};">
        <span>{status_icon}</span>
        <span>{status_text}</span>
        <span>• Objectif {objectif:.0f}%</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


def _render_composition_editor(ingr_modifie, ingredients):
    """Éditeur de composition"""
    st.markdown("""
    <div class="section-block">
        <div class="section-title-inline">🥣 Composition</div>
        <div style="font-size: 0.75rem; color: #64748b;">Modifiez les quantités ou remplacez des ingrédients</div>
    </div>
    """, unsafe_allow_html=True)
    
    feedback = st.session_state.pop("composition_editor_feedback", None)
    if feedback:
        st.markdown("""
        <div style="background: #f0fdf4; border-left: 3px solid #22c55e; padding: 0.5rem 0.75rem; border-radius: 4px; margin: 0.5rem 0 1rem 0;">
            <span style="color: #15803d; font-size: 0.85rem; font-weight: 500;">✓ Composition mise à jour</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Fonction pour suggérer une quantité selon la catégorie
    def get_suggested_quantity(ingredient_name):
        """Retourne une suggestion de quantité basée sur le type d'ingrédient"""
        if not ingredient_name or pd.isna(ingredient_name):
            return 50.0
        ing_lower = str(ingredient_name).lower()
        if any(x in ing_lower for x in ['boeuf', 'poulet', 'porc', 'agneau', 'veau', 'saumon', 'thon', 'cabillaud', 'merguez', 'chorizo', 'viande']):
            return 150.0
        elif any(x in ing_lower for x in ['riz', 'pâtes', 'pates', 'semoule', 'quinoa', 'pomme de terre']):
            return 70.0
        elif any(x in ing_lower for x in ['tomate', 'salade', 'oignon', 'carotte', 'courgette', 'poivron', 'aubergine', 'champignon', 'légume', 'legume']):
            return 120.0
        elif any(x in ing_lower for x in ['fromage', 'mozzarella', 'parmesan', 'emmental', 'chèvre', 'chevre', 'feta']):
            return 40.0
        elif any(x in ing_lower for x in ['sauce', 'crème', 'creme']):
            return 60.0
        elif any(x in ing_lower for x in ['huile', 'beurre', 'margarine']):
            return 15.0
        elif any(x in ing_lower for x in ['sel', 'poivre', 'épice', 'epice', 'herbe', 'ail', 'persil']):
            return 3.0
        else:
            return 50.0
    
    ingr_modifie = ingr_modifie.reset_index(drop=True)
    composition_view = ingr_modifie[["ingredient", "quantite_g", "Coût (€)"]].rename(columns={
        "ingredient": "Ingrédient",
        "quantite_g": "Quantité (g)",
        "Coût (€)": "Coût (€)"
    })
    composition_view["Coût (€)"] = composition_view["Coût (€)"].round(2)
    composition_view["Remplacer par"] = ""
    
    options_ingredients = sorted(ingredients["ingredient"].unique())
    initial_ingredients = composition_view["Ingrédient"].tolist()
    
    # Info d'aide
    st.markdown("""
    <div style="background: #f8fafc; border-left: 3px solid #3b82f6; padding: 0.5rem 0.75rem; border-radius: 4px; margin: 0.5rem 0; font-size: 0.8rem; color: #475569;">
        💡 <strong>Astuce :</strong> Les nouvelles lignes reçoivent automatiquement une quantité suggérée (ex: viandes 150g, légumes 120g, épices 3g)
    </div>
    """, unsafe_allow_html=True)
    
    editor_df = st.data_editor(
        composition_view,
        hide_index=True,
        num_rows="dynamic",
        use_container_width=True,
        key="composition_editor",
        column_config={
            "Ingrédient": st.column_config.SelectboxColumn("Ingrédient", options=options_ingredients),
            "Quantité (g)": st.column_config.NumberColumn("Quantité (g)", min_value=0.0, step=5.0, format="%.1f"),
            "Coût (€)": st.column_config.NumberColumn("Coût (€)", format="%.2f", disabled=True),
            "Remplacer par": st.column_config.SelectboxColumn("Remplacer par", options=[""] + options_ingredients),
        },
    )
    
    # Détecter les nouvelles lignes et appliquer quantités suggérées
    for idx, row in enumerate(editor_df.to_dict(orient="records")):
        ingredient_name = row.get("Ingrédient")
        qty_value = row.get("Quantité (g)")
        
        # Si c'est une nouvelle ligne (ingrédient renseigné mais quantité vide ou 0)
        if ingredient_name and not pd.isna(ingredient_name):
            if pd.isna(qty_value) or qty_value == 0 or qty_value is None:
                # C'est un nouvel ingrédient ajouté, appliquer suggestion
                suggested_qty = get_suggested_quantity(ingredient_name)
                editor_df.at[idx, "Quantité (g)"] = suggested_qty
    
    # Traitement des modifications
    _process_composition_changes(editor_df, initial_ingredients, ingr_modifie, ingredients)
    
    cout_total = float(ingr_modifie["Coût (€)"].sum())
    st.markdown(f"""
    <div style='background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; 
                padding: 0.6rem 1rem; margin: 0.75rem 0; 
                display: flex; justify-content: space-between; align-items: center;'>
        <span style='color: #64748b; font-size: 0.85rem;'>Coût total</span>
        <span style='color: #0f172a; font-size: 1.1rem; font-weight: 600;'>{cout_total:.2f}€</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)


def _process_composition_changes(editor_df, initial_ingredients, ingr_modifie, ingredients):
    """Traite les modifications de composition"""
    edited_records = []
    for idx, row in enumerate(editor_df.to_dict(orient="records")):
        replacement = row.get("Remplacer par")
        ingredient_name = replacement or row.get("Ingrédient")
        if (not ingredient_name or pd.isna(ingredient_name)) and idx < len(initial_ingredients):
            ingredient_name = initial_ingredients[idx]
        qty_value = row.get("Quantité (g)")
        if not ingredient_name or pd.isna(ingredient_name) or pd.isna(qty_value) or float(qty_value) <= 0:
            continue
        edited_records.append({"ingredient": ingredient_name, "quantite_g": float(qty_value)})
    
    new_df = pd.DataFrame(edited_records)
    if not new_df.empty:
        new_df = new_df.groupby("ingredient", as_index=False)["quantite_g"].sum()
    
    original_df = pd.DataFrame([
        {"ingredient": row["ingredient"], "quantite_g": float(row["quantite_g"])}
        for row in ingr_modifie.to_dict(orient="records")
    ])
    if not original_df.empty:
        original_df = original_df.groupby("ingredient", as_index=False)["quantite_g"].sum()
    
    new_sorted = new_df.sort_values("ingredient").reset_index(drop=True)
    orig_sorted = original_df.sort_values("ingredient").reset_index(drop=True)
    new_sorted["quantite_g"] = new_sorted["quantite_g"].round(3)
    orig_sorted["quantite_g"] = orig_sorted["quantite_g"].round(3)
    
    if not new_sorted.equals(orig_sorted):
        updated_rows = []
        for _, row in new_sorted.iterrows():
            base_row = ingredients[ingredients["ingredient"] == row["ingredient"]]
            if not base_row.empty:
                prix_kg = float(base_row.iloc[0]["prix_kg"])
                qty = float(row["quantite_g"])
                updated_rows.append({
                    "ingredient": row["ingredient"],
                    "quantite_g": qty,
                    "prix_kg": prix_kg,
                    "Coût (€)": (qty * prix_kg) / 1000,
                })
        
        if updated_rows:
            ingr_modifie = pd.DataFrame(updated_rows)
            st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
            st.session_state.suggestions = []
            st.session_state["composition_editor_feedback"] = "Composition mise à jour"
            st.rerun()


def _render_optimization_assistant(ingr_modifie, prix_ht, seuil_marge, taux_actuel):
    """Assistant d'optimisation avec indicateurs de performance"""
    # Calcul des métriques
    ecart = taux_actuel - seuil_marge
    status_color = "#22c55e" if ecart >= 0 else "#f59e0b" if ecart >= -10 else "#ef4444"
    
    # Calcul du gain potentiel (seulement si objectif non atteint)
    cout_actuel = ingr_modifie["Coût (€)"].sum()
    marge_actuelle_euros = prix_ht - cout_actuel
    cout_optimal = prix_ht * (1 - seuil_marge/100)
    
    # Si objectif atteint, pas de gain potentiel
    if ecart >= 0:
        gain_potentiel = 0
        gain_pourcentage = 0
    else:
        gain_potentiel = cout_actuel - cout_optimal
        gain_pourcentage = (gain_potentiel / cout_actuel * 100) if cout_actuel > 0 else 0
    
    # Nombre d'ingrédients optimisables
    nb_ingredients = len(ingr_modifie)
    
    # Indicateur de priorité
    if ecart < -10:
        priorite = "🔴 URGENT"
        priorite_color = "#ef4444"
        priorite_msg = "Optimisation fortement recommandée"
    elif ecart < 0:
        priorite = "🟠 IMPORTANT"
        priorite_color = "#f59e0b"
        priorite_msg = "Optimisation conseillée"
    else:
        priorite = "🟢 OPTIMAL"
        priorite_color = "#22c55e"
        priorite_msg = "Recette déjà optimale"
    
    st.markdown(f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1.25rem; margin: 1rem 0 0.5rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div class="section-title-inline">⚖️ Optimisation grammages</div>
                    <span style="background: {priorite_color}20; color: {priorite_color}; font-size: 0.7rem; font-weight: 600; padding: 0.2rem 0.5rem; border-radius: 3px;">{priorite}</span>
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.2rem;">
                    {priorite_msg} • {nb_ingredients} ingrédients analysables
                </div>
            </div>
            <div style="text-align: right; font-size: 0.7rem; color: #64748b;">
                <div>Objectif: <strong style="color: #0f172a;">{seuil_marge:.0f}%</strong></div>
                <div>Actuel: <strong style="color: {status_color};">{taux_actuel:.1f}%</strong></div>
            </div>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin: 0.75rem 0;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.75rem; text-align: center;">
            <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem;">Gain potentiel</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: {'#22c55e' if ecart >= 0 else '#0f172a'};">
                {('Aucune optimisation nécessaire' if ecart >= 0 else f'{abs(gain_potentiel):.2f}€')}
            </div>
            <div style="font-size: 0.65rem; color: #64748b; margin-top: 0.2rem;">
                {('Objectif atteint' if ecart >= 0 else f'{abs(gain_pourcentage):.1f}% d\'économie')}
            </div>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.75rem; text-align: center;">
            <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem;">Marge actuelle</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: {status_color};">{marge_actuelle_euros:.2f}€</div>
            <div style="font-size: 0.65rem; color: #64748b; margin-top: 0.2rem;">Coût : {cout_actuel:.2f}€</div>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.75rem; text-align: center;">
            <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem;">Écart objectif</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: {status_color};">{ecart:+.1f}%</div>
            <div style="font-size: 0.65rem; color: #64748b; margin-top: 0.2rem;">{'Dépassé' if ecart >= 0 else 'À combler'}</div>
        </div>
    </div>
    
    <style>
    button[key="generate_optimization"] {{
        font-size: 14px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        min-height: 44px !important;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.4) !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }}
    button[key="generate_optimization"]:hover {{
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5) !important;
        transform: translateY(-2px) !important;
    }}
    button[key="generate_optimization"]:active {{
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3) !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    generate_btn = st.button("⚡ Optimiser", key="generate_optimization", use_container_width=True)
    
    if generate_btn:
        with st.spinner("Analyse en cours..."):
            try:
                df_opt = optimize_grammages_balanced(ingr_modifie, prix_ht, seuil_marge)
                suggestions = []
                total_economie = 0
                for _, row in ingr_modifie.iterrows():
                    ing = row["ingredient"]
                    old_q = row["quantite_g"]
                    prix_kg = row["prix_kg"]
                    match = df_opt[df_opt["ingredient"] == ing]
                    new_q = float(match["new_qty"].iloc[0]) if not match.empty else old_q
                    if abs(new_q - old_q) > 0.9:
                        economie = (old_q - new_q) * prix_kg / 1000
                        total_economie += economie
                        suggestions.append((ing, old_q, new_q, economie))
                st.session_state.suggestions = suggestions
                st.session_state.total_economie = total_economie
                if not suggestions:
                    st.markdown("""
                    <div style="background: #f0fdf4; border-left: 3px solid #22c55e; padding: 0.5rem 0.75rem; border-radius: 4px; margin: 0.5rem 0;">
                        <span style="color: #15803d; font-size: 0.85rem; font-weight: 500;">✓ Objectif atteint</span>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur : {e}")
    
    # Affichage sobre des suggestions avec impact financier
    suggestions = st.session_state.get("suggestions", [])
    total_economie = st.session_state.get("total_economie", 0)
    
    if suggestions:
        st.markdown(f"""
        <div class="section-block">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div class="section-title-inline">🎯 Suggestions</div>
                    <div style="font-size: 0.75rem; color: #64748b;">Ajustements proposés • Économie totale: <strong style="color: #22c55e;">{total_economie:.2f}€</strong></div>
                </div>
                <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 4px; padding: 0.3rem 0.6rem;">
                    <span style="color: #15803d; font-size: 0.75rem; font-weight: 600;">💰 +{total_economie:.2f}€ par plat</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tableau avec économie
        summary_df = pd.DataFrame([
            {
                "Ingrédient": ing,
                "Avant (g)": round(old_q, 1),
                "Après (g)": round(new_q, 1),
                "Écart": f"{((new_q - old_q) / old_q * 100):+.1f}%",
                "Économie": f"{economie:.2f}€"
            }
            for ing, old_q, new_q, economie in suggestions
        ])
        
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Boutons d'action sobres
        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns([3, 2])
        with c1:
            if st.button(
                "Appliquer",
                type="primary",
                use_container_width=True,
                key="apply_suggestions"
            ):
                for ing, _, new_q in suggestions:
                    mask = ingr_modifie["ingredient"] == ing
                    if mask.any():
                        ingr_modifie.loc[mask, "quantite_g"] = new_q
                        ingr_modifie.loc[mask, "Coût (€)"] = (new_q * ingr_modifie.loc[mask, "prix_kg"]) / 1000
                st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
                st.session_state.suggestions = []
                st.session_state["composition_editor_feedback"] = "Appliqué"
                st.rerun()
        with c2:
            if st.button(
                "Ignorer",
                use_container_width=True,
                key="ignore_suggestions"
            ):
                st.session_state.suggestions = []
                st.rerun()
    
    st.markdown('<div style="height: 1px; background: #eee; margin: 1rem 0;"></div>', unsafe_allow_html=True)


def _render_edition_actions(nouveau_nom, prix_ttc_edit, ingr_modifie, plat_data):
    """Boutons d'actions d'édition"""
    # Vérifier modifications
    modifications_faites = _check_modifications(nouveau_nom, prix_ttc_edit)
    
    action_cols = st.columns([2.5, 2, 0.8, 0.8])
    
    with action_cols[0]:
        save_btn = st.button(
            "💾 Sauvegarder" if modifications_faites else "✓ Sauvegardé", 
            use_container_width=True, 
            type="primary" if modifications_faites else "secondary",
            disabled=not modifications_faites,
            key="save_main"
        )
    
    with action_cols[1]:
        if st.button("← Retour", use_container_width=True, key="back_main"):
            if modifications_faites:
                st.session_state.confirm_back = True
            else:
                st.session_state.plat_actif = None
                if "plat_initial" in st.session_state:
                    del st.session_state.plat_initial
                st.session_state.edit_view = "liste"
            st.rerun()
    
    with action_cols[2]:
        if st.button("🔄", use_container_width=True, disabled=not modifications_faites, key="reset_main", help="Réinitialiser"):
            if "plat_initial" in st.session_state:
                st.session_state.plat_actif = copy.deepcopy(st.session_state.plat_initial)
                st.toast("Annulé", icon="🔄")
                st.rerun()
    
    with action_cols[3]:
        if st.button("🗑", use_container_width=True, key="delete_main", help="Supprimer"):
            st.session_state.confirm_delete_dish = True
            st.rerun()
    
    # Sauvegarde
    if save_btn:
        _save_dish(nouveau_nom, prix_ttc_edit, ingr_modifie, plat_data)
    
    # Confirmations
    _render_confirmations(plat_data)


def _check_modifications(nouveau_nom, prix_ttc_edit):
    """Vérifie si des modifications ont été faites"""
    if "plat_initial" not in st.session_state:
        return False
    
    plat_initial = st.session_state.plat_initial
    initial_price = float(plat_initial.get("prix_affiche", 0) or 0)
    current_price = float(prix_ttc_edit or 0)
    
    if nouveau_nom != plat_initial.get("nom", ""):
        return True
    if not math.isclose(current_price, initial_price, rel_tol=1e-3):
        return True
    
    current_comp = pd.DataFrame(st.session_state.plat_actif.get("composition", []))
    initial_comp = pd.DataFrame(plat_initial.get("composition", []))
    
    if current_comp.empty != initial_comp.empty:
        return True
    if not current_comp.empty:
        current_sorted = current_comp[["ingredient", "quantite_g"]].sort_values("ingredient").reset_index(drop=True)
        initial_sorted = initial_comp[["ingredient", "quantite_g"]].sort_values("ingredient").reset_index(drop=True)
        current_sorted["quantite_g"] = current_sorted["quantite_g"].round(3)
        initial_sorted["quantite_g"] = initial_sorted["quantite_g"].round(3)
        if not current_sorted.equals(initial_sorted):
            return True
    
    return False


def _save_dish(nouveau_nom, prix_ttc_edit, ingr_modifie, plat_data):
    """Sauvegarde le plat"""
    if not nouveau_nom or nouveau_nom.strip() == "":
        st.error("Nom requis")
        return
    
    nom_original = st.session_state.plat_actif.get("nom_original", plat_data["nom"])
    
    # Vérifier doublon
    nom_existe = any(
        p["nom"].lower() == nouveau_nom.lower() and p["nom"] != nom_original 
        for p in st.session_state.brouillons
    )
    
    if nom_existe:
        st.error("Nom déjà utilisé")
        return
    
    # Mise à jour
    plat_data["nom"] = nouveau_nom
    plat_data["prix_affiche"] = prix_ttc_edit
    plat_data["composition"] = ingr_modifie.to_dict(orient="records")
    
    # Remplacer ou ajouter
    plat_trouve = False
    for i, p in enumerate(st.session_state.brouillons):
        if p["nom"] == nom_original:
            st.session_state.brouillons[i] = plat_data
            plat_trouve = True
            break
    
    if not plat_trouve:
        st.session_state.brouillons.append(plat_data)
    
    # Sauvegarder
    save_drafts(st.session_state.brouillons)
    
    # Réinitialiser
    plat_data["nom_original"] = plat_data["nom"]
    st.session_state.plat_actif = plat_data
    st.session_state.plat_initial = copy.deepcopy(plat_data)
    
    st.toast("✓ Sauvegardé", icon="✅")
    st.rerun()


def _render_confirmations(plat_data):
    """Affiche les dialogues de confirmation"""
    # Confirmation retour
    if st.session_state.get("confirm_back", False):
        st.markdown("""
        <div style="background: #fef3c7; border: 1px solid #fbbf24; border-left: 3px solid #f59e0b; border-radius: 4px; padding: 0.5rem; margin: 0.5rem 0;">
            <div style="font-weight: 600; color: #92400e; font-size: 0.8rem;">⚠️ Modifications non sauvegardées</div>
            <div style="font-size: 0.7rem; color: #78350f;">Quitter sans sauvegarder ?</div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Continuer", use_container_width=True, key="cancel_back"):
                st.session_state.confirm_back = False
                st.rerun()
        with c2:
            if st.button("Quitter", use_container_width=True, key="confirm_back_btn", type="primary"):
                st.session_state.confirm_back = False
                st.session_state.plat_actif = None
                if "plat_initial" in st.session_state:
                    del st.session_state.plat_initial
                st.session_state.edit_view = "liste"
                st.rerun()
    
    # Confirmation suppression
    if st.session_state.get("confirm_delete_dish", False):
        st.markdown("""
        <div style="background: #fee2e2; border: 1px solid #fca5a5; border-left: 3px solid #dc2626; border-radius: 4px; padding: 0.5rem; margin: 0.5rem 0;">
            <div style="font-weight: 600; color: #991b1b; font-size: 0.8rem;">🗑️ Supprimer ce plat ?</div>
            <div style="font-size: 0.7rem; color: #7f1d1d;">Action irréversible</div>
        </div>
        """, unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            if st.button("Annuler", use_container_width=True, key="cancel_delete"):
                st.session_state.confirm_delete_dish = False
                st.rerun()
        with d2:
            if st.button("Supprimer", use_container_width=True, key="confirm_delete_btn", type="primary"):
                nom_a_supprimer = st.session_state.plat_actif.get("nom_original", plat_data["nom"])
                st.session_state.brouillons = [p for p in st.session_state.brouillons if p["nom"] != nom_a_supprimer]
                save_drafts(st.session_state.brouillons)
                st.session_state.confirm_delete_dish = False
                st.session_state.plat_actif = None
                if "plat_initial" in st.session_state:
                    del st.session_state.plat_initial
                st.session_state.edit_view = "liste"
                st.toast("✓ Supprimé", icon="🗑️")
                st.rerun()

