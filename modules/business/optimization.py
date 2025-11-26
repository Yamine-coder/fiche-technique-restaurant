"""
Module d'optimisation des grammages pour atteindre des objectifs de marge.

Ce module fournit plusieurs algorithmes d'optimisation pour ajuster les quantités
d'ingrédients dans les recettes tout en respectant des contraintes de coût et de marge.
"""

import numpy as np
import pandas as pd
import pulp
from scipy.optimize import linprog

from modules.business.cost_calculator import calculer_cout


def optimize_grammages_linprog(df_ing, prix_affiche, marge_cible, q_min=5):
    """
    Optimise les grammages en utilisant la programmation linéaire (linprog).
    
    Minimise ∑ dᵢ avec qᵢ ≥ q_min, dᵢ ≥ |qᵢ–q0ᵢ|,
    sous contrainte ∑(qᵢ·prix_kgᵢ/1000) ≤ budget.
    Exclut toute pâte de l'optimisation (reste fixe).
    
    Args:
        df_ing (pd.DataFrame): DataFrame des ingrédients avec colonnes 'ingredient', 
                               'quantite_g', 'prix_kg', 'Coût (€)'
        prix_affiche (float): Prix de vente affiché du plat
        marge_cible (float): Marge cible en pourcentage (ex: 70 pour 70%)
        q_min (int): Quantité minimale en grammes pour chaque ingrédient (défaut: 5)
    
    Returns:
        pd.DataFrame: DataFrame avec colonnes 'new_qty' et 'new_cout' ajoutées
    """
    all_ing = df_ing["ingredient"].tolist()
    # on ne touche pas aux pâtes
    fixed = [i for i in all_ing if "pâte à pizza" in i.lower() or "pâte à panini" in i.lower()]
    opt_ing = [i for i in all_ing if i not in fixed]
    n = len(opt_ing)
    prix_kg = dict(zip(all_ing, df_ing["prix_kg"]))
    q0      = dict(zip(all_ing, df_ing["quantite_g"]))
    budget  = prix_affiche * (1 - marge_cible/100)

    # variables x = [q_0…q_{n-1}, d_0…d_{n-1}]
    c = np.hstack([np.zeros(n), np.ones(n)])
    # bornes
    bounds = [(q_min, None)]*n + [(0, None)]*n

    # A_ub x ≤ b_ub
    rows = []
    rhs  = []

    # 1) coût total ≤ budget
    a = np.zeros(2*n)
    for j, ing in enumerate(opt_ing):
        a[j] = prix_kg[ing] / 1000
    rows.append(a)
    rhs.append(budget)

    # 2) linéarisation |q–q0|
    for j, ing in enumerate(opt_ing):
        # q_j - d_j ≤ q0_j
        r = np.zeros(2*n); r[j] = 1; r[n+j] = -1
        rows.append(r); rhs.append(q0[ing])
        # -q_j - d_j ≤ -q0_j
        r = np.zeros(2*n); r[j] = -1; r[n+j] = -1
        rows.append(r); rhs.append(-q0[ing])

    A_ub = np.vstack(rows)
    b_ub = np.array(rhs)

    sol = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not sol.success:
        # Si l'optimisation échoue, retourner les valeurs originales
        df2 = df_ing.copy()
        df2["new_qty"] = df2["quantite_g"]
        df2["new_cout"] = df2["Coût (€)"]
        return df2

    q_opt = sol.x[:n]
    df2 = df_ing.copy()
    def get_new(ing):
        if ing in opt_ing:
            idx = opt_ing.index(ing)
            if 0 <= idx < len(q_opt):
                return max(q_min, float(q_opt[idx]))
            return q0[ing]
        return q0[ing]
    df2["new_qty"]  = df2["ingredient"].apply(get_new)
    df2["new_cout"] = df2["new_qty"] * df2["prix_kg"] / 1000
    return df2


