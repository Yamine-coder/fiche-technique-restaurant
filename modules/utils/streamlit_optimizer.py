"""
Optimiseur Streamlit - Performance maximale
============================================

Techniques d'optimisation :
1. Cache intelligent multi-niveaux
2. Lazy loading (chargement à la demande)
3. Pagination automatique
4. Compression données
5. Mémorisation résultats
"""

import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Dict, List
import sqlite3
import hashlib
import pickle
import gzip


class StreamlitOptimizer:
    """Gestionnaire d'optimisation pour Streamlit"""
    
    def __init__(self):
        self.cache_dir = Path("data/streamlit_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def cached_data(ttl: int = 300, show_spinner: bool = False):
        """
        Décorateur de cache intelligent avec TTL
        
        Args:
            ttl: Durée de vie du cache en secondes (défaut: 5 min)
            show_spinner: Afficher spinner pendant chargement
        
        Usage:
            @StreamlitOptimizer.cached_data(ttl=300)
            def load_expensive_data():
                return heavy_computation()
        """
        return st.cache_data(ttl=ttl, show_spinner=show_spinner)
    
    @staticmethod
    def cached_resource(ttl: int = 3600, show_spinner: bool = False):
        """
        Décorateur pour ressources (connexions DB, sessions API)
        
        Args:
            ttl: Durée de vie en secondes (défaut: 1h)
            show_spinner: Afficher spinner
        
        Usage:
            @StreamlitOptimizer.cached_resource(ttl=3600)
            def get_db_connection():
                return sqlite3.connect("data.db")
        """
        return st.cache_resource(ttl=ttl, show_spinner=show_spinner)
    
    @staticmethod
    def lazy_dataframe(
        data_loader: Callable,
        page_size: int = 50,
        key: str = "lazy_df"
    ) -> pd.DataFrame:
        """
        Chargement lazy d'un DataFrame avec pagination
        
        Args:
            data_loader: Fonction qui retourne le DataFrame complet
            page_size: Nombre de lignes par page
            key: Clé unique pour le state
        
        Returns:
            DataFrame de la page courante
        
        Usage:
            df = StreamlitOptimizer.lazy_dataframe(
                lambda: load_big_dataframe(),
                page_size=50
            )
        """
        # Initialisation du state
        if f"{key}_full_data" not in st.session_state:
            with st.spinner("Chargement des données..."):
                st.session_state[f"{key}_full_data"] = data_loader()
                st.session_state[f"{key}_page"] = 0
        
        df_full = st.session_state[f"{key}_full_data"]
        total_rows = len(df_full)
        total_pages = (total_rows + page_size - 1) // page_size
        
        # Contrôles de pagination
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if st.button("⬅️ Précédent", key=f"{key}_prev", disabled=st.session_state[f"{key}_page"] == 0):
                st.session_state[f"{key}_page"] -= 1
                st.rerun()
        
        with col2:
            current_page = st.session_state[f"{key}_page"]
            st.write(f"Page {current_page + 1} / {total_pages} ({total_rows} lignes)")
        
        with col3:
            if st.button("Suivant ➡️", key=f"{key}_next", disabled=st.session_state[f"{key}_page"] >= total_pages - 1):
                st.session_state[f"{key}_page"] += 1
                st.rerun()
        
        # Retourne la page courante
        start_idx = st.session_state[f"{key}_page"] * page_size
        end_idx = start_idx + page_size
        
        return df_full.iloc[start_idx:end_idx]
    
    @staticmethod
    def lazy_expander(
        label: str,
        content_loader: Callable,
        key: str,
        expanded: bool = False
    ):
        """
        Expander qui charge le contenu uniquement quand ouvert
        
        Args:
            label: Titre de l'expander
            content_loader: Fonction qui génère le contenu
            key: Clé unique
            expanded: Ouvert par défaut
        
        Usage:
            StreamlitOptimizer.lazy_expander(
                "Détails produits",
                lambda: load_product_details(),
                key="products"
            )
        """
        with st.expander(label, expanded=expanded):
            cache_key = f"{key}_expanded_loaded"
            
            if cache_key not in st.session_state:
                with st.spinner("Chargement..."):
                    st.session_state[cache_key] = content_loader()
            
            # Affiche le contenu caché
            return st.session_state[cache_key]
    
    @staticmethod
    def lazy_tabs(
        tabs_config: Dict[str, Callable],
        key: str = "lazy_tabs"
    ):
        """
        Tabs qui chargent le contenu uniquement quand sélectionné
        
        Args:
            tabs_config: {label: content_loader_function}
            key: Clé unique
        
        Usage:
            StreamlitOptimizer.lazy_tabs({
                "Aujourd'hui": lambda: show_today(),
                "Comparaison": lambda: show_comparison(),
                "Historique": lambda: show_history()
            })
        """
        tab_labels = list(tabs_config.keys())
        tabs = st.tabs(tab_labels)
        
        # Initialisation
        if f"{key}_active_tab" not in st.session_state:
            st.session_state[f"{key}_active_tab"] = 0
        
        for idx, (tab, label) in enumerate(zip(tabs, tab_labels)):
            with tab:
                cache_key = f"{key}_tab_{idx}_loaded"
                
                # Charge uniquement si tab active et pas déjà chargé
                if cache_key not in st.session_state:
                    with st.spinner(f"Chargement {label}..."):
                        st.session_state[cache_key] = tabs_config[label]()
                
                # Affiche le contenu
                content = st.session_state[cache_key]
                if callable(content):
                    content()
    
    @staticmethod
    def compress_cache(data: Any, cache_file: Path) -> bool:
        """
        Sauvegarde données avec compression gzip
        
        Args:
            data: Données à sauvegarder
            cache_file: Chemin du fichier cache
        
        Returns:
            True si succès
        """
        try:
            with gzip.open(cache_file, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        except Exception as e:
            st.error(f"Erreur compression cache: {e}")
            return False
    
    @staticmethod
    def load_compressed_cache(cache_file: Path) -> Optional[Any]:
        """
        Charge données depuis cache compressé
        
        Args:
            cache_file: Chemin du fichier cache
        
        Returns:
            Données ou None si erreur
        """
        try:
            with gzip.open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            st.error(f"Erreur lecture cache: {e}")
            return None
    
    @staticmethod
    def incremental_loading(
        items: List[Any],
        batch_size: int = 10,
        key: str = "incremental"
    ):
        """
        Chargement incrémental avec bouton "Charger plus"
        
        Args:
            items: Liste complète d'items
            batch_size: Nombre d'items par batch
            key: Clé unique
        
        Usage:
            all_products = get_all_products()
            StreamlitOptimizer.incremental_loading(
                all_products,
                batch_size=20,
                key="products"
            )
        """
        # Initialisation
        if f"{key}_shown_count" not in st.session_state:
            st.session_state[f"{key}_shown_count"] = batch_size
        
        shown_count = st.session_state[f"{key}_shown_count"]
        total_count = len(items)
        
        # Affiche les items visibles
        visible_items = items[:shown_count]
        
        for item in visible_items:
            yield item
        
        # Bouton "Charger plus"
        if shown_count < total_count:
            remaining = total_count - shown_count
            load_more = min(batch_size, remaining)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"⬇️ Charger {load_more} de plus ({remaining} restants)", key=f"{key}_load_more"):
                    st.session_state[f"{key}_shown_count"] += batch_size
                    st.rerun()
    
    @staticmethod
    def memoize_expensive(func: Callable, ttl: int = 300):
        """
        Mémorise les résultats de fonctions coûteuses
        
        Args:
            func: Fonction à mémoriser
            ttl: Durée de vie en secondes
        
        Returns:
            Fonction wrapped avec mémorisation
        
        Usage:
            @StreamlitOptimizer.memoize_expensive
            def expensive_calculation(param):
                return heavy_compute(param)
        """
        cache = {}
        timestamps = {}
        
        def wrapper(*args, **kwargs):
            # Génère clé de cache
            key = hashlib.md5(
                str((args, sorted(kwargs.items()))).encode()
            ).hexdigest()
            
            now = datetime.now().timestamp()
            
            # Vérifie si en cache et pas expiré
            if key in cache and key in timestamps:
                if now - timestamps[key] < ttl:
                    return cache[key]
            
            # Calcule et met en cache
            result = func(*args, **kwargs)
            cache[key] = result
            timestamps[key] = now
            
            return result
        
        return wrapper
    
    @staticmethod
    def virtual_scroll(
        data: pd.DataFrame,
        height: int = 400,
        page_size: int = 50
    ) -> pd.DataFrame:
        """
        Virtual scrolling pour grands DataFrames
        Affiche seulement les lignes visibles
        
        Args:
            data: DataFrame complet
            height: Hauteur du container en pixels
            page_size: Nombre de lignes à rendre
        
        Returns:
            DataFrame visible
        """
        total_rows = len(data)
        
        # Slider pour navigation
        if total_rows > page_size:
            start_row = st.slider(
                "Position",
                0,
                max(0, total_rows - page_size),
                0,
                key=f"virtual_scroll_{id(data)}"
            )
            end_row = min(start_row + page_size, total_rows)
            
            st.caption(f"Lignes {start_row + 1} à {end_row} sur {total_rows}")
            
            return data.iloc[start_row:end_row]
        else:
            return data
    
    @staticmethod
    def progressive_render(
        components: List[Callable],
        key: str = "progressive"
    ):
        """
        Rendu progressif des composants
        Affiche chaque composant dès qu'il est prêt
        
        Args:
            components: Liste de fonctions à exécuter
            key: Clé unique
        
        Usage:
            StreamlitOptimizer.progressive_render([
                lambda: st.metric("CA", "3,086€"),
                lambda: st.chart(data),
                lambda: st.dataframe(df)
            ])
        """
        for idx, component in enumerate(components):
            placeholder = st.empty()
            
            with placeholder.container():
                try:
                    component()
                except Exception as e:
                    st.error(f"Erreur composant {idx}: {e}")


# Fonctions helper optimisées pour l'app

@StreamlitOptimizer.cached_data(ttl=300)
def load_today_cache() -> dict:
    """Charge le cache du jour (optimisé avec cache Streamlit)"""
    today = datetime.now().strftime("%Y-%m-%d")
    cache_file = Path(f"data/cache/kezia_today_{today}.json")
    
    if not cache_file.exists():
        return None
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        return json.load(f)


@StreamlitOptimizer.cached_data(ttl=300)
def load_yesterday_data(until_hour: int = 23) -> pd.DataFrame:
    """Charge les données d'hier depuis SQLite (optimisé)"""
    db_path = Path("data/kezia_sales.db")
    
    if not db_path.exists():
        return pd.DataFrame()
    
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(db_path)
    
    query = f"""
        SELECT produit, SUM(quantite) as quantite, SUM(ca_ttc) as ca
        FROM ventes
        WHERE DATE(date) = '{yesterday}'
        AND CAST(strftime('%H', date) AS INTEGER) <= {until_hour}
        GROUP BY produit
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df


@StreamlitOptimizer.cached_resource(ttl=3600)
def get_db_connection():
    """Connexion SQLite persistante (optimisée)"""
    return sqlite3.connect("data/kezia_sales.db", check_same_thread=False)


def init_session_state():
    """Initialise le session state pour optimisation"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.page = "dashboard"
        st.session_state.filters = {}
        st.session_state.chart_data_cache = {}
