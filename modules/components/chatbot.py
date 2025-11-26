"""Composant UI du coach guidé, avec vraie bulle de chat à droite."""

import json
from typing import Optional

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from chatbot.chatbot_router import HybridRouter
from modules.data import sales_data
from modules.business.cost_calculator import calculer_cout


def _pick_focus_plat(df_plats: pd.DataFrame, objectif_marge: float):
    """Choisit le plat focus (marge la plus faible sous objectif)."""
    if df_plats is None or df_plats.empty:
        return None
    sous_obj = df_plats[df_plats["marge_pct"] < objectif_marge]
    target_df = sous_obj if not sous_obj.empty else df_plats
    if target_df.empty:
        return None
    return target_df.nsmallest(1, "marge_pct").iloc[0]


def _calculate_price_target(plat_row, objectif_marge: float):
    """Calcule le prix TTC cible pour atteindre l'objectif de marge."""
    cout = plat_row["cout_matiere"]
    prix_ttc_cible = cout / (1 - objectif_marge / 100)
    delta_ttc = prix_ttc_cible - plat_row["prix_ttc"]
    
    class PriceTarget:
        def __init__(self, prix_ttc_cible, delta_ttc):
            self.prix_ttc_cible = prix_ttc_cible
            self.delta_ttc = delta_ttc
    
    return PriceTarget(prix_ttc_cible, delta_ttc)


def _calculate_negotiation_gap(plat_row, objectif_marge: float, ingredients_df):
    """Calcule l'écart à combler par négociation sur l'ingrédient principal."""
    marge_actuelle = plat_row["marge_pct"]
    ecart_marge = objectif_marge - marge_actuelle
    
    if ecart_marge <= 0:
        class NegoResult:
            def __init__(self):
                self.manque_euros = 0.0
                self.reduction_pct = 0.0
                self.focus_ingredient = None
        return NegoResult()
    
    # Calcul du manque en euros
    prix_ht = plat_row["prix_ttc"] / 1.1
    manque_euros = prix_ht * (ecart_marge / 100)
    
    # Trouver l'ingrédient le plus cher
    focus_ingredient = None
    if isinstance(ingredients_df, pd.DataFrame) and not ingredients_df.empty:
        # Le plat peut être dans 'nom' (df_plats) mais ingredients_df utilise 'plat'
        plat_nom = plat_row.get("nom", plat_row.get("plat", ""))
        print(f"[DEBUG _calculate_negotiation_gap] Recherche pour plat: '{plat_nom}'")
        ing_plat = ingredients_df[ingredients_df["plat"].str.lower() == str(plat_nom).lower()]
        print(f"[DEBUG] Ingrédients trouvés: {len(ing_plat)}")
        if not ing_plat.empty and "Coût (€)" in ing_plat.columns:
            focus_ingredient = ing_plat.nlargest(1, "Coût (€)").iloc[0]["ingredient"]
            print(f"[DEBUG] Focus ingredient: '{focus_ingredient}'")
    
    # Calculer % de réduction nécessaire
    cout_total = plat_row["cout_matiere"]
    reduction_pct = (manque_euros / cout_total * 100) if cout_total > 0 else 0
    
    class NegoResult:
        def __init__(self, manque_euros, reduction_pct, focus_ingredient):
            self.manque_euros = manque_euros
            self.reduction_pct = reduction_pct
            self.focus_ingredient = focus_ingredient
    
    return NegoResult(manque_euros, reduction_pct, focus_ingredient)


def _build_guided_data(
    df_plats: pd.DataFrame,
    ingredients_df: pd.DataFrame,
    objectif_marge: float,
) -> dict:
    """Construit les données pour le chatbot guidé conversationnel.
    
    Retourne :
    - Liste des plats pour sélection
    - Plat focus suggéré
    - Données de diagnostic pour chaque plat
    """
    
    print(f"[DEBUG _build_guided_data] DÉBUT - df_plats: {len(df_plats) if df_plats is not None else 0}, ingredients: {len(ingredients_df) if ingredients_df is not None else 0}")
    
    if df_plats is None or df_plats.empty:
        return {"plats": [], "focus": None, "diagnostics": {}}
    
    # IMPORTANT: Calculer les coûts pour TOUS les ingrédients au début
    # Car _calculate_negotiation_gap a besoin de la colonne "Coût (€)"
    if isinstance(ingredients_df, pd.DataFrame) and not ingredients_df.empty:
        print(f"[DEBUG] Calcul des coûts pour tous les ingrédients...")
        ingredients_df = calculer_cout(ingredients_df.copy())
        print(f"[DEBUG] Colonnes après calculer_cout: {list(ingredients_df.columns)}")
    
    # Charger les données de ventes depuis SQLite (30 derniers jours)
    try:
        from modules.data.sales_data import load_ventes
        df_sales = load_ventes(nb_jours=30)
        # Renommer les colonnes pour compatibilité avec le code existant
        if not df_sales.empty:
            df_sales = df_sales.rename(columns={'produit': 'plat', 'quantite': 'quantite_totale'})
    except Exception as e:
        print(f"[WARN] Impossible de charger les ventes SQLite: {e}")
        df_sales = pd.DataFrame()
    
    focus_row = _pick_focus_plat(df_plats, objectif_marge)
    focus_name = str(focus_row["nom"]) if focus_row is not None else ""
    
    plats_list = sorted(df_plats["nom"].dropna().unique().tolist())
    
    # Préparer diagnostics pour chaque plat
    diagnostics = {}
    for plat_nom in plats_list:
        plat_row = df_plats[df_plats["nom"] == plat_nom].iloc[0]
        
        # Calculs métier
        price_target = _calculate_price_target(plat_row, objectif_marge)
        nego = _calculate_negotiation_gap(plat_row, objectif_marge, ingredients_df)
        
        # Calculer les détails de l'ingrédient focus
        focus_cost = 0.0
        focus_pct = 0.0
        focus_kg_annuel = 0.0
        
        if nego.focus_ingredient and isinstance(ingredients_df, pd.DataFrame) and not ingredients_df.empty:
            try:
                # Filtrer les ingrédients pour ce plat (les coûts sont déjà calculés)
                ing_plat = ingredients_df[ingredients_df["plat"].str.lower() == plat_nom.lower()].copy()
                print(f"[DEBUG] Ingrédients filtrés pour '{plat_nom}': {len(ing_plat)} lignes")
                
                if not ing_plat.empty:
                    # Rechercher l'ingrédient focus
                    ing_rows = ing_plat[ing_plat["ingredient"].str.lower() == str(nego.focus_ingredient).lower()]
                    print(f"[DEBUG] Recherche ingrédient '{nego.focus_ingredient}' dans '{plat_nom}': {len(ing_rows)} lignes")
                else:
                    ing_rows = pd.DataFrame()
                    print(f"[DEBUG] Aucun ingrédient trouvé pour '{plat_nom}'")
            except Exception as e:
                print(f"[ERROR] Exception dans _build_guided_data pour '{plat_nom}': {e}")
                ing_rows = pd.DataFrame()
            
            if not ing_rows.empty:
                ing_row = ing_rows.iloc[0]
                
                # Utiliser directement "Coût (€)" qui est maintenant calculé
                focus_cost = float(ing_row.get("Coût (€)", 0))
                
                # Récupérer quantité pour calcul kg annuel
                quantite_g = float(ing_row.get("quantite_g", 0))
                
                # Calculer pourcentage dans le coût total
                focus_pct = float((focus_cost / plat_row["cout_matiere"] * 100) if plat_row["cout_matiere"] > 0 and focus_cost > 0 else 0)
                
                # Calculer consommation annuelle en kg
                volume_annuel = 200 * 12  # Estimation base
                focus_kg_annuel = float(quantite_g / 1000 * volume_annuel) if quantite_g > 0 else 0.0
                
                print(f"[DEBUG] Détails trouvés: cost={focus_cost:.2f}€, pct={focus_pct:.1f}%, kg={focus_kg_annuel:.1f}")
        
        # Récupérer données N-1 pour ce plat depuis SQLite
        n1_data = None
        if not df_sales.empty:
            plat_ventes = df_sales[df_sales['plat'].str.lower() == plat_nom.lower()]
            if not plat_ventes.empty:
                n1_data = {
                    'quantite_totale': plat_ventes['quantite_totale'].sum(),
                    'ca_total': plat_ventes['ca_ttc'].sum()
                }
        
        print(f"[DEBUG] Diagnostic pour '{plat_nom}': focus_ingredient={nego.focus_ingredient}, focus_cost={focus_cost:.2f}, focus_pct={focus_pct:.1f}, focus_kg={focus_kg_annuel:.1f}")
        
        diagnostics[plat_nom] = {
            "marge_pct": float(plat_row["marge_pct"]),
            "prix_ttc": float(plat_row["prix_ttc"]),
            "cout_matiere": float(plat_row["cout_matiere"]),
            "prix_cible": float(price_target.prix_ttc_cible),
            "delta_prix": float(price_target.delta_ttc),
            "manque_euros": float(nego.manque_euros),
            "reduction_pct": float(nego.reduction_pct),
            "focus_ingredient": nego.focus_ingredient or "",
            "focus_cost": focus_cost,
            "focus_pct": focus_pct,
            "focus_kg_annuel": focus_kg_annuel,
            # Données N-1 réelles (depuis SQLite)
            "n1_volume": int(n1_data["quantite_totale"]) if n1_data else 0,
            "n1_ca": float(n1_data["ca_total"]) if n1_data else 0.0,
            "n1_ca_ht": float(n1_data["ca_total"] / 1.055) if n1_data else 0.0,
            "n1_prix_moyen": float(n1_data["ca_total"] / n1_data["quantite_totale"]) if n1_data and n1_data["quantite_totale"] > 0 else 0.0,
            # Données d'évolution N-1 → Current (non disponibles pour l'instant)
            "volume_n1": int(n1_data["quantite_totale"]) if n1_data else 0,
            "volume_current": int(n1_data["quantite_totale"]) if n1_data else 0,
            "evolution_pct": 0.0,
        }
    
    return {
        "plats": plats_list,
        "focus": focus_name,
        "diagnostics": diagnostics,
        "objectif": float(objectif_marge),
    }


