"""
Module d'insights intelligents basés sur les données de ventes Kezia
"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple
from difflib import SequenceMatcher


def normalize_product_name(name: str) -> str:
    """
    Normalise un nom de produit pour le matching
    """
    name = name.lower().strip()
    
    # Conversions communes
    replacements = {
        ' m': ' 2 pers',
        ' s': ' 1 pers',
        'pâte ': 'pasta ',
        'pate ': 'pasta ',
        'mexicaine': 'mexicaine',
        'panini pizz': 'panini',
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    return name


def find_best_match_in_db(product_name: str, db_path: str) -> Optional[str]:
    """
    Trouve la meilleure correspondance dans la base SQLite
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT produit FROM ventes")
        all_products = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Normaliser le nom recherché
        normalized_search = normalize_product_name(product_name)
        
        best_match = None
        best_score = 0
        
        for db_product in all_products:
            normalized_db = normalize_product_name(db_product)
            
            # Calcul de similarité
            ratio = SequenceMatcher(None, normalized_search, normalized_db).ratio()
            
            # Bonus si contient des mots clés
            if any(word in normalized_db for word in normalized_search.split() if len(word) > 3):
                ratio += 0.2
            
            if ratio > best_score:
                best_score = ratio
                best_match = db_product
        
        # Seuil de confiance
        if best_score >= 0.6:
            return best_match
        
        return None
        
    except Exception as e:
        print(f"Erreur lors du matching: {e}")
        return None


def get_product_sales_insight(product_name: str, db_path: str = "data/kezia_sales.db") -> Optional[Dict]:
    """
    Génère un insight intelligent pour un produit basé sur ses ventes réelles
    
    Args:
        product_name: Nom du produit à analyser
        db_path: Chemin vers la base SQLite
    
    Returns:
        Dict avec les insights ou None si pas de données
    """
    if not Path(db_path).exists():
        return None
    
    # Essayer de trouver une correspondance dans la base
    matched_product = find_best_match_in_db(product_name, db_path)
    
    if not matched_product:
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Ventes des 7 derniers jours
        cursor.execute("""
            SELECT 
                SUM(quantite) as total_qty,
                SUM(ca_ttc) as total_ca,
                COUNT(DISTINCT date) as nb_jours,
                AVG(prix_moyen) as prix_moyen
            FROM ventes
            WHERE produit = ?
            AND date >= date('now', '-7 days')
        """, (matched_product,))
        
        result_7d = cursor.fetchone()
        
        if not result_7d or result_7d[0] is None:
            conn.close()
            return None
        
        total_qty_7d = result_7d[0] or 0
        total_ca_7d = result_7d[1] or 0
        nb_jours_7d = result_7d[2] or 1
        prix_moyen = result_7d[3] or 0
        
        # 2. Ventes du mois en cours
        cursor.execute("""
            SELECT 
                SUM(quantite) as total_qty,
                SUM(ca_ttc) as total_ca
            FROM ventes
            WHERE produit = ?
            AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        """, (matched_product,))
        
        result_month = cursor.fetchone()
        total_qty_month = result_month[0] or 0
        total_ca_month = result_month[1] or 0
        
        # 3. Comparaison avec le mois dernier
        cursor.execute("""
            SELECT 
                SUM(quantite) as total_qty
            FROM ventes
            WHERE produit = ?
            AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')
        """, (matched_product,))
        
        result_last_month = cursor.fetchone()
        total_qty_last_month = result_last_month[0] or 0
        
        # 4. Jour de la semaine le plus populaire
        cursor.execute("""
            SELECT 
                CASE CAST(strftime('%w', date) AS INTEGER)
                    WHEN 0 THEN 'Dimanche'
                    WHEN 1 THEN 'Lundi'
                    WHEN 2 THEN 'Mardi'
                    WHEN 3 THEN 'Mercredi'
                    WHEN 4 THEN 'Jeudi'
                    WHEN 5 THEN 'Vendredi'
                    WHEN 6 THEN 'Samedi'
                END as jour,
                SUM(quantite) as total
            FROM ventes
            WHERE produit = ?
            AND date >= date('now', '-30 days')
            GROUP BY strftime('%w', date)
            ORDER BY total DESC
            LIMIT 1
        """, (matched_product,))
        
        best_day = cursor.fetchone()
        best_day_name = best_day[0] if best_day else None
        best_day_qty = best_day[1] if best_day else 0
        
        # 5. Classement du produit (top produits du mois)
        cursor.execute("""
            SELECT produit, SUM(quantite) as total
            FROM ventes
            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
            GROUP BY produit
            ORDER BY total DESC
        """)
        
        all_products = cursor.fetchall()
        product_rank = None
        for idx, (prod, _) in enumerate(all_products, 1):
            if prod == matched_product:
                product_rank = idx
                break
        
        conn.close()
        
        # Calculs dérivés
        avg_qty_per_day = total_qty_7d / max(nb_jours_7d, 1)
        evolution_pct = 0
        if total_qty_last_month > 0:
            evolution_pct = ((total_qty_month - total_qty_last_month) / total_qty_last_month) * 100
        
        return {
            "total_qty_7d": int(total_qty_7d),
            "total_ca_7d": round(total_ca_7d, 2),
            "avg_qty_per_day": round(avg_qty_per_day, 1),
            "prix_moyen": round(prix_moyen, 2),
            "total_qty_month": int(total_qty_month),
            "total_ca_month": round(total_ca_month, 2),
            "evolution_vs_last_month": round(evolution_pct, 1),
            "best_day": best_day_name,
            "best_day_qty": int(best_day_qty) if best_day_qty else 0,
            "product_rank": product_rank,
            "total_products": len(all_products),
        }
        
    except Exception as e:
        print(f"Erreur lors de la récupération des insights: {e}")
        return None


