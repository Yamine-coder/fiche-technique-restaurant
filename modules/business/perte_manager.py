"""
Gestionnaire de pertes et ajustements non enregistrés dans Kezia
"""
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path


class PerteManager:
    """Gère les pertes, remboursements et ajustements non enregistrés dans Kezia"""
    
    def __init__(self, db_path="data/pertes.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialise la base de données des pertes"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des pertes/ajustements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pertes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                heure TEXT NOT NULL,
                type TEXT NOT NULL,
                montant REAL NOT NULL,
                produit TEXT,
                client TEXT,
                raison TEXT NOT NULL,
                commentaire TEXT,
                mode_paiement TEXT,
                responsable TEXT,
                statut TEXT DEFAULT 'en_attente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table de validation en fin de journée
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS validation_journee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                ca_kezia REAL NOT NULL,
                ca_reel_compte REAL NOT NULL,
                ecart_total REAL NOT NULL,
                pertes_declarees REAL NOT NULL,
                ecart_inexplique REAL NOT NULL,
                nb_tickets_kezia INTEGER,
                nb_tickets_reel INTEGER,
                commentaire TEXT,
                valide_par TEXT,
                valide_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def ajouter_perte(self, montant, type_perte, raison, produit=None, client=None, 
                      commentaire=None, mode_paiement=None, responsable=None, date=None, heure=None):
        """
        Enregistre une perte non déclarée dans Kezia
        
        Args:
            montant: Montant de la perte (positif)
            type_perte: 'remboursement', 'erreur_caisse', 'geste_commercial', 'produit_offert', 'annulation', 'vol', 'casse'
            raison: Explication de la perte
            produit: Produit concerné si applicable
            client: Nom/ID client si applicable
            commentaire: Détails supplémentaires
            mode_paiement: 'especes', 'carte', 'ticket_restaurant'
            responsable: Qui a fait l'opération
            date: Date (auto si None)
            heure: Heure (auto si None)
        
        Returns:
            int: ID de la perte créée
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        if heure is None:
            heure = datetime.now().strftime("%H:%M:%S")
        
        cursor.execute("""
            INSERT INTO pertes (date, heure, type, montant, produit, client, raison, 
                               commentaire, mode_paiement, responsable, statut)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'confirmee')
        """, (date, heure, type_perte, abs(montant), produit, client, raison, 
              commentaire, mode_paiement, responsable))
        
        perte_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Perte enregistrée (ID: {perte_id}) - {montant:.2f}€ - {raison}")
        
        return perte_id
    
    def get_pertes_jour(self, date=None):
        """Récupère toutes les pertes d'une journée"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM pertes WHERE date = ? ORDER BY heure DESC",
            conn,
            params=(date,)
        )
        conn.close()
        
        return df
    
    def get_pertes_periode(self, date_debut, date_fin):
        """Récupère les pertes sur une période"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(
            "SELECT * FROM pertes WHERE date BETWEEN ? AND ? ORDER BY date DESC, heure DESC",
            conn,
            params=(date_debut, date_fin)
        )
        conn.close()
        
        return df
    
    def total_pertes_jour(self, date=None):
        """Calcule le total des pertes du jour"""
        df = self.get_pertes_jour(date)
        return df['montant'].sum() if not df.empty else 0.0
    
    def valider_journee(self, date, ca_kezia, ca_reel_compte, nb_tickets_kezia=None, 
                       nb_tickets_reel=None, commentaire=None, valide_par=None):
        """
        Valide la journée en comparant Kezia vs réalité
        
        Args:
            date: Date à valider
            ca_kezia: CA selon Kezia (scraped)
            ca_reel_compte: CA réellement compté (Z caisse, fond de caisse, etc.)
            nb_tickets_kezia: Nombre de tickets Kezia
            nb_tickets_reel: Nombre de tickets réel si différent
            commentaire: Notes sur la journée
            valide_par: Nom du validateur
        
        Returns:
            dict avec analyse complète
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupérer les pertes déclarées
        pertes_df = self.get_pertes_jour(date)
        pertes_declarees = pertes_df['montant'].sum() if not pertes_df.empty else 0.0
        
        # Calculer les écarts
        ecart_total = ca_reel_compte - ca_kezia
        ecart_inexplique = ecart_total + pertes_declarees  # Si pertes déclarées, elles expliquent une partie de l'écart
        
        # Enregistrer la validation
        cursor.execute("""
            INSERT OR REPLACE INTO validation_journee 
            (date, ca_kezia, ca_reel_compte, ecart_total, pertes_declarees, 
             ecart_inexplique, nb_tickets_kezia, nb_tickets_reel, commentaire, valide_par)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, ca_kezia, ca_reel_compte, ecart_total, pertes_declarees,
              ecart_inexplique, nb_tickets_kezia, nb_tickets_reel, commentaire, valide_par))
        
        conn.commit()
        conn.close()
        
        result = {
            'date': date,
            'ca_kezia': ca_kezia,
            'ca_reel': ca_reel_compte,
            'ecart_brut': ecart_total,
            'pertes_declarees': pertes_declarees,
            'ecart_inexplique': ecart_inexplique,
            'taux_ecart': abs(ecart_total / ca_kezia * 100) if ca_kezia > 0 else 0,
            'taux_pertes': abs(pertes_declarees / ca_kezia * 100) if ca_kezia > 0 else 0,
            'alertes': []
        }
        
        # Générer des alertes
        if abs(ecart_inexplique) > 50:
            result['alertes'].append(f"⚠️ Écart inexpliqué de {ecart_inexplique:.2f}€")
        
        if result['taux_pertes'] > 5:
            result['alertes'].append(f"🚨 Taux de pertes élevé: {result['taux_pertes']:.1f}%")
        
        if result['taux_ecart'] < 1:
            result['alertes'].append(f"✅ Écart négligeable: {result['taux_ecart']:.2f}%")
        
        return result
    
    def rapport_jour(self, date=None):
        """Génère un rapport des pertes du jour"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        df = self.get_pertes_jour(date)
        
        print("=" * 70)
        print(f"📊 RAPPORT DES PERTES - {date}")
        print("=" * 70)
        
        if df.empty:
            print("\n✅ Aucune perte enregistrée")
        else:
            print(f"\n💸 Total pertes: {df['montant'].sum():.2f}€")
            print(f"📝 Nombre d'incidents: {len(df)}")
            
            # Par type
            print("\n📋 Par type:")
            par_type = df.groupby('type')['montant'].agg(['sum', 'count'])
            for type_perte, row in par_type.iterrows():
                print(f"   {type_perte}: {row['sum']:.2f}€ ({int(row['count'])} incidents)")
            
            # Détail
            print("\n📄 Détail des pertes:")
            for _, row in df.iterrows():
                print(f"\n   [{row['heure']}] {row['type'].upper()} - {row['montant']:.2f}€")
                print(f"   Raison: {row['raison']}")
                if row['produit']:
                    print(f"   Produit: {row['produit']}")
                if row['commentaire']:
                    print(f"   Note: {row['commentaire']}")
        
        print("\n" + "=" * 70)
    
    def statistiques_periode(self, jours=30):
        """Statistiques des pertes sur une période"""
        from datetime import timedelta
        
        date_fin = datetime.now().strftime("%Y-%m-%d")
        date_debut = (datetime.now() - timedelta(days=jours)).strftime("%Y-%m-%d")
        
        df = self.get_pertes_periode(date_debut, date_fin)
        
        if df.empty:
            return {
                'message': f"Aucune perte sur les {jours} derniers jours"
            }
        
        stats = {
            'periode': f"{date_debut} → {date_fin}",
            'nb_jours': jours,
            'total_pertes': df['montant'].sum(),
            'moyenne_jour': df.groupby('date')['montant'].sum().mean(),
            'nb_incidents': len(df),
            'par_type': df.groupby('type')['montant'].sum().to_dict(),
            'jours_avec_pertes': df['date'].nunique(),
            'top_raisons': df.groupby('raison')['montant'].sum().sort_values(ascending=False).head(5).to_dict()
        }
        
        return stats


# Fonctions helper pour usage rapide
def enregistrer_perte_rapide(montant, raison, type_perte='geste_commercial'):
    """Enregistrement rapide d'une perte"""
    manager = PerteManager()
    return manager.ajouter_perte(montant, type_perte, raison)


def voir_pertes_aujourdhui():
    """Affiche les pertes du jour"""
    manager = PerteManager()
    manager.rapport_jour()


def cloturer_journee(ca_kezia, ca_reel):
    """Clôture de journée simplifiée"""
    manager = PerteManager()
    date = datetime.now().strftime("%Y-%m-%d")
    
    result = manager.valider_journee(
        date=date,
        ca_kezia=ca_kezia,
        ca_reel_compte=ca_reel,
        valide_par="Manager"
    )
    
    print("=" * 70)
    print(f"🔒 CLÔTURE DE JOURNÉE - {date}")
    print("=" * 70)
    print(f"\n💰 CA Kezia: {result['ca_kezia']:.2f}€")
    print(f"💰 CA Réel: {result['ca_reel']:.2f}€")
    print(f"⚖️ Écart brut: {result['ecart_brut']:.2f}€")
    print(f"💸 Pertes déclarées: {result['pertes_declarees']:.2f}€")
    print(f"❓ Écart inexpliqué: {result['ecart_inexplique']:.2f}€")
    print(f"\n📊 Taux d'écart: {result['taux_ecart']:.2f}%")
    print(f"📊 Taux de pertes: {result['taux_pertes']:.2f}%")
    
    if result['alertes']:
        print(f"\n🚨 Alertes:")
        for alerte in result['alertes']:
            print(f"   {alerte}")
    
    print("\n" + "=" * 70)
    
    return result
