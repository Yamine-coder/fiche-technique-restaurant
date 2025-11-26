"""Application-wide configuration values."""

from pathlib import Path
import os

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Data sources
RECIPES_PATH = DATA_DIR / "recettes_complet_MAJ2.xlsx"
INGREDIENTS_PATH = DATA_DIR / "ingredients_nettoyes_et_standardises.xlsx"
DRAFTS_PATH = DATA_DIR / "brouillons.json"

# Kezia API credentials
# For Streamlit Cloud: set in Secrets (https://share.streamlit.io → Manage app → Secrets)
# For local dev: create config_local.py with KEZIA_EMAIL and KEZIA_PASSWORD
try:
    import streamlit as st
    KEZIA_EMAIL = st.secrets.get("KEZIA_EMAIL", os.getenv("KEZIA_EMAIL", ""))
    KEZIA_PASSWORD = st.secrets.get("KEZIA_PASSWORD", os.getenv("KEZIA_PASSWORD", ""))
except:
    # Fallback for local development
    try:
        from config_local import KEZIA_EMAIL, KEZIA_PASSWORD
    except ImportError:
        KEZIA_EMAIL = os.getenv("KEZIA_EMAIL", "")
        KEZIA_PASSWORD = os.getenv("KEZIA_PASSWORD", "")

# Tax rates
TVA_MP = 0.055  # TVA appliquée sur les achats de matières premières
TVA_VENTE = 0.10  # TVA appliquée sur les ventes restauration

# Streamlit cache durations (seconds)
CACHE_TTL_SECONDS = 600
