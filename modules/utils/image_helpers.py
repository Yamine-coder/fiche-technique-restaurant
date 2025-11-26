"""
Utilitaires de gestion des images
"""

import base64
import os
from functools import lru_cache

from modules.data import IMAGES_PLATS, IMAGE_FALLBACK
from modules.utils.text_helpers import normalize_label


# Lookup normalisé pour recherche rapide
IMAGES_PLATS_LOOKUP = {
    normalize_label(name): filename 
    for name, filename in IMAGES_PLATS.items()
}


def get_plat_image_filename(plat_nom: str) -> str:
    """
    Retourne le nom de fichier image associé au plat.
    
    Args:
        plat_nom: Nom du plat
        
    Returns:
        Nom du fichier image (ex: "savoyarde.webp")
        Si non trouvé, retourne IMAGE_FALLBACK
        
    Example:
        >>> get_plat_image_filename("Savoyarde S")
        'savoyarde.webp'
    """
    # Recherche avec normalisation
    normalized_name = normalize_label(plat_nom)
    filename = IMAGES_PLATS_LOOKUP.get(normalized_name)
    
    # Tentative sans la taille (S/M) si pas trouvé
    if filename is None and normalized_name.endswith((" s", " m")):
        filename = IMAGES_PLATS_LOOKUP.get(normalized_name[:-2].strip())
    
    # Fallback sur logo par défaut
    if not filename:
        filename = IMAGE_FALLBACK
    
    return filename


def get_plat_image_path(plat_nom: str) -> str:
    """
    Construit le chemin complet du fichier image pour un plat.
    
    Args:
        plat_nom: Nom du plat
        
    Returns:
        Chemin complet vers l'image (ex: "images/savoyarde.webp")
        Si le fichier n'existe pas, retourne le chemin du logo de fallback
        
    Example:
        >>> get_plat_image_path("Savoyarde S")
        'images/savoyarde.webp'
    """
    filename = get_plat_image_filename(plat_nom)
    candidate_path = os.path.join("images", filename)
    
    # Vérifie que le fichier existe
    if os.path.exists(candidate_path):
        return candidate_path
    
    # Fallback sur logo
    fallback_path = os.path.join("images", IMAGE_FALLBACK)
    return fallback_path if os.path.exists(fallback_path) else ""


@lru_cache(maxsize=256)
def get_image_data_uri(image_path: str) -> str:
    """
    Encode une image en data URI pour affichage HTML inline.
    
    Args:
        image_path: Chemin vers le fichier image
        
    Returns:
        Data URI de l'image (base64)
        Chaîne vide si l'image n'existe pas
        
    Note:
        Utilise un cache LRU pour optimiser les performances
        
    Example:
        >>> get_image_data_uri("images/savoyarde.webp")
        'data:image/webp;base64,UklGRiQAAABXRUJQ...'
    """
    if not image_path or not os.path.exists(image_path):
        return ""
    
    # Détection du type MIME
    mime_by_ext = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
    }
    
    ext = os.path.splitext(image_path)[1].lower()
    mime_type = mime_by_ext.get(ext, "image/png")
    
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime_type};base64,{data}"
    except Exception:
        return ""
