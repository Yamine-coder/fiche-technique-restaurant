"""
Module des vues de l'application.
Contient les 4 vues principales : Vue d'ensemble, Analyse d'un plat, Analyse comparative, Modifier un plat.
"""

from .overview_view import render_overview_view
from .dish_analysis_view import render_dish_analysis_view
from .comparative_view import render_comparative_view
# from .edit_dish_view import render_edit_dish_view  # TODO: Debug SyntaxError Streamlit Cloud

__all__ = [
    "render_overview_view",
    "render_dish_analysis_view", 
    "render_comparative_view",
    # "render_edit_dish_view",
]
