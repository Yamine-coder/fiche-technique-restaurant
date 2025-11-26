"""
Vue d'ensemble - Grille et liste de tous les plats avec métriques clés
"""
import streamlit as st
import pandas as pd
import html
from urllib.parse import quote

from modules.data.constants import TVA_VENTE, prix_vente_dict
from modules.business.cost_calculator import calculer_cout, get_dough_cost
from modules.utils.image_helpers import get_plat_image_path, get_image_data_uri
from modules.components.chatbot import render_floating_chatbot


def render_overview_view(recettes, ingredients, objectif_marge):
    """
    Affiche la vue d'ensemble avec grille ou liste des plats.
    
    Args:
        recettes: DataFrame des recettes
        ingredients: DataFrame des ingrédients
        objectif_marge: Objectif de marge en pourcentage
    """
    # Initialiser le mode de vue
    if "overview_view_mode" not in st.session_state:
        st.session_state["overview_view_mode"] = "grille"
    
    current_mode = st.session_state["overview_view_mode"]
    
    # CSS pour créer un header unifié avec le bouton intégré à droite
    st.markdown(
        """
        <style>
        /* Cibler le conteneur de colonnes et le styler comme un header unifié */
        div[data-testid="stHorizontalBlock"]:has(.vue-ensemble-left) {
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
        
        /* Retirer les paddings des colonnes internes */
        div[data-testid="stHorizontalBlock"]:has(.vue-ensemble-left) > div {
            padding: 0 !important;
        }
        
        /* Contenu gauche avec icône et texte */
        .vue-ensemble-left {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .vue-ensemble-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background: rgba(217, 35, 50, 0.08);
            border-radius: 6px;
            flex-shrink: 0;
        }
        
        .vue-ensemble-icon svg {
            width: 18px;
            height: 18px;
        }
        
        .vue-ensemble-text {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .vue-ensemble-title {
            font-weight: 600;
            color: #1e293b;
            font-size: 1rem;
            letter-spacing: -0.01em;
            margin: 0;
            line-height: 1.3;
        }
        
        .vue-ensemble-subtitle {
            font-size: 0.8rem;
            color: #64748b;
            font-weight: 400;
            margin: 0.15rem 0 0;
            line-height: 1.25;
        }

        
        /* Bouton à droite - compact et aligné */
        div[data-testid="stHorizontalBlock"]:has(.vue-ensemble-left) button[kind="secondary"] {
            min-width: 90px !important;
            padding: 0.5rem 0.8rem !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            white-space: nowrap !important;
            height: auto !important;
        }
        
        /* Styles pour les simulateurs d'aide à la décision */
        .simulator-warning {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 1.5px solid #fbbf24;
            border-radius: 10px;
            padding: 0.85rem 1rem;
            margin: 0 0 1.2rem 0;
            font-size: 0.88rem;
            color: #78350f;
            display: flex;
            align-items: center;
            gap: 0.7rem;
            box-shadow: 0 2px 8px rgba(251, 191, 36, 0.15);
        }
        
        .simulator-warning svg {
            flex-shrink: 0;
        }
        
        .simulator-section {
            background: linear-gradient(to bottom, #ffffff 0%, #f9fafb 100%);
            border: 1.5px solid #e5e7eb;
            border-radius: 12px;
            padding: 1.3rem;
            margin: 0 0 1.2rem 0;
            box-shadow: 0 2px 12px rgba(15, 23, 42, 0.05);
        }
        
        .simulator-header {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 1.1rem;
            padding-bottom: 0.9rem;
            border-bottom: 1.5px solid #e5e7eb;
        }
        
        .simulator-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, #D92332 0%, #b91c28 100%);
            border-radius: 9px;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(217, 35, 50, 0.25);
        }
        
        .simulator-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: #0f172a;
            flex: 1;
            letter-spacing: -0.01em;
        }
        
        .simulator-result {
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border: 1.5px solid #86efac;
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1.2rem 0;
            box-shadow: 0 2px 10px rgba(16, 185, 129, 0.12);
        }
        
        .simulator-result-value {
            font-size: 2rem;
            font-weight: 700;
            color: #047857;
            margin: 0.4rem 0;
            letter-spacing: -0.02em;
        }
        
        .simulator-result-label {
            font-size: 0.88rem;
            color: #065f46;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        
        .simulator-breakdown {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.9rem;
            margin-top: 1rem;
        }
        
        .simulator-breakdown-item {
            background: white;
            border: 1.5px solid #e5e7eb;
            border-radius: 10px;
            padding: 0.8rem;
            text-align: center;
            transition: all 0.2s ease;
        }
        
        .simulator-breakdown-item:hover {
            border-color: #10b981;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.15);
        }
        
        .simulator-breakdown-value {
            font-size: 1.25rem;
            font-weight: 600;
            color: #0f172a;
            letter-spacing: -0.01em;
        }
        
        .simulator-breakdown-label {
            font-size: 0.78rem;
            color: #64748b;
            margin-top: 0.3rem;
            font-weight: 500;
        }
        
        .simulator-reference {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1.5px dashed #cbd5e1;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1.2rem;
            font-size: 0.88rem;
            color: #475569;
            line-height: 1.6;
        }
        
        .simulator-reference strong {
            color: #0f172a;
            font-weight: 600;
        }
        
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Créer deux colonnes : 85% pour le titre, 15% pour le bouton
    col_left, col_right = st.columns([0.85, 0.15])
    
    with col_left:
        st.markdown(
            """
            <div class="vue-ensemble-left">
                <div class="vue-ensemble-icon">
                    <svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 3h5v5H3zM11 3h5v5h-5zM3 11h5v5H3zM11 11h5v5h-5z" 
                              stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div class="vue-ensemble-text">
                    <div class="vue-ensemble-title">Vue d'ensemble</div>
                    <div class="vue-ensemble-subtitle">Tous vos plats en un coup d'œil avec leurs métriques clés</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col_right:
        # Bouton de basculement
        if current_mode == "grille":
            if st.button("☰ Liste", key="overview_toggle_list", type="secondary", use_container_width=True):
                st.session_state["overview_view_mode"] = "liste"
                st.rerun()
        else:
            if st.button("⊞ Grille", key="overview_toggle_grid", type="secondary", use_container_width=True):
                st.session_state["overview_view_mode"] = "grille"
                st.rerun()
    
    # Section filtres minimaliste
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div class="sidebar-section-label">Pilotage des filtres</div>
        <div class="sidebar-section-subtitle">Affinez la grille selon vos besoins</div>
        """,
        unsafe_allow_html=True,
    )

    categories_dispo = ["Toutes"] + sorted(list(recettes["categorie"].unique()))
    categorie_filtre = st.sidebar.selectbox("Catégorie", categories_dispo, key="overview_cat_filter")

    tri_option = st.sidebar.selectbox(
        "Trier par",
        [
            "Nom (A-Z)",
            "Marge (↓)",
            "Marge (↑)",
            "Coût matière (↓)",
            "Coût matière (↑)",
            "Prix de vente (↓)",
            "Prix de vente (↑)",
        ],
        key="overview_sort",
    )

    search_term = st.sidebar.text_input("Recherche rapide", "", key="overview_search").strip()

    slider_container = st.sidebar.container()
    slider_label_placeholder = slider_container.empty()
    marge_min = slider_container.slider(
        "Marge minimale (%)",
        0,
        100,
        0,
        5,
        key="overview_margin_min",
        label_visibility="collapsed",
    )
    slider_label_placeholder.markdown(
        f"""
        <div class="sidebar-slider-label">
            <span>Marge minimale</span>
            <span class="sidebar-slider-value">{marge_min}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <div class="sidebar-hint">
            Astuce : combinez tri et recherche pour isoler vos best-sellers ou les plats à optimiser.
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_filter_chips = []
    if categorie_filtre != "Toutes":
        active_filter_chips.append(
            f'<span class="filter-chip"><span class="filter-chip-label">Catégorie</span>{html.escape(categorie_filtre.title())}</span>'
        )
    if search_term:
        active_filter_chips.append(
            f'<span class="filter-chip"><span class="filter-chip-label">Recherche</span>{html.escape(search_term)}</span>'
        )
    if tri_option != "Nom (A-Z)":
        active_filter_chips.append(
            f'<span class="filter-chip"><span class="filter-chip-label">Tri</span>{html.escape(tri_option)}</span>'
        )
    if marge_min > 0:
        active_filter_chips.append(
            f'<span class="filter-chip"><span class="filter-chip-label">Marge min.</span>{marge_min}%</span>'
        )

    filtered_recettes = recettes.copy()
    if categorie_filtre != "Toutes":
        filtered_recettes = filtered_recettes[filtered_recettes["categorie"] == categorie_filtre]
    if search_term:
        filtered_recettes = filtered_recettes[filtered_recettes["plat"].str.contains(search_term, case=False, regex=False)]

    plats_a_afficher = filtered_recettes["plat"].unique()

    # Calculer les métriques pour chaque plat
    plats_data = []
    for plat_nom in plats_a_afficher:
        plat_info = recettes[recettes['plat'] == plat_nom].iloc[0]
        categorie = plat_info['categorie']

        ingr_plat = ingredients[ingredients['plat'].str.lower() == plat_nom.lower()].copy()
        ingr_plat = calculer_cout(ingr_plat)

        cout_matiere = ingr_plat["Coût (€)"].sum() + get_dough_cost(plat_nom)

        salades_avec_pain = [
            "salade burrata di parma",
            "salade burrata di salmone",
            "salade césar",
            "salade chèvre",
            "salade végétarienne"
        ]
        if plat_nom.lower() in salades_avec_pain:
            cout_matiere += 0.21

        prix_ttc = prix_vente_dict.get(plat_nom, 0)
        prix_ht = prix_ttc / (1 + TVA_VENTE)

        if prix_ht > 0:
            marge_pct = ((prix_ht - cout_matiere) / prix_ht) * 100
        else:
            marge_pct = 0

        plats_data.append({
            "nom": plat_nom,
            "categorie": categorie,
            "cout_matiere": cout_matiere,
            "prix_ht": prix_ht,
            "prix_ttc": prix_ttc,
            "marge_pct": marge_pct
        })

    df_plats = pd.DataFrame(plats_data)
    
    if not df_plats.empty:
        df_plats = df_plats[df_plats["marge_pct"] >= marge_min]

        if tri_option == "Nom (A-Z)":
            df_plats = df_plats.sort_values("nom")
        elif tri_option == "Marge (↓)":
            df_plats = df_plats.sort_values("marge_pct", ascending=False)
        elif tri_option == "Marge (↑)":
            df_plats = df_plats.sort_values("marge_pct")
        elif tri_option == "Coût matière (↓)":
            df_plats = df_plats.sort_values("cout_matiere", ascending=False)
        elif tri_option == "Coût matière (↑)":
            df_plats = df_plats.sort_values("cout_matiere")
        elif tri_option == "Prix de vente (↓)":
            df_plats = df_plats.sort_values("prix_ttc", ascending=False)
        elif tri_option == "Prix de vente (↑)":
            df_plats = df_plats.sort_values("prix_ttc")

    st.markdown(f"""
    <div style="
        color: #64748b;
        font-size: 0.9rem;
        margin: 0.55rem 0 0.6rem;
        padding-left: 0.4rem;
        font-weight: 500;
    ">
        {df_plats.shape[0]} plat{'s' if df_plats.shape[0] > 1 else ''} correspondant{'s' if df_plats.shape[0] > 1 else ''} à vos filtres
    </div>
    """, unsafe_allow_html=True)

    if active_filter_chips:
        st.markdown(
            f"""
            <div class="filter-summary">
                <div class="filter-summary-label">Filtres actifs</div>
                <div class="filter-chip-group">{''.join(active_filter_chips)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    objectif_marge_actuel = st.session_state.get("objectif_marge", 70)

    if df_plats.empty:
        st.info("Aucun plat ne correspond aux filtres actuels.")
    else:
        df_plats = df_plats.copy()
        df_plats["marge_euros"] = (df_plats["prix_ht"] - df_plats["cout_matiere"]).round(2)
        df_plats["taux_cout"] = df_plats.apply(
            lambda row: (row["cout_matiere"] / row["prix_ht"] * 100) if row["prix_ht"] > 0 else 0,
            axis=1,
        ).round(1)

        if "overview_view_mode" not in st.session_state:
            st.session_state["overview_view_mode"] = "grille"

        if st.session_state["overview_view_mode"] == "liste":
            vue_liste = df_plats[[
                "nom",
                "categorie",
                "prix_ttc",
                "prix_ht",
                "cout_matiere",
                "marge_pct",
                "marge_euros",
                "taux_cout",
            ]].rename(columns={
                "nom": "Plat",
                "categorie": "Catégorie",
                "prix_ttc": "Prix TTC (€)",
                "prix_ht": "Prix HT (€)",
                "cout_matiere": "Coût matière (€)",
                "marge_pct": "Marge (%)",
                "marge_euros": "Marge (€)",
                "taux_cout": "Taux coût (%)",
            }).copy()

            vue_liste["Plat"] = vue_liste["Plat"].str.title()
            vue_liste["Catégorie"] = vue_liste["Catégorie"].str.title()

            st.dataframe(
                vue_liste,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Prix TTC (€)": st.column_config.NumberColumn(format="%.2f€"),
                    "Prix HT (€)": st.column_config.NumberColumn(format="%.2f€"),
                    "Coût matière (€)": st.column_config.NumberColumn(format="%.2f€"),
                    "Marge (€)": st.column_config.NumberColumn(format="%.2f€"),
                    "Marge (%)": st.column_config.ProgressColumn(
                        "Marge (%)",
                        format="%.1f%%",
                        min_value=0,
                        max_value=100,
                    ),
                    "Taux coût (%)": st.column_config.NumberColumn(format="%.1f%%"),
                },
            )
        else:
            plats_data = df_plats.to_dict("records")

            cols_per_row = 4 if len(plats_data) >= 4 else (3 if len(plats_data) >= 3 else (2 if len(plats_data) > 1 else 1))
            for i in range(0, len(plats_data), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(plats_data):
                        plat_d = plats_data[i + j]
                        plat_nom_affichage = plat_d["nom"]

                        if plat_d["marge_pct"] >= objectif_marge_actuel + 5:
                            marge_color = "#10b981"
                            status_text = "✓ Rentable"
                            status_bg = "rgba(34,197,94,0.95)"
                        elif plat_d["marge_pct"] >= objectif_marge_actuel:
                            marge_color = "#f59e0b"
                            status_text = "À surveiller"
                            status_bg = "rgba(245,158,11,0.95)"
                        else:
                            marge_color = "#ef4444"
                            status_text = "À corriger"
                            status_bg = "rgba(239,68,68,0.95)"

                        progress_width = max(0, min(100, int(round(plat_d["marge_pct"]))))

                        image_path = get_plat_image_path(plat_d["nom"])
                        image_data_uri = get_image_data_uri(image_path)
                        image_html = ""
                        if image_data_uri:
                            image_html = (
                                f'<img src="{image_data_uri}" alt="{plat_nom_affichage}" '
                                'style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;" />'
                            )
                        target_url = f"?mode=analyse&plat={quote(plat_nom_affichage)}"

                        idx = i + j
                        
                        with cols[j]:
                            # Afficher la card avec l'icône intégrée
                            card_lines = [
                                '<div style="background: white; border: 1px solid #e2e8f0; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 16px rgba(15, 23, 42, 0.06); transition: transform 0.2s ease, box-shadow 0.2s ease; height: 100%; display: flex; flex-direction: column; position: relative;">',
                                f'    <div style="position: relative;">',
                                f'        <a href="{target_url}" title="Voir la fiche technique" target="_self" class="plat-card-link" style="position: relative; display: block; width: 100%; padding-top: 62%; background: #f8fafc; overflow: hidden; text-decoration: none; cursor: pointer;">',
                                f'            {image_html}',
                                '            <div class="overlay-gradient" style="position: absolute; inset: 0; background: rgba(15, 23, 42, 0.05); transition: all 0.3s ease;"></div>',
                                f'            <span style="position: absolute; top: 0.6rem; left: 0.6rem; background: {status_bg}; color: white; font-size: 0.72rem; font-weight: 600; padding: 0.2rem 0.55rem; border-radius: 999px; box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);">{status_text}</span>',
                                f'            <span style="position: absolute; top: 0.6rem; right: 0.6rem; background: rgba(255, 255, 255, 0.9); color: {marge_color}; font-size: 0.78rem; font-weight: 700; padding: 0.28rem 0.65rem; border-radius: 999px; box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25); border: 1px solid rgba(255, 255, 255, 0.85); backdrop-filter: blur(6px);">{plat_d["marge_pct"]:.1f}%</span>',
                                f'            <span style="position: absolute; bottom: 0.6rem; left: 0.6rem; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; padding: 0.25rem 0.55rem; border-radius: 999px; background: rgba(255, 255, 255, 0.92); color: #475569; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.18);">{plat_d["categorie"]}</span>',
                                '            <div class="fiche-technique-center" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 0; transition: all 0.3s ease;">',
                                '                <div style="font-size: 0.8rem; font-weight: 600; color: white; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);">',
                                '                    Voir la fiche →',
                                '                </div>',
                                '            </div>',
                                '        </a>',
                                f'    </div>',
                                '    <div style="padding: 0.9rem 1rem 1rem; display: flex; flex-direction: column; gap: 0.75rem; flex: 1;">',
                                f'        <div style="font-weight: 600; font-size: 1.02rem; color: #0f172a; line-height: 1.25;">{plat_d["nom"]}</div>',
                                '        <div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.6rem;">',
                                '            <div style="background: #f8fafc; border-radius: 10px; padding: 0.55rem 0.65rem;">',
                                '                <div style="font-size: 0.72rem; color: #64748b;">Coût matière</div>',
                                f'                <div style="font-size: 0.98rem; font-weight: 600; color: #0f172a;">{plat_d["cout_matiere"]:.2f}€</div>',
                                '            </div>',
                                '            <div style="background: #f8fafc; border-radius: 10px; padding: 0.55rem 0.65rem;">',
                                '                <div style="font-size: 0.72rem; color: #64748b;">Prix carte TTC</div>',
                                f'                <div style="font-size: 0.98rem; font-weight: 600; color: #0f172a;">{plat_d["prix_ttc"]:.2f}€</div>',
                                '            </div>',
                                '        </div>',
                                '        <div style="margin-top: auto;">',
                                f'            <div style="font-size: 0.72rem; color: #64748b; margin-bottom: 0.25rem;">Progression vs objectif {objectif_marge_actuel:.0f}%</div>',
                                '            <div style="position: relative; height: 6px; background: #e2e8f0; border-radius: 999px; overflow: hidden;">',
                                f'                <div style="width: {progress_width}%; background: {marge_color}; height: 100%;"></div>',
                                '            </div>',
                        '        </div>',
                        '    </div>',
                        '    <!-- 🆕 Badge ventes -->',
                        ''
                            ]
                            
                            # 🆕 Ajouter badge de ventes si disponible
                            if 'quantite_vendue' in plat_d and plat_d.get('quantite_vendue', 0) > 0:
                                ventes_html = f'''
                                <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border-radius: 10px; padding: 0.6rem 0.7rem; border: 1.5px solid #86efac; margin: 0 1rem 0.8rem;">
                                    <div style="font-size: 0.72rem; color: #065f46; font-weight: 600; margin-bottom: 0.25rem;">🔥 Performance</div>
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <div>
                                            <div style="font-size: 0.98rem; font-weight: 700; color: #047857;">{int(plat_d['quantite_vendue'])} vendus</div>
                                        </div>
                                        <div style="text-align: right;">
                                            <div style="font-size: 0.95rem; font-weight: 600; color: #059669;">{plat_d['ca_total']:.0f}€</div>
                                            <div style="font-size: 0.7rem; color: #10b981;">CA généré</div>
                                        </div>
                                    </div>
                                </div>
                                '''
                                card_lines.append(ventes_html)
                            
                            card_lines.extend([
                        '</div>',
                        '<style>',
                        '.plat-card-link:hover .fiche-technique-center {',
                        '    opacity: 1 !important;',
                        '}',
                        '.plat-card-link:hover .overlay-gradient {',
                        '    background: rgba(15, 23, 42, 0.5) !important;',
                        '}',
                        '</style>'
                            ])
                            html_card = "\n".join(card_lines)
                            st.markdown(html_card, unsafe_allow_html=True)    # Coach guidé - Décisions express
    # Seul assistant conservé : bouton qui ouvre le dialog guidé
    render_floating_chatbot(df_plats, ingredients, objectif_marge_actuel)
