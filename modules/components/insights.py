"""
Composants pour afficher les insights et métriques clés.
"""

import streamlit as st
import pandas as pd


def render_overview_insights(df_plats: pd.DataFrame, objectif_marge: float) -> None:
    """
    Affiche une ceinture d'insights avec les métriques clés :
    - Nombre de plats sous objectif
    - Top marge
    - Objectif de marge
    
    Args:
        df_plats: DataFrame avec les données des plats
        objectif_marge: Seuil de marge à atteindre (%)
    """
    if df_plats.empty:
        return

    sous_objectif = df_plats[df_plats["marge_pct"] < objectif_marge]
    best_row = df_plats.sort_values("marge_pct", ascending=False).head(1)
    weak_row = sous_objectif.sort_values("marge_pct").head(1)

    best_name = best_row["nom"].iloc[0] if not best_row.empty else "—"
    best_rate = best_row["marge_pct"].iloc[0] if not best_row.empty else 0
    weak_name = weak_row["nom"].iloc[0] if not weak_row.empty else "—"
    weak_rate = weak_row["marge_pct"].iloc[0] if not weak_row.empty else 0

    st.markdown(
        f"""
        <div class="insights-belt">
            <div class="insight-card">
                <div class="insight-label">Sous objectif</div>
                <div class="insight-value">{sous_objectif.shape[0]} / {df_plats.shape[0]}</div>
                <div class="insight-meta">{"Aucun plat" if sous_objectif.empty else f"{weak_name} ({weak_rate:.1f}% de marge)"}</div>
                <div class="insight-action">⚠️ Prioriser ces recettes</div>
            </div>
            <div class="insight-card">
                <div class="insight-label">Top marge</div>
                <div class="insight-value">{best_rate:.1f}%</div>
                <div class="insight-meta">{best_name}</div>
                <div class="insight-action">🔥 Répliquer ce modèle</div>
            </div>
            <div class="insight-card">
                <div class="insight-label">Objectif</div>
                <div class="insight-value">{objectif_marge:.0f}%</div>
                <div class="insight-meta">Seuil de marge matière</div>
                <div class="insight-action">🎯 Ajustez depuis la barre latérale</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
