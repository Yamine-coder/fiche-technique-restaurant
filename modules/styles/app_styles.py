"""
Module de gestion des styles CSS de l'application.
Centralise tous les styles pour faciliter la maintenance et éviter la duplication.
"""

import streamlit as st


def inject_global_styles():
    """
    Injecte les styles CSS globaux de l'application.
    À appeler une seule fois au début de app.py.
    """
    st.markdown(
        """
        <style>
            .stAppHeader {
                background-color: rgba(255, 255, 255, 0.0);
                visibility: visible;
            }

            .block-container {
                padding-top: 0.2rem;
                padding-bottom: 0rem;
                padding-left: 2rem;
                padding-right: 2rem;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            /* Responsive : adapter les marges selon la taille d'écran */
            @media (max-width: 1200px) {
                .block-container {
                    padding-left: 1.5rem;
                    padding-right: 1.5rem;
                }
            }
            
            @media (max-width: 768px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
            }
            
            @media (max-width: 480px) {
                .block-container {
                    padding-left: 0.75rem;
                    padding-right: 0.75rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_creative_header_styles():
    """
    Injecte les styles créatifs pour l'entête et la mise en page générale.
    """
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
      
      html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
      }

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

        div[data-testid="stMarkdownContainer"]:has(style) {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Harmoniser les espacements entre les blocs clés */
        div[data-testid="stMarkdownContainer"]:has(.plat-grid-container) {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        .plat-grid-container {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        .context-message {
            margin: 0 !important;
        }

        div[data-testid="element-container"]:has(.modifier-header-container),
        div[data-testid="element-container"]:has(.dish-header-premium),
        div[data-testid="element-container"]:has(.nav-buttons),
        div[data-testid="element-container"]:has(.context-message),
        div[data-testid="element-container"]:has(.plat-grid-container) {
            padding-top: 0 !important;
            padding-bottom: 0.35rem !important;
            margin: 0 !important;
        }
        
        /* Forcer tous les conteneurs entre le message et la grille à se réduire */
        div[data-testid="stMarkdownContainer"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }

        .view-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 0.7rem;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
            border-left: 3px solid #D92332;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
            margin: -0.5rem 0 0.4rem;
        }
        
        .view-header-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
            background: rgba(217, 35, 50, 0.06);
            border-radius: 5px;
        }
        
        .view-header-title {
            font-weight: 600;
            color: #1e293b;
            font-size: 0.9rem;
            letter-spacing: -0.01em;
        }
        
        .view-header-subtitle {
            font-size: 0.7rem;
            color: #64748b;
            font-weight: 400;
            display: block;
            margin-top: 0.08rem;
        }

        /* Styles pour les cartes de plats */
        .plat-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
            margin-top: 0.75rem;
        }

        /* Styles pour les insights */
        .insights-belt {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 0.8rem;
            margin: 0.5rem 0 1rem;
            align-items: stretch;
        }
        
        .insight-card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 0.7rem 0.95rem;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
            min-height: 125px;
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }
        
        .insight-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            color: #94a3b8;
            letter-spacing: 0.05em;
        }
        
        .insight-value {
            font-size: 1.2rem;
            font-weight: 600;
            color: #0f172a;
            margin: 0.15rem 0 0.2rem;
        }
        
        .insight-meta {
            font-size: 0.8rem;
            color: #475569;
        }
        
        .insight-meta strong {
            color: #0f172a;
        }
        
        .insight-action {
            margin-top: 0.35rem;
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.78rem;
            color: #D92332;
            font-weight: 600;
        }

        /* Styles pour le simulateur global */
        .global-simulator {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin-top: 1.5rem;
            background: #ffffff;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        }
        
        .global-simulator h3 {
            margin: 0 0 0.4rem;
            font-size: 1rem;
            color: #0f172a;
        }
        
        .global-simulator small {
            color: #94a3b8;
            font-size: 0.78rem;
        }

        /* Styles pour le simulateur de décision */
        .decision-wrapper {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin: 0.5rem 0 1.2rem;
            background: #ffffff;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }
        
        .decision-wrapper h3 {
            margin: 0 0 0.4rem;
            font-size: 1rem;
            color: #0f172a;
        }
        
        .decision-note {
            font-size: 0.78rem;
            color: #94a3b8;
            margin-bottom: 0.6rem;
        }

        /* Styles pour les cartes métriques */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
            border-radius: 10px;
            padding: 0.7rem 0.75rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            text-align: center;
            margin-bottom: 0.6rem;
            position: relative;
            overflow: hidden;
            transition: all 0.2s ease;
            cursor: pointer;
            border: 1px solid #f1f5f9;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent 0%, 
                #D92332 50%, 
                transparent 100%);
            transition: left 0.4s ease;
        }
        
        .metric-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, 
                rgba(217, 35, 50, 0.005) 0%, 
                rgba(217, 35, 50, 0.015) 100%);
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 8px 20px rgba(0,0,0,0.1),
                0 4px 10px rgba(217, 35, 50, 0.05);
            border-color: #e2e8f0;
        }
        
        .metric-card:hover::before {
            left: 100%;
        }
        
        .metric-card:hover::after {
            opacity: 1;
        }
        
        .metric-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: #D92332;
            transition: all 0.2s ease;
            position: relative;
            z-index: 2;
            line-height: 1.2;
        }
        
        .metric-card:hover .metric-value {
            transform: scale(1.05);
            color: #C41E3A;
        }
        
        .metric-title {
            font-size: 0.8rem;
            font-weight: 500;
            color: #64748b;
            transition: all 0.2s ease;
            position: relative;
            z-index: 2;
            margin-top: 0.35rem;
        }
        
        .metric-card:hover .metric-title {
            color: #475569;
        }

        /* Styles pour les filtres actifs */
        .filter-summary {
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.6rem 0.85rem;
            margin: 0.2rem 0 0.75rem;
            box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
        }

        .filter-summary-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            color: #94a3b8;
            letter-spacing: 0.08em;
            margin-top: 0.05rem;
        }

        .filter-chip-group {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }

        .filter-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            font-size: 0.78rem;
            font-weight: 500;
            padding: 0.18rem 0.55rem;
            border-radius: 999px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: #f8fafc;
            color: #0f172a;
        }

        .filter-chip-label {
            font-size: 0.62rem;
            text-transform: uppercase;
            color: #94a3b8;
            letter-spacing: 0.08em;
        }

        @media (max-width: 768px) {
            .filter-summary {
                flex-direction: column;
            }
            .filter-chip-group {
                width: 100%;
            }
        }

        /* Styles pour la sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #fcfcfc 100%);
            border-right: 1px solid #e2e8f0;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        /* Labels minimalistes */
        .sidebar .stRadio > label,
        .sidebar .stSelectbox > label,
        .sidebar .stSlider > label {
            font-size: 0.8rem;
            font-weight: 500;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.35rem;
        }

        /* Radio buttons plus compacts */
        .sidebar div.row-widget.stRadio > div {
            gap: 0.3rem;
        }

        .sidebar .stRadio [role="radiogroup"] label {
            font-size: 0.85rem;
            padding: 0.4rem 0.65rem;
            border-radius: 6px;
            transition: all 0.15s ease;
            border: 1px solid transparent;
        }

        .sidebar .stRadio [role="radiogroup"] label:hover {
            background: #f8fafc;
            border-color: #e2e8f0;
        }

        .sidebar .stRadio [role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
            background: white;
            border: 1.5px solid #cbd5e1;
        }

        .sidebar .stRadio [role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] {
            background: rgba(217, 35, 50, 0.06);
            border-color: rgba(217, 35, 50, 0.2);
        }

        .sidebar .stRadio [role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] > div:first-child {
            background: #D92332;
            border-color: #D92332;
        }

        /* Selectbox minimaliste */
        .sidebar .stSelectbox [data-baseweb="select"] {
            border-radius: 6px;
            border-color: #e2e8f0;
            font-size: 0.85rem;
        }

        .sidebar .stSelectbox [data-baseweb="select"]:hover {
            border-color: #cbd5e1;
        }

        /* Slider épuré */
        .sidebar .stSlider [data-baseweb="slider"] {
            padding-top: 0.5rem;
        }

        .sidebar .stSlider [data-baseweb="slider"] [role="slider"] {
            background: #D92332;
        }

        /* Réduction des marges globales */
        .sidebar [data-testid="stVerticalBlock"] > div {
            padding-top: 0.3rem;
            padding-bottom: 0.3rem;
        }

        .sidebar .element-container {
            margin-bottom: 0.5rem;
        }

        .sidebar-section-label {
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #C22C35;
            margin: 0.2rem 0 0.25rem;
        }

        .sidebar-section-subtitle {
            font-size: 0.72rem;
            color: #94a3b8;
            margin: -0.1rem 0 0.8rem;
        }

        .sidebar-slider-label {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.72rem;
            color: #94a3b8;
            margin-bottom: 0.15rem;
        }

        .sidebar-slider-label span {
            font-size: 0.68rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .sidebar-slider-value {
            background: #fef2f2;
            color: #C22C35;
            font-weight: 600;
            padding: 0.05rem 0.45rem;
            border-radius: 999px;
            border: 1px solid rgba(217, 35, 50, 0.15);
        }

        .sidebar-hint {
            font-size: 0.68rem;
            color: #94a3b8;
            margin-top: 0.7rem;
            border-top: 1px solid rgba(148, 163, 184, 0.3);
            padding-top: 0.45rem;
            line-height: 1.4;
        }

        /* Cards des plats - Style minimaliste ultra moderne */
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
        
        .dish-card-modern::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--neutral-200);
            transition: var(--transition);
        }
        
        .dish-card-modern.excellent {
            border-left: 4px solid var(--success);
            background: white;
        }
        
        .dish-card-modern.good {
            border-left: 4px solid var(--warning);
            background: white;
        }
        
        .dish-card-modern.poor {
            border-left: 4px solid var(--danger);
            background: white;
        }
        
        .dish-card-modern.excellent::before,
        .dish-card-modern.good::before,
        .dish-card-modern.poor::before { 
            content: none;
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
            padding: 0;
            display: inline-block;
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
            border: none;
            position: relative;
            transition: all 0.2s ease;
        }
        
        .dish-card-status::before {
            display: none;
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
        
        .dish-card-actions {
            display: flex;
            gap: 0.75rem;
            margin-top: 1.5rem;
        }
        
        /* Boutons modernes */
        .btn-modern {
            flex: 1;
            padding: 0.75rem 1rem;
            border-radius: var(--radius);
            font-weight: 500;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: var(--transition);
            cursor: pointer;
            border: 1px solid;
            text-decoration: none;
        }
        
        .btn-primary {
            background: white;
            color: var(--primary);
            border-color: var(--primary);
        }
        
        .btn-primary:hover {
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 12px rgba(217, 35, 50, 0.25);
            transform: translateY(-1px);
        }
        
        .btn-secondary {
            background: white;
            color: var(--neutral-500);
            border-color: var(--neutral-200);
        }
        
        .btn-secondary:hover {
            background: var(--danger);
            color: white;
            border-color: var(--danger);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
            transform: translateY(-1px);
        }

        /* Styles pour les headers modernes */
        .modern-subheader {
            position: relative;
            padding: 0.65rem 0.9rem;
            margin: 0.4rem 0 0.6rem;
            border-radius: 6px;
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border: 1px solid #e2e8f0;
            border-left: 3px solid #D92332;
            overflow: hidden;
        }
        
        .modern-subheader::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 0;
            height: 100%;
            background: linear-gradient(90deg, 
              rgba(217, 35, 50, 0.02) 0%, 
              rgba(217, 35, 50, 0.04) 100%);
            transition: width 0.3s ease;
        }
        
        .modern-subheader:hover::before {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)


def inject_all_styles():
    """
    Injecte tous les styles CSS de l'application en une seule fois.
    Fonction pratique pour initialiser rapidement tous les styles au démarrage.
    """
    inject_global_styles()
    inject_creative_header_styles()


# Fonction utilitaire pour _ensure_css_once déjà utilisée dans app.py
def ensure_css_once(flag_name: str, css_block: str) -> None:
    """
    Injecte un bloc CSS une seule fois par session Streamlit.
    
    Args:
        flag_name: Nom du flag dans session_state pour vérifier si déjà injecté
        css_block: Bloc CSS à injecter (doit contenir les balises <style>)
    """
    if st.session_state.get(flag_name):
        return
    st.markdown(css_block, unsafe_allow_html=True)
    st.session_state[flag_name] = True
