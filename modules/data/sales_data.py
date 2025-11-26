"""
📊 SALES DATA LOADER - Chargement données ventes depuis SQLite
✅ Queries ultra-rapides (<0.1s)
✅ Compatible Streamlit avec cache
✅ API simple pour le frontend
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

# Import du gestionnaire DB (optionnel pour déploiement sans DB)
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from kezia_db_manager import get_db_manager
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("[WARN] kezia_db_manager non disponible, mode sans DB")
    
def get_db_manager():
    """Wrapper pour gérer l'absence de DB"""
    if not DB_AVAILABLE:
        return None
    from kezia_db_manager import get_db_manager as _get_db
    return _get_db()

@st.cache_data(ttl=300)  # Cache 5 minutes
def load_ventes(nb_jours: int = 30, 
                date_debut: Optional[str] = None,
                date_fin: Optional[str] = None,
                produit: Optional[str] = None,
                temporality: str = 'hour') -> pd.DataFrame:
    """
    Charge les ventes depuis SQLite avec cache Streamlit
    
    Args:
        nb_jours: Nombre de jours à charger (si date_debut/fin non spécifiés)
        date_debut: Date début au format YYYY-MM-DD (optionnel)
        date_fin: Date fin au format YYYY-MM-DD (optionnel)
        produit: Filtrer par produit (optionnel)
        temporality: Granularité (hour/day/week/month)
    
    Returns:
        DataFrame avec colonnes: date, produit, quantite, ca_ttc, prix_moyen, shop_id, temporality
    
    Example:
        >>> df = load_ventes(nb_jours=7)  # 7 derniers jours
        >>> df = load_ventes(date_debut='2025-01-01', date_fin='2025-01-31')  # Janvier 2025
        >>> df = load_ventes(nb_jours=30, produit='Pizza Margherita')  # Un produit spécifique
    """
    db = get_db_manager()
    
    # Si DB non disponible, retourner DataFrame vide
    if db is None:
        return pd.DataFrame(columns=['date', 'produit', 'quantite', 'ca_ttc', 'prix_moyen', 'shop_id', 'temporality'])
    
    # Si dates non spécifiées, calculer depuis nb_jours
    if not date_debut:
        date_debut = (datetime.now() - timedelta(days=nb_jours)).strftime('%Y-%m-%d')
    if not date_fin:
        date_fin = datetime.now().strftime('%Y-%m-%d')
    
    try:
        df = db.query_ventes(
            date_debut=date_debut,
            date_fin=date_fin,
            produit=produit,
            temporality=temporality
        )
        return df
    except Exception as e:
        print(f"[ERROR] Erreur chargement ventes: {e}")
        return pd.DataFrame(columns=['date', 'produit', 'quantite', 'ca_ttc', 'prix_moyen', 'shop_id', 'temporality'])

@st.cache_data(ttl=600)  # Cache 10 minutes
def get_stats_globales() -> Dict[str, Any]:
    """
    Récupère les statistiques globales de la base
    
    Returns:
        dict avec: nb_ventes, nb_produits, date_min, date_max, ca_total, quantite_total, db_size_mb
    
    Example:
        >>> stats = get_stats_globales()
        >>> st.metric("CA Total", f"{stats['ca_total']:.0f}€")
    """
    db = get_db_manager()
    
    if db is None:
        return {
            'nb_ventes': 0,
            'nb_produits': 0,
            'date_min': None,
            'date_max': None,
            'ca_total': 0,
            'quantite_total': 0,
            'db_size_mb': 0
        }
    
    try:
        return db.get_stats()
    except Exception as e:
        print(f"[ERROR] Erreur récupération stats: {e}")
        return {
            'nb_ventes': 0,
            'nb_produits': 0,
            'date_min': None,
            'date_max': None,
            'ca_total': 0,
            'quantite_total': 0,
            'db_size_mb': 0
        }

@st.cache_data(ttl=600)
def get_top_produits(nb_jours: int = 30, limit: int = 10, order_by: str = 'quantite') -> pd.DataFrame:
    """
    Récupère le top des produits les plus vendus
    
    Args:
        nb_jours: Période à analyser
        limit: Nombre de produits à retourner
        order_by: Critère de tri ('quantite' ou 'ca_ttc')
    
    Returns:
        DataFrame avec: produit, quantite, ca_ttc, prix_moyen
    
    Example:
        >>> top = get_top_produits(nb_jours=7, limit=5, order_by='ca_ttc')
        >>> st.bar_chart(top.set_index('produit')['ca_ttc'])
    """
    df = load_ventes(nb_jours=nb_jours)
    
    if df.empty:
        return pd.DataFrame()
    
    # Agréger par produit
    agg = df.groupby('produit').agg({
        'quantite': 'sum',
        'ca_ttc': 'sum'
    }).reset_index()
    
    # Calculer prix moyen
    agg['prix_moyen'] = agg['ca_ttc'] / agg['quantite']
    
    # Trier et limiter
    agg = agg.nlargest(limit, order_by)
    
    return agg