def optimize_grammages_balanced(df_ing, prix_affiche, marge_cible, q_min=5):
    """
    Optimise les grammages en répartissant équitablement les réductions.
    
    Utilise l'approche minimax (Chebyshev) pour minimiser l'écart maximum
    en pourcentage sur l'ensemble des ingrédients. Cette méthode garantit
    que tous les ingrédients sont réduits de manière proportionnelle.
    
    Args:
        df_ing (pd.DataFrame): DataFrame des ingrédients avec colonnes 'ingredient', 
                               'quantite_g', 'prix_kg', 'Coût (€)'
        prix_affiche (float): Prix de vente affiché du plat
        marge_cible (float): Marge cible en pourcentage (ex: 70 pour 70%)
        q_min (int): Quantité minimale en grammes pour chaque ingrédient (défaut: 5)
    
    Returns:
        pd.DataFrame: DataFrame avec colonnes 'new_qty' et 'new_cout' ajoutées
    """
    # Séparation des ingrédients fixes (pâtes) et variables
    all_ing = df_ing["ingredient"].tolist()
    fixed = [i for i in all_ing if "pâte" in i.lower()]
    opt_ing = [i for i in all_ing if i not in fixed]
    
    # Extraction des données
    prix_kg = dict(zip(all_ing, df_ing["prix_kg"]))
    q0 = dict(zip(all_ing, df_ing["quantite_g"]))
    budget = prix_affiche * (1 - marge_cible/100)
    
    # Coût fixe des pâtes
    fixed_cost = sum(q0[i] * prix_kg[i] / 1000 for i in fixed)
    
    # Budget disponible pour les ingrédients variables
    remaining_budget = budget - fixed_cost
    
    # Création du problème d'optimisation
    prob = pulp.LpProblem("OptimisationEquilibree", pulp.LpMinimize)
    
    # Variables: qᵢ (nouveaux grammages)
    q = {ing: pulp.LpVariable(f"q_{i}", lowBound=q_min) 
         for i, ing in enumerate(opt_ing)}
    
    # Variable max_pct_reduction: écart maximal en pourcentage
    max_pct_reduction = pulp.LpVariable("max_pct_reduction", lowBound=0, upBound=1)
    
    # Contrainte de budget
    prob += pulp.lpSum(q[ing] * prix_kg[ing] / 1000 for ing in opt_ing) <= remaining_budget
    
    # Contrainte minimax: pour chaque ingrédient, la réduction proportionnelle est ≤ max_pct_reduction
    for ing in opt_ing:
        if q0[ing] > 0:  # Éviter division par zéro
            prob += (q0[ing] - q[ing])/q0[ing] <= max_pct_reduction
            prob += q[ing] <= q0[ing]  # On ne peut pas augmenter les quantités
    
    # Objectif: minimiser la réduction maximale en %
    prob += max_pct_reduction
    
    # Résolution
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Vérification du statut de résolution
    if prob.status != pulp.LpStatusOptimal:
        # Si l'optimisation échoue, retourner les valeurs originales
        df_result = df_ing.copy()
        df_result["new_qty"] = df_result["quantite_g"]
        df_result["new_cout"] = df_result["Coût (€)"]
        return df_result
    
    # Construction du résultat
    df_result = df_ing.copy()
    
    # Appliquer les nouvelles quantités
    for ing in all_ing:
        if ing in opt_ing:
            new_val = q[ing].value()
            if new_val is not None:
                # Arrondir au multiple de 5 le plus proche
                df_result.loc[df_result["ingredient"] == ing, "new_qty"] = max(q_min, round(new_val/5)*5)
            else:
                # Si la valeur est None, garder la quantité originale
                df_result.loc[df_result["ingredient"] == ing, "new_qty"] = q0[ing]
        else:
            df_result.loc[df_result["ingredient"] == ing, "new_qty"] = q0[ing]
    
    # Calculer les nouveaux coûts
    df_result["new_cout"] = df_result["new_qty"] * df_result["prix_kg"] / 1000
    
    return df_result


def optimize_grammages_exact(df_ing, prix_affiche, marge_cible, q_min=5):
    """
    Optimisation en deux phases pour atteindre exactement la marge cible.
    
    Phase 1: Minimiser les changements avec contrainte de marge minimale
    Phase 2: Ajuster proportionnellement pour atteindre exactement la marge cible
    
    Args:
        df_ing (pd.DataFrame): DataFrame des ingrédients avec colonnes 'ingredient', 
                               'quantite_g', 'prix_kg', 'Coût (€)'
        prix_affiche (float): Prix de vente affiché du plat
        marge_cible (float): Marge cible en pourcentage (ex: 70 pour 70%)
        q_min (int): Quantité minimale en grammes pour chaque ingrédient (défaut: 5)
    
    Returns:
        pd.DataFrame: DataFrame avec colonnes 'new_qty' et 'new_cout' ajoutées
    """
    # Phase 1: Optimisation standard (comme avant)
    df_opt = optimize_grammages_balanced(df_ing, prix_affiche, marge_cible, q_min)
    
    # Phase 2: Ajustement pour atteindre exactement la marge cible
    cout_opt = df_opt["new_cout"].sum()
    cout_cible = prix_affiche * (1 - marge_cible/100)
    
    # Si le coût est trop bas (marge trop élevée), ajuster à la hausse
    if cout_opt < cout_cible:
        # Exclure les ingrédients fixes
        mask_fixed = df_opt["ingredient"].str.lower().str.contains("pâte")
        ajustables = ~mask_fixed
        
        if ajustables.any():
            # Facteur d'ajustement pour atteindre exactement le coût cible
            cout_ajustable = df_opt.loc[ajustables, "new_cout"].sum()
            facteur = (cout_cible - df_opt.loc[~ajustables, "new_cout"].sum()) / cout_ajustable
            
            # Appliquer l'ajustement sur les quantités et coûts
            df_opt.loc[ajustables, "new_qty"] *= facteur
            df_opt.loc[ajustables, "new_cout"] *= facteur
            
            # Arrondir au multiple de 5 le plus proche
            df_opt.loc[ajustables, "new_qty"] = (df_opt.loc[ajustables, "new_qty"] / 5).round() * 5
            df_opt.loc[ajustables, "new_cout"] = df_opt.loc[ajustables, "new_qty"] * df_opt.loc[ajustables, "prix_kg"] / 1000
    
    return df_opt


