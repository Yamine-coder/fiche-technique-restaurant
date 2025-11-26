"""
Composants pour les simulateurs d'aide à la décision.
"""

import streamlit as st
import pandas as pd
from config import TVA_VENTE


def render_global_simulator(
    df_plats: pd.DataFrame,
    tva_vente: float,
    objectif_marge: float,
    container=None,
    state_prefix: str = "global_decision_simulator",
) -> None:
    """
    Affiche le simulateur global pour projeter les volumes, prix et marges sur plusieurs plats.
    
    Args:
        df_plats: DataFrame avec les données des plats
        tva_vente: Taux de TVA appliqué
        objectif_marge: Objectif de marge (%)
        container: Container Streamlit optionnel
        state_prefix: Préfixe pour les clés de session
    """
    if df_plats.empty:
        return

    target = container or st
    selection_key = f"{state_prefix}_selection"
    objectif_key = f"{state_prefix}_objectif"
    variation_cout_key = f"{state_prefix}_variation_cout"
    variation_prix_key = f"{state_prefix}_variation_prix"

    target.markdown(
        """
        <div class="global-simulator">
            <h3>Simulateur global d'aide à la décision</h3>
            <small>Répondez en un clic aux questions du patron : volumes, prix et marges.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    default_selection = df_plats.sort_values("marge_pct", ascending=False)["nom"].head(4).tolist()
    session_state = st.session_state
    if selection_key not in session_state or not session_state[selection_key]:
        session_state[selection_key] = default_selection
    session_state.setdefault(objectif_key, 2000.0)
    session_state.setdefault(variation_cout_key, 0)
    session_state.setdefault(variation_prix_key, 0.0)

    with target.form(f"{state_prefix}_form"):
        selected_plats = target.multiselect(
            "Sélectionnez les plats à projeter",
            options=df_plats["nom"].tolist(),
            default=default_selection,
            key=selection_key,
        )
        objectif_financier = target.number_input(
            "Objectif financier à atteindre (€ HT)",
            min_value=500.0,
            step=100.0,
            key=objectif_key,
        )
        col_var_cost, col_var_price = target.columns(2)
        with col_var_cost:
            variation_cout = target.slider(
                "Variation fournisseurs (%)",
                -20,
                20,
                help="Simulez une hausse ou baisse globale des coûts matières",
                key=variation_cout_key,
            )
        with col_var_price:
            variation_prix = target.slider(
                "Ajustement prix carte (€/plat TTC)",
                -3.0,
                3.0,
                step=0.1,
                help="Testez une variation uniforme du prix de vente",
                key=variation_prix_key,
            )
        submitted = target.form_submit_button("Calculer la projection", use_container_width=True)

    if not submitted:
        return
    if not selected_plats:
        target.warning("Sélectionnez au moins un plat pour lancer la simulation.")
        return

    records = []
    df_selection = df_plats[df_plats["nom"].isin(selected_plats)]
    total_marge = 0.0
    for _, row in df_selection.iterrows():
        cout_ht = row["cout_matiere"] * (1 + variation_cout / 100)
        prix_ttc = max(0.5, row["prix_ttc"] + variation_prix)
        prix_ht = prix_ttc / (1 + tva_vente)
        marge_euros = max(prix_ht - cout_ht, 0.0)
        marge_pct = (marge_euros / prix_ht * 100) if prix_ht > 0 else 0.0
        volume_cible = objectif_financier / marge_euros if marge_euros > 0 else None
        total_marge += marge_euros
        records.append({
            "Plat": row["nom"],
            "Marge unitaire (€)": round(marge_euros, 2),
            "Marge (%)": round(marge_pct, 1),
            "Prix carte simulé (€ TTC)": round(prix_ttc, 2),
            "Coût matière simulé (€)": round(cout_ht, 2),
            "Volume pour objectif": f"{volume_cible:.1f}" if volume_cible else "—",
        })

    result_df = pd.DataFrame(records)
    target.dataframe(result_df, use_container_width=True)

    if total_marge > 0:
        target.markdown(
            f"<div style='margin-top:0.5rem; font-size:0.85rem; color:#475569;'>"
            f"Chaque plat sélectionné génère en moyenne <strong>{total_marge/len(records):.2f}€</strong> de marge unitaire dans ce scénario."
            f"</div>",
            unsafe_allow_html=True,
        )


def render_decision_simulator(
    plat_nom: str,
    prix_ht: float,
    prix_ttc: float,
    cout_matiere: float,
    ingredients_df: pd.DataFrame,
    objectif_marge: float,
    container=None,
) -> None:
    """
    Affiche le simulateur de décision pour un plat spécifique avec 3 onglets :
    - Volume : Combien vendre pour atteindre un objectif
    - Prix : Quel prix pratiquer pour une marge cible
    - Négociation : Quelle réduction négocier sur les ingrédients
    
    Args:
        plat_nom: Nom du plat
        prix_ht: Prix HT
        prix_ttc: Prix TTC
        cout_matiere: Coût matière
        ingredients_df: DataFrame des ingrédients
        objectif_marge: Objectif de marge (%)
        container: Container Streamlit optionnel
    """
    if prix_ht is None or prix_ht <= 0:
        return

    target = container or st
    plat_key = plat_nom.replace(" ", "_").lower()

    target.markdown(
        f"""
        <div class="decision-wrapper">
            <h3>🎯 Simulateur de décision : {plat_nom}</h3>
            <div class="decision-note">Trois scénarios pour optimiser ce plat</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    marge_unitaire = max(prix_ht - cout_matiere, 0.0)
    tab_volume, tab_prix, tab_negociation = target.tabs(["📦 Volume", "💰 Prix", "🤝 Négociation"])

    with tab_volume:
        objectif_ht = target.number_input(
            "Objectif financier (€ HT)",
            min_value=500.0,
            value=2000.0,
            step=100.0,
            key=f"objectif_volume_{plat_key}",
        )
        if marge_unitaire <= 0:
            target.error("Ce plat ne génère pas de marge actuellement.")
        else:
            volume = objectif_ht / marge_unitaire
            quotidien = volume / 30
            target.metric("Volumes à vendre", f"{volume:.1f} plats")
            target.caption(f"≈ {quotidien:.1f} plats par jour (sur 30 jours)")

    with tab_prix:
        marge_cible = target.slider(
            "Taux de marge cible (%)",
            40,
            85,
            int(objectif_marge),
            key=f"marge_cible_{plat_key}",
        )
        cout_reference = cout_matiere
        prix_ht_cible = cout_reference / (1 - marge_cible / 100) if marge_cible < 100 else None
        if prix_ht_cible is None:
            target.error("Sélectionnez un objectif réaliste (<100%).")
        else:
            prix_ttc_cible = prix_ht_cible * (1 + TVA_VENTE)
            delta = prix_ttc_cible - prix_ttc if prix_ttc else None
            target.metric("Prix TTC conseillé", f"{prix_ttc_cible:.2f}€", f"{delta:+.2f}€" if delta else None)
            target.caption("Basé sur votre coût matière actuel.")

    with tab_negociation:
        cout_cible = prix_ht * (1 - objectif_marge / 100)
        delta = cout_matiere - cout_cible
        if delta <= 0:
            target.success("Ce plat respecte déjà l'objectif de marge.")
        else:
            reduction_pct = delta / cout_matiere * 100 if cout_matiere > 0 else 0
            target.warning(
                f"Il manque {delta:.2f}€ sur la matière pour atteindre {objectif_marge:.0f}% (soit {reduction_pct:.1f}% du coût)."
            )
            if ingredients_df.empty:
                target.info("Pas de détail ingrédient disponible pour simuler une négociation.")
                return
            ingredients_df = ingredients_df.sort_values("Coût (€)", ascending=False)
            ingredient_names = ingredients_df["ingredient"].tolist()
            choix = target.selectbox("Ingrédient à cibler", ingredient_names, key=f"negociation_ing_{plat_key}")
            cout_ing = ingredients_df.loc[ingredients_df["ingredient"] == choix, "Coût (€)"].iloc[0]
            if cout_ing <= 0:
                target.info("Ingrédient sans coût : choisissez-en un autre.")
                return
            reduction_requise_pct = min(100.0, (delta / cout_ing) * 100)
            slider_max = min(100.0, max(reduction_requise_pct * 1.3, 10.0))
            reduction_simulee = target.slider(
                "Réduction envisagée sur cet ingrédient (%)",
                0.0,
                slider_max,
                value=min(reduction_requise_pct, slider_max),
                step=0.5,
                key=f"negociation_pct_{plat_key}",
            )
            gain = cout_ing * (reduction_simulee / 100)
            cout_apres = max(cout_matiere - gain, 0.0)
            marge_apres = max(prix_ht - cout_apres, 0.0)
            taux_apres = (marge_apres / prix_ht * 100) if prix_ht > 0 else 0
            target.metric("Nouvelle marge", f"{taux_apres:.1f}%", f"{taux_apres - objectif_marge:+.1f} pts")
            target.caption(
                f"Réduction nécessaire sur {choix} pour atteindre l'objectif : {reduction_requise_pct:.1f}%."
            )
