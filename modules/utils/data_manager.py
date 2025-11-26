"""
Gestionnaire de données (chargement/sauvegarde JSON et Excel)
"""

import json
import os
import pandas as pd
import streamlit as st


# ============================================================================
# GESTION DES BROUILLONS (JSON)
# ============================================================================

def save_drafts(drafts: list, filename: str = "data/brouillons.json") -> None:
    """
    Sauvegarde la liste des brouillons dans un fichier JSON.
    
    Args:
        drafts: Liste des brouillons de plats
        filename: Chemin du fichier JSON
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(drafts, f, indent=2, ensure_ascii=False)


def load_drafts(filename: str = "data/brouillons.json") -> list:
    """
    Charge la liste des brouillons depuis un fichier JSON.
    
    Args:
        filename: Chemin du fichier JSON
        
    Returns:
        Liste des brouillons (vide si le fichier n'existe pas)
    """
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def autosave_plat(plat_data: dict) -> None:
    """
    Sauvegarde automatiquement un plat dans les brouillons.
    
    Si le plat existe déjà (même nom), il sera mis à jour,
    sinon il sera ajouté à la liste.
    
    Args:
        plat_data: Dictionnaire contenant les données du plat
                   Doit contenir au minimum la clé "nom"
                   
    Note:
        Utilise st.session_state.brouillons pour stocker en mémoire
    """
    if not plat_data or "nom" not in plat_data:
        return
    
    # Initialiser les brouillons si nécessaire
    if "brouillons" not in st.session_state:
        st.session_state.brouillons = load_drafts()
    
    # Chercher et mettre à jour le plat existant
    plat_trouve = False
    for i, plat in enumerate(st.session_state.brouillons):
        if plat["nom"] == plat_data["nom"]:
            st.session_state.brouillons[i] = plat_data
            plat_trouve = True
            break
    
    # Ajouter le plat s'il n'existe pas
    if not plat_trouve:
        st.session_state.brouillons.append(plat_data)
    
    # Sauvegarder dans le fichier
    save_drafts(st.session_state.brouillons)


# ============================================================================
# CHARGEMENT DES DONNÉES EXCEL
# ============================================================================

@st.cache_data
def load_data():
    """
    Charge les données des recettes et des ingrédients depuis Excel.
    
    Returns:
        tuple: (recettes_df, ingredients_df) ou (None, None) en cas d'erreur
        
    Note:
        - Utilise le cache Streamlit pour optimiser les performances
        - Unifie les noms des variantes de Panini Pizz
        - Conserve les noms originaux dans la colonne "original_plat"
    """
    try:
        recettes = pd.read_excel("data/recettes_complet_MAJ2.xlsx")
        ingredients = pd.read_excel("data/ingredients_nettoyes_et_standardises.xlsx")
        
        # Stockage du nom original
        recettes["original_plat"] = recettes["plat"]
        ingredients["original_plat"] = ingredients["plat"]

        # Unification des noms pour Panini Pizz
        unification_map = {
            'panini pizz base crème': 'panini pizz',
            'panini pizz base tomate': 'panini pizz'
        }
        
        recettes['plat'] = recettes['plat'].replace(unification_map)
        ingredients['plat'] = ingredients['plat'].replace(unification_map)
        
        return recettes, ingredients
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {e}")
        return None, None
