import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 🚀 Configuration de la page
st.set_page_config(page_title="🍕 Fiche Technique - Restaurant", layout="wide")

# --- Fonctions Utilitaires ---

@st.cache_data
def load_data():
    """Charge les données des recettes et des ingrédients depuis des fichiers Excel."""
    try:
        recettes = pd.read_excel("data/recettes_final.xlsx")
        ingredients = pd.read_excel("data/ingredients_final.xlsx")
        return recettes, ingredients
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None, None

def calculer_cout(ingredients_df):
    """Calcule le coût des ingrédients pour chaque ingrédient."""
    ingredients_df["Coût (€)"] = (ingredients_df["prix_kg"] * ingredients_df["quantite_g"]) / 1000
    return ingredients_df

def afficher_image_plat(plat, images_dict):
    """Affiche l'image du plat ou une image par défaut si non trouvée."""
    image_path = f'images/{images_dict.get(plat, "default.jpg")}'
    if not os.path.exists(image_path):
        image_path = "images/default.jpg"  # image par défaut
    st.image(image_path, use_container_width=True)

# --- Chargement des données ---
recettes, ingredients = load_data()
if recettes is None or ingredients is None:
    st.stop()  # Arrête l'exécution en cas d'erreur

# --- Gestion des images ---
images_plats = {
    "Savoyarde S": "savoyarde.jpg",
    "Norvegienne S": "norvegienne.jpg",
    "Normande S": "normande.jpg",
    "Raclette S": "raclette.jpg",
    "4 fromages S": "4fromages.jpg",
    "Hanna S": "hanna.jpg",
    "Truffe S": "pizza_truffe.webp",
}

# --- Sélection du plat ---
plat = st.selectbox("🍕 Sélectionnez un plat", recettes["plat"])

# --- Filtrage et Calcul des Coûts ---
ingr_plat = ingredients[ingredients['plat'] == plat].copy()
ingr_plat = calculer_cout(ingr_plat)

cout_total = ingr_plat["Coût (€)"].sum()
coeff_surplus = st.slider("Coefficient de surplus", min_value=1.0, max_value=2.0, value=1.25, step=0.05)
cout_total_genereux = cout_total * coeff_surplus

# --- Définition du type de plat ---
if "pizza" in plat.lower():
    type_plat = "Coût total pour une pizza"
elif "panini" in plat.lower():
    type_plat = "Coût total pour un panini"
elif "salade" in plat.lower():
    type_plat = "Coût total pour une salade"
elif "pâtes" in plat.lower() or "pasta" in plat.lower():
    type_plat = "Coût total pour une assiette de pâtes"
else:
    type_plat = "Coût total du plat"

# --- Affichage du Titre et de l'Image ---
st.markdown(f"<h2 style='text-align: left; color: #D92332;'>{plat}</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])
with col1:
    afficher_image_plat(plat, images_plats)

with col2:
    st.markdown(
        f"""
        <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
            <div style='background-color:#F8F9FA; padding:15px; border-radius:10px; width: 48%; text-align: center;'>
                <strong>💰 Coût total du plat</strong><br><span style='font-size: 22px;'>{cout_total:.2f} €</span>
            </div>
            <div style='background-color:#F8F9FA; padding:15px; border-radius:10px; width: 48%; text-align: center;'>
                <strong>🧀 Coût généreux (avec surplus)</strong><br><span style='font-size: 22px;'>{cout_total_genereux:.2f} €</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# --- Affichage du Tableau des Ingrédients ---
st.subheader("🍅 Composition de la recette")
st.dataframe(
    ingr_plat[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]]
    .rename(columns={
        "ingredient": "Ingrédient",
        "quantite_g": "Quantité (g)",
        "prix_kg": "Prix au kg (€)"
    }),
    use_container_width=True, hide_index=True
)

# --- Graphique de Répartition des Coûts ---
st.subheader("📊 Répartition des coûts")
fig = px.pie(ingr_plat, values="Coût (€)", names="ingredient",
             title="Répartition des coûts par ingrédient", hole=0.3)
st.plotly_chart(fig, use_container_width=True)

# --- Graphique en Barres (Supplémentaire) ---
# st.subheader("📊 Coût par ingrédient")
# fig_bar = px.bar(ingr_plat, x="ingredient", y="Coût (€)",
#                  title="Coût par ingrédient", labels={"ingredient": "Ingrédient", "Coût (€)": "Coût en €"})
# st.plotly_chart(fig_bar, use_container_width=True)