def format_insight_message(product_name: str, insights: Dict) -> str:
    """
    Formate un message d'insight intelligent basé sur les données
    
    Args:
        product_name: Nom du produit
        insights: Dict des insights calculés
    
    Returns:
        Message HTML formaté
    """
    if not insights:
        return ""
    
    # Déterminer le niveau de popularité
    if insights["product_rank"] and insights["total_products"]:
        rank_pct = (insights["product_rank"] / insights["total_products"]) * 100
        
        if rank_pct <= 10:
            popularity = "⭐ **Top seller** du mois"
            popularity_color = "#16a34a"
        elif rank_pct <= 25:
            popularity = "🔥 **Très populaire**"
            popularity_color = "#D92332"
        elif rank_pct <= 50:
            popularity = "👍 **Bien vendu**"
            popularity_color = "#2563eb"
        else:
            popularity = "📊 **Ventes standard**"
            popularity_color = "#64748b"
    else:
        popularity = "📊 **Ventes en cours**"
        popularity_color = "#64748b"
    
    # Tendance
    evolution = insights["evolution_vs_last_month"]
    if evolution > 10:
        trend = f"📈 <span style='color:#16a34a;'>+{evolution:.0f}%</span> vs mois dernier"
    elif evolution < -10:
        trend = f"📉 <span style='color:#dc2626;'>{evolution:.0f}%</span> vs mois dernier"
    else:
        trend = f"➡️ <span style='color:#64748b;'>Stable</span> ({evolution:+.0f}%)"
    
    # Construction du message
    message = f"""<div style="background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%); border: 1px solid #e2e8f0; border-left: 3px solid {popularity_color}; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
<div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
<span style="font-size: 1.1rem;">💡</span>
<strong style="color: #1e293b; font-size: 0.95rem;">Insights Ventes Réelles</strong>
</div>
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin: 0.75rem 0;">
<div style="background: white; padding: 0.5rem; border-radius: 6px; border: 1px solid #f1f5f9;">
<div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.2rem;">7 derniers jours</div>
<div style="font-size: 1.1rem; font-weight: 600; color: #0f172a;">{insights["total_qty_7d"]} ventes</div>
<div style="font-size: 0.7rem; color: #64748b; margin-top: 0.1rem;">≈ {insights["avg_qty_per_day"]:.1f}/jour · {insights["total_ca_7d"]:.2f}€</div>
</div>
<div style="background: white; padding: 0.5rem; border-radius: 6px; border: 1px solid #f1f5f9;">
<div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.2rem;">Ce mois</div>
<div style="font-size: 1.1rem; font-weight: 600; color: #0f172a;">{insights["total_qty_month"]} ventes</div>
<div style="font-size: 0.7rem; color: #64748b; margin-top: 0.1rem;">{insights["total_ca_month"]:.2f}€ de CA</div>
</div>
</div>
<div style="display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.8rem; color: #475569; padding-top: 0.5rem; border-top: 1px solid #f1f5f9;">
<div><strong style="color: {popularity_color};">{popularity}</strong> (#{insights["product_rank"]}/{insights["total_products"]})</div>
<div>{trend}</div>"""
    
    # Meilleur jour
    if insights["best_day"]:
        message += f"""<div>🗓️ Meilleur jour: <strong>{insights["best_day"]}</strong></div>"""
    
    message += """</div></div>"""
    
    return message
