import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json

st.set_page_config(
    page_title="🍕 Fiche Technique - Chez Antoine",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style id="layout-fix">
/* --- ①  rétrécir la sidebar --- */
section[data-testid="stSidebar"] {width:18rem;}
section[data-testid="stSidebar"][aria-expanded="false"]{
    transform:translateX(-18rem);}

/* --- ②  avancer la zone main exactement de 18 rem --- */
[data-testid="stAppViewContainer"] > .main {
    padding-left: calc(18rem + 1rem);   /* +1 rem = l’espace gou­tter par défaut */
}

/* --- ③  sur mobile (<768 px) on remet à zéro --- */
@media (max-width:768px){
  [data-testid="stAppViewContainer"] > .main{padding-left:1rem;}
}
</style>
""", unsafe_allow_html=True)



def save_drafts(drafts, filename="data/brouillons.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(drafts, f, indent=2, ensure_ascii=False)

def load_drafts(filename="data/brouillons.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# ============== FONCTIONS ET DONNÉES ==============
@st.cache_data
def load_data():
    """Charge les données des recettes et des ingrédients depuis des fichiers Excel."""
    try:
        recettes = pd.read_excel("data/recettes_complet_MAJ2.xlsx")
        ingredients = pd.read_excel("data/ingredients_nettoyes_et_standardises.xlsx")
        # Stockage du nom original
        recettes["original_plat"] = recettes["plat"]
        ingredients["original_plat"] = ingredients["plat"]

        # Unification des noms pour Panini Pizz
        recettes['plat'] = recettes['plat'].replace({
            'panini pizz base crème': 'panini pizz',
            'panini pizz base tomate': 'panini pizz'
        })
        ingredients['plat'] = ingredients['plat'].replace({
            'panini pizz base crème': 'panini pizz',
            'panini pizz base tomate': 'panini pizz'
        })
        return recettes, ingredients
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None, None

def calculer_cout(ingredients_df: pd.DataFrame) -> pd.DataFrame:
    """Calcule le coût des ingrédients (colonne 'Coût (€)')."""
    ingredients_df["Coût (€)"] = (ingredients_df["prix_kg"] * ingredients_df["quantite_g"]) / 1000
    return ingredients_df

def get_dough_cost(plat: str) -> float:
    """
    Renvoie le coût de la pâte selon le plat :
      - panini pizz => 0.12 €
      - plat finissant par S => 0.12 €
      - plat finissant par M => 0.20 €
      - pains => 0.10 € (1/2 pâte M)
      - sinon => 0 €
    """
    plat_low = plat.lower()
    # Cas pains
    if "pain aux herbes et mozzarella" in plat_low or "pain aux herbes" in plat_low:
        return 0.10
    # Cas pizzas
    elif plat_low == "panini pizz":
        return 0.12
    elif plat.endswith("S"):
        return 0.12
    elif plat.endswith("M"):
        return 0.20
    else:
        return 0.0



# Dictionnaire de prix de vente
prix_vente_dict = {
    "Savoyarde S": 11.50,
    "Savoyarde M": 13.50,
    "Norvegienne S": 11.50,
    "Norvegienne M": 13.50,
    "Normande S": 11.50,
    "Normande M": 13.50,
    "Raclette S": 11.50,
    "Raclette M": 13.50,
    "4 fromages S": 11.50,
    "4 fromages M": 13.50,
    "Hanna S": 11.50,
    "Hanna M": 13.50,
    "Truffe S": 11.50,
    "Truffe M": 13.50,
    "panini pizz": 5.50,
    "Margarita S": 8.50,
    "Margarita M": 10.50,
    "Calzone S": 9.50,
    "Reine S": 9.50,    
    "Reine M": 11.50,
    "Napolitaine S": 9.50,
    "Napolitaine M": 11.50,
    "Fermière S": 9.50,
    "Fermière M": 11.50,
    "3 Fromages S": 10.50,
    "3 Fromages M": 12.50,
    "Calzone S": 9.50,
    "Orientale S": 10.50,
    "Orientale M": 12.50,
    "Carnée S": 10.50,
    "Carnée M": 12.50,
    "Paysanne S": 10.50,
    "Paysanne M": 12.50,
    "Aubergine S": 10.50,
    "Aubergine M": 12.50,
    "Chèvre-Miel S": 9.50,
    "Chèvre-Miel M": 11.50,
    "Charcutière S": 10.50,
    "Charcutière M": 12.50,
    "Mexicaine S": 10.50,
    "Mexicaine M": 12.50,
    "4 Saisons S": 10.50,
    "4 Saisons M": 12.50,
    "Silicienne S": 10.50,
    "Silicienne M": 12.50,
    "Végétarienne S": 10.50,
    "Végétarienne M": 12.50,
    "Margarita S": 8.50,
    "Margarita M": 10.50,
    "Salade Burrata di Parma": 13.50,
    "Salade burrata di salmone": 13.50,
    "Burrata feuille La véritable": 6.50,
    "Pizza Burrata di Parma": 13.50,
    "Salade César": 9.50,
    "Salade végétarienne": 9.50,
    "Salade chèvre": 9.50,
    "Salade Burrata di Salmone": 13.50,
    "Pizza Burrata Di Salmone": 13.50,
    "Pizza Burrata Di Parma": 13.50,
    "Bolognaise": 9.90,
    "Truffe": 9.90,
    "Saumon": 9.90,
    "Carbonara": 9.90,
    "Fermière": 9.90,
    "3 Fromages": 9.90,
    "Napolitaine": 9.90,
    "Sicilienne": 9.90,
    "Arrabiata": 8.90,
    "Pain aux herbes et mozzarella": 3.00,
    "Pain aux herbes": 2.50,
    "Assiette Artichauts": 5.50,
    "Salade Verte": 5.50,
    "Arrabiata Poulet": 9.90,
  
}


# Dictionnaire d'images (exemple)
images_plats = {
    "Savoyarde S": "savoyarde.webp",
    "Savoyarde M": "savoyarde.webp",
    "Norvegienne S": "Norvégienne.webp",
    "Norvegienne M": "Norvégienne.webp",
    "Normande S": "Normande.webp",
    "Normande M": "Normande.webp",
    "Raclette S": "Raclette.webp",
    "Raclette M": "Raclette.webp",
    "4 fromages S": "pizza_4fromages.webp",
    "4 fromages M": "pizza_4fromages.webp",
    "Hanna S": "Hanna.webp",
    "Hanna M": "Hanna.webp",
    "Truffe S": "pizza_truffe.webp",
    "Truffe M": "pizza_truffe.webp",
    "panini pizz": "Panini_pizz_creme.webp",
    "Margarita S": "marga.webp",
    "Margarita M": "marga.webp",
    "Calzone S": "Calzone.webp",
    "Reine S": "Reine.webp",
    "Reine M": "Reine.webp",
    "Paysanne S": "Paysanne.webp",
    "Paysanne M": "Paysanne.webp",
    "Chèvre-Miel S": "chevre-miel.webp",
    "Chèvre-Miel M": "chevre-miel.webp",
    "Aubergine S": "Aubergine.webp",
    "Aubergine M": "Aubergine.webp",
    "Napolitaine S": "Napo.webp",
    "Napolitaine M": "Napo.webp",
    "Fermière S": "fermiere.webp",
    "Fermière M": "fermiere.webp",
    "3 Fromages S": "3Fromage.webp",
    "3 Fromages M": "3Fromage.webp",
    "Orientale S": "Orientale.webp",
    "Orientale M": "Orientale.webp",
    "Carnée S": "Carnée.webp",
    "Carnée M": "Carnée.webp",
    "Mexicaine S": "Mexicaine.webp",
    "Mexicaine M": "Mexicaine.webp",
    "Charcutière S": "charcut.webp",
    "Charcutière M": "charcut.webp",
    "Végétarienne S": "Vege.webp",
    "Végétarienne M": "Vege.webp",
    "Silicienne S": "Sicili.webp",
    "Silicienne M": "Sicili.webp",
    "4 Saisons S": "4 saisons.webp",
    "4 Saisons M": "4 saisons.webp",
    # --- PÂTES ---
    "Bolognaise": "pates_bolognaise.webp",
    "Truffe": "pates_truffe.webp",
    "Saumon": "pates_saumon.webp",
    "Carbonara": "pates_carbonara.webp",
    "Fermière": "pates_fermiere.webp",
    "3 Fromages": "pates_3fromages.webp",
    "Napolitaine": "pates_napolitaine.webp",
    "Sicilienne": "pates_sicilienne.webp",
    "Arrabiata": "pates_arrabiata.webp",
    "Arrabiata Poulet": "pates_arrabiata_poulet.jpeg",

    # --- PAINS MAISON ---
    "Pain aux herbes et mozzarella": "pain_herbes_mozza.webp",
    "Pain aux herbes": "pain_herbes.webp",

    # --- SALADES ---
    "Salade César": "salade_cesar.webp",
    "Salade végétarienne": "salade_vegetarienne.webp",
    "Salade chèvre": "salade_chevre.webp",
    "Assiette Artichauts": "assiette_artichauts.jpeg",
    "Salade Verte": "salade_verte.jpeg",

    # --- BURRATAS ---
    "Pizza Burrata di Parma": "pizza_burrata_parma.jpeg",
    "Burrata feuille La véritable": "burata_feuille.webp",
    "Pizza Burrata Di Salmone": "pizza_burrata_saumon.jpeg",
    "Salade Burrata di Salmone": "salade_burrata_saumon.webp",
    "Salade Burrata di Parma": "salade_burrata_parma.webp",
    
}

def afficher_image_plat(plat: str, images_dict: dict):
    """Affiche l'image du plat ou l'image par défaut."""
    image_path = f'images/{images_dict.get(plat, "default.jpg")}'
    if not os.path.exists(image_path):
        image_path = "images/default.jpg"
    st.image(image_path, use_container_width=True)

def generer_detailed_breakdown(plat, composition_finale, cout_matiere, prix_affiche):
    """
    Génère une chaîne de texte expliquant le calcul.
    """
    breakdown = f"**Détails du calcul pour {plat}**\n\n"
    for idx, row in composition_finale.iterrows():
        breakdown += f"- {row['ingredient']}: {row['Coût (€)']:.2f} €\n"
    breakdown += f"\n**Coût Matière (ingrédients + pâte)**: {cout_matiere:.2f} €\n"
    return breakdown

# ============== CONFIGURATION DE LA PAGE ==============

# ============== STYLES CSS ==============

# ============== TITRE PRINCIPAL ==============
st.markdown("<h1 class='title-card'>🍽️ Fiche Technique - Chez Antoine</h1>", unsafe_allow_html=True)

# ============== CHARGEMENT DES DONNÉES ==============
recettes, ingredients = load_data()
if recettes is None or ingredients is None:
    st.stop()

# ============== SIDEBAR : PARAMÈTRES ==============
st.sidebar.markdown("<h3 style='color: #D92332;'>📌 Paramètres</h3>", unsafe_allow_html=True)

# Choix du mode d'analyse
mode_analysis = st.sidebar.radio("Mode d'analyse", ["Analyse d'un plat", "Analyse comparative", "Modifier un plat"], key="mode_analysis")

# Coefficient surplus (clé unique pour éviter les conflits)
coeff_surplus = st.sidebar.slider("Coefficient surplus", 1.0, 2.0, 1.25, 0.05, key="coeff_surplus")

# ============== TRAITEMENT DES MODES ==============
if mode_analysis == "Analyse d'un plat":
    # ------------------- Analyse d'un plat -------------------
    # 1️⃣ Sélection de la catégorie
    categories = recettes["categorie"].unique()
    categories = ["Tout"] + list(categories)  # Ajoute 'Tout' en premier
    categorie_choisie = st.sidebar.selectbox("Catégorie", categories)
    
    if categorie_choisie == "Tout":
        plats_dispo = recettes["plat"].unique()
    else:
        plats_dispo = recettes[recettes["categorie"] == categorie_choisie]["plat"].unique()

    plat = st.sidebar.selectbox("Choisissez un plat", plats_dispo, key="plat_unique")

    # 🎯 Gérer la portion si catégorie = "Pâtes"
    portion_faim = "Petite Faim"  # Par défaut
    if categorie_choisie.lower() == "pâtes":
        st.sidebar.markdown("#### 🍝 Portion")
        portion_faim = st.sidebar.radio(
            "Choisissez la portion :",
            ["Petite Faim", "Grosse Faim"],
            horizontal=True,
            key="portion_faim_analyse"
        )

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
    if categorie_choisie.lower() == "pâtes":
        plat_key = plat.lower().strip()
        mask_pate = ingr_plat["ingredient"].str.lower().str.contains("spaghetti|penné|pâtes")

        if portion_faim == "Grosse Faim":
            if plat_key in quantites_grosse_faim and mask_pate.any():
                nouvelle_quantite = quantites_grosse_faim[plat_key]
                ingr_plat.loc[mask_pate, "quantite_g"] = nouvelle_quantite
                
        else:
            # Ne rien modifier : on garde les quantités de base (Petite Faim)
            pass

    # 4. Recalcul du coût matière avec les quantités à jour
    ingr_plat = calculer_cout(ingr_plat)

    # 5. Ajustement du prix de vente pour les pâtes en Grosse Faim
    prix_affiche = prix_vente_dict.get(plat, 0)
    if categorie_choisie.lower() == "pâtes" and portion_faim == "Grosse Faim":
        prix_affiche += 3  # Ajoute 3€ pour la Grosse Faim
    # Choix de l'affichage TTC ou HT
    affichage_prix = st.radio("Affichage des prix :", ["TTC", "HT"], horizontal=True)
    

    # Taux de TVA applicable (ajuste-le si besoin)
    taux_tva = 0.10

    # Calcul dynamique selon affichage
    if affichage_prix == "HT" and prix_affiche:
        prix_affiche = prix_affiche / (1 + taux_tva)
    else:
        prix_affiche = prix_affiche

    


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
        cost_creme = ingr_plat.loc[ingr_plat["ingredient"].str.lower() == "crème", "Coût (€)"].sum()
        cost_sauce = ingr_plat.loc[ingr_plat["ingredient"].str.lower() == "sauce tomate", "Coût (€)"].sum()
        base_selection = st.sidebar.radio("Choisissez la base du panini :", ["Crème", "Sauce Tomate"], index=0, key="base_panini")
        cost_base = cost_creme if base_selection == "Crème" else cost_sauce

        additional = ingr_plat[~ingr_plat["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
        avg_add = additional["Coût (€)"].mean() if not additional.empty else 0.0

        mode_avance = st.sidebar.checkbox("⭐ Mode avancé : Choisir deux ingrédients manuellement", key="mode_avance")
        if base_selection == "Crème":
            composition_candidates = ingr_plat[ingr_plat["original_plat"].str.contains("base crème", case=False, na=False)].copy()
        else:
            composition_candidates = ingr_plat[ingr_plat["original_plat"].str.contains("base tomate", case=False, na=False)].copy()

        if not mode_avance:
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
            st.write("Vous pouvez choisir deux fois le même ingrédient si vous le souhaitez.")
            already_included = ["crème", "sauce tomate"]
            additional_clean = additional.drop_duplicates(subset=["ingredient"])
            all_ingrs = list(additional_clean.loc[~additional_clean["ingredient"].str.lower().isin(already_included), "ingredient"].unique())
            slot1 = st.sidebar.selectbox("Ingrédient #1", ["Aucun"] + all_ingrs, key="slot1")
            slot2 = st.sidebar.selectbox("Ingrédient #2", ["Aucun"] + all_ingrs, key="slot2")

            cost_slot1 = additional_clean.loc[additional_clean["ingredient"] == slot1, "Coût (€)"].iloc[0] if slot1 != "Aucun" else 0
            cost_slot2 = additional_clean.loc[additional_clean["ingredient"] == slot2, "Coût (€)"].iloc[0] if slot2 != "Aucun" else 0
            cout_panini = cost_base + cost_slot1 + cost_slot2

            composition_finale = pd.DataFrame(columns=composition_candidates.columns)
            if base_selection == "Crème":
                df_base = composition_candidates.loc[composition_candidates["ingredient"].str.lower() == "crème"].iloc[[0]]
            else:
                df_base = composition_candidates.loc[composition_candidates["ingredient"].str.lower() == "sauce tomate"].iloc[[0]]
            composition_finale = pd.concat([composition_finale, df_base], ignore_index=True)
            if slot1 != "Aucun":
                composition_finale = pd.concat([
                    composition_finale,
                    additional_clean.loc[additional_clean["ingredient"] == slot1]
                ], ignore_index=True)
            if slot2 != "Aucun":
                composition_finale = pd.concat([
                    composition_finale,
                    additional_clean.loc[additional_clean["ingredient"] == slot2]
                ], ignore_index=True)
        # Gestion de la Mozzarella
        composition_finale = composition_finale[composition_finale["ingredient"].str.lower() != "mozzarella"]
        cost_mozza = 0.234  # Coût final pour 40g de mozzarella
        row_mozza = pd.DataFrame([{
            "ingredient": "Mozzarella",
            "quantite_g": 40,
            "prix_kg": 5.85,
            "Coût (€)": cost_mozza,
            "ingredient_lower": "mozzarella"
        }])
        composition_finale = pd.concat([composition_finale, row_mozza], ignore_index=True)
        # ✅ Ajout pâte (visuellement et comptablement)
        row_pate = pd.DataFrame([{
            "ingredient": "Pâte à panini",
            "quantite_g": 0,
            "prix_kg": 0,
            "Coût (€)": pate_cost,
            "ingredient_lower": "pâte à panini"
        }])
        composition_finale = pd.concat([composition_finale, row_pate], ignore_index=True)

        # Total panini = base + ingr. + mozza + pâte
        cout_panini += cost_mozza + pate_cost

        # Calcul de la différence
        base_ingr_cost = ingr_plat["Coût (€)"].sum()
        difference = cout_panini - base_ingr_cost
        cout_matiere += difference
    # Fin du traitement spécifique Panini
    
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

    # 7. Texte explicatif
    detailed_breakdown = generer_detailed_breakdown(plat, grouped_finale, cout_matiere, prix_affiche)

    # 🔥 Affichage des KPI fusionnés
    cols = st.columns(5)

    # Bloc 0 : Prix Vente
    with cols[0]:
        val = f"{prix_affiche:.2f}€" if prix_affiche else "N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Prix Vente</div>"
            f"</div>", unsafe_allow_html=True
        )

    # Bloc 1 : Coût Matière
    with cols[1]:
        val = f"{cout_matiere:.2f}€"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Coût Matière</div>"
            f"</div>", unsafe_allow_html=True
        )

    # Bloc 2 : Coût Généreux + Marge Généreuse + Taux dans la même carte
    with cols[2]:
        val_gen = f"{cout_genereux:.2f}€"
        val_marge = f"{marge_generuse:.2f}€"
        val_taux = f"{taux_generuse:.1f}%" if taux_generuse is not None else "N/A"
        percent_text = f"(+{(coeff_surplus - 1)*100:.0f}%)"
        
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val_gen}</div>"
            f"<div style='font-size:13px; color: #999;'>{percent_text}</div>"
            f"<div class='metric-title'>Coût Généreux</div>"
            f"<div style='font-size:13px; margin-top:8px;'>"
            f"💸 Marge : <strong>{val_marge}</strong><br>"
            f"📈 Taux : <strong>{val_taux}</strong>"
            f"</div>"
            f"</div>", unsafe_allow_html=True
        )

    # Bloc 3 : Marge Brute
    with cols[3]:
        val = f"{marge_brute:.2f}€" if marge_brute is not None else "N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Marge Brute</div>"
            f"</div>", unsafe_allow_html=True
        )

    # Bloc 4 : Taux de Marge
    with cols[4]:
        val = f"{taux_marge:.1f}%" if taux_marge is not None else "N/A"
        st.markdown(
            f"<div class='metric-card'>"    
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Taux de Marge</div>"
            f"</div>", unsafe_allow_html=True
        )

    # Affichage de l'image et des détails
    col1, col2 = st.columns([1, 2])
    with col1:
        afficher_image_plat(plat, images_plats)
    with col2:
        if not grouped_finale.empty:
            top_ing = grouped_finale.sort_values("Coût (€)", ascending=False).iloc[0]
            part = (top_ing["Coût (€)"] / cout_matiere) * 100 if cout_matiere > 0 else 0
            st.markdown(f"""
<div style="padding: 0.8rem 1rem; border-left: 4px solid #2563eb; background-color: #f9fafb; border-radius: 6px;">
  <span style="font-weight: 600; font-size: 1rem;">🔎 Focus Ingrédient Principal</span><br>
  <span style="font-size: 0.95rem;">
    L'ingrédient le plus coûteux est <strong>{top_ing['ingredient']}</strong>, représentant <strong>{part:.1f}%</strong> du coût matière total (<em>{top_ing['Coût (€)']:.2f} €</em>).
  </span>
</div>
""", unsafe_allow_html=True)

    if taux_marge is not None:
        if taux_marge >= 70:
            st.success("✅ Ce plat est **très rentable** (marge supérieure à 70%).")
        elif taux_marge >= 50:
            st.warning("⚠️ Rentabilité **correcte** mais améliorable (entre 50% et 70%).")
        else:
            st.error("❌ Rentabilité **faible** (marge inférieure à 50%).")

    st.subheader("🛒 Composition du Plat")
    affichage_final = grouped_finale[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]].copy()
    affichage_final.rename(columns={
        'ingredient': 'Ingrédient',
        'quantite_g': 'Quantité (g)',
        'prix_kg': 'Prix (€/kg)',
        'Coût (€)': 'Coût (€)'
    }, inplace=True)
    st.dataframe(affichage_final, use_container_width=True, hide_index=True)
    
    st.subheader("📉 Répartition des coûts par Ingrédient")
    fig_pie = px.pie(grouped_finale, values="Coût (€)", names="ingredient", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.subheader("📈 Coût Matière par Ingrédient")
    fig_bar = px.bar(grouped_finale, x="ingredient", y="Coût (€)")
    st.plotly_chart(fig_bar, use_container_width=True)

elif mode_analysis == "Analyse comparative":
    st.subheader("🔍 Analyse Comparative")

    all_plats = recettes["plat"].unique()

    categories = recettes["categorie"].unique()
    categories = ["Tout"] + list(categories)  # Ajoute 'Tout' tout en haut

    categorie_comp = st.sidebar.selectbox("Catégorie pour comparaison", categories, key="cat_comp")

    if categorie_comp == "Tout":
        plats_cat = recettes["plat"].unique()
    else:
        plats_cat = recettes[recettes["categorie"] == categorie_comp]["plat"].unique()

    selected_plats = st.sidebar.multiselect("Plats à comparer", plats_cat, key="selected_plats")
    seuil_marge = st.sidebar.slider("Seuil de rentabilité (%)", 40, 90, 70)
    # Choix de l'affichage HT ou TTC
    affichage_prix_comparatif = st.sidebar.radio("Base de calcul :", ["TTC", "HT"], horizontal=True, key="affichage_comparatif")
    with st.sidebar.expander("ℹ️ Pourquoi afficher en HT ?"):
        st.markdown("""
        <b>Pourquoi HT ?</b><br>
        • En restauration, la TVA est <b>reversée à l’État</b>, donc ne constitue pas un gain.<br>
        • Il est plus juste de calculer les marges en <b>hors taxes (HT)</b>.<br><br>
        <u>Sources :</u><br>
        – Zenchef, Combo, Compta-Facile, Wikipedia (marge en restauration)
        """, unsafe_allow_html=True)



    with st.sidebar.expander("❓ Pourquoi 70% est un bon seuil ?"):
        st.markdown("""
    - En restauration, on vise **un taux de marge matière de 70%** (ou plus).
    - Cela signifie que **30% du prix** est consacré aux ingrédients, et le reste couvre :
      - ✅ Main d'œuvre
      - ✅ Charges (loyer, énergie…)
      - ✅ Bénéfices

    👉 **Moins de 50%** = souvent à perte  
    👉 **50–70%** = à surveiller  
    👉 **≥ 70%** = bon rendement

    📚 *Source :* [EHL - École Hôtelière de Lausanne](https://www.ehl.edu/fr)
    """)


    classement_par = st.sidebar.radio("Critère de classement", ["Marge (€)", "Taux (%)"])
    filtre_sous_seuil = st.sidebar.checkbox("Afficher uniquement les plats sous le seuil dans le graphe")

    with st.sidebar.expander("ℹ️ Quel critère choisir ?"):
        st.markdown("""
        - **Marge (€)** : met en avant les plats qui rapportent le plus d'argent brut.
        - **Taux (%)** : montre les plats les plus efficaces proportionnellement (rentabilité relative).

        👉 Exemple : un plat pas cher peut avoir un taux élevé mais une petite marge en valeur.
        """)

    def analyse_plat(plat, seuil_marge, affichage_ht=True):
        ingr = ingredients[ingredients['plat'].str.lower() == plat.lower()].copy()
        ingr = calculer_cout(ingr)
        base_cost = ingr["Coût (€)"].sum()
        dough = get_dough_cost(plat)

        if plat.lower() == "panini pizz":
            base = ingr[ingr["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
            base_cost = base["Coût (€)"].sum()
            add = ingr[~ingr["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
            avg_add = add["Coût (€)"].mean() if not add.empty else 0.0
            total_cost = base_cost + 2 * avg_add + 0.234 + dough
        else:
            total_cost = base_cost + dough

        prix_ttc = prix_vente_dict.get(plat, 0)
        taux_tva = 0.10
        prix_affiche = prix_ttc / (1 + taux_tva) if affichage_ht else prix_ttc

        marge = prix_affiche - total_cost
        taux = (marge / prix_affiche * 100) if prix_affiche > 0 else None


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
        delta_prix = prix_conseille - prix_affiche if prix_conseille else None
        delta_pct = (delta_prix / prix_affiche * 100) if prix_affiche > 0 and delta_prix else None

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
            "Prix (€)": round(prix_affiche, 2),
            "Coût (€)": round(total_cost, 2),
            "Marge (€)": round(marge, 2),
            "Taux (%)": round(taux, 1) if taux else None,
            "Note": note,
            "Prix conseillé (€)": round(prix_conseille, 2) if prix_conseille else None,
            "Delta (€)": round(delta_prix, 2) if delta_prix else None,
            "Delta (%)": round(delta_pct, 1) if delta_pct else None,
            "Ajustement": ajustement
        }

    plats_analyzes = selected_plats if selected_plats else plats_cat

    affichage_ht = affichage_prix_comparatif == "HT"
    df = pd.DataFrame([analyse_plat(p, seuil_marge, affichage_ht=affichage_ht) for p in plats_analyzes])


    marge_moy = df["Marge (€)"].mean()
    taux_moy = df["Taux (%)"].mean()

    col1, col2 = st.columns(2)
    col1.metric("💰 Marge Moyenne", f"{marge_moy:.2f} €")
    col2.metric("📈 Taux de Marge Moyen", f"{taux_moy:.1f} %")
    if not affichage_ht:
        st.info("ℹ️ Les prix sont affichés **TTC** dans cette analyse comparative.")
    else:
        st.info("ℹ️ Les prix sont affichés **HT** pour une meilleure analyse de rentabilité.")


    classement_key = "Marge (€)" if classement_par == "Marge (€)" else "Taux (%)"

    if not selected_plats:
        top5 = df[df["Taux (%)"] >= seuil_marge].sort_values(classement_key, ascending=False).head(5)
        flop5 = df[df["Taux (%)"] < seuil_marge].sort_values(classement_key, ascending=True).head(5)

        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"### 🥇 Top 5 ({classement_key})")
            st.dataframe(top5, use_container_width=True, hide_index=True)
        with col4:
            st.markdown(f"### ❌ Flop 5 ({classement_key})")
            st.dataframe(flop5, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📌 Recommandations")
        if not flop5.empty:
            for _, row in flop5.iterrows():
                st.warning(f"🔧 \"{row['Plat']}\" est sous le seuil ({row['Taux (%)']}%). Pensez à ajuster le prix ou les ingrédients.")
        else:
            st.success("✅ Tous les plats analysés sont au-dessus du seuil de rentabilité.")

    st.markdown("### 🔎 Détail des plats sélectionnés")
    st.dataframe(df.sort_values(classement_key, ascending=False), use_container_width=True, hide_index=True)
    
    import plotly.express as px
    st.markdown("### 📊 Comparaison Visuelle (Prix vs Coût vs Marge)")

    df_chart = df[["Plat", "Prix (€)", "Coût (€)", "Marge (€)", "Taux (%)"]].copy().dropna()
    if filtre_sous_seuil:
        df_chart = df_chart[df_chart["Taux (%)"] < seuil_marge]

    df_melt = df_chart.melt(id_vars="Plat", value_vars=["Prix (€)", "Coût (€)", "Marge (€)"],
                            var_name="Type", value_name="Valeur (€)")
    fig = px.bar(df_melt, x="Plat", y="Valeur (€)", color="Type", barmode="group")
    st.plotly_chart(fig, use_container_width=True)





elif mode_analysis == "Modifier un plat":
    st.markdown("## ✏️ Gestion des plats personnalisés")

    if "brouillons" not in st.session_state:
        st.session_state.brouillons = load_drafts()
    if "plat_actif" not in st.session_state:
        st.session_state.plat_actif = None
    if "vue_actuelle" not in st.session_state:
        st.session_state.vue_actuelle = "Mes plats"

    mode_vue = st.radio("Navigation", ["Mes plats", "Édition"], index=0 if st.session_state.vue_actuelle == "Mes plats" else 1)

    # ======= MES PLATS =======
    if mode_vue == "Mes plats":
        st.session_state.vue_actuelle = "Mes plats"
        st.markdown("### 📋 Mes plats personnalisés")

        if not st.session_state.brouillons:
            st.info("Aucun plat personnalisé pour le moment.")
        else:
            for i, plat in enumerate(st.session_state.brouillons):
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                col1.markdown(f"**{plat['nom']}** (base : _{plat['base']}_)")
                col2.markdown(f"💰 Vente : **{plat.get('prix_affiche', 0):.2f} €**")
                if col3.button("✏️ Modifier", key=f"edit_{i}"):
                    st.session_state.plat_actif = plat
                    st.session_state.vue_actuelle = "Édition"
                    st.rerun()
                if col4.button("🗑️ Supprimer", key=f"delete_{i}"):
                    st.session_state.brouillons = [b for b in st.session_state.brouillons if b["nom"] != plat["nom"]]
                    save_drafts(st.session_state.brouillons)
                    st.success(f"Plat supprimé : {plat['nom']}")
                    st.rerun()

    # ======= ÉDITEUR =======
    elif mode_vue == "Édition":
        st.session_state.vue_actuelle = "Édition"

        if st.button("🔄 Réinitialiser la modification"):
            st.session_state.plat_actif = None
            st.rerun()

        if st.session_state.plat_actif is None:
            st.markdown("### ➕ Créer un nouveau plat personnalisé")
            plat_selectionne = st.selectbox("🍕 Choisissez un plat de base", recettes["plat"].unique(), key="plat_de_base")
            ingr_base = ingredients[ingredients["plat"].str.lower() == plat_selectionne.lower()].copy()
            ingr_base = calculer_cout(ingr_base)

            nom_personnalise = st.text_input("✏️ Nom du nouveau plat", value=f"{plat_selectionne} personnalisé", key="nom_creation")
            prix_base = prix_vente_dict.get(plat_selectionne, 10.0)
            prix_nouveau = st.number_input("💰 Prix de vente", min_value=1.0, value=prix_base, step=0.5, key="prix_creation")

            if st.button("🚀 Démarrer la modification", key="btn_creer"):
                st.session_state.plat_actif = {
                    "nom": nom_personnalise,
                    "base": plat_selectionne,
                    "composition": ingr_base.to_dict(orient="records"),
                    "prix_affiche": prix_nouveau
                }
                st.rerun()
            st.stop()

        # --- Édition ---
        plat_data = st.session_state.plat_actif
        ingr_modifie = pd.DataFrame(plat_data["composition"])
        ingr_dispo = ingredients["ingredient"].unique()

        nouveau_nom = st.text_input("✏️ Nom du plat", value=plat_data["nom"], key="edit_nom")
        prix_affiche = st.number_input("💰 Prix de vente (€)", min_value=1.0, value=plat_data.get("prix_affiche", 10.0), step=0.5, key="edit_prix")

        st.markdown("### 🔁 Modifier des ingrédients")

        max_replace = 3
        for idx in range(max_replace):
            with st.expander(f"🔄 Remplacement #{idx + 1}", expanded=(idx == 0)):
                if not ingr_modifie.empty:
                    ingr_orig = st.selectbox(f"Ingrédient à remplacer #{idx + 1}", ingr_modifie["ingredient"].unique(), key=f"rempl_orig_{idx}")
                    ingr_nouv = st.selectbox(f"Remplacer par", ingr_dispo, key=f"rempl_nouv_{idx}")
                    qty_nouv = st.number_input("Quantité (g)", min_value=0.0, value=50.0, step=5.0, key=f"rempl_qty_{idx}")

                    if st.button("✔️ Appliquer", key=f"btn_apply_{idx}"):
                        ingr_modifie = ingr_modifie[ingr_modifie["ingredient"] != ingr_orig]
                        data_new = ingredients[ingredients["ingredient"] == ingr_nouv].iloc[0]
                        new_row = {
                            "ingredient": ingr_nouv,
                            "quantite_g": qty_nouv,
                            "prix_kg": data_new["prix_kg"],
                            "Coût (€)": (qty_nouv * data_new["prix_kg"]) / 1000
                        }
                        ingr_modifie = pd.concat([ingr_modifie, pd.DataFrame([new_row])], ignore_index=True)
                        st.success(f"Remplacement effectué : {ingr_orig} → {ingr_nouv}")
                        st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
                        st.rerun()

        st.markdown("### ➕ Ajouter un ingrédient")
        ingr_suppl = st.selectbox("Ingrédient à ajouter", ingr_dispo, key="suppl_ajout")
        qty_suppl = st.number_input("Quantité du supplément (g)", min_value=0.0, value=0.0, step=5.0, key="qty_supp")

        if st.button("➕ Ajouter le supplément") and qty_suppl > 0:
            data_suppl = ingredients[ingredients["ingredient"] == ingr_suppl].iloc[0]
            supp_row = {
                "ingredient": ingr_suppl,
                "quantite_g": qty_suppl,
                "prix_kg": data_suppl["prix_kg"],
                "Coût (€)": (qty_suppl * data_suppl["prix_kg"]) / 1000
            }
            ingr_modifie = pd.concat([ingr_modifie, pd.DataFrame([supp_row])], ignore_index=True)
            st.success(f"Ajouté : {ingr_suppl}")
            st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
            st.rerun()

        st.markdown("### 📝 Modifier le grammage d'un ingrédient")
        for idx, row in ingr_modifie.iterrows():
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(row["ingredient"])
            new_qty = col2.number_input(
                "Quantité (g)", 
                min_value=0.0, 
                value=float(row["quantite_g"]), 
                step=5.0, 
                key=f"edit_qty_{idx}"
            )
            if new_qty != row["quantite_g"]:
                ingr_modifie.at[idx, "quantite_g"] = new_qty
                ingr_modifie = calculer_cout(ingr_modifie)
                st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
                st.success(f"Quantité modifiée pour {row['ingredient']}")
                st.rerun()

        ingr_modifie = calculer_cout(ingr_modifie)
        cout_matiere = ingr_modifie["Coût (€)"].sum()
        marge_brute = prix_affiche - cout_matiere
        taux_marge = (marge_brute / prix_affiche) * 100 if prix_affiche and prix_affiche > 0 else None


        st.markdown("### 🧾 Récapitulatif")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Prix vente", f"{prix_affiche:.2f} €")
        col2.metric("Coût matière", f"{cout_matiere:.2f} €")
        col3.metric("Marge brute", f"{marge_brute:.2f} €")
        col4.metric("Taux marge", f"{taux_marge:.1f} %")

        st.markdown("### 📋 Nouvelle composition")
        st.dataframe(ingr_modifie[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]], use_container_width=True)

        # Utilisation d'un formulaire pour la sauvegarde
        with st.form(key="form_sauvegarde"):
            submit_save = st.form_submit_button("💾 Sauvegarder")
            if submit_save:
                plat_final = {
                    "nom": nouveau_nom,
                    "base": plat_data["base"],
                    "composition": ingr_modifie.to_dict(orient="records"),
                    "prix_affiche": prix_affiche,
                }
                # Remplace le plat si même nom, sinon ajoute
                brouillons = [b for b in st.session_state.brouillons if b["nom"] != nouveau_nom]
                brouillons.append(plat_final)
                save_drafts(brouillons)
                st.session_state.brouillons = brouillons
                st.session_state.plat_actif = plat_final
                st.success("✔️ Plat sauvegardé avec succès !")

       

        # Ajout du bouton de retour
        if st.button("⬅️ Retour à mes plats"):
            st.session_state.vue_actuelle = "Mes plats"
            st.session_state.plat_actif = None
            st.rerun()
