"""
Module des composants UI réutilisables.
Contient tous les éléments d'interface (headers, cards, insights, chatbot, etc.).
"""

from .headers import render_view_header
from .insights import render_overview_insights
from .simulators import render_global_simulator, render_decision_simulator
from .images import afficher_image_plat
from .chatbot import render_floating_chatbot

__all__ = [
    "render_view_header",
    "render_overview_insights",
    "render_global_simulator",
    "render_decision_simulator",
    "afficher_image_plat",
    "render_floating_chatbot",
]