def render_floating_chatbot(
    df_plats: pd.DataFrame, ingredients_df: pd.DataFrame, objectif_marge: float
) -> None:
    """Affiche une bulle de chat fixe + panneau à d roite, style chatbot.

    Visuellement : bulle en bas à droite ; au clic, panneau "Assistant marge".
    Les réponses rapides utilisent la même logique métier que le coach guidé.
    """

    # Debug: toujours afficher même si vide pour tester
    if df_plats is None or df_plats.empty:
        # Créer des données minimales pour debug
        df_plats = pd.DataFrame([{
            "nom": "Test Plat",
            "marge_pct": 50.0,
            "prix_ht": 10.0,
            "prix_ttc": 12.0,
            "cout_matiere": 5.0,
        }])

    plats_problemes = df_plats[df_plats["marge_pct"] < objectif_marge]
    nb_problemes = int(len(plats_problemes))
    marge_moy = float(df_plats["marge_pct"].mean()) if not df_plats.empty else 0.0

    guided_data = _build_guided_data(df_plats, ingredients_df, objectif_marge)
    
    # Charger statistiques depuis SQLite (30 derniers jours)
    try:
        from modules.data.sales_data import load_ventes
        df_sales = load_ventes(nb_jours=30)
        if not df_sales.empty:
            ca_total = df_sales['ca_ttc'].sum()
            volume_total = df_sales['quantite'].sum()
            sales_stats = {
                'ca_total': ca_total,
                'volume_total': volume_total
            }
        else:
            sales_stats = None
    except Exception as e:
        print(f"[WARN] Erreur chargement stats ventes: {e}")
        sales_stats = None
    
    # Préparer résumé pour affichage
    n1_info = ""
    if sales_stats:
        ca_total = sales_stats['ca_total']
        volume_total = sales_stats['volume_total']
        n1_info = f" : {ca_total:,.0f}€ CA sur {volume_total:,.0f} produits vendus (30j)"

    stats = {
        "nbProblems": nb_problemes,
        "objectif": round(objectif_marge, 1),
        "margeMoy": round(marge_moy, 1),
        "hasN1": sales_stats is not None,
        "n1Info": n1_info,
    }

    css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    :root {
        --chat-primary: #D92332;
        --chat-primary-hover: #b41c29;
        --chat-primary-light: rgba(217, 35, 50, 0.1);
        --chat-primary-lighter: rgba(217, 35, 50, 0.05);
        --neutral-50: #f8fafc;
        --neutral-100: #f1f5f9;
        --neutral-200: #e2e8f0;
        --neutral-300: #cbd5e1;
        --neutral-500: #64748b;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1e293b;
        --neutral-900: #0f172a;
        --success: #22c55e;
        --warning: #f59e0b;
    }
    
    #coach-chatbot-root {
        position: fixed;
        inset: 0;
        pointer-events: none;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
        z-index: 9999;
    }
    
    .coach-chatbot-floating {
        position: fixed;
        bottom: calc(24px + env(safe-area-inset-bottom, 0px));
        right: 24px;
        z-index: 10000;
        pointer-events: none;
    }
    
    .coach-chatbot-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 64px;
        height: 64px;
        border-radius: 50%;
        border: none;
        background: linear-gradient(135deg, #D92332 0%, #b91c28 100%);
        color: #ffffff;
        box-shadow: 0 6px 20px rgba(217, 35, 50, 0.4), 0 0 0 4px rgba(217, 35, 50, 0.1);
        cursor: pointer;
        pointer-events: auto;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
    }
    
    .coach-chatbot-button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 10px 30px rgba(217, 35, 50, 0.5), 0 0 0 6px rgba(217, 35, 50, 0.15);
    }
    
    .coach-chatbot-button:active {
        transform: translateY(-2px) scale(1.02);
    }
    
    .coach-button-icon {
        width: 24px;
        height: 24px;
        color: inherit;
    }
    
    .coach-alert-badge {
        position: absolute;
        top: -2px;
        right: -2px;
        min-width: 22px;
        height: 22px;
        padding: 0 6px;
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
        border: 3px solid #ffffff;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
        animation: pulse-badge 2s infinite;
    }
    
    @keyframes pulse-badge {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .coach-chatbot-button[data-has-alerts="false"] .coach-alert-badge {
        background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
        animation: none;
        box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
    }
    .coach-chatbot-panel {
        position: absolute;
        right: 0;
        bottom: 80px;
        width: min(420px, calc(100vw - 40px));
        max-height: min(85vh, 700px);
        background: linear-gradient(to bottom, var(--neutral-50) 0%, #ffffff 100%);
        border-radius: 24px;
        box-shadow: 0 25px 60px rgba(15, 23, 42, 0.3), 0 0 0 1px rgba(203, 213, 225, 0.5);
        pointer-events: auto;
        opacity: 0;
        transform: translateY(20px) scale(0.95);
        transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .coach-chatbot-panel--open {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
    .coach-chatbot-panel__header {
        padding: 1.25rem 1.5rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        display: flex;
        align-items: center;
        gap: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, var(--neutral-50) 100%);
        flex-shrink: 0;
        backdrop-filter: blur(10px);
    }
    
    .coach-logo {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #D92332 0%, #b41c29 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(217, 35, 50, 0.25);
    }
    
    .coach-logo svg {
        width: 22px;
        height: 22px;
        color: #ffffff;
    }
    
    .coach-header-text {
        flex: 1;
        min-width: 0;
    }
    
    .coach-header-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--neutral-900);
        letter-spacing: -0.01em;
        margin: 0;
    }
    
    .coach-header-sub {
        font-size: 0.75rem;
        color: var(--neutral-500);
        margin-top: 3px;
        line-height: 1.4;
    }
    
    .coach-header-close {
        background: transparent;
        border: none;
        color: #94a3b8;
        cursor: pointer;
        padding: 0.375rem;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 6px;
        transition: all 0.2s ease;
        margin-left: auto;
        flex-shrink: 0;
    }
    
    .coach-header-close svg {
        width: 16px;
        height: 16px;
    }
    
    .coach-header-close:hover {
        background: var(--neutral-100);
        color: var(--neutral-500);
    }
    .coach-chat-history {
        flex: 1;
        padding: 1.25rem 1rem;
        overflow-y: auto;
        background: linear-gradient(to bottom, var(--neutral-50) 0%, #ffffff 100%);
        display: flex;
        flex-direction: column;
        gap: 0.875rem;
    }
    
    .coach-chat-history::-webkit-scrollbar {
        width: 6px;
    }
    
    .coach-chat-history::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .coach-chat-history::-webkit-scrollbar-thumb {
        background: var(--neutral-300);
        border-radius: 10px;
    }
    
    .coach-chat-history::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    .coach-chat-message {
        display: flex;
        align-items: flex-start;
        gap: 0.625rem;
        animation: slideInMessage 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes slideInMessage {
        from { opacity: 0; transform: translateY(15px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    .coach-chat-message.bot {
        flex-direction: row;
    }
    
    .coach-chat-message.user {
        flex-direction: row-reverse;
    }
    
    .chat-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
    
    .chat-avatar.bot {
        background: linear-gradient(135deg, #D92332 0%, #b41c29 100%);
        color: #ffffff;
    }
    
    .chat-avatar.user {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
    }
    
    .chat-bubble {
        padding: 0.875rem 1.125rem;
        border-radius: 18px;
        font-size: 0.9rem;
        line-height: 1.5;
        max-width: 75%;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        word-wrap: break-word;
    }
    
    .coach-chat-message.bot .chat-bubble {
        background: #ffffff;
        color: var(--neutral-800);
        border-bottom-left-radius: 6px;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .coach-chat-message.user .chat-bubble {
        background: linear-gradient(135deg, #D92332 0%, #b41c29 100%);
        color: #ffffff;
        border-bottom-right-radius: 6px;
    }
    .coach-chat-quick {
        padding: 0.9rem 1rem;
        border-top: 1px solid var(--neutral-200);
        background: #ffffff;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        max-height: 240px;
        overflow-y: auto;
        flex-shrink: 0;
    }
    
    .coach-chat-quick::-webkit-scrollbar {
        width: 6px;
    }
    
    .coach-chat-quick::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .coach-chat-quick::-webkit-scrollbar-thumb {
        background: var(--neutral-300);
        border-radius: 10px;
    }
    
    .coach-chat-quick button {
        border-radius: 10px;
        border: 1.5px solid var(--neutral-200);
        padding: 0.7rem 0.85rem;
        font-size: 0.83rem;
        background: #ffffff;
        cursor: pointer;
        text-align: left;
        color: var(--neutral-700);
        transition: all 0.2s ease;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        line-height: 1.3;
    }
    
    .coach-chat-quick button:hover {
        border-color: #D92332;
        background: rgba(217, 35, 50, 0.02);
    }
    .coach-chat-input {
        padding: 0.85rem 1rem;
        display: flex;
        gap: 0.5rem;
        background: var(--neutral-50);
        border-top: 1px solid var(--neutral-200);
        flex-shrink: 0;
    }
    
    .coach-chat-input input {
        flex: 1;
        border-radius: 20px;
        border: 1.5px solid var(--neutral-200);
        padding: 0.6rem 0.95rem;
        font-size: 0.85rem;
        background: #ffffff;
        transition: all 0.2s ease;
    }
    
    .coach-chat-input input:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.08);
    }
    
    .coach-chat-input button {
        background: #D92332;
        border: none;
        color: #ffffff;
        border-radius: 8px;
        width: 40px;
        height: 40px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    
    .coach-chat-input button svg {
        width: 20px;
        height: 20px;
    }
    
    .coach-chat-input button:hover {
        background: #b41c29;
    }
    
    /* Sliders */
    input[type="range"] {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        height: 10px;
        border-radius: 5px;
        outline: none;
        cursor: pointer;
    }
    
    input[type="range"]::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #ffffff;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        border: 3px solid #667eea;
        transition: all 0.2s ease;
    }
    
    input[type="range"]::-webkit-slider-thumb:hover {
        transform: scale(1.15);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    input[type="range"]::-webkit-slider-thumb:active {
        transform: scale(1.05);
    }
    
    input[type="range"]::-moz-range-thumb {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #ffffff;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        border: 3px solid #667eea;
        transition: all 0.2s ease;
    }
    
    input[type="range"]::-moz-range-thumb:hover {
        transform: scale(1.15);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .coach-chatbot-floating {
            right: 16px;
            bottom: calc(16px + env(safe-area-inset-bottom, 0px));
        }
        
        .coach-chatbot-button {
            width: 56px;
            height: 56px;
        }
        
        .coach-button-icon {
            font-size: 1.5rem;
        }
        
        .coach-chatbot-panel {
            width: calc(100vw - 32px);
            max-height: min(85vh, 600px);
            bottom: 76px;
            border-radius: 20px;
        }
        
        .coach-chat-quick {
            padding: 0.9rem 1rem;
        }
        
        .coach-chat-input {
            padding: 0.9rem 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .coach-chatbot-panel {
            max-height: calc(100vh - 100px);
        }
        
        .coach-header-title {
            font-size: 0.95rem;
        }
        
        .coach-header-sub {
            font-size: 0.75rem;
        }
    }
    """.strip()

    html_markup = """
    <div class="coach-chatbot-floating">
        <button id="coachChatbotButton" type="button" class="coach-chatbot-button" aria-haspopup="dialog" aria-expanded="false">
            <svg class="coach-button-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-4 4v-4z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="coach-alert-badge" data-role="alert-badge">0</div>
        </button>
        <div id="coachChatbotPanel" class="coach-chatbot-panel" aria-label="Assistant décisionnel">
            <div class="coach-chatbot-panel__header">
                <svg class="coach-logo" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" stroke="#D92332" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <div class="coach-header-text">
                    <div class="coach-header-title">Assistant Décisionnel</div>
                    <div class="coach-header-sub" data-role="summary"></div>
                </div>
                <button class="coach-header-close" type="button" data-role="close">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6 18L18 6M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
            <div class="coach-chat-history" data-role="history"></div>
            <div class="coach-chat-quick" data-role="quick"></div>
            <div class="coach-chat-input">
                <input type="text" placeholder="Posez votre question..." data-role="input" />
                <button type="button" data-role="send">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
    """.strip()

    # Préparer toutes les données en JSON côté Python pour éviter les problèmes d'échappement
    css_json = json.dumps(css)
    html_json = json.dumps(html_markup)
    guided_json = json.dumps(guided_data, ensure_ascii=True)
    stats_json = json.dumps(stats, ensure_ascii=True)
    
    script = f"""
    <script>
    (function() {{
      try {{
        let doc = document;
        let parentDoc = null;
        try {{
          if (window.parent && window.parent !== window && window.parent.document) {{
            parentDoc = window.parent.document;
          }}
        }} catch (err) {{
          console.warn('Chatbot: parent inaccessible, fallback iframe', err);
        }}
        if (parentDoc) {{
          doc = parentDoc;
        }}
        const existingRoot = doc.getElementById('coach-chatbot-root');
        if (existingRoot) existingRoot.remove();

        const styleId = 'coach-chatbot-style';
        if (!doc.getElementById(styleId)) {{
          const style = doc.createElement('style');
          style.id = styleId;
          style.textContent = {css_json};
          doc.head.appendChild(style);
        }}

        const container = doc.createElement('div');
        container.id = 'coach-chatbot-root';
        container.innerHTML = {html_json};
        doc.body.appendChild(container);

        const button = doc.getElementById('coachChatbotButton');
        const panel = doc.getElementById('coachChatbotPanel');
        if (!button || !panel) {{
          console.error('❌ Chatbot: Éléments introuvables');
          return;
        }}

      const history = panel.querySelector('[data-role="history"]');
      const quickZone = panel.querySelector('[data-role="quick"]');
      const input = panel.querySelector('[data-role="input"]');
      const sendBtn = panel.querySelector('[data-role="send"]');
      const closeBtn = panel.querySelector('[data-role="close"]');
      const summary = panel.querySelector('[data-role="summary"]');
      const alertBadge = button.querySelector('[data-role="alert-badge"]');

      const guided = {guided_json};
      const stats = {stats_json};
      
      let currentStep = 'welcome';
      let selectedPlat = null;

      const openPanel = () => {{
        panel.classList.add('coach-chatbot-panel--open');
        button.setAttribute('aria-expanded', 'true');
      }};
      const closePanel = () => {{
        panel.classList.remove('coach-chatbot-panel--open');
        button.setAttribute('aria-expanded', 'false');
      }};

      button.addEventListener('click', () => {{
        const isOpen = panel.classList.contains('coach-chatbot-panel--open');
        if (isOpen) closePanel(); else {{ 
          openPanel();
          // Retirer badge au clic
          if (alertBadge) {{
            button.dataset.hasAlerts = 'false';
          }}
        }}
      }});
      closeBtn.addEventListener('click', () => closePanel());
      
      // Ouvrir automatiquement au chargement après 1 seconde
      setTimeout(() => {{
        openPanel();
      }}, 1000);

      const clearQuickZone = () => {{
        quickZone.innerHTML = '';
      }};

      const appendMessage = (author, text) => {{
        const messageDiv = doc.createElement('div');
        messageDiv.className = 'coach-chat-message ' + (author === 'user' ? 'user' : 'bot');
        
        // Avatar
        const avatar = doc.createElement('div');
        avatar.className = 'chat-avatar ' + (author === 'user' ? 'user' : 'bot');
        avatar.innerHTML = author === 'user' ? '👤' : '🤖';
        
        // Bulle de texte
        const bubble = doc.createElement('div');
        bubble.className = 'chat-bubble';
        bubble.innerHTML = text.replace(/\\n/g, '<br/>');
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        history.appendChild(messageDiv);
        
        // Scroll smooth
        setTimeout(() => {{
          history.scrollTo({{
            top: history.scrollHeight,
            behavior: 'smooth'
          }});
        }}, 100);
      }};

      // Résumé + badge
      summary.textContent = stats.nbProblems + ' plat(s) sous ' + stats.objectif + '% • marge moyenne ' + stats.margeMoy + '%';
      if (alertBadge) {{
        if (stats.nbProblems > 0) {{
          alertBadge.textContent = stats.nbProblems;
          button.dataset.hasAlerts = 'true';
        }} else {{
          alertBadge.textContent = '✓';
          button.dataset.hasAlerts = 'false';
        }}
      }}

      // ===== ÉTAPE 1: SÉLECTION DU PLAT =====
      const showWelcome = () => {{
        currentStep = 'welcome';
        clearQuickZone();
        
        // Message de bienvenue conversationnel
        appendMessage('bot', `Bonjour ! Sélectionnez un plat pour l'analyser.`);
        
        // Compteur compact si problèmes
        if (stats.nbProblems > 0) {{
          const alertDiv = doc.createElement('div');
          alertDiv.style.cssText = 'padding: 0.5rem 0.75rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; font-size: 0.8rem; color: #991b1b; margin-bottom: 0.75rem;';
          alertDiv.innerHTML = '<strong>' + stats.nbProblems + '</strong> plat' + (stats.nbProblems > 1 ? 's' : '') + ' sous objectif (' + stats.objectif + '%)';
          quickZone.appendChild(alertDiv);
        }}
        
        // Trier plats par priorité
        const platsSorted = [...guided.plats].sort((a, b) => {{
          const diagA = guided.diagnostics[a];
          const diagB = guided.diagnostics[b];
          return (diagA?.marge_pct || 100) - (diagB?.marge_pct || 100);
        }});
        
        // Barre de recherche
        const searchContainer = doc.createElement('div');
        searchContainer.style.cssText = 'margin-bottom: 0.75rem;';
        
        const searchInput = doc.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Rechercher un plat...';
        searchInput.style.cssText = 'width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 0.85rem; background: #ffffff;';
        
        searchContainer.appendChild(searchInput);
        quickZone.appendChild(searchContainer);
        
        // Liste compacte style table
        const listContainer = doc.createElement('div');
        listContainer.style.cssText = 'display: flex; flex-direction: column; gap: 0; max-height: 360px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 8px; background: #ffffff;';
        
        platsSorted.forEach((plat, index) => {{
          const diag = guided.diagnostics[plat];
          if (!diag) return;
          
          const isUrgent = diag.marge_pct < stats.objectif;
          
          const platBtn = doc.createElement('button');
          platBtn.type = 'button';
          platBtn.dataset.platName = plat.toLowerCase();
          platBtn.style.cssText = 
            'padding: 0.65rem 0.875rem; ' +
            'background: #ffffff; ' +
            'border: none; ' +
            'border-bottom: 1px solid #f1f5f9; ' +
            'text-align: left; cursor: pointer; transition: all 0.15s ease; ' +
            'display: flex; align-items: center; gap: 0.75rem;';
          
          const statusDot = '<div style="width: 6px; height: 6px; border-radius: 50%; background: ' + (isUrgent ? '#D92332' : '#22c55e') + '; flex-shrink: 0;"></div>';
          
          platBtn.innerHTML = 
            statusDot +
            '<div style="flex: 1; min-width: 0; display: flex; align-items: center; justify-content: space-between; gap: 0.75rem;">' +
            '<span style="font-weight: 500; color: #1e293b; font-size: 0.875rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + plat + '</span>' +
            '<div style="display: flex; align-items: center; gap: 0.5rem; flex-shrink: 0;">' +
            '<span style="font-size: 0.8rem; font-weight: 600; color: ' + (isUrgent ? '#D92332' : '#22c55e') + ';">' + diag.marge_pct.toFixed(1) + '%</span>' +
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg>' +
            '</div>' +
            '</div>';
          
          if (index === platsSorted.length - 1) {{
            platBtn.style.borderBottom = 'none';
          }}
          
          platBtn.addEventListener('click', () => {{
            appendMessage('user', plat);
            showDiagnostic(plat);
          }});
          
          platBtn.addEventListener('mouseenter', () => {{
            platBtn.style.background = '#f8fafc';
          }});
          
          platBtn.addEventListener('mouseleave', () => {{
            platBtn.style.background = '#ffffff';
          }});
          
          listContainer.appendChild(platBtn);
        }});
        
        quickZone.appendChild(listContainer);
        
        // Fonction de recherche
        searchInput.addEventListener('input', (e) => {{
          const query = e.target.value.toLowerCase().trim();
          const buttons = listContainer.querySelectorAll('button');
          
          buttons.forEach(btn => {{
            const platName = btn.dataset.platName || '';
            if (platName.includes(query)) {{
              btn.style.display = 'flex';
            }} else {{
              btn.style.display = 'none';
            }}
          }});
        }});
      }};
      


      // ===== ÉTAPE 2: DIAGNOSTIC SIMPLE + CHOIX ACTION =====
      const showDiagnostic = (platNom) => {{
        currentStep = 'diagnostic';
        clearQuickZone();
        selectedPlat = platNom;
        
        const diag = guided.diagnostics[platNom];
        if (!diag) return;
        
        const isOK = diag.marge_pct >= stats.objectif;
        
        // Message diagnostic sobre
        let diagMessage = '<strong>' + platNom + '</strong><br/>';
        diagMessage += '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin-top: 0.5rem; font-size: 0.85rem;">';
        diagMessage += '<div><span style="color: #64748b;">Prix TTC</span><br/><strong>' + diag.prix_ttc.toFixed(2) + ' €</strong></div>';
        diagMessage += '<div><span style="color: #64748b;">Coût</span><br/><strong>' + diag.cout_matiere.toFixed(2) + ' €</strong></div>';
        diagMessage += '<div><span style="color: #64748b;">Marge</span><br/><strong style="color: ' + (isOK ? '#22c55e' : '#D92332') + ';">' + diag.marge_pct.toFixed(1) + '%</strong></div>';
        diagMessage += '<div><span style="color: #64748b;">Objectif</span><br/><strong>' + stats.objectif + '%</strong></div>';
        diagMessage += '</div>';
        
        if (!isOK) {{
          diagMessage += '<div style="margin-top: 0.625rem; padding: 0.5rem 0.75rem; background: #fef2f2; border-radius: 6px; font-size: 0.8rem; color: #991b1b;">Manque <strong>' + diag.manque_euros.toFixed(2) + ' €</strong> pour atteindre l&rsquo;objectif</div>';
        }}
        
        appendMessage('bot', diagMessage);
        
        // Message évolution si disponible
        if (diag.volume_n1 && diag.volume_current && diag.evolution_pct !== 0) {{
          setTimeout(() => {{
            const trend = diag.evolution_pct > 0 ? 'Hausse' : 'Baisse';
            const color = diag.evolution_pct > 0 ? '#22c55e' : '#ef4444';
            let evoMessage = '<div style="font-size: 0.85rem;"><span style="color: #64748b;">Volume 2025</span> ';
            evoMessage += diag.volume_n1.toLocaleString() + ' → <strong>' + diag.volume_current.toLocaleString() + '</strong> ';
            evoMessage += '<span style="color: ' + color + '; font-weight: 600;">(' + (diag.evolution_pct > 0 ? '+' : '') + diag.evolution_pct.toFixed(0) + '%)</span></div>';
            appendMessage('bot', evoMessage);
          }}, 400);
        }}
        
        // Message action simplifié
        setTimeout(() => {{
          appendMessage('bot', 'Choisissez une action :');
        }}, diag.volume_n1 ? 800 : 400);
        
        // Boutons d'action compacts
        const actionsContainer = doc.createElement('div');
        actionsContainer.style.cssText = 'display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem;';
        
        const actions = [
          {{ 
            label: 'Négocier fournisseurs', 
            action: 'nego'
          }},
          {{ 
            label: 'Augmenter le prix', 
            action: 'prix'
          }},
          {{ 
            label: 'Objectif volume', 
            action: 'volume'
          }}
        ];
        
        actions.forEach((action) => {{
          const btn = doc.createElement('button');
          btn.type = 'button';
          btn.style.cssText = 
            'padding: 0.7rem 0.85rem; ' +
            'background: #ffffff; ' +
            'border: 1.5px solid #e2e8f0; ' +
            'border-radius: 10px; ' +
            'text-align: left; ' +
            'cursor: pointer; ' +
            'transition: all 0.2s ease; ' +
            'font-size: 0.83rem; ' +
            'font-weight: 500; ' +
            'color: #334155;';
          
          btn.innerHTML = 
            '<div style="display: flex; align-items: center; justify-content: space-between;">' +
            '<span>' + action.label + '</span>' +
            '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="2"><path d="M9 5l7 7-7 7"/></svg>' +
            '</div>';
          
          btn.addEventListener('mouseenter', () => {{ 
            btn.style.background = 'rgba(217, 35, 50, 0.02)';
            btn.style.borderColor = '#D92332';
          }});
          btn.addEventListener('mouseleave', () => {{ 
            btn.style.background = '#ffffff';
            btn.style.borderColor = '#e2e8f0';
          }});
          btn.addEventListener('click', () => {{
            appendMessage('user', action.label);
            if (action.action === 'nego') showAction('Négo');
            else if (action.action === 'prix') showAction('Prix');
            else if (action.action === 'volume') showAction('Volume');
          }});
          
          actionsContainer.appendChild(btn);
        }});
        
        quickZone.appendChild(actionsContainer);
        
        // Bouton retour sobre
        const backBtn = doc.createElement('button');
        backBtn.type = 'button';
        backBtn.innerHTML = '← Retour';
        backBtn.style.cssText = 'margin-top: 0.75rem; padding: 0.65rem; background: #ffffff; color: #64748b; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; transition: all 0.2s; width: 100%; font-size: 0.85rem;';
        backBtn.addEventListener('mouseenter', () => {{ backBtn.style.background = '#f8fafc'; }});
        backBtn.addEventListener('mouseleave', () => {{ backBtn.style.background = '#ffffff'; }});
        backBtn.addEventListener('click', () => {{
          appendMessage('user', 'Retour');
          showWelcome();
        }});
        quickZone.appendChild(backBtn);
      }};

      // ÉTAPE 3: Action spécifique avec jauges interactives (compacté)
      const showAction = (actionType) => {{
        currentStep = 'action';
        clearQuickZone();
        
        const platNom = selectedPlat;
        const diag = guided.diagnostics[platNom];
        
        if (actionType === 'Volume') {{
          appendMessage('bot', '<strong>Objectif volume</strong>');
          
          // Contrôle compact
          const gaugeContainer = doc.createElement('div');
          gaugeContainer.style.cssText = 'padding: 0.875rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 0.5rem;';
          
          const labelCA = doc.createElement('label');
          labelCA.innerHTML = '<span style="font-size: 0.8rem; color: #64748b; font-weight: 500;">CA annuel cible</span>';
          labelCA.style.cssText = 'display: block; margin-bottom: 0.375rem;';
          
          const sliderCA = doc.createElement('input');
          sliderCA.type = 'range';
          
          // Utiliser données N-1 réelles
          const caN1 = diag.n1_ca || 0;
          const caMin = Math.max(500, Math.round(caN1 * 0.5 / 100) * 100);
          const caMax = Math.max(10000, Math.round(caN1 * 3 / 100) * 100);
          const caInit = caN1 > 0 ? Math.round(caN1 / 100) * 100 : 2000;
          
          sliderCA.min = caMin.toString();
          sliderCA.max = caMax.toString();
          sliderCA.step = '100';
          sliderCA.value = caInit.toString();
          sliderCA.style.cssText = 'width: 100%; height: 8px; border-radius: 4px; background: linear-gradient(to right, #e2e8f0, #D92332); outline: none; -webkit-appearance: none; appearance: none; cursor: pointer;';
          
          const valueDisplay = doc.createElement('div');
          valueDisplay.innerHTML = '<strong style="font-size: 1.1rem; color: #D92332;">' + sliderCA.value.toLocaleString() + ' €</strong>';
          valueDisplay.style.cssText = 'text-align: center; margin: 0.5rem 0;';
          
          const resultDiv = doc.createElement('div');
          resultDiv.id = 'volumeResult';
          resultDiv.style.cssText = 'padding: 0.75rem; background: #ffffff; border-radius: 6px; border: 1px solid #e2e8f0; margin-top: 0.5rem; font-size: 0.8rem;';
          
          const updateVolume = () => {{
            const ca = parseFloat(sliderCA.value);
            const prixTTC = diag.prix_ttc;
            const volumeAnnuel = Math.round(ca / prixTTC);
            const volumeMensuel = Math.round(volumeAnnuel / 12);
            const margeUnit = prixTTC * (diag.marge_pct / 100);
            const margeTotal = Math.round(volumeAnnuel * margeUnit);
            
            // Récupérer données évolution
            const volumeN1Hist = diag.volume_n1 || 0;
            const volumeCurrent = diag.volume_current || diag.n1_volume || 0;
            const evolutionPct = diag.evolution_pct || 0;
            
            valueDisplay.innerHTML = '<span style="font-size: 1.25rem; font-weight: 600; color: #D92332;">' + ca.toLocaleString() + ' €</span>';
            
            // Comparer avec N-1 et projeter N+1
            let compareHTML = '';
            let projectionHTML = '';
            const volumeN1 = volumeCurrent > 0 ? volumeCurrent : 0;
            
            if (volumeN1 > 0) {{
              const ecartVolume = Math.round((volumeAnnuel - volumeN1) / volumeN1 * 100);
              const color = ecartVolume > 0 ? '#10b981' : ecartVolume < 0 ? '#ef4444' : '#64748b';
              const tendance = ecartVolume > 0 ? '↑' : ecartVolume < 0 ? '↓' : '→';
              
              // Afficher évolution N-1 → Current avec icône
              let evolutionBadge = '';
              if (evolutionPct !== 0) {{
                const evolutionColor = evolutionPct > 0 ? '#16a34a' : '#dc2626';
                const evolutionSymbol = evolutionPct > 0 ? '📈' : '📉';
                evolutionBadge = ' <span style="color: ' + evolutionColor + '; font-size: 0.85rem;">' + evolutionSymbol + ' ' + (evolutionPct > 0 ? '+' : '') + evolutionPct.toFixed(0) + '%</span>';
              }}
              
              compareHTML = '<div style="grid-column: span 2; padding: 0.5rem; background: #f8fafc; border-radius: 6px; margin-top: 0.4rem;">' +
                '<span style="color: #64748b; font-size: 0.75rem; font-weight: 500;">VS 2025 (' + volumeN1.toLocaleString() + ' vendus, ' + caN1.toLocaleString() + '€)' + evolutionBadge + '</span><br/>' +
                '<strong style="font-size: 1rem; color: ' + color + ';">' + tendance + ' ' + (ecartVolume > 0 ? '+' : '') + ecartVolume + '%</strong>' +
                '</div>';
              
              // Projection N+1 basée sur tendance actuelle
              if (evolutionPct !== 0 && Math.abs(evolutionPct) > 5) {{
                const volumeProjetN1 = Math.round(volumeCurrent * (1 + evolutionPct / 100));
                const caProjetN1 = Math.round(volumeProjetN1 * prixTTC);
                const margeProjetN1 = Math.round(volumeProjetN1 * margeUnit);
                const bgColor = evolutionPct > 0 ? '#f0fdf4' : '#fef2f2';
                const borderColor = evolutionPct > 0 ? '#22c55e' : '#ef4444';
                const textColor = evolutionPct > 0 ? '#166534' : '#991b1b';
                
                projectionHTML = '<div style="grid-column: span 2; padding: 0.6rem; background: ' + bgColor + '; border-radius: 6px; border-left: 3px solid ' + borderColor + '; margin-top: 0.4rem;">' +
                  '<span style="color: ' + textColor + '; font-size: 0.75rem; font-weight: 600;">📊 Projection 2026 (si tendance continue)</span><br/>' +
                  '<div style="display: flex; gap: 1rem; margin-top: 0.3rem; flex-wrap: wrap;">' +
                  '<div><span style="color: #64748b; font-size: 0.7rem;">Volume</span><br/><strong style="color: ' + textColor + '; font-size: 0.95rem;">' + volumeProjetN1.toLocaleString() + '</strong></div>' +
                  '<div><span style="color: #64748b; font-size: 0.7rem;">CA</span><br/><strong style="color: ' + textColor + '; font-size: 0.95rem;">' + caProjetN1.toLocaleString() + ' €</strong></div>' +
                  '<div><span style="color: #64748b; font-size: 0.7rem;">Marge</span><br/><strong style="color: ' + textColor + '; font-size: 0.95rem;">' + margeProjetN1.toLocaleString() + ' €</strong></div>' +
                  '</div>' +
                  '</div>';
              }}
            }}
            
            resultDiv.innerHTML = 
              '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem;">' +
              '<div><span style="color: #64748b; font-size: 0.75rem; font-weight: 500;">Annuel</span><br/><strong style="font-size: 1rem; color: #0f172a;">' + volumeAnnuel.toLocaleString() + '</strong></div>' +
              '<div><span style="color: #64748b; font-size: 0.75rem; font-weight: 500;">Mensuel</span><br/><strong style="font-size: 1rem; color: #0f172a;">' + volumeMensuel.toLocaleString() + '</strong></div>' +
              '<div style="grid-column: span 2; padding-top: 0.4rem; border-top: 1px solid #e2e8f0;"><span style="color: #64748b; font-size: 0.75rem; font-weight: 500;">Marge totale</span><br/><strong style="font-size: 1.1rem; color: #10b981;">' + margeTotal.toLocaleString() + ' €</strong></div>' +
              compareHTML +
              projectionHTML +
              '</div>';
          }};
          
          sliderCA.addEventListener('input', updateVolume);
          
          gaugeContainer.appendChild(labelCA);
          gaugeContainer.appendChild(sliderCA);
          gaugeContainer.appendChild(valueDisplay);
          quickZone.appendChild(gaugeContainer);
          quickZone.appendChild(resultDiv);
          updateVolume();
          
          // Bouton retour
          const backBtn = doc.createElement('button');
          backBtn.type = 'button';
          backBtn.innerHTML = '← Retour';
          backBtn.style.cssText = 'margin-top: 0.5rem; padding: 0.65rem; background: #ffffff; color: #64748b; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; transition: all 0.2s; width: 100%; font-size: 0.85rem;';
          backBtn.addEventListener('mouseenter', () => {{ backBtn.style.background = '#f8fafc'; }});
          backBtn.addEventListener('mouseleave', () => {{ backBtn.style.background = '#ffffff'; }});
          backBtn.addEventListener('click', () => {{
            showDiagnostic(platNom);
          }});
          quickZone.appendChild(backBtn);
          
        }} else if (actionType === 'Prix') {{
          appendMessage('bot', '<strong>Simulation prix</strong>');
          
          // Contrôle compact
          const gaugeContainer = doc.createElement('div');
          gaugeContainer.style.cssText = 'padding: 0.875rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 0.5rem;';
          
          const labelPrix = doc.createElement('label');
          labelPrix.innerHTML = '<span style="font-size: 0.8rem; color: #64748b; font-weight: 500;">Augmentation</span>';
          labelPrix.style.cssText = 'display: block; margin-bottom: 0.375rem;';
          
          const sliderPrix = doc.createElement('input');
          sliderPrix.type = 'range';
          sliderPrix.min = '0';
          sliderPrix.max = '5';
          sliderPrix.step = '0.1';
          sliderPrix.value = '0.5';
          sliderPrix.style.cssText = 'width: 100%; height: 8px; border-radius: 4px; background: linear-gradient(to right, #e2e8f0, #D92332); outline: none; -webkit-appearance: none; appearance: none; cursor: pointer;';
          
          const valueDisplay = doc.createElement('div');
          valueDisplay.innerHTML = '<strong style="font-size: 1.1rem; color: #D92332;">+' + sliderPrix.value + ' €</strong>';
          valueDisplay.style.cssText = 'text-align: center; margin: 0.5rem 0;';
          
          const resultDiv = doc.createElement('div');
          resultDiv.id = 'prixResult';
          resultDiv.style.cssText = 'padding: 0.75rem; background: #ffffff; border-radius: 6px; border: 1px solid #e2e8f0; margin-top: 0.5rem; font-size: 0.8rem;';
          
          const updatePrix = () => {{
            const hausse = parseFloat(sliderPrix.value);
            const prixActuel = diag.prix_ttc;
            const nouveauPrix = prixActuel + hausse;
            const haussePct = (hausse / prixActuel * 100).toFixed(1);
            
            // ===== MODÉLISATION ÉCONOMÉTRIQUE AVANCÉE =====
            
            // 1. Récupérer données historiques
            const volumeN1Hist = diag.volume_n1 || 0;
            const volumeCurrent = diag.volume_current || diag.n1_volume || 2400;
            const evolutionPct = diag.evolution_pct || 0;
            const volumeAnnuelN1 = volumeCurrent;
            const volumeMensuelN1 = Math.round(volumeAnnuelN1 / 12);
            const caN1 = diag.n1_ca || (volumeAnnuelN1 * prixActuel);
            const prixN1 = diag.n1_prix_moyen || prixActuel;
            
            // 2. ÉLASTICITÉ-PRIX DYNAMIQUE (modèle log-log avec contexte)
            // Formule : ε = β₀ + β₁·ln(P) + β₂·Tendance + β₃·Seuil_psycho
            let elasticiteBase = -0.8; // Restauration rapide : -0.6 à -1.2 (études empiriques)
            
            // Ajustement selon niveau de prix (courbe en U inversé)
            const categoriesPrix = {{ 'entrée': 0.7, 'plat': 1.0, 'premium': 1.3 }};
            let facteurCategorie = 1.0;
            if (prixActuel < 8) facteurCategorie = 0.7; // Produits accessibles → moins sensibles
            else if (prixActuel > 15) facteurCategorie = 1.3; // Produits premium → très sensibles
            
            elasticiteBase = elasticiteBase * facteurCategorie;
            
            // Ajustement selon amplitude hausse (effet non-linéaire)
            // Petites hausses (-3%) → clients moins réactifs
            // Grosses hausses (-12%) → forte réaction
            let facteurAmplitude = 1.0;
            if (haussePct < 3) facteurAmplitude = 0.6;
            else if (haussePct < 6) facteurAmplitude = 0.8;
            else if (haussePct > 10) facteurAmplitude = 1.4;
            else if (haussePct > 15) facteurAmplitude = 1.8;
            
            let elasticiteFinal = elasticiteBase * facteurAmplitude;
            
            // 3. SEUILS PSYCHOLOGIQUES (9.90€ vs 10.10€ = -15% volume)
            const seuilsPsycho = [4.99, 5.99, 6.99, 7.99, 8.99, 9.99, 10.99, 11.99, 12.99, 14.99];
            let penaliteSeuil = 0;
            for (let seuil of seuilsPsycho) {{
              if (prixActuel < seuil && nouveauPrix >= seuil) {{
                penaliteSeuil = -8; // Franchissement seuil = -8% volume supplémentaire
                break;
              }}
            }}
            
            // 4. MOMENTUM DE CROISSANCE (tendance exponentielle lissée)
            // Si croissance N-1→N, projeter avec décélération réaliste
            let facteurMomentum = 0;
            let persistanceTendance = 0.6; // 60% de la tendance persiste (régression à la moyenne)
            
            if (volumeN1Hist > 0 && evolutionPct !== 0) {{
              // Calculer taux de croissance composé annuel (CAGR)
              const tauxCroissanceAnnuel = evolutionPct / 100;
              
              // Persistance : forte croissance → momentum fort MAIS décélération probable
              if (evolutionPct > 80) {{
                persistanceTendance = 0.4; // Croissance exceptionnelle → régression forte
              }} else if (evolutionPct > 40) {{
                persistanceTendance = 0.5;
              }} else if (evolutionPct > 20) {{
                persistanceTendance = 0.6;
              }} else if (evolutionPct > 0) {{
                persistanceTendance = 0.7; // Croissance modérée → plus stable
              }} else if (evolutionPct < -20) {{
                persistanceTendance = 0.8; // Déclin → inertie forte
              }}
              
              facteurMomentum = tauxCroissanceAnnuel * persistanceTendance;
            }}
            
            // 5. CALCUL VOLUME PROJETÉ (modèle hybride)
            // V_projeté = V_actuel × (1 + ε×ΔP/P + momentum + seuil_psycho)
            const impactPrixPct = elasticiteFinal * (hausse / prixActuel) * 100;
            const impactMomentumPct = facteurMomentum * 100;
            const impactTotalPct = impactPrixPct + impactMomentumPct + penaliteSeuil;
            
            const nouveauVolumeAnnuel = Math.round(volumeAnnuelN1 * (1 + impactTotalPct / 100));
            const nouveauVolumeMensuel = Math.round(nouveauVolumeAnnuel / 12);
            const evolutionProjetePct = Math.round((nouveauVolumeAnnuel - volumeAnnuelN1) / volumeAnnuelN1 * 100);
            
            // 6. SCORING DE CONFIANCE (0-100%)
            let scoreConfiance = 50; // Base
            if (volumeN1Hist > 0) scoreConfiance += 20; // Données N-1 disponibles
            if (volumeN1Hist > 500) scoreConfiance += 10; // Volume significatif
            if (Math.abs(evolutionPct) < 30) scoreConfiance += 10; // Évolution normale
            if (haussePct < 8) scoreConfiance += 10; // Hausse raisonnable
            scoreConfiance = Math.min(100, scoreConfiance);
            
            const margeAct = diag.marge_pct / 100 * prixActuel;
            const margePrix = diag.marge_pct / 100 * nouveauPrix;
            const impactMargeAnnuel = Math.round((margePrix - margeAct) * nouveauVolumeAnnuel);
            const nouveauCAannuel = Math.round(nouveauPrix * nouveauVolumeAnnuel);
            const ancienCAannuel = Math.round(caN1);
            const nouvelleMarge = ((nouveauPrix - diag.cout_matiere) / nouveauPrix * 100).toFixed(1);
            
            // ===== AIDE À LA DÉCISION BASÉE SUR MODÈLE ÉCONOMÉTRIQUE =====
            
            let analyseStrategique = '';
            let recommandation = '';
            let detailsCalcul = '';
            
            // Détails du modèle pour transparence
            detailsCalcul = '<div style="padding: 0.5rem; background: #f8fafc; border-radius: 6px; font-size: 0.7rem; color: #64748b; line-height: 1.4;">' +
              '<strong>Modèle économétrique :</strong><br/>' +
              '• Élasticité-prix : ' + elasticiteFinal.toFixed(2) + ' (impact: ' + impactPrixPct.toFixed(1) + '%)<br/>' +
              '• Momentum tendance : ' + (persistanceTendance * 100).toFixed(0) + '% persistance (impact: ' + impactMomentumPct.toFixed(1) + '%)<br/>' +
              (penaliteSeuil !== 0 ? '• ⚠️ Seuil psychologique franchi : ' + penaliteSeuil + '%<br/>' : '') +
              '• <strong>Confiance projection : ' + scoreConfiance + '%</strong>' +
              '</div>';
            
            // Scoring décision multi-critères (pondéré)
            const gainMargeAbsolu = impactMargeAnnuel;
            const gainMargePct = (impactMargeAnnuel / ancienCAannuel * 100);
            const ratioRisqueRecompense = gainMargeAbsolu / Math.max(1, Math.abs(evolutionProjetePct) * volumeAnnuelN1 * 0.01);
            
            // Score de décision (0-100)
            let scoreDecision = 50;
            if (gainMargeAbsolu > 5000) scoreDecision += 20;
            else if (gainMargeAbsolu > 2000) scoreDecision += 10;
            else if (gainMargeAbsolu < 0) scoreDecision -= 30;
            
            if (evolutionProjetePct > 5) scoreDecision += 15;
            else if (evolutionProjetePct > -5) scoreDecision += 5;
            else if (evolutionProjetePct < -10) scoreDecision -= 20;
            else if (evolutionProjetePct < -15) scoreDecision -= 30;
            
            if (penaliteSeuil !== 0) scoreDecision -= 10;
            if (scoreConfiance > 70) scoreDecision += 10;
            
            scoreDecision = Math.max(0, Math.min(100, scoreDecision));
            
            // DÉCISION FINALE basée sur scoring
            if (scoreDecision >= 70) {{
              // ✅ RECOMMANDATION FORTE : GO
              const roiMois = Math.round(gainMargeAbsolu / 12);
              recommandation = '<div style="padding: 0.65rem; background: #f0fdf4; border-left: 3px solid #22c55e; border-radius: 6px; margin-top: 0.5rem;">' +
                '<div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.3rem;">' +
                '<span style="color: #166534; font-size: 0.8rem; font-weight: 600;">✓ AUGMENTER</span>' +
                '<span style="background: #22c55e; color: white; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.6rem; font-weight: 600;">CONF. ' + scoreConfiance + '%</span>' +
                '</div>' +
                '<small style="color: #15803d; line-height: 1.4; font-size: 0.75rem; display: block;">' +
                '<strong>Gain : +' + impactMargeAnnuel.toLocaleString() + '€/an</strong> (' + roiMois.toLocaleString() + '€/mois)<br/>' +
                'Volume : ' + nouveauVolumeAnnuel.toLocaleString() + ' (' + (evolutionProjetePct > 0 ? '+' : '') + evolutionProjetePct + '%)<br/>' +
                (evolutionPct > 0 ? 'Momentum +' + evolutionPct.toFixed(0) + '%' : 'Projection stable') +
                '</small>' +
                '</div>';
              analyseStrategique = '<div style="padding: 0.4rem; background: #f8fafc; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem;">Risque/gain favorable (' + ratioRisqueRecompense.toFixed(1) + ')</span>' +
                '</div>';
                
            }} else if (scoreDecision >= 50) {{
              // ⚠️ RECOMMANDATION MODÉRÉE : TESTER
              const hausseSuggere = hausse * 0.7;
              const prixSuggere = prixActuel + hausseSuggere;
              recommandation = '<div style="padding: 0.65rem; background: #fffbeb; border-left: 3px solid #f59e0b; border-radius: 6px; margin-top: 0.5rem;">' +
                '<div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.3rem;">' +
                '<span style="color: #92400e; font-size: 0.8rem; font-weight: 600;">⚠ TESTER</span>' +
                '<span style="background: #f59e0b; color: white; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.6rem; font-weight: 600;">CONF. ' + scoreConfiance + '%</span>' +
                '</div>' +
                '<small style="color: #78350f; line-height: 1.4; font-size: 0.75rem; display: block;">' +
                'Gain : +' + impactMargeAnnuel.toLocaleString() + '€/an<br/>' +
                (penaliteSeuil !== 0 ? 'Seuil : réduire à +' + hausseSuggere.toFixed(2) + '€<br/>' : '') +
                (evolutionProjetePct < 0 ? 'Perte volume ' + evolutionProjetePct + '% → surveiller' : 'Surveiller 2 premiers mois') +
                '</small>' +
                '</div>';
              analyseStrategique = '<div style="padding: 0.4rem; background: #f8fafc; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem;">Gain potentiel, risque modéré</span>' +
                '</div>';
                
            }} else {{
              // 🛑 RECOMMANDATION NÉGATIVE : STOP
              const alternativeMarge = Math.round(volumeAnnuelN1 * diag.manque_euros * 0.7);
              recommandation = '<div style="padding: 0.65rem; background: #fef2f2; border-left: 3px solid #ef4444; border-radius: 6px; margin-top: 0.5rem;">' +
                '<div style="display: flex; align-items: center; gap: 0.4rem; margin-bottom: 0.3rem;">' +
                '<span style="color: #991b1b; font-size: 0.8rem; font-weight: 600;">✗ NE PAS AUGMENTER</span>' +
                '<span style="background: #ef4444; color: white; padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 0.6rem; font-weight: 600;">CONF. ' + scoreConfiance + '%</span>' +
                '</div>' +
                '<small style="color: #dc2626; line-height: 1.4; font-size: 0.75rem; display: block;">' +
                'Risque : ' + (gainMargeAbsolu < 0 ? 'Perte ' + gainMargeAbsolu.toLocaleString() + '€' : 'Gain faible vs perte volume ' + evolutionProjetePct + '%') + '<br/>' +
                (evolutionPct < 0 ? 'Déclin ' + evolutionPct.toFixed(0) + '% en cours<br/>' : '') +
                'Alternative : négo fournisseurs (~' + alternativeMarge.toLocaleString() + '€)' +
                '</small>' +
                '</div>';
              analyseStrategique = '<div style="padding: 0.4rem; background: #f8fafc; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem;">Risque élevé, ratio défavorable</span>' +
                '</div>';
            }}
            
            valueDisplay.innerHTML = '<strong style="color: #D92332; font-size: 1.1rem;">+' + hausse.toFixed(2) + ' €</strong> <span style="color: #64748b; font-size: 0.8rem;">→ ' + nouveauPrix.toFixed(2) + ' € (+' + haussePct + '%)</span>';
            
            // Contexte évolution pour aider la compréhension
            let contexteEvolution = '';
            if (evolutionPct !== 0) {{
              const evolutionColor = evolutionPct > 0 ? '#16a34a' : '#dc2626';
              const evolutionSymbol = evolutionPct > 0 ? '📈' : '📉';
              contexteEvolution = '<div style="padding: 0.4rem; background: #f8fafc; border-radius: 6px; border-left: 2px solid #94a3b8;">' +
                '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Contexte</span><br/>' +
                '<span style="color: ' + evolutionColor + '; font-size: 0.8rem; font-weight: 600;">' + evolutionSymbol + ' ' + (evolutionPct > 0 ? '+' : '') + evolutionPct.toFixed(0) + '%</span> ' +
                '<span style="color: #64748b; font-size: 0.7rem;">(' + volumeN1Hist.toLocaleString() + ' → ' + volumeCurrent.toLocaleString() + ')</span>' +
                '</div>';
            }}
            
            resultDiv.innerHTML = 
              '<div style="display: grid; gap: 0.6rem;">' +
              contexteEvolution +
              '<div style="padding: 0.5rem; background: ' + (evolutionProjetePct < 0 ? '#fef2f2' : '#f8fafc') + '; border-radius: 6px; border-left: 3px solid ' + (evolutionProjetePct < 0 ? '#ef4444' : '#22c55e') + ';">' +
              '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Volume projeté</span><br/>' +
              '<strong style="color: ' + (evolutionProjetePct < 0 ? '#ef4444' : '#10b981') + '; font-size: 0.95rem;">' + nouveauVolumeAnnuel.toLocaleString() + '</strong> ' +
              '<span style="font-size: 0.8rem; color: ' + (evolutionProjetePct < 0 ? '#ef4444' : '#10b981') + '; font-weight: 600;">' + (evolutionProjetePct > 0 ? '+' : '') + evolutionProjetePct + '%</span> ' +
              '<small style="color: #64748b; font-size: 0.7rem;">(vs ' + volumeAnnuelN1.toLocaleString() + ')</small>' +
              '</div>' +
              '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">' +
              '<div style="padding: 0.5rem; background: ' + (impactMargeAnnuel > 0 ? '#f0fdf4' : '#fef2f2') + '; border-radius: 6px;">' +
              '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Impact marge</span><br/>' +
              '<strong style="color: ' + (impactMargeAnnuel > 0 ? '#10b981' : '#ef4444') + '; font-size: 0.9rem;">' + (impactMargeAnnuel > 0 ? '+' : '') + impactMargeAnnuel.toLocaleString() + ' €</strong>' +
              '</div>' +
              '<div style="padding: 0.5rem; background: #f8fafc; border-radius: 6px;">' +
              '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">CA projeté</span><br/>' +
              '<strong style="font-size: 0.9rem; color: #0f172a;">' + nouveauCAannuel.toLocaleString() + ' €</strong>' +
              '</div>' +
              '</div>' +
              recommandation +
              '<details style="margin-top: 0.5rem;"><summary style="cursor: pointer; padding: 0.4rem; background: #f8fafc; border-radius: 6px; font-size: 0.7rem; color: #64748b;">Détails modèle</summary>' +
              detailsCalcul +
              analyseStrategique +
              '</details>' +
              '</div>';
          }};
          
          sliderPrix.addEventListener('input', updatePrix);
          
          gaugeContainer.appendChild(labelPrix);
          gaugeContainer.appendChild(sliderPrix);
          gaugeContainer.appendChild(valueDisplay);
          quickZone.appendChild(gaugeContainer);
          quickZone.appendChild(resultDiv);
          updatePrix();
          
          // Bouton retour
          const backBtn = doc.createElement('button');
          backBtn.type = 'button';
          backBtn.innerHTML = '← Retour';
          backBtn.style.cssText = 'margin-top: 0.5rem; padding: 0.65rem; background: #ffffff; color: #64748b; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; transition: all 0.2s; width: 100%; font-size: 0.85rem;';
          backBtn.addEventListener('mouseenter', () => {{ backBtn.style.background = '#f8fafc'; }});
          backBtn.addEventListener('mouseleave', () => {{ backBtn.style.background = '#ffffff'; }});
          backBtn.addEventListener('click', () => {{
            showDiagnostic(platNom);
          }});
          quickZone.appendChild(backBtn);
          
        }} else if (actionType === 'Négo') {{
          if (diag && diag.manque_euros > 0) {{
            const focusTxt = diag.focus_ingredient ? diag.focus_ingredient : "l'ingrédient principal";
            const focusCost = diag.focus_cost || 0;
            const focusPct = diag.focus_pct || 0;
            const focusKgAnnuel = diag.focus_kg_annuel || 0;
            
            // Debug: vérifier les valeurs
            console.log('Négo Debug:', {{ focusTxt, focusCost, focusPct, focusKgAnnuel, diag }});
            
            appendMessage('bot', '<strong>Négociation</strong><br/><small style="color: #64748b;">Ciblée sur <strong>' + focusTxt + '</strong> (' + focusPct.toFixed(0) + '% du coût · ' + focusCost.toFixed(2) + ' €/plat)</small>');
            
            // Afficher le contexte de négociation avec vraies données et évolution
            const volumeN1Hist = diag.volume_n1 || 0;
            const volumeCurrent = diag.volume_current || diag.n1_volume || 0;
            const evolutionPct = diag.evolution_pct || 0;
            const kgAnnuel = focusKgAnnuel > 0 ? focusKgAnnuel : 0;
            
            const contextDiv = doc.createElement('div');
            contextDiv.style.cssText = 'padding: 0.65rem; background: #fffbeb; border-left: 3px solid #f59e0b; border-radius: 6px; margin-bottom: 0.5rem;';
            
            let consoText = '';
            if (volumeCurrent > 0) {{
              let evolutionText = '';
              if (volumeN1Hist > 0 && evolutionPct !== 0) {{
                const evolutionSymbol = evolutionPct > 0 ? '📈' : '📉';
                const evolutionColor = evolutionPct > 0 ? '#16a34a' : '#dc2626';
                const deltaVentes = volumeCurrent - volumeN1Hist;
                evolutionText = '<br/><span style="color: ' + evolutionColor + '; font-weight: 600; font-size: 0.8rem;">' + evolutionSymbol + ' ' + (evolutionPct > 0 ? '+' : '') + evolutionPct.toFixed(0) + '%</span> <span style="color: #64748b; font-size: 0.75rem;">(' + (deltaVentes > 0 ? '+' : '') + deltaVentes.toLocaleString() + ' ventes vs N-1)</span>';
              }}
              consoText = '<div style="color: #78350f; font-size: 0.8rem; line-height: 1.5;">Conso. annuelle : <strong>~' + kgAnnuel.toFixed(0) + ' kg</strong> (base ' + volumeCurrent.toLocaleString() + ' ventes)' + evolutionText + '<br/>' +
                'Coût unitaire : <strong>' + focusCost.toFixed(2) + ' €</strong> · Poids : <strong>' + focusPct.toFixed(0) + '%</strong></div>';
            }} else {{
              consoText = '<div style="color: #78350f; font-size: 0.8rem; line-height: 1.4;">Conso. annuelle : <strong>~' + kgAnnuel.toFixed(0) + ' kg</strong> (est. 200/mois)<br/>' +
                'Coût unitaire : <strong>' + focusCost.toFixed(2) + ' €</strong> · Poids : <strong>' + focusPct.toFixed(0) + '%</strong></div>';
            }}
            
            contextDiv.innerHTML = 
              '<div style="color: #92400e; font-weight: 600; margin-bottom: 0.375rem; font-size: 0.8rem;">Contexte</div>' +
              consoText;
            quickZone.appendChild(contextDiv);
            
            // Créer un contrôle de jauge pour la négociation
            const gaugeContainer = doc.createElement('div');
            gaugeContainer.style.cssText = 'padding: 0.875rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; margin-bottom: 0.5rem;';
            
            const labelNego = doc.createElement('label');
            labelNego.innerHTML = '<span style="font-size: 0.8rem; color: #64748b; font-weight: 500;">Réduction sur ' + focusTxt + '</span>';
            labelNego.style.cssText = 'display: block; margin-bottom: 0.375rem;';
            
            const sliderNego = doc.createElement('input');
            sliderNego.type = 'range';
            sliderNego.min = '0';
            sliderNego.max = '30';
            sliderNego.step = '1';
            sliderNego.value = Math.min(diag.reduction_pct, 30).toFixed(0);
            sliderNego.style.cssText = 'width: 100%; height: 8px; border-radius: 4px; background: linear-gradient(to right, #e2e8f0, #D92332); outline: none; -webkit-appearance: none; appearance: none; cursor: pointer;';
            
            const valueDisplay = doc.createElement('div');
            valueDisplay.innerHTML = '<strong style="font-size: 1.1rem; color: #D92332;">-' + sliderNego.value + '%</strong>';
            valueDisplay.style.cssText = 'text-align: center; margin: 0.5rem 0;';
            
            const resultDiv = doc.createElement('div');
            resultDiv.id = 'negoResult';
            resultDiv.style.cssText = 'padding: 0.75rem; background: #ffffff; border-radius: 6px; border: 1px solid #e2e8f0; margin-top: 0.5rem; font-size: 0.8rem;';
            
            const updateNego = () => {{
              const reductionPct = parseFloat(sliderNego.value);
              
              // Utiliser volume N-1 réel
              const volumeAnnuelN1 = diag.n1_volume || 2400;
              const volumeMensuelN1 = Math.round(volumeAnnuelN1 / 12);
              
              // Calcul sur l'ingrédient spécifique
              const coutIngredientActuel = focusCost;
              const nouveauCoutIngredient = coutIngredientActuel * (1 - reductionPct / 100);
              const economieParPlat = coutIngredientActuel - nouveauCoutIngredient;
              
              // Impact sur le plat complet
              const nouveauCoutPlat = diag.cout_matiere - economieParPlat;
              const nouvelleMarge = ((diag.prix_ttc - nouveauCoutPlat) / diag.prix_ttc * 100).toFixed(1);
              const nouvelleMargePlat = diag.prix_ttc - nouveauCoutPlat;
              const ancienneMargePlat = diag.prix_ttc - diag.cout_matiere;
              
              // Économies annuelles sur volume N-1
              const economieAnnuelle = Math.round(economieParPlat * volumeAnnuelN1);
              const margeAnnuelleNv = Math.round(nouvelleMargePlat * volumeAnnuelN1);
              const margeAnnuelleAnc = Math.round(ancienneMargePlat * volumeAnnuelN1);
              const gainMarge = margeAnnuelleNv - margeAnnuelleAnc;
              const objectifAtteint = nouvelleMarge >= stats.objectif;
              
              // Volume annuel d'ingrédient (déjà calculé côté Python avec les bonnes données)
              const volumeIngredient = Math.round(kgAnnuel); // Utiliser la valeur calculée, pas recalculer
              
              valueDisplay.innerHTML = '<strong style="color: #D92332; font-size: 1.1rem;">-' + reductionPct + '%</strong>';
              // Argument négo enrichi avec évolution
              let argumentNego = '"Engagement ' + volumeIngredient.toLocaleString() + ' kg/an sur 12 mois, paiement 30j';
              if (evolutionPct > 0) {{
                argumentNego += ', <strong>croissance ' + (evolutionPct > 50 ? 'forte' : 'régulière') + ' +' + evolutionPct.toFixed(0) + '%</strong>';
              }} else if (evolutionPct < -10) {{
                argumentNego += ', ajustement volume anticipé ' + evolutionPct.toFixed(0) + '%';
              }}
              argumentNego += '"';
              
              resultDiv.innerHTML = 
                '<div style="display: grid; gap: 0.5rem;">' +
                '<div style="padding: 0.5rem; background: #f8fafc; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Nouveau coût plat</span><br/>' +
                '<strong style="color: #10b981; font-size: 0.95rem;">' + nouveauCoutPlat.toFixed(2) + ' €</strong> <span style="text-decoration: line-through; color: #94a3b8; font-size: 0.75rem;">' + diag.cout_matiere.toFixed(2) + '€</span>' +
                '</div>' +
                '<div style="padding: 0.5rem; background: #f0fdf4; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Économies annuelles</span><br/>' +
                '<strong style="color: #10b981; font-size: 0.95rem;">+' + economieAnnuelle.toLocaleString() + ' €</strong>' +
                '</div>' +
                '<div style="padding: 0.5rem; background: ' + (objectifAtteint ? '#f0fdf4' : '#fffbeb') + '; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Nouvelle marge</span><br/>' +
                '<strong style="color: ' + (objectifAtteint ? '#10b981' : '#f59e0b') + '; font-size: 0.95rem;">' + nouvelleMarge + '%</strong> <span style="font-size: 0.75rem;">' + (objectifAtteint ? '✓' : '·') + '</span>' +
                '</div>' +
                '<div style="padding: 0.5rem; background: #f8fafc; border-radius: 6px;">' +
                '<span style="color: #64748b; font-size: 0.7rem; font-weight: 500;">Impact marge (' + volumeAnnuelN1.toLocaleString() + ' N-1)</span><br/>' +
                '<strong style="font-size: 0.85rem; color: #0f172a;">' + margeAnnuelleNv.toLocaleString() + ' €</strong> <span style="font-size: 0.7rem; color: #64748b;">(+' + gainMarge.toLocaleString() + '€)</span>' +
                '</div>' +
                '<div style="padding: 0.5rem; background: #f0fdf4; border-radius: 6px;">' +
                '<span style="color: #15803d; font-size: 0.7rem; font-weight: 600;">Argument négo</span><br/>' +
                '<small style="color: #166534; font-size: 0.75rem; line-height: 1.4;">' + argumentNego + '</small>' +
                '</div>' +
                '</div>';
            }};
            
            sliderNego.addEventListener('input', updateNego);
            
            gaugeContainer.appendChild(labelNego);
            gaugeContainer.appendChild(sliderNego);
            gaugeContainer.appendChild(valueDisplay);
            quickZone.appendChild(gaugeContainer);
            quickZone.appendChild(resultDiv);
            updateNego();
            
            // Bouton retour
            const backBtn = doc.createElement('button');
            backBtn.type = 'button';
            backBtn.innerHTML = '← Retour';
            backBtn.style.cssText = 'margin-top: 0.5rem; padding: 0.65rem; background: #ffffff; color: #64748b; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; transition: all 0.2s; width: 100%; font-size: 0.85rem;';
            backBtn.addEventListener('mouseenter', () => {{ backBtn.style.background = '#f8fafc'; }});
            backBtn.addEventListener('mouseleave', () => {{ backBtn.style.background = '#ffffff'; }});
            backBtn.addEventListener('click', () => {{
              showDiagnostic(platNom);
            }});
            quickZone.appendChild(backBtn);
          }} else {{
            appendMessage('bot', 'Aucune négociation nécessaire pour ce plat.');
            
            // Bouton retour même si pas de négo
            const backBtn = doc.createElement('button');
            backBtn.type = 'button';
            backBtn.innerHTML = '← Retour';
            backBtn.style.cssText = 'margin-top: 0.5rem; padding: 0.65rem; background: #ffffff; color: #64748b; border: 1px solid #e2e8f0; border-radius: 6px; cursor: pointer; transition: all 0.2s; width: 100%; font-size: 0.85rem;';
            backBtn.addEventListener('mouseenter', () => {{ backBtn.style.background = '#f8fafc'; }});
            backBtn.addEventListener('mouseleave', () => {{ backBtn.style.background = '#ffffff'; }});
            backBtn.addEventListener('click', () => {{
              showDiagnostic(platNom);
            }});
            quickZone.appendChild(backBtn);
          }}
        }}
      }};

        // Désactiver l'input texte (navigation par boutons uniquement)
        if (input) input.style.display = 'none';
        if (sendBtn) sendBtn.style.display = 'none';

        // Message d'accueil
        showWelcome();
        
        console.log('✅ Chatbot initialisé avec succès');
      }} catch (error) {{
        console.error('❌ Erreur chatbot:', error);
      }}
    }})();
    </script>
    """

    # Debug: afficher un message pour confirmer que la fonction est appelée
    print(f"[DEBUG render_floating_chatbot] Rendu du chatbot - {len(guided_data.get('plats', []))} plats, {stats['nbProblems']} problèmes")
    
    with open('debug_chatbot_script.js', 'w', encoding='utf-8') as _debug_file:
      _debug_file.write(script)
    components.html(script, height=0, width=0)


__all__ = ["render_floating_chatbot"]
