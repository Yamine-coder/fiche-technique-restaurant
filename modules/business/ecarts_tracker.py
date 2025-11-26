"""
Système de détection des écarts entre données Kezia et réalité terrain
"""
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from kezia_db_manager import get_db_manager


class EcartsTracker:
    """Détecte et analyse les écarts dans les données de ventes"""
    
    def __init__(self):
        self.db = get_db_manager()
    
    def get_ecarts_journee(self, date=None):
        """
        Analyse les écarts pour une journée donnée
        
        Returns:
            dict avec les écarts détectés
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # 1. Récupérer les données Kezia scrapées
        df_ventes = self.db.query_ventes(
            date_debut=date,
            date_fin=date,
            temporality='hour'
        )
        
        # Charger les CSV si disponibles
        csv_moyens = Path("data/kezia_moyens_paiement.csv")
        csv_categories = Path("data/kezia_categories_enriched.csv")
        
        ecarts = {
            'date': date,
            'ca_scrape': 0,
            'ca_moyens_paiement': 0,
            'ca_categories': 0,
            'tickets_moyens': 0,
            'tickets_categories': 0,
            'pertes_identifiees': 0,
            'ecarts': [],
            'alertes': []
        }
        
        # CA depuis SQLite
        if not df_ventes.empty:
            ecarts['ca_scrape'] = df_ventes['ca_ttc'].sum()
        
        # CA depuis moyens de paiement
        if csv_moyens.exists():
            df_moyens = pd.read_csv(csv_moyens, encoding='utf-8-sig')
            ecarts['ca_moyens_paiement'] = df_moyens['paymentAmount'].sum()
            ecarts['tickets_moyens'] = int(df_moyens['paymentCount'].sum())
            
            # Détecter les pertes (montants négatifs)
            pertes = df_moyens[df_moyens['paymentAmount'] < 0]
            if not pertes.empty:
                ecarts['pertes_identifiees'] = abs(pertes['paymentAmount'].sum())
                for _, p in pertes.iterrows():
                    ecarts['alertes'].append({
                        'type': 'perte',
                        'montant': p['paymentAmount'],
                        'detail': p['paymentName']
                    })
        
        # CA depuis catégories
        if csv_categories.exists():
            df_categories = pd.read_csv(csv_categories, encoding='utf-8-sig')
            ecarts['ca_categories'] = df_categories['turnover'].sum()
            ecarts['tickets_categories'] = int(df_categories['ticketCount'].sum())
        
        # Calculer les écarts
        if ecarts['ca_moyens_paiement'] > 0 and ecarts['ca_categories'] > 0:
            ecart_ca = ecarts['ca_moyens_paiement'] - ecarts['ca_categories']
            ecart_pct = abs(ecart_ca / ecarts['ca_moyens_paiement'] * 100)
            
            ecarts['ecarts'].append({
                'type': 'ca',
                'source1': 'moyens_paiement',
                'source2': 'categories',
                'valeur1': ecarts['ca_moyens_paiement'],
                'valeur2': ecarts['ca_categories'],
                'difference': ecart_ca,
                'pourcentage': ecart_pct
            })
            
            # Alertes selon seuils
            if ecart_pct > 5:
                ecarts['alertes'].append({
                    'type': 'ecart_ca_important',
                    'montant': ecart_ca,
                    'pourcentage': ecart_pct,
                    'detail': f"Écart de {ecart_ca:.2f}€ ({ecart_pct:.2f}%) entre moyens paiement et catégories"
                })
            elif ecart_pct > 1:
                ecarts['alertes'].append({
                    'type': 'ecart_ca_modere',
                    'montant': ecart_ca,
                    'pourcentage': ecart_pct,
                    'detail': f"Écart de {ecart_ca:.2f}€ ({ecart_pct:.2f}%)"
                })
        
        # Écart sur les tickets (indicateur de qualité des données)
        if ecarts['tickets_moyens'] > 0 and ecarts['tickets_categories'] > 0:
            # Les tickets des catégories sont en réalité des articles vendus
            # On peut détecter un problème si le ratio est trop éloigné de 2-3 articles/ticket
            ratio = ecarts['tickets_categories'] / ecarts['tickets_moyens']
            
            ecarts['ecarts'].append({
                'type': 'tickets',
                'source1': 'moyens_paiement',
                'source2': 'categories',
                'valeur1': ecarts['tickets_moyens'],
                'valeur2': ecarts['tickets_categories'],
                'difference': ecarts['tickets_moyens'] - ecarts['tickets_categories'],
                'ratio_articles_par_ticket': ratio
            })
            
            # Alertes sur ratio anormal
            if ratio < 1.5:
                ecarts['alertes'].append({
                    'type': 'ratio_faible',
                    'detail': f"Ratio articles/ticket très faible ({ratio:.2f}). Possible problème de données."
                })
            elif ratio > 5:
                ecarts['alertes'].append({
                    'type': 'ratio_eleve',
                    'detail': f"Ratio articles/ticket élevé ({ratio:.2f}). Tickets complexes ou erreur."
                })
        
        return ecarts
    
    def comparer_avec_reel(self, date, ca_reel, nb_tickets_reel=None):
        """
        Compare les données scrapées avec les valeurs réelles saisies
        
        Args:
            date: Date à comparer (YYYY-MM-DD)
            ca_reel: CA réel compté (en fin de journée, Z de caisse, etc.)
            nb_tickets_reel: Nombre réel de tickets si disponible
            
        Returns:
            dict avec les écarts vs réel
        """
        ecarts_kezia = self.get_ecarts_journee(date)
        
        comparison = {
            'date': date,
            'ca_reel': ca_reel,
            'ca_kezia': ecarts_kezia['ca_moyens_paiement'],
            'ecart_ca': ca_reel - ecarts_kezia['ca_moyens_paiement'],
            'ecart_ca_pct': 0,
            'pertes_non_enregistrees': 0,
            'alertes': []
        }
        
        if ecarts_kezia['ca_moyens_paiement'] > 0:
            comparison['ecart_ca_pct'] = abs(comparison['ecart_ca'] / ca_reel * 100)
        
        # Détecter les pertes non enregistrées
        if comparison['ecart_ca'] < -50:  # Si le réel est inférieur de plus de 50€
            comparison['pertes_non_enregistrees'] = abs(comparison['ecart_ca'])
            comparison['alertes'].append({
                'type': 'pertes_importantes',
                'montant': abs(comparison['ecart_ca']),
                'detail': f"Le CA réel est inférieur de {abs(comparison['ecart_ca']):.2f}€. Possible remboursements non enregistrés ou erreurs."
            })
        
        # Détecter les sur-déclarations (fraude potentielle?)
        if comparison['ecart_ca'] > 50:
            comparison['alertes'].append({
                'type': 'ca_superieur',
                'montant': comparison['ecart_ca'],
                'detail': f"Le CA réel est supérieur de {comparison['ecart_ca']:.2f}€ à Kezia. Vérifier les ventes non enregistrées."
            })
        
        # Comparer les tickets si disponibles
        if nb_tickets_reel is not None:
            comparison['tickets_reel'] = nb_tickets_reel
            comparison['tickets_kezia'] = ecarts_kezia['tickets_moyens']
            comparison['ecart_tickets'] = nb_tickets_reel - ecarts_kezia['tickets_moyens']
            
            if abs(comparison['ecart_tickets']) > 5:
                comparison['alertes'].append({
                    'type': 'ecart_tickets',
                    'detail': f"Écart de {comparison['ecart_tickets']} tickets entre réel et Kezia"
                })
        
        # Score de fiabilité (0-100)
        if comparison['ecart_ca_pct'] < 1:
            comparison['score_fiabilite'] = 100
        elif comparison['ecart_ca_pct'] < 3:
            comparison['score_fiabilite'] = 90
        elif comparison['ecart_ca_pct'] < 5:
            comparison['score_fiabilite'] = 70
        else:
            comparison['score_fiabilite'] = 50
        
        return comparison
    
    def tendance_ecarts(self, nb_jours=7):
        """
        Analyse la tendance des écarts sur plusieurs jours
        
        Returns:
            dict avec statistiques sur les écarts
        """
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=nb_jours)
        
        ecarts_history = []
        
        for i in range(nb_jours):
            date = (date_debut + timedelta(days=i)).strftime("%Y-%m-%d")
            ecarts = self.get_ecarts_journee(date)
            
            if ecarts['ca_moyens_paiement'] > 0:  # Seulement si on a des données
                ecarts_history.append({
                    'date': date,
                    'ca': ecarts['ca_moyens_paiement'],
                    'pertes': ecarts['pertes_identifiees'],
                    'nb_alertes': len(ecarts['alertes'])
                })
        
        if not ecarts_history:
            return {
                'message': f"Pas de données sur les {nb_jours} derniers jours"
            }
        
        df = pd.DataFrame(ecarts_history)
        
        return {
            'nb_jours': len(ecarts_history),
            'ca_total': df['ca'].sum(),
            'ca_moyen': df['ca'].mean(),
            'pertes_totales': df['pertes'].sum(),
            'pertes_moyennes': df['pertes'].mean(),
            'jours_avec_alertes': (df['nb_alertes'] > 0).sum(),
            'detail_par_jour': ecarts_history
        }
    
    def rapport_ecarts(self, date=None):
        """
        Génère un rapport formaté des écarts
        
        Returns:
            str: Rapport texte formaté
        """
        ecarts = self.get_ecarts_journee(date)
        date = ecarts['date']
        
        rapport = []
        rapport.append("=" * 70)
        rapport.append(f"📊 RAPPORT DES ÉCARTS - {date}")
        rapport.append("=" * 70)
        
        # CA
        rapport.append("\n💰 CHIFFRE D'AFFAIRES:")
        rapport.append(f"   Moyens de paiement: {ecarts['ca_moyens_paiement']:.2f}€")
        rapport.append(f"   Catégories: {ecarts['ca_categories']:.2f}€")
        rapport.append(f"   SQLite (scrape): {ecarts['ca_scrape']:.2f}€")
        
        # Tickets
        rapport.append("\n🎫 TICKETS:")
        rapport.append(f"   Transactions réelles: {ecarts['tickets_moyens']}")
        rapport.append(f"   Panier moyen: {ecarts['ca_moyens_paiement']/ecarts['tickets_moyens']:.2f}€" if ecarts['tickets_moyens'] > 0 else "   N/A")
        
        # Pertes
        if ecarts['pertes_identifiees'] > 0:
            rapport.append(f"\n💸 PERTES IDENTIFIÉES: {ecarts['pertes_identifiees']:.2f}€")
        
        # Écarts
        if ecarts['ecarts']:
            rapport.append("\n⚖️ ÉCARTS DÉTECTÉS:")
            for e in ecarts['ecarts']:
                if e['type'] == 'ca':
                    rapport.append(f"   CA: {abs(e['difference']):.2f}€ ({e['pourcentage']:.2f}%)")
                    if e['pourcentage'] < 1:
                        rapport.append("   ✅ Écart négligeable")
                    elif e['pourcentage'] < 5:
                        rapport.append("   ⚠️ Écart modéré, à surveiller")
                    else:
                        rapport.append("   🚨 ALERTE: Écart important!")
        
        # Alertes
        if ecarts['alertes']:
            rapport.append(f"\n🚨 ALERTES ({len(ecarts['alertes'])}):")
            for alerte in ecarts['alertes']:
                rapport.append(f"   • {alerte['type']}: {alerte.get('detail', 'N/A')}")
        else:
            rapport.append("\n✅ Aucune alerte détectée")
        
        rapport.append("\n" + "=" * 70)
        
        return "\n".join(rapport)


# Fonction helper pour utilisation rapide
def analyser_ecarts_aujourdhui():
    """Analyse rapide des écarts du jour"""
    tracker = EcartsTracker()
    return tracker.rapport_ecarts()


def comparer_avec_z_caisse(ca_z_caisse, nb_tickets=None):
    """
    Compare avec le Z de caisse
    
    Args:
        ca_z_caisse: Montant du Z de caisse (fin de journée)
        nb_tickets: Nombre de tickets si disponible
    """
    tracker = EcartsTracker()
    date = datetime.now().strftime("%Y-%m-%d")
    comparison = tracker.comparer_avec_reel(date, ca_z_caisse, nb_tickets)
    
    print("=" * 70)
    print(f"🔍 COMPARAISON AVEC Z DE CAISSE - {date}")
    print("=" * 70)
    print(f"\n💰 CA Z de caisse: {comparison['ca_reel']:.2f}€")
    print(f"💰 CA Kezia: {comparison['ca_kezia']:.2f}€")
    print(f"⚖️ Écart: {comparison['ecart_ca']:.2f}€ ({comparison['ecart_ca_pct']:.2f}%)")
    
    if comparison['pertes_non_enregistrees'] > 0:
        print(f"\n💸 Pertes non enregistrées: {comparison['pertes_non_enregistrees']:.2f}€")
    
    print(f"\n📊 Score de fiabilité: {comparison['score_fiabilite']}/100")
    
    if comparison['alertes']:
        print(f"\n🚨 ALERTES ({len(comparison['alertes'])}):")
        for alerte in comparison['alertes']:
            print(f"   • {alerte['detail']}")
    else:
        print("\n✅ Aucune alerte")
    
    print("=" * 70)
    
    return comparison
