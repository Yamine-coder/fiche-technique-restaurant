"""
Utilitaires de traitement de texte
"""

import unicodedata
import pandas as pd


def normalize_label(value: str) -> str:
    """
    Normalise un libellé pour faciliter les correspondances.
    
    Transformations :
    - Suppression des accents
    - Conversion en minuscules
    - Normalisation des espaces
    - Normalisation des apostrophes et tirets
    
    Args:
        value: Chaîne à normaliser
        
    Returns:
        Chaîne normalisée (sans accents, minuscules, espaces normalisés)
        
    Example:
        >>> normalize_label("Chèvre-Miel S")
        'chevre miel s'
    """
    if not isinstance(value, str):
        return ""
    
    # Normalisation Unicode (suppression des accents)
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ASCII", "ignore").decode("ASCII")
    
    # Normalisation des caractères spéciaux
    ascii_value = ascii_value.replace("'", "'")
    ascii_value = ascii_value.replace("-", " ")
    
    # Conversion en minuscules
    ascii_value = ascii_value.lower()
    
    # Normalisation des espaces
    ascii_value = " ".join(ascii_value.split())
    
    return ascii_value


def generer_detailed_breakdown(plat: str, composition_finale: pd.DataFrame, 
                               cout_matiere: float, prix_affiche: float) -> str:
    """
    Génère une chaîne de texte expliquant le calcul détaillé du coût d'un plat.
    
    Args:
        plat: Nom du plat
        composition_finale: DataFrame avec colonnes 'ingredient' et 'Coût (€)'
        cout_matiere: Coût total de la matière (ingrédients + pâte)
        prix_affiche: Prix de vente affiché (non utilisé dans le calcul actuel)
        
    Returns:
        Chaîne de caractères formatée en Markdown avec le détail des coûts
        
    Example:
        >>> breakdown = generer_detailed_breakdown("Pizza Margherita", df, 2.50, 8.00)
        >>> print(breakdown)
        **Détails du calcul pour Pizza Margherita**
        
        - Tomate: 0.50 €
        - Mozzarella: 1.20 €
        ...
    """
    breakdown = f"**Détails du calcul pour {plat}**\n\n"
    for idx, row in composition_finale.iterrows():
        breakdown += f"- {row['ingredient']}: {row['Coût (€)']:.2f} €\n"
    breakdown += f"\n**Coût Matière (ingrédients + pâte)**: {cout_matiere:.2f} €\n"
    return breakdown
