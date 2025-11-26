"""
Analyse d'un plat - Vue détaillée avec composition et métriques
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from modules.data.constants import TVA_VENTE, prix_vente_dict, images_plats
from modules.business.cost_calculator import calculer_cout, get_dough_cost
from modules.components import render_view_header, afficher_image_plat
from modules.data.sales_data import get_ventes_produit, get_stats_globales
from modules.data.sales_insights import get_product_sales_insight, format_insight_message


def render_dish_analysis_view(recettes, ingredients, objectif_marge):
    """
    Affiche l'analyse détaillée d'un plat avec composition et métriques.
    
    Args:
        recettes: DataFrame des recettes
        ingredients: DataFrame des ingrédients
        objectif_marge: Objectif de marge en pourcentage
    """
    # Séparateur minimaliste
    st.sidebar.markdown("""
    <div style="
        height: 1px;
        background: #f1f5f9;
        margin: 0.5rem 0 0.4rem;
    "></div>
    """, unsafe_allow_html=True)

    objectif_marge_actuel = st.session_state.get("objectif_marge", 70)
    
    # Coefficient d'ajustement minimaliste
    st.sidebar.markdown(
        """
        <div class="sidebar-section-label">Coût généreux</div>
        <div class="sidebar-section-subtitle">Majorez virtuellement vos ingrédients pour simuler un service plus généreux</div>
        """,
        unsafe_allow_html=True,
    )

    coeff_container = st.sidebar.container()
    coeff_label_placeholder = coeff_container.empty()
    coeff_surplus = coeff_container.slider(
        "Coefficient généreux",
        1.0,
        2.0,
        1.3,
        0.05,
        help="Majore le coût des ingrédients pour obtenir le coût généreux (1.3 = +30%)",
        label_visibility="collapsed",
        key="analyse_coeff_surplus",
    )
    coeff_label_placeholder.markdown(
        f"""
        <div class="sidebar-slider-label">
            <span>Coefficient généreux</span>
            <span class="sidebar-slider-value">x{coeff_surplus:.2f} · +{(coeff_surplus - 1)*100:.0f}%</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Séparateur
    st.sidebar.markdown("""
    <div style="
        height: 1px;
        background: #f1f5f9;
        margin: 0.4rem 0;
    "></div>
    """, unsafe_allow_html=True)
    
    # Sélection du plat minimaliste
    st.sidebar.markdown(
        """
        <div class="sidebar-section-label">Sélection</div>
        <div class="sidebar-section-subtitle">Choisissez la catégorie et le plat à analyser</div>
        """,
        unsafe_allow_html=True,
    )
    
    # Sélection de la catégorie
    categorie_choisie = st.sidebar.selectbox(
        "Catégorie", 
        ["Tout"] + sorted(list(recettes["categorie"].unique())), 
        key="categorie_analyse"
    )

    # Liste des plats selon la catégorie
    if categorie_choisie == "Tout":
        plats_dispo = recettes["plat"].unique()
    else:
        plats_dispo = recettes[recettes["categorie"] == categorie_choisie]["plat"].unique()

    # Sélection du plat
    plat = st.sidebar.selectbox(
        "Plat", 
        plats_dispo, 
        key="plat_unique",
        help="Sélectionnez le plat que vous souhaitez analyser"
    )

    current_mode_values = st.query_params.get("mode")
    current_plat_values = st.query_params.get("plat")
    current_mode = (
        current_mode_values[0] if isinstance(current_mode_values, list) and current_mode_values else
        (str(current_mode_values) if current_mode_values else "")
    )
    current_plat = (
        current_plat_values[0] if isinstance(current_plat_values, list) and current_plat_values else
        (str(current_plat_values) if current_plat_values else "")
    )

    if current_mode != "analyse" or current_plat != plat:
        st.query_params["mode"] = "analyse"
        st.query_params["plat"] = plat
    
    # Options simplifiées - Section supprimée car coefficient d'ajustement déplacé en haut
    
    # ️ Récupération de la catégorie du plat pour l'affichage
    plat_info = recettes[recettes['plat'] == plat].iloc[0] if len(recettes[recettes['plat'] == plat]) > 0 else None
    categorie_plat = plat_info['categorie'] if plat_info is not None else "Non définie"
    
    # 🎯 Gérer la portion si catégorie = "Pâtes" (déplacé dans la sidebar)
    portion_faim = "Petite Faim"  # Par défaut
    if categorie_plat.lower() == "pâtes":
        # Séparateur pour section pâtes
        st.sidebar.markdown("""
        <div style="
            height: 1px;
            background: rgba(49, 51, 63, 0.1);
            margin: 0.4rem 0 0.4rem;
        "></div>
        """, unsafe_allow_html=True)
        
        # Section Options Spécifiques Pâtes
        with st.sidebar.container():
            # On crée un div avec un ID unique pour cibler uniquement ce radio button
            st.markdown('<div id="portion_faim_container"></div>', unsafe_allow_html=True)
            portion_container = st.container()
            
            # Style CSS ciblant spécifiquement notre container
            option_style = """
            <style>
            /* Styles pour le conteneur des portions */
            #portion_faim_container + div div[data-testid="stRadio"] > div {
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }
            #portion_faim_container + div div[data-testid="stRadio"] > div:first-child {
                font-size: 0.85rem;
            }
            #portion_faim_container + div div[data-testid="stRadio"] > div > label {
                cursor: pointer;
                background: white;
                border: 1px solid #e2e8f0;
                padding: 0.3rem 0.5rem;
                border-radius: 4px;
                font-size: 0.8rem;
                transition: all 0.2s;
                color: #333;
            }
            #portion_faim_container + div div[data-testid="stRadio"] > div > label:hover {
                border-color: #D92332;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            </style>
            """
            st.markdown(option_style, unsafe_allow_html=True)
            
            # Placer le radio button dans le container spécifique
            with portion_container:
                portion_faim = st.radio(
                    "Taille de portion 🍝",
                    options=["Petite Faim", "Grosse Faim (+3€)"],
                    horizontal=True,
                    key="portion_faim_radio",
                    help="La portion 'Grosse Faim' augmente la quantité de pâtes (+40-52%) et le prix (+3€)"
                )
                
                # Indication discrète pour la portion sélectionnée
                if portion_faim.startswith("Grosse"):
                    st.markdown("<div style='font-size:0.7rem; color:#6b7280; margin-top:-0.2rem;'>Portion XL : +40-52% de pâtes selon le plat</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='font-size:0.7rem; color:#6b7280; margin-top:-0.2rem;'>Portion standard</div>", unsafe_allow_html=True)
    
    render_view_header(
        icon_svg="""<svg width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="9" cy="9" r="7" stroke="#D92332" stroke-width="1.5"/>
            <path d="M6 9h6M9 6v6" stroke="#D92332" stroke-width="1.5" stroke-linecap="round"/>
        </svg>""",
        title="Analyse d'un plat",
        subtitle="Visualisez la composition et les métriques détaillées du plat sélectionné",
    )
    
    # Message d'information TVA - Style personnalisé et compact
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fef2f2 0%, #fff5f5 100%);
        border: 1px solid #fecaca;
        border-left: 3px solid #D92332;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        margin: 0 0 0.75rem;
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
    
    # Interface du plat créative mais plus compacte
    st.markdown(f"""
    <div style="
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.5rem 0.9rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    ">
        <span style="
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: #1e293b;
            margin-right: 0.5rem;
        ">{plat}</span>
        <span style="
            background: rgba(217, 35, 50, 0.07);
            color: #D92332;
            font-size: 0.7rem;
            font-weight: 500;
            padding: 0.1rem 0.45rem;
            border-radius: 4px;
        ">{categorie_plat}</span>
    </div>
    """, unsafe_allow_html=True)

    # 📊 INSIGHT INTELLIGENT basé sur les ventes réelles Kezia
    try:
        sales_insights = get_product_sales_insight(plat)
        if sales_insights:
            insight_html = format_insight_message(plat, sales_insights)
            st.markdown(insight_html, unsafe_allow_html=True)
    except Exception as e:
        # Silencieux si pas de données disponibles
        pass

    # 1. Filtrer les ingrédients du plat sélectionné
    ingr_plat = ingredients[ingredients['plat'].str.lower() == plat.lower()].copy()


    # 2. 🔢 Quantités spécifiques pour chaque plat (Grosse Faim)
    quantites_grosse_faim = {
        "bolognaise": 330,
        "truffe": 330,
        "saumon": 350,
        "carbonara": 350,
        "fermière": 330,
        "3 fromages": 350,
        "napolitaine": 350,
        "sicilienne": 330,
        "arrabiata": 350,
        "arrabiata poulet": 330,
    }

 
    # 3. Adapter la quantité de pâtes si besoin
    if categorie_plat.lower() == "pâtes":
        plat_key = plat.lower().strip()
        mask_pate = ingr_plat["ingredient"].str.lower().str.contains("spaghetti|penné|pâtes")


        # Adapter la quantité de pâtes si besoin
        if portion_faim.startswith("Grosse"):
            if plat_key in quantites_grosse_faim and mask_pate.any():
                nouvelle_quantite = quantites_grosse_faim[plat_key]
                ingr_plat.loc[mask_pate, "quantite_g"] = nouvelle_quantite
               
        else:
            # Ne rien modifier : on garde les quantités de base (Petite Faim)
            pass


    # 4. Recalcul du coût matière avec les quantités à jour
    ingr_plat = calculer_cout(ingr_plat)


    # 5. Ajustement du prix de vente pour les pâtes en Grosse Faim
    prix_affiche = prix_vente_dict.get(plat, None)
    if categorie_plat.lower() == "pâtes" and portion_faim.startswith("Grosse"):
        prix_affiche += 3  # Ajoute 3€ pour Grosse Faim
   


    # Taux de TVA applicable
    taux_tva = TVA_VENTE

    # Conversion du prix TTC vers HT (tous les calculs en HT)
    prix_ht = prix_affiche / (1 + taux_tva) if prix_affiche else None
    prix_ttc = prix_affiche  # Sauvegarde pour affichage "Prix carte TTC"
    prix_affiche = prix_ht  # On travaille toujours en HT

   




    salades_avec_pain = [
    "salade burrata di parma",
    "salade burrata di salmone",
    "salade césar",
    "salade chèvre",
    "salade végétarienne"
]
    if plat.lower() in salades_avec_pain:
        ingr_plat = pd.concat([
        ingr_plat,
        pd.DataFrame([{
            "ingredient": "Pain aux herbes",
            "quantite_g": 0,
            "prix_kg": 0,
            "Coût (€)": 0.21,
            "ingredient_lower": "pain aux herbes"
        }])
    ], ignore_index=True)


    # 2. Coût matière initial + pâte
    cout_matiere = ingr_plat["Coût (€)"].sum() + get_dough_cost(plat)
    composition_finale = ingr_plat.copy()
   
    # 3. Ajouter la pâte à pizza si nécessaire
    pate_cost = get_dough_cost(plat)
    if pate_cost > 0:
        composition_finale = pd.concat([
            composition_finale,
            pd.DataFrame([{
                "ingredient": "Pâte à pizza",
                "quantite_g": 0,
                "prix_kg": 0,
                "Coût (€)": pate_cost,
                "ingredient_lower": "pâte à pizza"
            }])
        ], ignore_index=True)
   
    # 4. Traitement spécifique Panini Pizz
    if plat.lower() == "panini pizz":
        # Section panini avec séparateur simple
        st.sidebar.markdown("""
        <div style="height: 1px; background: rgba(49, 51, 63, 0.1); margin: 0.4rem 0;"></div>
        """, unsafe_allow_html=True)
        
        with st.sidebar.container():
            st.markdown("#### Options Panini")
            
            # Calcul des coûts
            cost_creme = ingr_plat.loc[ingr_plat["ingredient"].str.lower() == "crème", "Coût (€)"].sum()
            cost_sauce = ingr_plat.loc[ingr_plat["ingredient"].str.lower() == "sauce tomate", "Coût (€)"].sum()
            
            # Interface optimisée pour le panini
            st.markdown("""
            <style>
            /* Réduire l'espacement des widgets panini */
            div[data-testid="stRadio"] > div:first-child {
                margin-bottom: 0.2rem;
            }
            /* Réduire marge entre checkbox et label */
            div[data-testid="stCheckbox"] > label > div {
                margin-top: 0.1rem;
                margin-bottom: 0.1rem;
            }
            /* Réduire les marges des selectbox */
            div[data-testid="stSelectbox"] {
                margin-bottom: 0.3rem;
            }
            /* Réduire la taille des labels d'ingrédients */
            div[data-testid="stSelectbox"] > label > div {
                font-size: 0.85rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Titre compacte
            st.markdown('<div style="font-size:0.9rem; font-weight:500; margin-bottom:0.3rem; margin-top:-0.4rem;">Type de base:</div>', unsafe_allow_html=True)
            
            # Sélection de base simplifiée
            base_selection = st.radio(
                "Base", 
                ["Crème", "Sauce Tomate"], 
                index=0, 
                horizontal=True,
                key="base_panini"
            )
            
            # Option de personnalisation
            st.markdown('<div style="font-size:0.9rem; font-weight:500; margin-bottom:0.1rem; margin-top:0.3rem;">Options avancées:</div>', unsafe_allow_html=True)
            mode_avance = st.checkbox(
                "Personnaliser les ingrédients", 
                key="mode_avance",
                help="Permet de choisir les ingrédients spécifiques du panini"
            )
            
            # Calcul des ingrédients additionnels
            additional = ingr_plat[~ingr_plat["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
            avg_add = additional["Coût (€)"].mean() if not additional.empty else 0.0
            
            if mode_avance:
                # Préparation des données pour les sélecteurs
                already_included = ["crème", "sauce tomate"]
                additional_clean = additional.drop_duplicates(subset=["ingredient"])
                all_ingrs = list(additional_clean.loc[~additional_clean["ingredient"].str.lower().isin(already_included), "ingredient"].unique())
                all_ingrs.sort()
                
                # Ingrédients en disposition compacte
                st.markdown('<div style="font-size:0.9rem; font-weight:500; margin-top:0.4rem; margin-bottom:0.3rem;">Choix des ingrédients:</div>', unsafe_allow_html=True)
                
                slot1 = st.selectbox(
                    "Ingrédient #1", 
                    ["Aucun"] + all_ingrs, 
                    key="slot1"
                )
                
                slot2 = st.selectbox(
                    "Ingrédient #2", 
                    ["Aucun"] + all_ingrs, 
                    key="slot2"
                )
                
                # Astuce discrète
                st.markdown("<div style='font-size:0.7rem; color:#6b7280; margin-top:0.2rem'>💡 Vous pouvez choisir 2× le même ingrédient</div>", unsafe_allow_html=True)
                
                # Résumé visuel pour référence rapide
                st.markdown('<div style="margin-top:0.5rem; padding:0.5rem; background-color:#f8f9fa; border-radius:4px; font-size:0.8rem;">' +
                           f'<div style="font-weight:500;">Composition:</div>' +
                           f'<div>Base: <span style="color:#1E90FF">{base_selection}</span></div>' +
                           f'<div>Ingr. #1: <span style="color:#1E90FF">{slot1 if slot1 != "Aucun" else "-"}</span></div>' +
                           f'<div>Ingr. #2: <span style="color:#1E90FF">{slot2 if slot2 != "Aucun" else "-"}</span></div>' +
                           '</div>', unsafe_allow_html=True)
            
            # Définition du coût de base selon la sélection
            cost_base = cost_creme if base_selection == "Crème" else cost_sauce
            
            # Cette logique est maintenant intégrée dans la sidebar
            if base_selection == "Crème":
                composition_candidates = ingr_plat[ingr_plat["original_plat"].str.contains("base crème", case=False, na=False)].copy()
            else:
                composition_candidates = ingr_plat[ingr_plat["original_plat"].str.contains("base tomate", case=False, na=False)].copy()


            if not mode_avance:
                # Mode simple : utiliser la moyenne des ingrédients additionnels
                cout_panini = cost_base + 2 * avg_add
                df_fake_avg = pd.DataFrame()
                if not additional.empty:
                    row_avg = {
                        "ingredient": "Moyenne suppl",
                        "quantite_g": 0,
                        "prix_kg": 0,
                        "Coût (€)": avg_add,
                        "ingredient_lower": "moyenne suppl"
                    }
                    df_fake_avg = pd.DataFrame([row_avg, row_avg])
                if base_selection == "Crème":
                    df_base = composition_candidates[composition_candidates["ingredient"].str.lower() == "crème"]
                else:
                    df_base = composition_candidates[composition_candidates["ingredient"].str.lower() == "sauce tomate"]
                composition_finale = pd.concat([df_base, df_fake_avg], ignore_index=True)
            else:
                # Mode personnalisé - utiliser les sélections de la sidebar
                additional_clean = additional.drop_duplicates(subset=["ingredient"])
                
                # Calcul des coûts des ingrédients sélectionnés
                cost_slot1 = additional_clean.loc[additional_clean["ingredient"] == slot1, "Coût (€)"].iloc[0] if slot1 != "Aucun" else 0
                cost_slot2 = additional_clean.loc[additional_clean["ingredient"] == slot2, "Coût (€)"].iloc[0] if slot2 != "Aucun" else 0
                cout_panini = cost_base + cost_slot1 + cost_slot2

                # Construction de la composition finale personnalisée
                composition_finale = pd.DataFrame(columns=composition_candidates.columns)
                if base_selection == "Crème":
                    df_base = composition_candidates.loc[composition_candidates["ingredient"].str.lower() == "crème"].iloc[[0]]
                else:
                    df_base = composition_candidates.loc[composition_candidates["ingredient"].str.lower() == "sauce tomate"].iloc[[0]]
                composition_finale = pd.concat([composition_finale, df_base], ignore_index=True)
                
                # Ajout des ingrédients sélectionnés
                if slot1 != "Aucun":
                    ingr1 = additional_clean.loc[additional_clean["ingredient"] == slot1].copy()
                    if not ingr1.empty:
                        # Ajouter un identifiant unique si l'ingrédient est sélectionné deux fois
                        if slot1 == slot2:
                            ingr1["ingredient_id"] = f"{slot1}_1"
                        composition_finale = pd.concat([composition_finale, ingr1], ignore_index=True)
                
                if slot2 != "Aucun":
                    ingr2 = additional_clean.loc[additional_clean["ingredient"] == slot2].copy()
                    if not ingr2.empty:
                        # Ajouter un identifiant unique si l'ingrédient est sélectionné deux fois
                        if slot1 == slot2:
                            ingr2["ingredient_id"] = f"{slot2}_2"
                        composition_finale = pd.concat([composition_finale, ingr2], ignore_index=True)
            
            # Vérifier si la mozzarella est sélectionnée dans les ingrédients
            mozza_count = 0
            
            if mode_avance:
                mozza_count = (slot1 == "Mozzarella") + (slot2 == "Mozzarella")
            
            # Pour garantir que la mozzarella n'est pas présente en double quand elle est sélectionnée
            composition_finale = composition_finale[composition_finale["ingredient"].str.lower() != "mozzarella"]
            
            cost_mozza = 0.234  # Coût final pour 40g de mozzarella
            cost_pate_panini = 0.12  # Coût de la pâte à panini

        # Toujours ajouter une mozzarella de base, même si elle est aussi sélectionnée comme ingrédient
        row_mozza = pd.DataFrame([{
            "ingredient": "Mozzarella",
            "quantite_g": 40,
            "prix_kg": 5.85,
            "Coût (€)": cost_mozza,
            "ingredient_lower": "mozzarella"
        }])
        composition_finale = pd.concat([composition_finale, row_mozza], ignore_index=True)
        
        # Si la mozzarella a été sélectionnée comme ingrédient, on l'ajoute à nouveau (pour la double portion)
        if mozza_count > 0:
            for i in range(mozza_count):
                row_mozza_extra = pd.DataFrame([{
                    "ingredient": "Mozzarella (extra)",
                    "quantite_g": 40,
                    "prix_kg": 5.85,
                    "Coût (€)": cost_mozza,
                    "ingredient_lower": "mozzarella extra"
                }])
                composition_finale = pd.concat([composition_finale, row_mozza_extra], ignore_index=True)

        # Ajout de la pâte à panini
        row_pate = pd.DataFrame([{
            "ingredient": "Pâte à panini",
            "quantite_g": 0,
            "prix_kg": 0,
            "Coût (€)": cost_pate_panini,
            "ingredient_lower": "pâte à panini"
        }])

        # Ajouter la pâte à la composition finale
        composition_finale = pd.concat([composition_finale, row_pate], ignore_index=True)

        # S'assurer que le coût matière inclut tous les éléments
        cout_matiere = composition_finale["Coût (€)"].sum()
        
    # 5. Calcul du coût généreux (avec coefficient)
    # Calcul de la marge basée sur le coût généreux
    # 5. Calculs
    cout_genereux = cout_matiere * coeff_surplus
    marge_generuse = prix_affiche - cout_genereux
    taux_generuse = (marge_generuse / prix_affiche * 100) if prix_affiche and prix_affiche > 0 else None


    marge_brute = prix_affiche - cout_matiere if prix_affiche is not None else None
    taux_marge = (marge_brute / prix_affiche * 100) if marge_brute is not None and prix_affiche and prix_affiche > 0 else None


    # 6. Regroupement final
    my_agg = {
        "quantite_g": "sum",
        "prix_kg": "mean",
        "Coût (€)": "sum",
        "original_plat": "first"
    }
    grouped_finale = composition_finale.groupby("ingredient", as_index=False).agg(my_agg)
    ingredients_decision = grouped_finale[["ingredient", "Coût (€)"]].copy() if not grouped_finale.empty else grouped_finale


    # 7. Texte explicatif
    # Note: generer_detailed_breakdown temporairement désactivé
    # detailed_breakdown = generer_detailed_breakdown(plat, grouped_finale, cout_matiere, prix_affiche)


    # 🔥 Affichage des KPI fusionnés (format compact)
    st.markdown("<div style='margin-bottom:-0.5rem;'></div>", unsafe_allow_html=True)
    cols = st.columns(6)


    # Bloc 0 : Prix Vente HT
    with cols[0]:
        val = f"{prix_affiche:.2f}€" if prix_affiche else "N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Prix Vente HT</div>"
            f"</div>", unsafe_allow_html=True
        )

    # Bloc 1 : Prix carte TTC (référence)
    with cols[1]:
        val = f"{prix_ttc:.2f}€" if prix_ttc else "N/A"
        st.markdown(
            f"<div class='metric-card' style='background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);'>"
            f"<div class='metric-value' style='color: #64748b;'>{val}</div>"
            f"<div class='metric-title' style='color: #64748b;'>Prix carte TTC</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 2 : Coût Matière
    with cols[2]:
        val = f"{cout_matiere:.2f}€"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Coût Matière HT</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 3 : Coût Généreux + Marge Généreuse + Taux dans la même carte
    with cols[3]:
        val_gen = f"{cout_genereux:.2f}€"
        val_marge = f"{marge_generuse:.2f}€"
        val_taux = f"{taux_generuse:.1f}%" if taux_generuse is not None else "N/A"
        percent_text = f"(+{(coeff_surplus - 1)*100:.0f}%)"
       
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val_gen}</div>"
            f"<div style='font-size:12px; color: #999; line-height:1.1;'>{percent_text}</div>"
            f"<div class='metric-title'>Coût Généreux</div>"
            f"<div style='font-size:12px; margin-top:6px;'>"
            f"💸 Marge : <strong>{val_marge}</strong><br>"
            f"📈 Taux : <strong>{val_taux}</strong>"
            f"</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 4 : Marge Brute
    with cols[4]:
        val = f"{marge_brute:.2f}€" if marge_brute is not None else "N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Marge Brute</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 5 : Taux de Marge
    with cols[5]:
        val = f"{taux_marge:.1f}%" if taux_marge is not None else"N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Taux de Marge</div>"
            f"</div>", unsafe_allow_html=True
        )
    
    # Réduction de l'espace avant l'affichage de l'image
    st.markdown("<div style='margin-top:-1rem;'></div>", unsafe_allow_html=True)


    # Affichage de l'image et des détails
    col1, col2 = st.columns([1, 2])
    with col1:
        afficher_image_plat(plat, images_plats)
    with col2:
        if not grouped_finale.empty:
            top_ing = grouped_finale.sort_values("Coût (€)", ascending=False).iloc[0]
            part = (top_ing["Coût (€)"] / cout_matiere) * 100 if cout_matiere > 0 else 0
    
            
            # Focus Ingrédient Principal à côté de l'image
            st.markdown(f"""
<div style="
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #D92332;
    padding: 1.1rem 1.4rem;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
    position: relative;
    overflow: hidden;
    height: 100%;
">
    <div style="
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle at top right, 
            rgba(217, 35, 50, 0.03) 0%, 
            rgba(217, 35, 50, 0.01) 30%,
            transparent 70%);
        pointer-events: none;
    "></div>
    <div style="
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        margin-bottom: 0.7rem;
    ">
        <div style="
            width: 34px;
            height: 34px;
            min-width: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(217, 35, 50, 0.08);
            border-radius: 7px;
            margin-top: 2px;
        ">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 21L16.65 16.65" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M11 8V14" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 11H14" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="flex: 1;">
            <div style="
                color: #1e293b;
                font-weight: 600;
                font-size: 1rem;
                letter-spacing: -0.01em;
                margin-bottom: 0.6rem;
                display: flex;
                align-items: center;
                gap: 0.4rem;
            ">
                <span>Focus Ingrédient Principal</span>
                <div style="
                    width: 3px;
                    height: 3px;
                    border-radius: 50%;
                    background-color: #D92332;
                    opacity: 0.7;
                    margin-top: 1px;
                "></div>
            </div>
            <div style="
                color: #475569;
                font-size: 0.9rem;
                line-height: 1.5;
                position: relative;
                padding-left: 0;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            ">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span style="
                        font-weight: 600;
                        color: #D92332;
                    ">{top_ing['ingredient']}</span>
                    <div style="
                        height: 4px;
                        width: 4px;
                        background: #cbd5e1;
                        border-radius: 50%;
                    "></div>
                    <span>
                        représente <strong>{part:.1f}%</strong> du coût matière
                    </span>
                </div>
                <div style="
                    background: #f8fafc;
                    border-radius: 6px;
                    padding: 0.5rem 0.7rem;
                    font-size: 0.85rem;
                    color: #64748b;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                ">
                    <span>Coût de cet ingrédient:</span>
                    <span style="
                        font-weight: 600;
                        color: #334155;
                        font-variant-numeric: tabular-nums;
                    ">{top_ing['Coût (€)']:.2f} €</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # 📊 STATS VENTES RÉELLES (depuis SQLite avec mapping)
    try:
        from kezia_db_manager import get_db_manager
        from product_mapping import get_kezia_name
        
        # Récupérer le nom Kezia correspondant
        kezia_name = get_kezia_name(plat)
        
        # Récupérer les ventes depuis SQLite
        db = get_db_manager()
        conn = db.get_connection()
        query = """
            SELECT SUM(quantite) as qty, SUM(ca_ttc) as ca
            FROM ventes 
            WHERE produit = ?
        """
        result = pd.read_sql_query(query, conn, params=(kezia_name,))
        conn.close()
        
        if not result.empty and result['qty'].iloc[0] is not None:
            total_ventes = int(result['qty'].iloc[0])
            ca_ttc = float(result['ca_ttc'].iloc[0])
            ca_ht = ca_ttc / 1.055
            
            # Calculer la marge totale
            marge_totale = ca_ht - (cout_matiere * total_ventes) if cout_matiere else 0
            
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 1px solid #bae6fd;
    border-left: 3px solid #0284c7;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0 1rem;
    box-shadow: 0 2px 4px rgba(2, 132, 199, 0.08);
