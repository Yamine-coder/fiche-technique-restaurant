"""
Constantes et données statiques de l'application
Contient : prix de vente, images des plats, coûts de pâte, catégories
"""

# Import de la TVA depuis config
from config import TVA_VENTE, TVA_MP

# ============================================================================
# PRIX DE VENTE (TTC)
# ============================================================================

PRIX_VENTE_DICT = {
    # Pizzas Spéciales
    "Savoyarde S": 11.90,
    "Savoyarde M": 13.90,
    "Norvegienne S": 11.90,
    "Norvegienne M": 13.90,
    "Normande S": 11.90,
    "Normande M": 13.90,
    "Raclette S": 11.90,
    "Raclette M": 13.90,
    "4 fromages S": 11.90,
    "4 fromages M": 13.90,
    "Hanna S": 11.90,
    "Hanna M": 13.90,
    "Truffe S": 11.90,
    "Truffe M": 13.90,
    
    # Pizzas Classiques
    "Margarita S": 8.90,
    "Margarita M": 10.90,
    "Reine S": 9.90,
    "Reine M": 11.90,
    "Napolitaine S": 9.90,
    "Napolitaine M": 11.90,
    "Fermière S": 9.90,
    "Fermière M": 11.90,
    "3 Fromages S": 10.90,
    "3 Fromages M": 12.90,
    "Orientale S": 10.90,
    "Orientale M": 12.90,
    "Carnée S": 10.90,
    "Carnée M": 12.90,
    "Paysanne S": 10.90,
    "Paysanne M": 12.90,
    "Aubergine S": 10.90,
    "Aubergine M": 12.90,
    "Chèvre-Miel S": 9.90,
    "Chèvre-Miel M": 11.90,
    "Charcutière S": 10.90,
    "Charcutière M": 12.90,
    "Mexicaine S": 10.90,
    "Mexicaine M": 12.90,
    "4 Saisons S": 10.90,
    "4 Saisons M": 12.90,
    "Silicienne S": 10.90,
    "Silicienne M": 12.90,
    "Végétarienne S": 10.90,
    "Végétarienne M": 12.90,
    "Calzone S": 9.90,
    
    # Panini
    "panini pizz": 5.90,
    
    # Pizzas Burrata
    "Pizza Burrata di Parma": 13.90,
    "Pizza Burrata Di Salmone": 13.90,
    "Pizza Burrata Di Parma": 13.90,
    
    # Salades
    "Salade César": 10.90,
    "Salade végétarienne": 10.90,
    "Salade chèvre": 10.90,
    "Salade Burrata di Parma": 13.90,
    "Salade burrata di salmone": 13.90,
    "Salade Burrata di Salmone": 13.90,
    "Salade Verte": 5.90,
    "Assiette Artichauts": 5.90,
    
    # Burrata
    "Burrata feuille La véritable": 6.90,
    
    # Pâtes
    "Pâte Bolognaise": 9.90,
    "Pâte Truffe": 9.90,
    "Pâte Saumon": 9.90,
    "Pâte Carbonara": 9.90,
    "Pâte Fermière": 9.90,
    "Pâte 3 Fromages": 9.90,
    "Pâte Napolitaine": 9.90,
    "Pâte Sicilienne": 9.90,
    "Pâte Arrabiata": 8.90,
    "Pâte Arrabiata Poulet": 9.90,
    
    # Pains maison
    "Pain aux herbes et mozzarella": 3.00,
    "Pain aux herbes": 2.50,
}


# ============================================================================
# IMAGES DES PLATS
# ============================================================================

