"""
Analyse comparative - Comparaison des performances des plats
"""
import streamlit as st
import pandas as pd

from modules.data.constants import TVA_VENTE, prix_vente_dict
from modules.business.cost_calculator import calculer_cout, get_dough_cost
from modules.components import render_view_header


def render_comparative_view(recettes, ingredients, objectif_marge):
    """
    Affiche l'analyse comparative des plats avec KPIs et classements.
    
    Args:
        recettes: DataFrame des recettes
        ingredients: DataFrame des ingrédients
        objectif_marge: Objectif de marge en pourcentage
    """
    render_view_header(
        icon_svg="""<svg width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3v12h12" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="6" y="8" width="2" height="7" rx="0.5" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.2"/>
            <rect x="10" y="5" width="2" height="10" rx="0.5" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.2"/>
            <rect x="14" y="9" width="2" height="6" rx="0.5" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.2"/>
        </svg>""",
        title="Analyse comparative",
        subtitle="Comparez les performances de vos plats et identifiez les leviers d'optimisation",
    )
    
    # Message d'information TVA - Style personnalisé
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fef2f2 0%, #fff5f5 100%);
        border: 1px solid #fecaca;
        border-left: 3px solid #D92332;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 1px 2px rgba(217, 35, 50, 0.06);
    ">
        <div style="font-size: 1rem; flex-shrink: 0;">💡</div>
        <div style="color: #991b1b; font-size: 0.75rem; line-height: 1.4;">
            <strong>Coûts en HT</strong> : TVA 5,5% déduite (déductible sur déclaration trimestrielle)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu de navigation interne
    _render_navigation_menu()
    
    # Information sur les prix HT
    _render_ht_info()
    
    # CSS et animations
    _render_navigation_styles()
    
    # Contrôles sidebar
    categorie_comp, selected_plats, seuil_marge, classement_par, filtre_sous_seuil = _render_sidebar_controls(recettes)
    
    # Déterminer les plats à analyser
    if categorie_comp == "Tout":
        plats_cat = recettes["plat"].unique()
    else:
        plats_cat = recettes[recettes["categorie"] == categorie_comp]["plat"].unique()
    
    plats_analyzes = selected_plats if selected_plats else plats_cat
    
    # Fonction d'analyse d'un plat
    def analyse_plat(plat, seuil_marge):
        """Analyse un plat - tous les calculs sont en HT"""
        ingr = ingredients[ingredients['plat'].str.lower() == plat.lower()].copy()
        ingr = calculer_cout(ingr)
        base_cost = ingr["Coût (€)"].sum()
        dough = get_dough_cost(plat)

        if plat.lower() == "panini pizz":
            # Coût moyen des bases (crème et sauce tomate)
            bases = ingr[ingr["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
            mean_base = bases["Coût (€)"].mean() if not bases.empty else 0.0
            avg_add = 0.246  # Moyenne figée des suppléments
            cost_mozza = 0.234  # 40g de mozzarella
            cost_dough = 0.12   # pâte à panini
            total_cost = mean_base + 2 * avg_add + cost_mozza + cost_dough
        else:   
            total_cost = base_cost + dough

        prix_ttc = prix_vente_dict.get(plat, 0)
        taux_tva = TVA_VENTE
        # Toujours calculer en HT
        prix_ht = prix_ttc / (1 + taux_tva)

        marge = prix_ht - total_cost
        taux = (marge / prix_ht * 100) if prix_ht > 0 else None

        if taux is None:
            note = "❓ Données manquantes"  
        elif taux >= 70 and marge >= 5:
            note = "🔝 Excellent — très rentable"
        elif taux >= 70:
            note = "💡 Bon rendement — petit gain"
        elif taux >= 50 and marge >= 5:
            note = "👍 Correct — à surveiller"  
        elif taux >= 50:    
            note = "⚠️ Faible gain — améliorable"   
        else:
            note = "❌ À revoir — non rentable"

        prix_conseille = total_cost / (1 - seuil_marge / 100) if seuil_marge < 100 else None
        delta_prix = prix_conseille - prix_ht if prix_conseille else None
        delta_pct = (delta_prix / prix_ht * 100) if prix_ht > 0 and delta_prix else None

        if delta_pct is None:
            ajustement = "❓"
        elif delta_pct <= 10:
            ajustement = "✅ raisonnable"
        elif delta_pct <= 25:
            ajustement = "⚠️ à étudier"
        else:
            ajustement = "❌ trop écarté"

        return {
            "Plat": plat,
            "Prix HT (€)": round(prix_ht, 2),
            "Prix TTC (€)": round(prix_ttc, 2),
            "Coût (€)": round(total_cost, 2),
            "Marge (€)": round(marge, 2),
            "Taux (%)": round(taux, 1) if taux else None,
            "Note": note,
            "Prix conseillé (€)": round(prix_conseille, 2) if prix_conseille else None,
            "Delta (€)": round(delta_prix, 2) if delta_prix else None,
            "Delta (%)": round(delta_pct, 1) if delta_pct else None,
            "Ajustement": ajustement
        }
    
    # Analyser tous les plats
    df = pd.DataFrame([analyse_plat(p, seuil_marge) for p in plats_analyzes])
    
    # Afficher les KPIs
    _render_kpis(df, seuil_marge)
    
    # Déterminer la clé de classement
    classement_key = "Marge (€)" if classement_par == "Marge (€)" else "Taux (%)"
    
    # Afficher Top & Flop si aucune sélection spécifique
    if not selected_plats:
        _render_top_flop(df, seuil_marge, classement_key)
    
    # Analyse des ingrédients critiques
    _render_ingredients_critiques(plats_analyzes, ingredients)


def _render_navigation_menu():
    """Affiche le menu de navigation interne"""
    st.markdown("""
    <div id="navigation-menu" style="
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 7px;
        padding: 0.85rem 1.15rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.4rem;
            margin-bottom: 0.6rem;
        ">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 12h18M3 6h18M3 18h18" stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="
                font-weight: 600;
                color: #374151;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">Navigation Rapide</span>
        </div>
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        ">
            <a href="#section-kpis" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 1.2rem;
                    height: 1.2rem;
                    font-size: 1.1rem;
                    position: relative;
                ">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 3v18h18" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <rect x="6" y="13" width="3" height="5" rx="0.5" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                        <rect x="11" y="9" width="3" height="9" rx="0.5" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
                        <rect x="16" y="5" width="3" height="13" rx="0.5" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.5"/>
                    </svg>
                </span>
                <div>
                    <div style="font-weight: 500;">Indicateurs de Performance</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Marges et rentabilité</div>
                </div>
            </a>
            <a href="#section-top-flop" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="font-size: 1.1rem;">🏆</span>
                <div>
                    <div style="font-weight: 500;">Top & Flop 5</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Meilleurs et pires</div>
                </div>
            </a>
            <a href="#section-ingredients" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="font-size: 1.1rem;">🎯</span>
                <div>
                    <div style="font-weight: 500;">Ingrédients Critiques</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Analyse poussée</div>
                </div>
            </a>
        </div>
        <style>
        a:hover {
            background-color: #D92332 !important;
            color: white !important;
            border-color: #D92332 !important;
            transform: translateY(-1px);
        }
        a:hover * {
            color: white !important;
        }
        </style>
        <div style="
            padding: 0.5rem;
            background: rgba(217, 35, 50, 0.05);
            border-radius: 4px;
            text-align: center;
            font-size: 0.8rem;
            color: #64748b;
        ">
            💡 <strong>Astuce :</strong> Utilisez les boutons "Retour au menu" en bas de chaque section pour naviguer facilement
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_ht_info():
    """Affiche l'information sur les prix HT"""
    st.markdown("""
    <div style="
        margin: 0 0 0.8rem; 
        padding: 0.4rem 0.9rem;
        border: 1px solid #e9ecef;
        background: linear-gradient(to right, rgba(255, 255, 255, 0.9), rgba(250, 250, 252, 0.97));
        border-radius: 6px;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(to bottom, #D92332, rgba(217, 35, 50, 0.7));
        "></div>
        <div style="
            background: rgba(217, 35, 50, 0.08);
            color: #D92332;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            margin-right: 0.6rem;
            letter-spacing: 0.03em;
        ">HT</div>
        <span style="
            color: #475569;
            font-size: 0.8rem;
            font-weight: 400;
            letter-spacing: 0.01em;
        ">Tous les prix sont affichés en <b>HT</b></span>
    </div>
    """, unsafe_allow_html=True)


def _render_navigation_styles():
    """Affiche les styles CSS pour la navigation"""
    st.markdown("""
    <style>
    /* Animation et transitions fluides */
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Navigation fluide */
    html {
        scroll-behavior: smooth;
    }
    
    /* Ajustement des ancres */
    [id] {
        scroll-margin-top: 70px;
    }
    
    /* Style des liens de navigation */
    a {
        transition: all 0.2s ease;
        text-decoration: none;
    }
    a:hover {
        background-color: #D92332 !important;
        color: white !important;
        border-color: #D92332 !important;
        transform: translateY(-1px);
    }
    a:hover * {
        color: white !important;
    }
    
    /* Responsive */
    @media (max-width: 600px) {
        .section-title-minimal {
            margin: 1.5rem 0 1.5rem !important;
            padding: 1rem 1.2rem !important;
            gap: 0.8rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def _render_sidebar_controls(recettes):
    """Affiche les contrôles de la sidebar et retourne les valeurs"""
    # Séparateur
    st.sidebar.markdown("""
    <div style="height: 1px; background: #f1f5f9; margin: 0.5rem 0 0.4rem;"></div>
    """, unsafe_allow_html=True)
    
    # Sélection des plats
    st.sidebar.markdown("""
    <div style="
        font-size: 0.68rem;
        font-weight: 600;
        color: #D92332;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    ">Plats</div>
    """, unsafe_allow_html=True)
    
    categories = ["Tout"] + list(recettes["categorie"].unique())
    categorie_comp = st.sidebar.selectbox("Filtrer par catégorie", categories, key="cat_comp")
    
    if categorie_comp == "Tout":
        plats_cat = recettes["plat"].unique()
    else:
        plats_cat = recettes[recettes["categorie"] == categorie_comp]["plat"].unique()
    
    selected_plats = st.sidebar.multiselect("Plats à comparer", plats_cat, key="selected_plats")
    
    # Séparateur
    st.sidebar.markdown("""
    <div style="height: 1px; background: #f1f5f9; margin: 0.4rem 0;"></div>
    """, unsafe_allow_html=True)
    
    # Paramètres
    st.sidebar.markdown("""
    <div style="
        font-size: 0.68rem;
        font-weight: 600;
        color: #D92332;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    ">Paramètres</div>
    """, unsafe_allow_html=True)
    
    seuil_marge = st.sidebar.slider("Seuil de rentabilité (%)", 40, 90, 70)
    classement_par = st.sidebar.radio("Classement par", ["Marge (€)", "Taux (%)"])
    filtre_sous_seuil = st.sidebar.checkbox("Plats sous le seuil uniquement")
    
    # Séparateur
    st.sidebar.markdown("""
    <div style="height: 1px; background: #f1f5f9; margin: 0.4rem 0;"></div>
    """, unsafe_allow_html=True)
    
    # Informations
    with st.sidebar.expander("💡 Comprendre les métriques"):
        st.markdown("""
        <div style="font-size: 0.8rem; color: #475569; line-height: 1.6;">
        <strong style="color: #334155; font-size: 0.82rem;">Pourquoi afficher en HT ?</strong><br>
        • En restauration, la TVA est reversée à l'État, donc ne constitue pas un gain<br>
        • Il est plus juste de calculer les marges en hors taxes (HT)
        <br><br>
        <strong style="color: #334155; font-size: 0.82rem;">Pourquoi 70% est un bon seuil ?</strong><br>
        En restauration, on vise un taux de marge matière de 70% ou plus.
        <br><br>
        Cela signifie que 30% du prix est consacré aux ingrédients, le reste couvre :<br>
        • Main d'œuvre<br>
        • Charges (loyer, énergie...)<br>
        • Bénéfices
        <br><br>
        <strong style="color: #334155; font-size: 0.82rem;">📊 Niveaux de rentabilité :</strong><br>
        • < 50% = souvent à perte<br>
        • 50–70% = à surveiller<br>
        • ≥ 70% = bon rendement
        <br><br>
        <em style="font-size: 0.75rem; color: #64748b;">Source: École Hôtelière de Lausanne</em>
        <br><br>
        <strong style="color: #334155; font-size: 0.82rem;">Quel critère choisir ?</strong><br>
        • <strong>Marge (€)</strong> : met en avant les plats qui rapportent le plus d'argent brut<br>
        • <strong>Taux (%)</strong> : montre les plats les plus efficaces proportionnellement
        </div>
        """, unsafe_allow_html=True)
    
    return categorie_comp, selected_plats, seuil_marge, classement_par, filtre_sous_seuil


def _render_kpis(df, seuil_marge):
    """Affiche les KPIs de performance"""
    # Calculs
    marge_moy = df["Marge (€)"].mean()
    taux_moy = df["Taux (%)"].mean()
    nb_plats_total = len(df)
    nb_plats_rentables = len(df[df["Taux (%)"] >= seuil_marge])
    nb_plats_risque = len(df[(df["Taux (%)"] < seuil_marge) & (df["Taux (%)"] >= 50)])
    nb_plats_deficitaires = len(df[df["Taux (%)"] < 50])
    pct_plats_rentables = (nb_plats_rentables / nb_plats_total * 100) if nb_plats_total > 0 else 0
    prix_moyen = df["Prix HT (€)"].mean()
    cout_moyen = df["Coût (€)"].mean()
    ratio_cout_prix = (cout_moyen / prix_moyen * 100) if prix_moyen > 0 else 0
    
    # Section KPIs
    st.markdown('<div id="section-kpis"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 0.4rem 0 0.8rem;">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.8rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 34px;
                height: 34px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 7px;
            ">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3v18h18" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <rect x="6" y="13" width="3" height="5" rx="0.5" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                    <rect x="11" y="9" width="3" height="9" rx="0.5" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
                    <rect x="16" y="5" width="3" height="13" rx="0.5" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.5"/>
                </svg>
            </div>
            <div>
                <span style="font-weight: 600; color: #1e293b; font-size: 1.05rem;">
                    Indicateurs de Performance
                </span>
                <span style="font-size: 0.8rem; color: #64748b; font-weight: 400; display: block;">
                    Vue d'ensemble des marges et rentabilité
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Première rangée de KPIs
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    couleur_perf = "#22c55e" if pct_plats_rentables >= 75 else "#f59e0b" if pct_plats_rentables >= 60 else "#ef4444"
    
    with row1_col1:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; height: 90px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Marge Moyenne</div>
            <div style="display: flex; align-items: baseline; gap: 0.3rem;">
                <span style="font-size: 2rem; font-weight: 600; color: #0f172a; line-height: 1;">{marge_moy:.2f}</span>
                <span style="font-size: 0.9rem; color: #64748b; font-weight: 500;">€</span>
            </div>
            <div style="font-size: 0.7rem; color: #94a3b8;">par plat</div>
        </div>
        """, unsafe_allow_html=True)
    
    with row1_col2:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; height: 90px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Taux Moyen</div>
            <div style="display: flex; align-items: baseline; gap: 0.3rem;">
                <span style="font-size: 2rem; font-weight: 600; color: #0f172a; line-height: 1;">{taux_moy:.1f}</span>
                <span style="font-size: 0.9rem; color: #64748b; font-weight: 500;">%</span>
            </div>
            <div style="font-size: 0.7rem; color: #94a3b8;">rentabilité</div>
        </div>
        """, unsafe_allow_html=True)
    
    with row1_col3:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; height: 90px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Performance</div>
            <div style="display: flex; align-items: baseline; gap: 0.3rem;">
                <span style="font-size: 2rem; font-weight: 600; color: {couleur_perf}; line-height: 1;">{pct_plats_rentables:.0f}</span>
                <span style="font-size: 0.9rem; color: #64748b; font-weight: 500;">%</span>
            </div>
            <div style="font-size: 0.7rem; color: #94a3b8;">plats rentables</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
    
    # Deuxième rangée
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    
    couleur_ratio = "#22c55e" if ratio_cout_prix <= 30 else "#f59e0b" if ratio_cout_prix <= 40 else "#ef4444"
    
    with row2_col1:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; height: 90px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Santé Menu</div>
            <div style="display: flex; gap: 0.4rem; align-items: center; font-size: 0.75rem; font-weight: 500;">
                <span style="color: #22c55e;">✓ {nb_plats_rentables}</span>
                <span style="color: #e2e8f0;">•</span>
                <span style="color: #f59e0b;">⚠ {nb_plats_risque}</span>
                <span style="color: #e2e8f0;">•</span>
                <span style="color: #ef4444;">✕ {nb_plats_deficitaires}</span>
            </div>
            <div style="width: 100%; height: 4px; background: #f1f5f9; border-radius: 2px; overflow: hidden; display: flex;">
                <div style="width: {(nb_plats_rentables/nb_plats_total*100):.1f}%; background: #22c55e; height: 100%;"></div>
                <div style="width: {(nb_plats_risque/nb_plats_total*100):.1f}%; background: #f59e0b; height: 100%;"></div>
                <div style="width: {(nb_plats_deficitaires/nb_plats_total*100):.1f}%; background: #ef4444; height: 100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with row2_col2:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; height: 90px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Prix Moyen</div>
            <div style="display: flex; align-items: baseline; gap: 0.3rem;">
                <span style="font-size: 2rem; font-weight: 600; color: #0f172a; line-height: 1;">{prix_moyen:.2f}</span>
                <span style="font-size: 0.9rem; color: #64748b; font-weight: 500;">€</span>
            </div>
            <div style="font-size: 0.7rem; color: #94a3b8;">HT</div>
        </div>
        """, unsafe_allow_html=True)
    
    with row2_col3:
        st.markdown(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; height: 90px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Coût Moyen</div>
            <div style="display: flex; align-items: baseline; gap: 0.3rem;">
                <span style="font-size: 2rem; font-weight: 600; color: #0f172a; line-height: 1;">{cout_moyen:.2f}</span>
                <span style="font-size: 0.9rem; color: #64748b; font-weight: 500;">€</span>
            </div>
            <div style="font-size: 0.7rem; color: {couleur_ratio}; font-weight: 600;">{ratio_cout_prix:.0f}% du prix</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton retour
    _render_back_to_menu_button()


def _render_top_flop(df, seuil_marge, classement_key):
    """Affiche les sections Top 5 et Flop 5"""
    st.markdown('<div id="section-top-flop"></div>', unsafe_allow_html=True)
    
    top5 = df[df["Taux (%)"] >= seuil_marge].sort_values(classement_key, ascending=False).head(5)
    flop5 = df[df["Taux (%)"] < seuil_marge].sort_values(classement_key, ascending=True).head(5)
    
    st.markdown('<div style="margin: 1.5rem 0;">', unsafe_allow_html=True)
    
    # Top 5
    st.markdown(f"""
<div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 0.8rem; background: linear-gradient(to right, #fafafa 0%, #ffffff 100%); border-left: 2.5px solid #10b981; border-radius: 6px; margin: 1rem 0 0.8rem;">
    <div style="display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: rgba(16, 185, 129, 0.08); border-radius: 5px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8.21 13.89L7 23l4.5-2.5L16 23l-1.21-9.11" stroke="#10b981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M15 7a3 3 0 11-6 0 3 3 0 016 0z" stroke="#10b981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a; letter-spacing: -0.01em;">Top 5 Plats</div>
        <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.05rem;">Classement par {classement_key}</div>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.03) 0%, rgba(16, 185, 129, 0.01) 100%); border: 1px solid rgba(16, 185, 129, 0.15); border-radius: 8px; padding: 0.5rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
    st.dataframe(top5, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Flop 5
    st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 0.8rem; background: linear-gradient(to right, #fafafa 0%, #ffffff 100%); border-left: 2.5px solid #f43f5e; border-radius: 6px; margin: 1.2rem 0 0.8rem;">
    <div style="display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: rgba(244, 63, 94, 0.08); border-radius: 5px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 9v2M12 15h.01" stroke="#f43f5e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="#f43f5e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a; letter-spacing: -0.01em;">Flop 5 Plats</div>
        <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.05rem;">À optimiser en priorité</div>
    </div>
</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="background: linear-gradient(135deg, rgba(244, 63, 94, 0.03) 0%, rgba(244, 63, 94, 0.01) 100%); border: 1px solid rgba(244, 63, 94, 0.15); border-radius: 8px; padding: 0.5rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
    st.dataframe(flop5, use_container_width=True, hide_index=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    _render_back_to_menu_button()


def _render_ingredients_critiques(plats_analyzes, ingredients):
    """Analyse et affiche les ingrédients critiques"""
    st.markdown('<div id="section-ingredients"></div>', unsafe_allow_html=True)
    st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 0.8rem; background: linear-gradient(to right, #fafafa 0%, #ffffff 100%); border-left: 2.5px solid #D92332; border-radius: 6px; margin: 1.5rem 0 0.8rem;">
    <div style="display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: rgba(217, 35, 50, 0.08); border-radius: 5px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 7L2 10l3 3M19 7l3 3-3 3" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 5l-7 14h14L12 5z" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a; letter-spacing: -0.01em;">Ingrédients critiques</div>
        <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.05rem;">Impact sur vos coûts</div>
    </div>  
</div>
    """, unsafe_allow_html=True)
    
    def analyser_ingredients_critiques(plats_analyses):
        """Analyse les ingrédients qui pèsent le plus sur les coûts globaux"""
        tous_ingredients = []
        
        for plat_nom in plats_analyses:
            ingr_plat = ingredients[ingredients['plat'].str.lower() == plat_nom.lower()].copy()
            
            if not ingr_plat.empty:
                ingr_plat = calculer_cout(ingr_plat)
                
                cout_pate = get_dough_cost(plat_nom)
                if cout_pate > 0:
                    ingr_plat = pd.concat([
                        ingr_plat,
                        pd.DataFrame([{
                            "ingredient": "Pâte à pizza",
                            "plat": plat_nom,
                            "quantite_g": 250,
                            "prix_kg": cout_pate * 4,
                            "Coût (€)": cout_pate
                        }])
                    ], ignore_index=True)
                
                if plat_nom.lower() == "panini pizz":
                    bases = ingr_plat[ingr_plat["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
                    mean_base = bases["Coût (€)"].mean() if not bases.empty else 0.0
                    avg_add = 0.246
                    
                    ingr_plat = pd.DataFrame([
                        {"ingredient": "Base (moyenne)", "plat": plat_nom, "quantite_g": 50, "prix_kg": mean_base * 20, "Coût (€)": mean_base},
                        {"ingredient": "Suppléments (moyenne)", "plat": plat_nom, "quantite_g": 100, "prix_kg": avg_add * 10, "Coût (€)": avg_add * 2},
                        {"ingredient": "Mozzarella", "plat": plat_nom, "quantite_g": 40, "prix_kg": 5.85, "Coût (€)": 0.234},
                        {"ingredient": "Pâte à panini", "plat": plat_nom, "quantite_g": 120, "prix_kg": 1.0, "Coût (€)": 0.12}
                    ])
                
                ingr_plat["plat_origine"] = plat_nom
                tous_ingredients.append(ingr_plat)
        
        if not tous_ingredients:
            return pd.DataFrame()
        
        df_ingredients = pd.concat(tous_ingredients, ignore_index=True)
        
        analyse_ingredients = df_ingredients.groupby("ingredient").agg({
            "Coût (€)": ["sum", "count", "mean"],
            "quantite_g": "sum",
            "prix_kg": "mean",
            "plat_origine": lambda x: list(set(x))
        }).round(3)
        
        analyse_ingredients.columns = [
            "Coût Total (€)", "Nb Plats", "Coût Moyen (€)", 
            "Quantité Totale (g)", "Prix Moyen (€/kg)", "Plats Concernés"
        ]
        
        cout_total_global = analyse_ingredients["Coût Total (€)"].sum()
        analyse_ingredients["% du Coût Total"] = (
            analyse_ingredients["Coût Total (€)"] / cout_total_global * 100
        ).round(1)
        
        analyse_ingredients = analyse_ingredients.sort_values("Coût Total (€)", ascending=False)
        
        return analyse_ingredients.reset_index()
    
    ingredients_critiques = analyser_ingredients_critiques(plats_analyzes)
    
    if not ingredients_critiques.empty:
        top_ingredients = ingredients_critiques.head(5)
        
        st.markdown("""
        <style>
        .ingredient-card {
            background: #fafafa;
            border-left: 3px solid #D92332;
            border-radius: 4px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.75rem;
        }
        .ingredient-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .ingredient-name {
            font-size: 0.95rem;
            font-weight: 600;
            color: #111827;
            margin: 0;
        }
        .ingredient-details {
            font-size: 0.8rem;
            color: #6b7280;
            margin: 0.35rem 0;
        }
        .ingredient-impact {
            font-size: 1.1rem;
            font-weight: 700;
            color: #D92332;
        }
        .ingredient-action {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            padding: 0.5rem 0.75rem;
            margin-top: 0.5rem;
            font-size: 0.8rem;
            color: #374151;
            line-height: 1.4;
        }
        .action-label {
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.2rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        for idx, (_, ing) in enumerate(top_ingredients.iterrows(), 1):
            nom = ing["ingredient"]
            prix_kg = ing["Prix Moyen (€/kg)"]
            nb_plats = int(ing["Nb Plats"])
            cout_total = ing["Coût Total (€)"]
            impact = ing["% du Coût Total"]
            cout_par_plat = cout_total / nb_plats
            
            if prix_kg > 15:
                action_titre = "Prix élevé"
                action_texte = f"À {prix_kg:.2f}€/kg, négociez avec votre fournisseur ou cherchez une alternative"
            elif nb_plats > 20:
                action_titre = "Très utilisé"
                action_texte = f"Présent dans {nb_plats} plats, réduire la quantité aura un fort impact"
            else:
                action_titre = "Optimisable"
                action_texte = "Réduisez de 10% ou testez un achat groupé"
            
            st.markdown(f"""
            <div class="ingredient-card">
                <div class="ingredient-header">
                    <div style="flex: 1;">
                        <div class="ingredient-name">{idx}. {nom}</div>
                        <div class="ingredient-details">{prix_kg:.2f}€/kg • {nb_plats} plats • {cout_par_plat:.2f}€/plat</div>
                    </div>
                    <div class="ingredient-impact">{impact:.1f}%</div>
                </div>
                <div class="ingredient-action">
                    <div class="action-label">{action_titre}</div>
                    <div>{action_texte}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: white; border: 1px solid #e5e7eb; border-radius: 4px; padding: 0.75rem 1rem; margin-top: 0.75rem; font-size: 0.85rem; color: #374151;">
            💡 <strong>Conseil :</strong> Passez à <strong>Modifier un plat</strong> pour simuler des réductions de quantité et voir l'impact en temps réel
        </div>
        """, unsafe_allow_html=True)
        
        _render_back_to_menu_button()
    else:
        st.warning("Aucune donnée d'ingrédients disponible pour l'analyse.")


def _render_back_to_menu_button():
    """Affiche le bouton retour au menu"""
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0 2rem; padding-top: 0.5rem;">
        <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
            <span class="back-to-top-line"></span>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </a>
    </div>
    <style>
    .back-to-top {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.85);
        border-radius: 8px;
        color: #94a3b8;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        border: none;
        cursor: pointer;
        text-decoration: none;
        position: relative;
        backdrop-filter: blur(4px);
        transform-origin: center;
    }
    .back-to-top-line {
        position: absolute;
        top: -6px;
        width: 10px;
        height: 2px;
        background: #D92332;
        border-radius: 4px;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        opacity: 0;
    }
    .back-to-top:hover {
        background: rgba(255, 255, 255, 0.95);
        color: #D92332;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 16px rgba(217, 35, 50, 0.12);
    }
    .back-to-top:hover .back-to-top-line {
        width: 20px;
        opacity: 1;
    }
    .back-to-top svg {
        width: 18px;
        height: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
