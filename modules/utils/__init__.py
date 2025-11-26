"""
Module utils - Utilitaires (data, images, texte)
"""

from .data_manager import load_data, load_drafts, save_drafts, autosave_plat
from .image_helpers import (
    get_plat_image_filename,
    get_plat_image_path,
    get_image_data_uri,
)
from .text_helpers import normalize_label, generer_detailed_breakdown

__all__ = [
    # Data manager
    'load_data',
    'load_drafts',
    'save_drafts',
    'autosave_plat',
    # Image helpers
    'get_plat_image_filename',
    'get_plat_image_path',
    'get_image_data_uri',
    # Text helpers
    'normalize_label',
    'generer_detailed_breakdown',
]