def optimize_top2_ingredients(df_ing, prix_affiche, marge_cible, q_min=5):
    """
    Optimise uniquement les 2 ingrédients les plus coûteux pour atteindre la marge cible.
    
    Cette approche ciblée réduit principalement les ingrédients qui ont le plus d'impact
    sur le coût, en laissant les autres ingrédients inchangés.
    
    Args:
        df_ing (pd.DataFrame): DataFrame des ingrédients avec colonnes 'ingredient', 
                               'quantite_g', 'prix_kg', 'Coût (€)'
        prix_affiche (float): Prix de vente affiché du plat
        marge_cible (float): Marge cible en pourcentage (ex: 70 pour 70%)
        q_min (int): Quantité minimale en grammes pour chaque ingrédient (défaut: 5)
    
    Returns:
        pd.DataFrame: DataFrame avec colonnes 'new_qty' et 'new_cout' ajoutées
    """
    # Récupération des ingrédients et de leurs coûts
    ingr_courant = df_ing.copy()
    ingr_courant = calculer_cout(ingr_courant)
    
    # Exclure les pâtes de l'optimisation
    mask_pate = ingr_courant["ingredient"].str.lower().str.contains("pâte")
    ingr_ajustables = ingr_courant[~mask_pate].copy()
    
    # S'il n'y a pas assez d'ingrédients ajustables, renvoyer les valeurs initiales
    if len(ingr_ajustables) < 2:
        df_ing["new_qty"] = df_ing["quantite_g"]
        df_ing["new_cout"] = df_ing["Coût (€)"]
        return df_ing
    
    # Sélectionner les 2 ingrédients les plus coûteux
    top2 = ingr_ajustables.nlargest(2, "Coût (€)")
    
    # Calculer le coût actuel et le budget disponible
    cout_total = ingr_courant["Coût (€)"].sum()
    cout_cible = prix_affiche * (1 - marge_cible/100)
    
    # Si déjà sous le seuil, ne rien changer
    if cout_total <= cout_cible:
        df_ing["new_qty"] = df_ing["quantite_g"]
        df_ing["new_cout"] = df_ing["Coût (€)"]
        return df_ing
    
    # Coût des ingrédients non ajustables
    cout_fixe = ingr_courant[~ingr_courant.index.isin(top2.index)]["Coût (€)"].sum()
    
    # Budget restant pour les top2
    budget_top2 = cout_cible - cout_fixe
    cout_top2 = top2["Coût (€)"].sum()
    
    # Facteur de réduction
    facteur = max(0.05, min(1.0, budget_top2 / cout_top2))
    
    # Appliquer la réduction aux top2 ingrédients
    df_result = df_ing.copy()
    for idx, row in top2.iterrows():
        ing = row["ingredient"]
        old_qty = row["quantite_g"]
        # Réduire et arrondir au multiple de 5 le plus proche
        new_qty = max(q_min, round((old_qty * facteur) / 5) * 5)
        
        # Mettre à jour les valeurs
        mask = df_result["ingredient"] == ing
        df_result.loc[mask, "new_qty"] = new_qty
        df_result.loc[mask, "new_cout"] = (new_qty * df_result.loc[mask, "prix_kg"]) / 1000
    
    # Pour les autres ingrédients, garder les valeurs initiales
    mask_autres = ~df_result["ingredient"].isin(top2["ingredient"])
    df_result.loc[mask_autres, "new_qty"] = df_result.loc[mask_autres, "quantite_g"]
    df_result.loc[mask_autres, "new_cout"] = df_result.loc[mask_autres, "Coût (€)"]
    
    return df_result
