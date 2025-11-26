"""
Module styles - Gestion du CSS de l'application
"""

from .app_styles import (
    inject_global_styles,
    inject_creative_header_styles,
    inject_all_styles,
    ensure_css_once
)

__all__ = [
    'inject_global_styles',
    'inject_creative_header_styles', 
    'inject_all_styles',
    'ensure_css_once'
]
