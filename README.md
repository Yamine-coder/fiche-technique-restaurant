# 🍕 Fiche Technique - Chez Antoine

![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-ff4b4b?style=flat&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
![Langage](https://img.shields.io/badge/Python-3.10+-blue)

> Une application métier développée en **Python + Streamlit** pour visualiser, analyser et optimiser les **fiches techniques de plats** dans le secteur de la restauration rapide.

---

## 🎯 Objectifs de l'application

- 💰 **Calcul automatique du coût matière** et de la marge  
- 📊 Analyse visuelle de la rentabilité des plats  
- 🛠️ Création et modification de recettes personnalisées  
- 🧠 Suggestions d’ajustement des prix ou des compositions  
- 📂 Export possible des résultats en PDF / tableur (à venir)

---

## 🔍 Fonctionnalités principales

| Fonction                        | Description |
|--------------------------------|-------------|
| 🧾 Fiche technique              | Détail complet d’un plat : ingrédients, coût, marge |
| 📈 Analyse comparative          | Classement des plats les plus/moins rentables |
| ✏️ Éditeur de recettes          | Création de plats personnalisés (drag & drop) |
| 🧠 Aide à la décision           | Recommandations de marge et de prix |
| 📸 Visuels intégrés             | Illustration des plats dans l’analyse |

---


## 🧰 Stack technique

- **Python 3.10+**
- **Streamlit** (interface)
- **Pandas** (calculs & manipulations)
- **Plotly** (visualisations interactives)
- **Openpyxl** (lecture de fichiers Excel)

---

## 📦 Installation locale

1. **Clonez le repo** :

```bash
git clone https://github.com/Yamine-coder/fiche-technique-restaurant.git
cd fiche-technique-restaurant
```

2. **Installez les dépendances** :

```bash
pip install -r requirements.txt
```

3. **Lancez l'application** :

```bash
streamlit run app.py
```

---

## 🗂️ Structure du projet

```bash
📁 data/               # Données d'entrée (recettes, ingrédients, brouillons)
📁 images/             # Images des plats
📄 app.py              # Code principal Streamlit
📄 requirements.txt    # Dépendances Python
📄 brouillons.json     # Plats personnalisés sauvegardés
```

---

## 👨‍🍳 Exemple de cas d’usage

> Le gérant souhaite analyser ses pizzas "Truffe", "Savoyarde" et "Panini Pizz", et détecter les marges trop faibles.  
> En quelques clics, l’app affiche :
> - Le coût matière exact  
> - Le prix de vente conseillé  
> - Le taux de marge  
> - Des recommandations (ajustement prix ou composition)

---

## 📄 Licence

Projet sous licence MIT – libre d’utilisation et de modification pour un usage professionnel.

---

## 🙋‍♂️ Auteur

**Yamine Moussaoui**  
🎓 MSc Intelligence Artificielle & Big Data  
💼 Consultant en Solutions Data & IA  
🔗 [LinkedIn](https://www.linkedin.com/in/yamine-moussaoui-672a25205/)  
📧 moussaouiyamine1@gmail.com  
🔎 [GitHub](https://github.com/Yamine-coder)

---

> *Optimisez vos marges sans sacrifier la qualité.*  
> *Une solution simple, visuelle et intelligente pour les restaurateurs.*