IMAGES_PLATS = {
    # Pizzas Spéciales
    "Savoyarde S": "savoyarde.webp",
    "Savoyarde M": "savoyarde.webp",
    "Norvegienne S": "Norvégienne.webp",
    "Norvegienne M": "Norvégienne.webp",
    "Normande S": "Normande.webp",
    "Normande M": "Normande.webp",
    "Raclette S": "Raclette.webp",
    "Raclette M": "Raclette.webp",
    "4 fromages S": "pizza_4fromages.webp",
    "4 fromages M": "pizza_4fromages.webp",
    "Hanna S": "Hanna.webp",
    "Hanna M": "Hanna.webp",
    "Truffe S": "pizza_truffe.webp",
    "Truffe M": "pizza_truffe.webp",
    
    # Panini
    "panini pizz": "Panini_pizz_creme.webp",
    
    # Pizzas Classiques
    "Margarita S": "marga.webp",
    "Margarita M": "marga.webp",
    "Calzone S": "Calzone.webp",
    "Reine S": "Reine.webp",
    "Reine M": "Reine.webp",
    "Paysanne S": "Paysanne.webp",
    "Paysanne M": "Paysanne.webp",
    "Chèvre-Miel S": "chevre-miel.webp",
    "Chèvre-Miel M": "chevre-miel.webp",
    "Aubergine S": "Aubergine.webp",
    "Aubergine M": "Aubergine.webp",
    "Napolitaine S": "Napo.webp",
    "Napolitaine M": "Napo.webp",
    "Fermière S": "fermiere.webp",
    "Fermière M": "fermiere.webp",
    "3 Fromages S": "3Fromage.webp",
    "3 Fromages M": "3Fromage.webp",
    "Orientale S": "Orientale.webp",
    "Orientale M": "Orientale.webp",
    "Carnée S": "Carnée.webp",
    "Carnée M": "Carnée.webp",
    "Mexicaine S": "Mexicaine.webp",
    "Mexicaine M": "Mexicaine.webp",
    "Charcutière S": "charcut.webp",
    "Charcutière M": "charcut.webp",
    "Végétarienne S": "Vege.webp",
    "Végétarienne M": "Vege.webp",
    "Silicienne S": "Sicili.webp",
    "Silicienne M": "Sicili.webp",
    "4 Saisons S": "4 saisons.webp",
    "4 Saisons M": "4 saisons.webp",
    
    # Pâtes
    "Pâte Bolognaise": "pates_bolognaise.webp",
    "Pâte Truffe": "pates_truffe.webp",
    "Pâte Saumon": "pates_saumon.webp",
    "Pâte Carbonara": "pates_carbonara.webp",
    "Pâte Fermière": "pates_fermiere.webp",
    "Pâte 3 Fromages": "pates_3fromages.webp",
    "Pâte Napolitaine": "pates_napolitaine.webp",
    "Pâte Sicilienne": "pates_sicilienne.webp",
    "Pâte Arrabiata": "pates_arrabiata.webp",
    "Pâte Arrabiata Poulet": "pates_arrabiata_poulet.jpeg",
    
    # Pains maison
    "Pain aux herbes et mozzarella": "pain_herbes_mozza.webp",
    "Pain aux herbes": "pain_herbes.webp",
    
    # Salades
    "Salade César": "salade_cesar.webp",
    "Salade végétarienne": "salade_vegetarienne.webp",
    "Salade chèvre": "salade_chevre.webp",
    "Assiette Artichauts": "assiette_artichauts.jpeg",
    "Salade Verte": "salade_verte.jpeg",
    
    # Burratas
    "Pizza Burrata di Parma": "pizza_burrata_parma.jpeg",
    "Burrata feuille La véritable": "burata_feuille.webp",
    "Pizza Burrata Di Salmone": "pizza_burrata_saumon.jpeg",
    "Salade Burrata di Salmone": "salade_burrata_saumon.webp",
    "Salade Burrata di Parma": "salade_burrata_parma.webp",
}


# ============================================================================
# COÛTS DE PÂTE (en euros)
# ============================================================================

COUT_PATE = {
    # Pizzas taille S
    "S": 0.12,
    # Pizzas taille M
    "M": 0.20,
    # Panini
    "panini": 0.12,
    # Pains (moitié pâte M)
    "pain": 0.10,
    # Pizzas Burrata
    "burrata": 0.12,
    # Défaut (pâtes, salades, etc.)
    "default": 0.0,
}


# ============================================================================
# CATÉGORIES DE PLATS
# ============================================================================

CATEGORIES = {
    "pizza": "Pizza",
    "pate": "Pâte",
    "salade": "Salade",
    "burrata": "Burrata",
    "pain": "Pain",
    "panini": "Panini",
}


# ============================================================================
# TAILLES DISPONIBLES
# ============================================================================

TAILLES = ["S", "M"]


# ============================================================================
# FALLBACK / DÉFAUTS
# ============================================================================

IMAGE_FALLBACK = "logo.png"


# ============================================================================
# ALIASES POUR COMPATIBILITÉ (minuscules)
# ============================================================================

# Créer des alias en minuscules pour rétrocompatibilité avec le code existant
prix_vente_dict = PRIX_VENTE_DICT
images_plats = IMAGES_PLATS
cout_pate = COUT_PATE
categories = CATEGORIES
tailles = TAILLES
image_fallback = IMAGE_FALLBACK