">
    <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem;">
        <div style="
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(2, 132, 199, 0.1);
            border-radius: 6px;
        ">
            📊
        </div>
        <div style="font-weight: 600; color: #075985; font-size: 0.95rem;">
            Performances (historique complet)
        </div>
    </div>
    <div style="
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin-top: 0.6rem;
    ">
        <div style="
            background: white;
            border-radius: 6px;
            padding: 0.6rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        ">
            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.2rem;">Quantité vendue</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #0284c7;">{total_ventes:,}</div>
        </div>
        <div style="
            background: white;
            border-radius: 6px;
            padding: 0.6rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        ">
            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.2rem;">CA généré HT</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #0284c7;">{ca_ht:,.0f}€</div>
        </div>
        <div style="
            background: white;
            border-radius: 6px;
            padding: 0.6rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        ">
            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.2rem;">Marge totale</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: {'#16a34a' if marge_totale > 0 else '#dc2626'};">{marge_totale:,.0f}€</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    except Exception as e:
        # Si erreur, ne rien afficher
        pass
    
    st.markdown(f"""
<div style="
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #D92332;
    padding: 1.1rem 1.4rem;
    margin: 1rem 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle at top right, 
            rgba(217, 35, 50, 0.03) 0%, 
            rgba(217, 35, 50, 0.01) 30%,
            transparent 70%);
        pointer-events: none;
    "></div>
    <div style="
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        margin-bottom: 0.7rem;
    ">
        <div style="
            width: 34px;
            height: 34px;
            min-width: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(217, 35, 50, 0.08);
            border-radius: 7px;
            margin-top: 2px;
        ">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 21L16.65 16.65" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M11 8V14" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 11H14" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="flex: 1;">
            <div style="
                color: #1e293b;
                font-weight: 600;
                font-size: 1rem;
                letter-spacing: -0.01em;
                margin-bottom: 0.6rem;
                display: flex;
                align-items: center;
                gap: 0.4rem;
            ">
                <span>Focus Ingrédient Principal</span>
                <div style="
                    width: 3px;
                    height: 3px;
                    border-radius: 50%;
                    background-color: #D92332;
                    opacity: 0.7;
                    margin-top: 1px;
                "></div>
            </div>
            <div style="
                color: #475569;
                font-size: 0.9rem;
                line-height: 1.5;
                position: relative;
                padding-left: 0;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            ">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span style="
                        font-weight: 600;
                        color: #D92332;
                    ">{top_ing['ingredient']}</span>
                    <div style="
                        height: 4px;
                        width: 4px;
                        background: #cbd5e1;
                        border-radius: 50%;
                    "></div>
                    <span>
                        représente <strong>{part:.1f}%</strong> du coût matière
                    </span>
                </div>
                <div style="
                    background: #f8fafc;
                    border-radius: 6px;
                    padding: 0.5rem 0.7rem;
                    font-size: 0.85rem;
                    color: #64748b;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                ">
                    <span>Coût de cet ingrédient:</span>
                    <span style="
                        font-weight: 600;
                        color: #334155;
                        font-variant-numeric: tabular-nums;
                    ">{top_ing['Coût (€)']:.2f} €</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    if taux_marge is not None:
        if taux_marge >= 70:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #f0fdf4 0%, #f8fff5 100%);
    border: 1px solid #bbf7d0;
    border-left: 3px solid #22c55e;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 0.8rem;
    box-shadow: 0 1px 3px rgba(34, 197, 94, 0.07);
    position: relative;
    overflow: hidden;
">
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(34, 197, 94, 0.1);
            border-radius: 6px;
        ">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17L4 12" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="
            color: #16a34a;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
        ">
            <span>Ce plat est <strong>très rentable</strong></span>
            <span style="
                font-size: 0.8rem;
                opacity: 0.9;
                font-weight: 400;
                margin-top: 0.1rem;
            ">Marge supérieure à 70% ({taux_marge:.1f}%)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        elif taux_marge >= 50:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #fffbeb 0%, #fffdf5 100%);
    border: 1px solid #fde68a;
    border-left: 3px solid #f59e0b;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 0.8rem;
    box-shadow: 0 1px 3px rgba(245, 158, 11, 0.07);
    position: relative;
    overflow: hidden;
">
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(245, 158, 11, 0.1);
            border-radius: 6px;
        ">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 9V13" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 17.01L12.01 16.9989" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="
            color: #d97706;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
        ">
            <span>Rentabilité <strong>correcte</strong> mais améliorable</span>
            <span style="
                font-size: 0.8rem;
                opacity: 0.9;
                font-weight: 400;
                margin-top: 0.1rem;
            ">Marge entre 50% et 70% ({taux_marge:.1f}%)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #fef2f2 0%, #fff5f5 100%);
    border: 1px solid #fecaca;
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 0.8rem;
    box-shadow: 0 1px 3px rgba(239, 68, 68, 0.07);
    position: relative;
    overflow: hidden;
">
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(239, 68, 68, 0.1);
            border-radius: 6px;
        ">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="
            color: #dc2626;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
        ">
            <span>Rentabilité <strong>faible</strong> à optimiser</span>
            <span style="
                font-size: 0.8rem;
                opacity: 0.9;
                font-weight: 400;
                margin-top: 0.1rem;
            ">Marge inférieure à 50% ({taux_marge:.1f}%)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # CSS pour réduire les espaces entre les sections
    st.markdown("""
    <style>
    /* Réduire l'espace avant et après les graphiques */
    .stPlotlyChart {
        margin-top: -1rem;
        margin-bottom: -1rem;
    }
    /* Réduire la taille des titres des sections */
    .modern-subheader {
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
        padding: 0.3rem 0.6rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 0.8rem; background: linear-gradient(to right, #fafafa 0%, #ffffff 100%); border-left: 2.5px solid #D92332; border-radius: 6px; margin: 1rem 0 0.8rem;">
    <div style="display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: rgba(217, 35, 50, 0.08); border-radius: 5px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a; letter-spacing: -0.01em;">Composition du plat</div>
        <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.05rem;">Détail des ingrédients et coûts</div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    affichage_final = grouped_finale[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]].copy()
    affichage_final.rename(columns={
        'ingredient': 'Ingrédient',
        'quantite_g': 'Quantité (g)',
        'prix_kg': 'Prix (€/kg)',
        'Coût (€)': 'Coût (€)'
    }, inplace=True)
    
    st.markdown("""
    <style>
    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(affichage_final, use_container_width=True, hide_index=True)
   
    st.markdown("""
<div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 0.8rem; background: linear-gradient(to right, #fafafa 0%, #ffffff 100%); border-left: 2.5px solid #D92332; border-radius: 6px; margin: 1.2rem 0 0.8rem;">
    <div style="display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: rgba(217, 35, 50, 0.08); border-radius: 5px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 20V10M12 20V4M6 20v-6" stroke="#D92332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <div>
        <div style="font-size: 0.85rem; font-weight: 600; color: #0f172a; letter-spacing: -0.01em;">Répartition des coûts</div>
        <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.05rem;">Visualisation par ingrédient</div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Graphique avec style amélioré
    fig_bar = px.bar(
        grouped_finale, 
        x="ingredient", 
        y="Coût (€)", 
        height=280,
        color_discrete_sequence=['#D92332']
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.markdown("""
    <div style="border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.5rem; background: white; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);">
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
