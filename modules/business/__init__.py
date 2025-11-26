"""
Module business - Logique métier (calculs, coûts, marges, optimisations)
"""

from .cost_calculator import (
    calculate_margin_rate,
    calculer_cout,
    get_dough_cost,
)

__all__ = [
    'calculate_margin_rate',
    'calculer_cout',
    'get_dough_cost',
]

