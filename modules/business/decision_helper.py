"""
Module d'aide à la décision pour l'analyse de rentabilité.

Ce module fournit des fonctions pour préparer les données nécessaires
aux recommandations du chatbot décisionnel.
"""

from typing import Any, Dict
import pandas as pd

from config import TVA_VENTE
from modules.business.cost_calculator import calculer_cout


def build_decision_playbook(
    df_plats: pd.DataFrame,
    objectif_marge: float,
    ingredients_df: pd.DataFrame,
    objectif_financier: float = 2000.0,
) -> Dict[str, Any]:
    """
    Prépare les chiffres clés pour répondre aux questions du coach décisionnel.
    
    Analyse le plat le plus problématique (marge la plus faible ou en dessous de l'objectif)
    et calcule tous les indicateurs nécessaires pour proposer des recommandations :
    - Volume de vente nécessaire pour atteindre un objectif financier
    - Prix de vente cible pour atteindre la marge souhaitée
    - Réduction de coût nécessaire
    - Ingrédient le plus coûteux
    
    Args:
        df_plats: DataFrame des plats avec colonnes 'nom', 'prix_ht', 'prix_ttc', 
                  'cout_matiere', 'marge_pct'
        objectif_marge: Marge cible en pourcentage (ex: 70 pour 70%)
        ingredients_df: DataFrame des ingrédients avec colonnes 'plat', 'ingredient', 
                        'quantite_g', 'prix_kg'
        objectif_financier: Objectif mensuel de marge en euros (défaut: 2000.0)
    
    Returns:
        Dict contenant les métriques clés :
        - focus_name: Nom du plat à analyser
        - marge_unitaire: Marge unitaire en euros
        - volume_target: Volume mensuel nécessaire (unités)
        - volume_daily: Volume quotidien nécessaire (unités/jour)
        - price_target_ttc: Prix TTC cible pour atteindre la marge
        - price_delta: Différence entre prix actuel et prix cible
        - manque_cout: Réduction de coût nécessaire en euros
        - reduction_pct: Réduction de coût nécessaire en pourcentage
        - top_ingredient: Dict avec 'nom' et 'cout' de l'ingrédient le plus coûteux
        - prix_ttc: Prix TTC actuel
        - cout_matiere: Coût matière actuel
    
    Example:
        >>> playbook = build_decision_playbook(df_plats, 70, ingredients_df, 2000)
        >>> print(f"Plat à optimiser : {playbook['focus_name']}")
        >>> print(f"Volume quotidien nécessaire : {playbook['volume_daily']:.1f} unités")
    """
    default_payload = {
        "focus_name": None,
        "marge_unitaire": None,
        "volume_target": None,
        "volume_daily": None,
        "price_target_ttc": None,
        "price_delta": None,
        "manque_cout": None,
        "reduction_pct": None,
        "top_ingredient": None,
        "prix_ttc": None,
        "cout_matiere": None,
    }

    if df_plats.empty:
        return default_payload

    # Sélectionner le plat le plus problématique
    candidats = df_plats[df_plats["marge_pct"] < objectif_marge]
    if candidats.empty:
        # Si tous les plats atteignent l'objectif, prendre celui avec la marge la plus faible
        focus_row = df_plats.sort_values("marge_pct").head(1)
    else:
        # Prendre le plat avec la marge la plus faible parmi ceux sous l'objectif
        focus_row = candidats.sort_values("marge_pct").head(1)

    if focus_row.empty:
        return default_payload

    row = focus_row.iloc[0]
    
    # Calcul de la marge unitaire et du volume nécessaire
    marge_unitaire = max(row["prix_ht"] - row["cout_matiere"], 0.0)
    volume_target = objectif_financier / marge_unitaire if marge_unitaire > 0 else None
    volume_daily = volume_target / 30 if volume_target else None

    # Calcul du prix de vente cible pour atteindre la marge objectif
    price_target_ht = None
    price_target_ttc = None
    price_delta = None
    if 0 < objectif_marge < 100:
        price_target_ht = row["cout_matiere"] / (1 - objectif_marge / 100)
        price_target_ttc = price_target_ht * (1 + TVA_VENTE)
        price_delta = price_target_ttc - row["prix_ttc"]

    # Calcul de la réduction de coût nécessaire
    cout_cible = row["prix_ht"] * (1 - objectif_marge / 100)
    manque_cout = row["cout_matiere"] - cout_cible
    reduction_pct = (
        (manque_cout / row["cout_matiere"] * 100)
        if row["cout_matiere"] > 0
        else None
    )
 
    # Identification de l'ingrédient le plus coûteux
    top_ingredient = None
    if not ingredients_df.empty:
        plat_ingredients = ingredients_df[
            ingredients_df["plat"].str.lower() == row["nom"].lower()
        ].copy()
        if not plat_ingredients.empty:
            plat_ingredients = calculer_cout(plat_ingredients)
            plat_ingredients = plat_ingredients.sort_values("Coût (€)", ascending=False)
            if not plat_ingredients.empty:
                top_ingredient = {
                    "nom": plat_ingredients["ingredient"].iloc[0],
                    "cout": float(plat_ingredients["Coût (€)"].iloc[0]),
                }

    return {
        "focus_name": row["nom"],
        "marge_unitaire": marge_unitaire,
        "volume_target": volume_target,
        "volume_daily": volume_daily,
        "price_target_ttc": price_target_ttc,
        "price_delta": price_delta,
        "manque_cout": manque_cout,
        "reduction_pct": reduction_pct,
        "top_ingredient": top_ingredient,
        "prix_ttc": row["prix_ttc"],
        "cout_matiere": row["cout_matiere"],
    }
