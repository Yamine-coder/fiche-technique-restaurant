"""
Composant pour l'affichage des images de plats.
"""

import streamlit as st
from modules.utils import get_plat_image_path


def afficher_image_plat(plat: str, images_dict: dict):
    """
    Affiche l'image du plat ou l'image par défaut.
    
    Args:
        plat: Nom du plat
        images_dict: Dictionnaire des images (non utilisé, conservé pour compatibilité)
    """
    image_path = get_plat_image_path(plat)
    if image_path:
        st.image(image_path, use_container_width=True)
