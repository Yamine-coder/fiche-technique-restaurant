"""
Calculateur de coûts et marges
"""

import pandas as pd
from config import TVA_MP
from modules.data import COUT_PATE


# ============================================================================
# CALCUL DES MARGES
# ============================================================================

def calculate_margin_rate(plat: dict, taux_tva: float) -> float:
    """
    Calcule le taux de marge d'un plat (toujours en HT).
    
    Args:
        plat: Dictionnaire contenant la composition et le prix du plat
        taux_tva: Taux de TVA de vente (ex: 0.10 pour 10%)
        
    Returns:
        Taux de marge en pourcentage
        
    Example:
        >>> plat = {
        ...     "composition": [...],
        ...     "prix_affiche": 13.90
        ... }
        >>> calculate_margin_rate(plat, 0.10)
        68.5
    """
    try:
        ingr = pd.DataFrame(plat["composition"])
        
        # Calculer le coût si pas déjà fait
        if "Coût (€)" not in ingr.columns:
            ingr["Coût (€)"] = (ingr["prix_kg"] * ingr["quantite_g"]) / 1000
        
        cout_matiere = ingr["Coût (€)"].sum()
        prix_ttc = plat.get('prix_affiche', 0)
        
        # Toujours calculer en HT
        prix_ht = prix_ttc / (1 + taux_tva)
        marge = prix_ht - cout_matiere
        
        return (marge / prix_ht * 100) if prix_ht > 0 else 0
        
    except Exception:
        return 0


# ============================================================================
# CALCUL DES COÛTS D'INGRÉDIENTS
# ============================================================================

def calculer_cout(ingredients_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule le coût des ingrédients en retirant la TVA matière première.
    
    Args:
        ingredients_df: DataFrame avec colonnes prix_kg, quantite_g, ingredient
        
    Returns:
        DataFrame avec colonne "Coût (€)" ajoutée/mise à jour
        
    Note:
        - Retire la TVA matière première (5,5%)
        - Gère les cas spéciaux de pâte à panini et pizza
    """
    if "prix_kg" not in ingredients_df.columns or "quantite_g" not in ingredients_df.columns:
        return ingredients_df

    df = ingredients_df.copy()

    # Identifier les ingrédients spéciaux (pâtes)
    reference_col = "ingredient_original" if "ingredient_original" in df.columns else "ingredient"
    ref_values = df[reference_col].fillna("").str.lower()
    mask_pate_panini = ref_values == "pâte à panini"
    mask_pate_pizza = ref_values == "pâte à pizza"
    mask_special = mask_pate_panini | mask_pate_pizza

    if "Coût (€)" not in df.columns:
        df["Coût (€)"] = 0.0

    # Convertir les prix TTC en HT (retirer la TVA 5,5%)
    prix_ht = df["prix_kg"] / (1 + TVA_MP)
    df["prix_kg_ht"] = prix_ht

    # Recalculer les coûts pour les ingrédients non spéciaux
    df.loc[~mask_special, "Coût (€)"] = (
        prix_ht[~mask_special] * df.loc[~mask_special, "quantite_g"]
    ) / 1000

    # S'assurer que la pâte à panini a toujours un coût fixe
    if mask_pate_panini.any():
        df.loc[mask_pate_panini, "Coût (€)"] = COUT_PATE["panini"]

    # S'assurer que la pâte à pizza a le bon coût
    if mask_pate_pizza.any():
        for idx in df.index[mask_pate_pizza]:
            if df.loc[idx, "Coût (€)"] == 0:
                df.loc[idx, "Coût (€)"] = COUT_PATE["S"]  # Coût par défaut

    return df


# ============================================================================
# COÛT DE LA PÂTE
# ============================================================================

def get_dough_cost(plat: str) -> float:
    """
    Renvoie le coût de la pâte selon le type de plat.
    
    Args:
        plat: Nom du plat
        
    Returns:
        Coût de la pâte en euros
        
    Règles:
        - Pizzas Burrata → 0.12€
        - Pains → 0.10€
        - Panini pizz → 0.12€
        - Plats finissant par S → 0.12€
        - Plats finissant par M → 0.20€
        - Autres (pâtes, salades) → 0.00€
        
    Example:
        >>> get_dough_cost("Savoyarde S")
        0.12
        >>> get_dough_cost("Normande M")
        0.20
        >>> get_dough_cost("Bolognaise")
        0.0
    """
    plat_low = plat.lower()
    
    # Cas pizzas Burrata
    if plat_low.startswith("pizza burrata di parma") or plat_low.startswith("pizza burrata di salmone"):
        return COUT_PATE["burrata"]
    
    # Cas pains
    if "pain aux herbes et mozzarella" in plat_low or "pain aux herbes" in plat_low:
        return COUT_PATE["pain"]
    
    # Cas panini
    if plat_low == "panini pizz":
        return COUT_PATE["panini"]
    
    # Cas pizzas par taille
    if plat.endswith("S"):
        return COUT_PATE["S"]
    elif plat.endswith("M"):
        return COUT_PATE["M"]
    
    # Défaut (pâtes, salades, etc.)
    return COUT_PATE["default"]