@st.cache_data(ttl=600)
def get_ventes_par_jour(nb_jours: int = 30) -> pd.DataFrame:
    """
    Agrège les ventes par jour
    
    Args:
        nb_jours: Période à analyser
    
    Returns:
        DataFrame avec: date, quantite_totale, ca_total
    
    Example:
        >>> df_jours = get_ventes_par_jour(nb_jours=30)
        >>> st.line_chart(df_jours.set_index('date')['ca_total'])
    """
    df = load_ventes(nb_jours=nb_jours)
    
    if df.empty:
        return pd.DataFrame()
    
    # Extraire la date (sans heure)
    df['date_only'] = pd.to_datetime(df['date']).dt.date
    
    # Agréger par jour
    daily = df.groupby('date_only').agg({
        'quantite': 'sum',
        'ca_ttc': 'sum'
    }).reset_index()
    
    daily.columns = ['date', 'quantite_totale', 'ca_total']
    
    return daily

@st.cache_data(ttl=600)
def get_ventes_produit(produit: str, nb_jours: int = 30) -> Dict[str, Any]:
    """
    Récupère les stats d'un produit spécifique
    
    Args:
        produit: Nom du produit
        nb_jours: Période à analyser
    
    Returns:
        dict avec: quantite_totale, ca_total, prix_moyen, nb_ventes, df_historique
    
    Example:
        >>> stats = get_ventes_produit('Pizza Margherita', nb_jours=30)
        >>> st.metric("Quantité vendue", stats['quantite_totale'])
    """
    df = load_ventes(nb_jours=nb_jours, produit=produit)
    
    if df.empty:
        return {
            'quantite_totale': 0,
            'ca_total': 0,
            'prix_moyen': 0,
            'nb_ventes': 0,
            'df_historique': pd.DataFrame()
        }
    
    return {
        'quantite_totale': int(df['quantite'].sum()),
        'ca_total': float(df['ca_ttc'].sum()),
        'prix_moyen': float(df['prix_moyen'].mean()),
        'nb_ventes': len(df),
        'df_historique': df
    }

def needs_refresh(max_age_hours: int = 24) -> tuple[bool, str]:
    """
    Vérifie si un rafraîchissement des données est nécessaire
    
    Args:
        max_age_hours: Âge maximum acceptable en heures
    
    Returns:
        (bool, str): (needs_refresh, message)
    
    Example:
        >>> needs, msg = needs_refresh(max_age_hours=12)
        >>> if needs:
        >>>     st.warning(msg)
    """
    db = get_db_manager()
    
    if db is None:
        return False, "Base de données non disponible"
    
    try:
        last_sync = db.get_last_sync()
        
        if not last_sync:
            return True, "Aucune synchronisation effectuée"
        
        # Calculer l'âge
        sync_date = datetime.fromisoformat(last_sync['created_at'])
        age_hours = (datetime.now() - sync_date).total_seconds() / 3600
        
        if age_hours > max_age_hours:
            return True, f"Données obsolètes ({age_hours:.1f}h)"
        
        return False, f"Données à jour ({age_hours:.1f}h)"
    except Exception as e:
        print(f"[ERROR] Erreur vérification refresh: {e}")
        return False, "Erreur vérification"

def clear_cache():
    """
    Efface le cache Streamlit des données de ventes
    À utiliser après un rafraîchissement des données
    """
    load_ventes.clear()
    get_stats_globales.clear()
    get_top_produits.clear()
    get_ventes_par_jour.clear()
    get_ventes_produit.clear()


if __name__ == "__main__":
    # Test hors Streamlit
    print("🧪 TEST SALES DATA LOADER")
    print("=" * 60)
    
    # Stats globales
    stats = get_stats_globales()
    print(f"\n📊 Stats globales:")
    print(f"   • Ventes: {stats['nb_ventes']:,}")
    print(f"   • Produits: {stats['nb_produits']}")
    print(f"   • CA: {stats['ca_total']:.2f}€")
    print(f"   • Période: {stats['date_min']} → {stats['date_max']}")
    
    # Charger 7 jours
    print(f"\n📥 Chargement 7 derniers jours...")
    df = load_ventes(nb_jours=7)
    print(f"   • {len(df)} ventes chargées")
    print(f"   • Colonnes: {list(df.columns)}")
    
    # Top produits
    print(f"\n🏆 Top 5 produits (quantité):")
    top = get_top_produits(nb_jours=7, limit=5)
    for _, row in top.iterrows():
        print(f"   • {row['produit']}: {int(row['quantite'])} unités, {row['ca_ttc']:.0f}€")
    
    print("\n✅ Tests terminés")
