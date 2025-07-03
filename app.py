import streamlit as st
import time
import copy
st.set_page_config(page_title="🍕 Fiche Technique - Chez Antoine", layout="wide")

# Ajouter le script JavaScript pour gérer les clics sur les boutons
js_code = """
<script>
// Attendre que tout soit chargé
document.addEventListener('DOMContentLoaded', function() {
    // Définir un objet global pour notre application
    window.streamlitApp = {
        // Fonction pour gérer le clic sur le bouton Modifier
        handleEditClick: function(index) {
            console.log("Clic sur le bouton Modifier pour l'index", index);
            setTimeout(function() {
                // Rechercher le bouton d'édition pour cet index spécifique
                const editButton = document.querySelector(`button[data-testid="baseButton-secondary"][key="edit_${index}"]`);
                if (editButton) {
                    console.log("Bouton d'édition trouvé, clic en cours");
                    editButton.click();
                } else {
                    console.error(`Bouton d'édition avec index ${index} non trouvé`);
                    // Chercher tous les boutons d'édition comme solution de secours
                    const editButtons = document.querySelectorAll('button[data-testid="baseButton-secondary"]');
                    console.log("Nombre de boutons d'édition trouvés:", editButtons.length);
                    // Cliquer sur le premier bouton Modifier trouvé
                    for (let btn of editButtons) {
                        if (btn.innerText.includes("Modifier")) {
                            console.log("Bouton Modifier alternatif trouvé, clic en cours");
                            btn.click();
                            break;
                        }
                    }
                }
            }, 100); // Petit délai pour s'assurer que le DOM est stabilisé
        },
        
        // Fonction pour gérer le clic sur le bouton Supprimer
        handleDeleteClick: function(index) {
            console.log("Clic sur le bouton Supprimer pour l'index", index);
            setTimeout(function() {
                // Rechercher le bouton de suppression pour cet index spécifique
                const deleteButton = document.querySelector(`button[data-testid="baseButton-secondary"][key="delete_${index}"]`);
                if (deleteButton) {
                    console.log("Bouton de suppression trouvé, clic en cours");
                    deleteButton.click();
                } else {
                    console.error(`Bouton de suppression avec index ${index} non trouvé`);
                    // Chercher tous les boutons de suppression comme solution de secours
                    const deleteButtons = document.querySelectorAll('button[data-testid="baseButton-secondary"]');
                    console.log("Nombre de boutons de suppression trouvés:", deleteButtons.length);
                    // Cliquer sur le premier bouton Supprimer trouvé
                    for (let btn of deleteButtons) {
                        if (btn.innerText.includes("Supprimer")) {
                            console.log("Bouton Supprimer alternatif trouvé, clic en cours");
                            btn.click();
                            break;
                        }
                    }
                }
            }, 100); // Petit délai pour s'assurer que le DOM est stabilisé
        }
    };
    
    // Observer les mutations du DOM pour réappliquer les gestionnaires de clic lorsque le DOM change
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                // Si de nouveaux nœuds sont ajoutés, essayer de réappliquer les écouteurs d'événements
                console.log("DOM mis à jour, réattachement des gestionnaires");
            }
        });
    });
    
    // Observer tout le corps du document pour les changements
    observer.observe(document.body, { childList: true, subtree: true });
    
    console.log("Script d'interaction des boutons chargé avec succès");
});
</script>
"""
st.markdown(js_code, unsafe_allow_html=True)

# ─── ENTÊTE CRÉATIVE ET RAFFINÉE ─────────────────────────────────────────────────────────

# ─── STYLES CSS CRÉATIFS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
  
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }
  
  /* === ENTÊTE MINIMALISTE === */
  .creative-header {
    position: relative;
    padding: 0.3rem 0 0.2rem 0;
    margin-bottom: 0.5rem;
    overflow: hidden;
  }
  
  .header-backdrop {
    position: absolute;
    top: 0;
    left: -50%;
    right: -50%;
    height: 100%;
    background: radial-gradient(ellipse 100% 60% at 50% 0%, 
      rgba(217, 35, 50, 0.01) 0%, 
      rgba(217, 35, 50, 0.001) 50%, 
      transparent 100%);
    pointer-events: none;
  }
  
  .header-main {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }
  
  .brand-ensemble {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
  }
  
  .title-group {
    position: relative;
  }
  
  .brand-title {
    font-family: 'Crimson Text', serif;
    font-size: 1rem;
    font-weight: 500;
    color: #64748b;
    margin: 0;
    letter-spacing: -0.01em;
    line-height: 1;
    position: relative;
    cursor: default;
    transition: all 0.2s ease;
  }
  
  .brand-title:hover {
    color: #0f172a;
  }
  
  .brand-title::before {
    content: '';
    position: absolute;
    left: -0.4rem;
    top: 50%;
    transform: translateY(-50%);
    width: 2px;
    height: 50%;
    background: linear-gradient(180deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.4) 20%, 
      rgba(217, 35, 50, 0.6) 50%,
      rgba(217, 35, 50, 0.4) 80%, 
      transparent 100%);
    border-radius: 1px;
  }
  
  .title-underline {
    height: 1.5px;
    width: 0;
    background: linear-gradient(90deg, 
      #D92332 0%, 
      rgba(217, 35, 50, 0.4) 70%, 
      transparent 100%);
    margin-top: 0.15rem;
    border-radius: 1px;
    animation: expand-underline 1.2s ease-out 0.4s forwards;
  }
  
  @keyframes expand-underline {
    from { width: 0; }
    to { width: 90px; }
  }
  
  .restaurant-signature {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-left: 1.5rem;
  }
  
  .restaurant-text {
    font-size: 0.85rem;
    font-weight: 400;
    color: #64748b;
    font-style: italic;
    letter-spacing: 0.01em;
    position: relative;
  }
  
  .restaurant-text::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
      rgba(217, 35, 50, 0.2) 0%, 
      rgba(217, 35, 50, 0.05) 100%);
    transform: scaleX(0);
    transform-origin: left;
    animation: expand-line 0.8s ease-out 0.8s forwards;
  }
  
  @keyframes expand-line {
    to { transform: scaleX(1); }
  }
  
  .signature-dots {
    display: flex;
    gap: 0.3rem;
    align-items: center;
  }
  
  .dot {
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #D92332;
    opacity: 0;
    animation: fade-in-dot 0.3s ease-out forwards;
  }
  
  .dot-1 { animation-delay: 1s; }
  .dot-2 { animation-delay: 1.2s; }
  .dot-3 { animation-delay: 1.4s; }
  
  @keyframes fade-in-dot {
    to { opacity: 0.5; }
  }
  
  .header-ornament {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    opacity: 0;
    animation: fade-in-ornament 0.8s ease-out 0.6s forwards;
  }
  
  @keyframes fade-in-ornament {
    to { opacity: 1; }
  }
  
  .ornament-line {
    width: 1px;
    height: 25px;
    background: linear-gradient(180deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.3) 50%, 
      transparent 100%);
  }
  
  .ornament-circle {
    width: 6px;
    height: 6px;
    border: 1px solid rgba(217, 35, 50, 0.25);
    border-radius: 50%;
    position: relative;
  }
  
  .ornament-circle::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 2px;
    height: 2px;
    background: #D92332;
    border-radius: 50%;
    opacity: 0.6;
  }
  
  /* === ENTÊTE DU PLAT CRÉATIVE === */
  .dish-header-creative {
    background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0;
    margin: 0 0 1.25rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .dish-header-creative::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, 
      rgba(217, 35, 50, 0.1) 0%, 
      rgba(217, 35, 50, 0.5) 30%, 
      rgba(217, 35, 50, 0.7) 50%, 
      rgba(217, 35, 50, 0.5) 70%, 
      rgba(217, 35, 50, 0.1) 100%);
  }
  
  .dish-header-creative:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.04);
    border-color: #cbd5e1;
  }
  
  .dish-content {
    padding: 0.875rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
  }
  
  .dish-main {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .dish-name-creative {
    font-size: 1.2rem;
    font-weight: 500;
    color: #1e293b;
    margin: 0;
    letter-spacing: -0.01em;
    position: relative;
  }
  
  .dish-name-creative::after {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 0;
    height: 1.5px;
    background: linear-gradient(90deg, #D92332 0%, rgba(217, 35, 50, 0.3) 100%);
    border-radius: 1px;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .dish-header-creative:hover .dish-name-creative::after {
    width: 100%;
  }
  
  .dish-divider {
    width: 1px;
    height: 20px;
    background: linear-gradient(180deg, 
      transparent 0%, 
      #e2e8f0 50%, 
      transparent 100%);
  }
  
  .dish-category-creative {
    font-size: 0.75rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.3rem 0.6rem;
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    position: relative;
    transition: all 0.3s ease;
  }
  
  .dish-category-creative::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(217, 35, 50, 0.04) 0%, rgba(217, 35, 50, 0.01) 100%);
    border-radius: inherit;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .dish-header-creative:hover .dish-category-creative::before {
    opacity: 1;
  }
  
  .dish-header-creative:hover .dish-category-creative {
    color: #475569;
    border-color: #cbd5e1;
  }
  
  
  /* === TITRE DE SECTION CRÉATIF === */
  .section-title-minimal {
    font-size: 1.1rem;
    font-weight: 500;
    color: #1e293b;
    margin: 0 0 1rem 0;
    padding: 0.6rem 0 0.6rem 1rem;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    position: relative;
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
    border-radius: 6px;
    border: 1px solid #f1f5f9;
    overflow: hidden;
  }
  
  .section-title-minimal::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, 
      #D92332 0%, 
      rgba(217, 35, 50, 0.6) 50%, 
      rgba(217, 35, 50, 0.2) 100%);
    border-radius: 0 1px 1px 0;
  }
  
  .section-title-minimal::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 40px;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.015) 50%, 
      rgba(217, 35, 50, 0.03) 100%);
    pointer-events: none;
  }
  
  .section-title-minimal .icon {
    font-size: 1rem;
    opacity: 0.8;
    color: #D92332;
    filter: drop-shadow(0 1px 1px rgba(217, 35, 50, 0.1));
  }
  
  /* === RESPONSIVE CRÉATIF === */
  @media (max-width: 768px) {
    .creative-header {
      padding: 0.5rem 0 0.25rem 0;
      margin-bottom: 0.75rem;
    }
    
    .header-main {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }
    
    .brand-title {
      font-size: 1.35rem;
    }
    
    .restaurant-signature {
      margin-left: 0;
      gap: 0.5rem;
    }
    
    .restaurant-text {
      font-size: 0.8rem;
    }
    
    .header-ornament {
      align-self: flex-end;
    }
    
    .ornament-line {
      height: 20px;
    }
    
    .dish-header-creative {
      margin-bottom: 1rem;
    }
    
    .dish-content {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
      padding: 0.75rem 1rem;
    }
    
    .dish-main {
      width: 100%;
      justify-content: space-between;
    }
    
    .dish-divider {
      display: none;
    }
    
    .dish-name-creative {
      font-size: 1.1rem;
    }
    
    .dish-category-creative {
      font-size: 0.7rem;
      padding: 0.25rem 0.5rem;
    }
    
    .section-title-minimal {
      font-size: 1rem;
      padding: 0.5rem 0 0.5rem 0.8rem;
      margin-bottom: 0.75rem;
    }
    
    .section-title-minimal .icon {
      font-size: 0.9rem;
    }
  }
  
  @media (max-width: 480px) {
    .brand-title {
      font-size: 1.2rem;
    }
    
    .title-underline {
      animation: expand-underline 1.2s ease-out 0.4s forwards;
    }
    
    @keyframes expand-underline {
      from { width: 0; }
      to { width: 60px; }
    }
    
    .restaurant-text {
      font-size: 0.75rem;
    }
    
    .signature-dots {
      gap: 0.25rem;
    }
    
    .dot {
      width: 2.5px;
      height: 2.5px;
    }
    
    .dish-name-creative {
      font-size: 1rem;
    }
    
    .section-title-minimal {
      padding: 0.4rem 0 0.4rem 0.7rem;
      margin-bottom: 0.6rem;
    }
    
    .section-title-minimal::before {
      width: 2px;
    }
    
    .focus-card {
      padding: 0.75rem 1rem;
      margin: 0.75rem 0;
    }
    
    .focus-title {
      font-size: 0.9rem;
      margin-bottom: 0.4rem;
    }
    
    .focus-content {
      font-size: 0.85rem;
    }
    
    .modern-subheader {
      font-size: 1rem;
      padding: 0.6rem 0 0.6rem 0.8rem;
      margin: 1.5rem 0 0.75rem 0;
    }
    
    .modern-subheader .emoji {
      font-size: 0.9rem;
    }
    
    .alert-success, .alert-warning, .alert-error {
      padding: 0.7rem 0.8rem;
      font-size: 0.85rem;
    }
  }
  
  /* === ÉLÉMENTS HARMONISÉS - TOP 0,1% === */
  .focus-card {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
    border: 1px solid #e2e8f0;
    border-left: 3px solid #D92332;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    cursor: pointer;
  }
  
  .focus-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 0;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.02) 50%, 
      rgba(217, 35, 50, 0.04) 100%);
    transition: width 0.3s ease;
    pointer-events: none;
  }
  
  .focus-card::after {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.05) 50%, 
      transparent 100%);
    border-radius: 12px;
    opacity: 0;
    transition: opacity 0.2s ease;
    z-index: -1;
  }
  
  .focus-card:hover {
    border-color: #cbd5e1;
    box-shadow: 
      0 6px 20px rgba(0, 0, 0, 0.08),
      0 2px 8px rgba(217, 35, 50, 0.05);
    transform: translateY(-2px);
  }
  
  .focus-card:hover::before {
    width: 40px;
  }
  
  .focus-card:hover::after {
    opacity: 1;
  }
  
  .focus-title {
    font-weight: 600;
    font-size: 1rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
  }
  
  .focus-card:hover .focus-title {
    color: #D92332;
    transform: translateX(2px);
  }
  
  .focus-icon {
    color: #D92332;
    filter: drop-shadow(0 1px 2px rgba(217, 35, 50, 0.15));
    transition: all 0.2s ease;
  }
  
  .focus-card:hover .focus-icon {
    transform: scale(1.1);
    filter: drop-shadow(0 2px 4px rgba(217, 35, 50, 0.25));
  }
  
  .focus-content {
    font-size: 0.95rem;
    color: #475569;
    line-height: 1.5;
    transition: color 0.3s ease;
  }
  
  .focus-card:hover .focus-content {
    color: #334155;
  }
  
  .modern-subheader {
    font-size: 1.125rem;
    font-weight: 500;
    color: #1e293b;
    margin: 2rem 0 1rem 0;
    padding: 0.75rem 0 0.75rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    position: relative;
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 8px;
    border: 1px solid #f1f5f9;
    border-left: 3px solid #D92332;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    overflow: hidden;
  }
  
  .modern-subheader::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 0;
    height: 100%;
    background: linear-gradient(90deg, 
      rgba(217, 35, 50, 0.02) 0%, 
      rgba(217, 35, 50, 0.05) 50%, 
      rgba(217, 35, 50, 0.02) 100%);
    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: -1;
  }
  
  .modern-subheader::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 30px;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.02) 100%);
    pointer-events: none;
    transition: all 0.3s ease;
  }
  
  .modern-subheader:hover {
    transform: translateY(-2px);
    border-color: #cbd5e1;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    border-left-width: 4px;
  }
  
  .modern-subheader:hover::before {
    width: 100%;
  }
  
  .modern-subheader:hover::after {
    width: 50px;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.04) 100%);
  }
  
  .modern-subheader .emoji {
    font-size: 1rem;
    filter: drop-shadow(0 1px 1px rgba(217, 35, 50, 0.1));
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  
  .modern-subheader:hover .emoji {
    transform: rotate(-5deg) scale(1.15);
    filter: drop-shadow(0 2px 4px rgba(217, 35, 50, 0.2));
  }
  
  .alert-success {
    background: linear-gradient(135deg, #f0fdf4 0%, #f7fee7 100%);
    border: 1px solid #bbf7d0;
    border-left: 3px solid #22c55e;
    border-radius: 8px;
    padding: 0.875rem 1rem;
    margin: 0.75rem 0;
    color: #15803d;
    font-weight: 500;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    cursor: pointer;
  }
  
  .alert-success::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(34, 197, 94, 0.08) 50%, 
      transparent 100%);
    transition: left 0.4s ease;
  }
  
  .alert-success:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
    border-left-width: 4px;
  }
  
  .alert-success:hover::before {
    left: 100%;
  }
  
  .alert-warning {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border: 1px solid #fde68a;
    border-left: 3px solid #f59e0b;
    border-radius: 8px;
    padding: 0.875rem 1rem;
    margin: 0.75rem 0;
    color: #d97706;
    font-weight: 500;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    cursor: pointer;
  }
  
  .alert-warning::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(245, 158, 11, 0.08) 50%, 
      transparent 100%);
    transition: left 0.4s ease;
  }
  
  .alert-warning:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    border-left-width: 4px;
  }
  
  .alert-warning:hover::before {
    left: 100%;
  }
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(245, 158, 11, 0.1) 50%, 
      transparent 100%);
    transition: left 0.6s ease;
  }
  
  .alert-warning:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 6px 20px rgba(245, 158, 11, 0.15);
    border-left-width: 4px;
  }
  
  .alert-warning:hover::before {
    left: 100%;
  }
  
  .alert-error {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
    border: 1px solid #fecaca;
    border-left: 3px solid #D92332;
    border-radius: 8px;
    padding: 0.875rem 1rem;
    margin: 0.75rem 0;
    color: #dc2626;
    font-weight: 500;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
  }
  
  .alert-error::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.1) 50%, 
      transparent 100%);
    transition: left 0.6s ease;
  }
  
  .alert-error:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 6px 20px rgba(217, 35, 50, 0.15);
    border-left-width: 4px;
  }
  
  .alert-error:hover::before {
    left: 100%;
  }
  .minimal-card {
    background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    position: relative;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
  }
  
  .minimal-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, 
      transparent 0%, 
      rgba(217, 35, 50, 0.3) 50%, 
      transparent 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  
  .minimal-card:hover {
    transform: translateY(-2px);
    border-color: #cbd5e1;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  }
  
  .minimal-card:hover::before {
    opacity: 1;
  }
  
  /* === ANIMATIONS FLUIDES === */
  * {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  
  .creative-header * {
    will-change: transform, opacity;
  }
  
  .dish-header-creative {
    will-change: transform, box-shadow;
  }
  
  .minimal-button {
    background: linear-gradient(135deg, #D92332 0%, #c41e2e 100%);
    color: white !important;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.375rem;
  }
  
  .minimal-button:hover {
    background: linear-gradient(135deg, #c41e2e 0%, #b01a2a 100%);
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(217, 35, 50, 0.2);
  }
  
  .metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
    border-radius: 10px;
    padding: 0.7rem 0.75rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    text-align: center;
    margin-bottom: 0.6rem;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    cursor: pointer;
    border: 1px solid #f1f5f9;
  }
  
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, 
      transparent 0%, 
      #D92332 50%, 
      transparent 100%);
    transition: left 0.4s ease;
  }
  
  .metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, 
      rgba(217, 35, 50, 0.005) 0%, 
      rgba(217, 35, 50, 0.015) 100%);
    opacity: 0;
    transition: opacity 0.2s ease;
    pointer-events: none;
  }
  
  .metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 
      0 8px 20px rgba(0,0,0,0.1),
      0 4px 10px rgba(217, 35, 50, 0.05);
    border-color: #e2e8f0;
  }
  
  .metric-card:hover::before {
    left: 100%;
  }
  
  .metric-card:hover::after {
    opacity: 1;
  }
  
  .metric-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #D92332;
    transition: all 0.2s ease;
    position: relative;
    z-index: 2;
    line-height: 1.2;
  }
  
  .metric-card:hover .metric-value {
    transform: scale(1.05);
    color: #C41E3A;
  }
  
  .metric-title {
    font-size: 0.8rem;
    font-weight: 500;
    color: #64748b;
    transition: all 0.2s ease;
    position: relative;
    z-index: 2;
    margin-top: 0.35rem;
  }
  
  .metric-card:hover .metric-title {
    color: #475569;
  }
  
  /* === ANIMATIONS DISCRÈTES === */
  .focus-icon:hover {
    transform: scale(1.1);
    transition: transform 0.2s ease;
  }
  
  .modern-subheader .emoji:hover {
    transform: scale(1.1);
    transition: transform 0.2s ease;
  }
  
  .modern-subheader::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 0;
    height: 100%;
    background: linear-gradient(90deg, 
      rgba(217, 35, 50, 0.02) 0%, 
      rgba(217, 35, 50, 0.04) 100%);
    transition: width 0.3s ease;
  }
  
  .modern-subheader:hover::before {
    width: 100%;
  }
</style>
""", unsafe_allow_html=True)

import pandas as pd
import plotly.express as px
import os
import json
import numpy as np
from scipy.optimize import linprog
import pulp
import datetime
import matplotlib.pyplot as plt


def save_drafts(drafts, filename="data/brouillons.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(drafts, f, indent=2, ensure_ascii=False)


def load_drafts(filename="data/brouillons.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def autosave_plat(plat_data):
    """
    Sauvegarde automatiquement un plat modifié dans les brouillons.
    Si le plat existe déjà (même nom), il sera mis à jour, sinon il sera ajouté.
    
    Args:
        plat_data (dict): Les données du plat à sauvegarder
    """
    if not plat_data or "nom" not in plat_data:
        return
        
    # Trouver et remplacer le plat existant ou l'ajouter
    plat_trouve = False
    for i, plat in enumerate(st.session_state.brouillons):
        if plat["nom"] == plat_data["nom"]:
            st.session_state.brouillons[i] = plat_data
            plat_trouve = True
            break
    
    if not plat_trouve:
        st.session_state.brouillons.append(plat_data)
    
    # Sauvegarder dans le fichier
    save_drafts(st.session_state.brouillons)


# ============== FONCTIONS ET DONNÉES ==============
@st.cache_data
def load_data():
    """Charge les données des recettes et des ingrédients depuis des fichiers Excel."""
    try:
        recettes = pd.read_excel("data/recettes_complet_MAJ2.xlsx")
        ingredients = pd.read_excel("data/ingredients_nettoyes_et_standardises.xlsx")
        # Stockage du nom original
        recettes["original_plat"] = recettes["plat"]
        ingredients["original_plat"] = ingredients["plat"]

        # Unification des noms pour Panini Pizz
        recettes['plat'] = recettes['plat'].replace({
            'panini pizz base crème': 'panini pizz',
            'panini pizz base tomate': 'panini pizz'
        })
        ingredients['plat'] = ingredients['plat'].replace({
            'panini pizz base crème': 'panini pizz',
            'panini pizz base tomate': 'panini pizz'
        })
        return recettes, ingredients
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return None, None


def calculate_margin_rate(plat, affichage_ht, taux_tva):
    """Calcule le taux de marge d'un plat"""
    try:
        ingr = pd.DataFrame(plat["composition"])
        if "Coût (€)" not in ingr.columns:
            ingr["Coût (€)"] = (ingr["prix_kg"] * ingr["quantite_g"]) / 1000
        
        cout_matiere = ingr["Coût (€)"].sum()
        prix = plat.get('prix_affiche', 0)
        prix_affiche = prix / (1 + taux_tva) if affichage_ht and not plat.get("affichage_ht", False) else prix
        marge = prix_affiche - cout_matiere
        return (marge / prix_affiche * 100) if prix_affiche > 0 else 0
    except:
        return 0


def calculer_cout(ingredients_df: pd.DataFrame) -> pd.DataFrame:
    """Calcule le coût des ingrédients (colonne 'Coût (€)')."""
    # Préserver les coûts fixes pour les ingrédients spéciaux (pâtes)
    if 'ingredient_original' in ingredients_df.columns:
        # Utiliser l'ingrédient original pour détecter les ingrédients spéciaux
        mask_pate_panini = ingredients_df["ingredient_original"].str.lower() == "pâte à panini"
        mask_pate_pizza = ingredients_df["ingredient_original"].str.lower() == "pâte à pizza"
    else:
        # === VUE ÉDITION D'UN PLAT ===
        plat_data = st.session_state.plat_actif
        
        # Vérification automatique du message de succès
        if "save_success_time" in st.session_state:
            current_time = time.time()
            if current_time - st.session_state.save_success_time > 3:
                del st.session_state.save_success_time
                st.rerun()
        
        # Stocker une copie de l'état initial du plat si ce n'est pas déjà fait
        mask_pate_panini = ingredients_df["ingredient"].str.lower() == "pâte à panini"
        mask_pate_pizza = ingredients_df["ingredient"].str.lower() == "pâte à pizza"
    
    mask_special = mask_pate_panini | mask_pate_pizza
    
    # Recalculer uniquement les coûts pour les ingrédients non spéciaux
    ingredients_df.loc[~mask_special, "Coût (€)"] = (
        ingredients_df.loc[~mask_special, "prix_kg"] * 
        ingredients_df.loc[~mask_special, "quantite_g"]
    ) / 1000
    
    # S'assurer que la pâte à panini a toujours un coût de 0.12€
    if mask_pate_panini.any():
        ingredients_df.loc[mask_pate_panini, "Coût (€)"] = 0.12
    
    # S'assurer que la pâte à pizza a toujours le bon coût selon le type de pizza
    if mask_pate_pizza.any():
        # On préserve le coût existant si déjà défini, sinon on utilise 0.12€ (taille S) par défaut
        for idx in ingredients_df.index[mask_pate_pizza]:
            if ingredients_df.loc[idx, "Coût (€)"] == 0:
                ingredients_df.loc[idx, "Coût (€)"] = 0.12  # valeur par défaut (S)
        
    return ingredients_df


def get_dough_cost(plat: str) -> float:
    """
    Renvoie le coût de la pâte selon le plat :
      - panini pizz => 0.12 €
      - plat finissant par S => 0.12 €
      - plat finissant par M => 0.20 €
      - pains => 0.10 € (1/2 pâte M)
      - sinon => 0 €
    """
    plat_low = plat.lower()
        # Cas pizzas Burrata
    if plat_low.startswith("pizza burrata di parma") or plat_low.startswith("pizza burrata di salmone"):
        return 0.12
    # Cas pains
    if "pain aux herbes et mozzarella" in plat_low or "pain aux herbes" in plat_low:
        return 0.10
    # Cas pizzas
    elif plat_low == "panini pizz":
        return 0.12
    elif plat.endswith("S"):
        return 0.12
    elif plat.endswith("M"):
        return 0.20
    else:
        return 0.0


# Dictionnaire de prix de vente
prix_vente_dict = {
    "Savoyarde S": 11.50,
    "Savoyarde M": 13.50,
    "Norvegienne S": 11.50,
    "Norvegienne M": 13.50,
    "Normande S": 11.50,
    "Normande M": 13.50,
    "Raclette S": 11.50,
    "Raclette M": 13.50,
    "4 fromages S": 11.50,
    "4 fromages M": 13.50,
    "Hanna S": 11.50,
    "Hanna M": 13.50,
    "Truffe S": 11.50,
    "Truffe M": 13.50,
    "panini pizz": 5.50,
    "Margarita S": 8.50,
    "Margarita M": 10.50,
    "Calzone S": 9.50,
    "Reine S": 9.50,    
    "Reine M": 11.50,
    "Napolitaine S": 9.50,
    "Napolitaine M": 11.50,
    "Fermière S": 9.50,
    "Fermière M": 11.50,
    "3 Fromages S": 10.50,
    "3 Fromages M": 12.50,
    "Calzone S": 9.50,
    "Orientale S": 10.50,
    "Orientale M": 12.50,
    "Carnée S": 10.50,
    "Carnée M": 12.50,
    "Paysanne S": 10.50,
    "Paysanne M": 12.50,
    "Aubergine S": 10.50,
    "Aubergine M": 12.50,
    "Chèvre-Miel S": 9.50,
    "Chèvre-Miel M": 11.50,
    "Charcutière S": 10.50,
    "Charcutière M": 12.50,
    "Mexicaine S": 10.50,
    "Mexicaine M": 12.50,
    "4 Saisons S": 10.50,
    "4 Saisons M": 12.50,
    "Silicienne S": 10.50,
    "Silicienne M": 12.50,
    "Végétarienne S": 10.50,
    "Végétarienne M": 12.50,
    "Margarita S": 8.50,
    "Margarita M": 10.50,
    "Salade Burrata di Parma": 13.50,
    "Salade burrata di salmone": 13.50,
    "Burrata feuille La véritable": 6.50,
    "Pizza Burrata di Parma": 13.50,
    "Salade César": 9.50,
    "Salade végétarienne": 9.50,
    "Salade chèvre": 9.50,
    "Salade Burrata di Salmone": 13.50,
    "Pizza Burrata Di Salmone": 13.50,
    "Pizza Burrata Di Parma": 13.50,
    "Bolognaise": 9.90,
    "Truffe": 9.90,
    "Saumon": 9.90,
    "Carbonara": 9.90,
    "Fermière": 9.90,
    "3 Fromages": 9.90,
    "Napolitaine": 9.90,
    "Sicilienne": 9.90,
    "Arrabiata": 8.90,
    "Pain aux herbes et mozzarella": 3.00,
    "Pain aux herbes": 2.50,
    "Assiette Artichauts": 5.50,
    "Salade Verte": 5.50,
    "Arrabiata Poulet": 9.90,
}


# Dictionnaire d'images (exemple)
images_plats = {
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
    "panini pizz": "Panini_pizz_creme.webp",
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
    # --- PÂTES ---
    "Bolognaise": "pates_bolognaise.webp",
    "Truffe": "pates_truffe.webp",
    "Saumon": "pates_saumon.webp",
    "Carbonara": "pates_carbonara.webp",
    "Fermière": "pates_fermiere.webp",
    "3 Fromages": "pates_3fromages.webp",
    "Napolitaine": "pates_napolitaine.webp",
    "Sicilienne": "pates_sicilienne.webp",
    "Arrabiata": "pates_arrabiata.webp",
    "Arrabiata Poulet": "pates_arrabiata_poulet.jpeg",
    # --- PAINS MAISON ---
    "Pain aux herbes et mozzarella": "pain_herbes_mozza.webp",
    "Pain aux herbes": "pain_herbes.webp",
    # --- SALADES ---
    "Salade César": "salade_cesar.webp",
    "Salade végétarienne": "salade_vegetarienne.webp",
    "Salade chèvre": "salade_chevre.webp",
    "Assiette Artichauts": "assiette_artichauts.jpeg",
    "Salade Verte": "salade_verte.jpeg",
    # --- BURRATAS ---
    "Pizza Burrata di Parma": "pizza_burrata_parma.jpeg",
    "Burrata feuille La véritable": "burata_feuille.webp",
    "Pizza Burrata Di Salmone": "pizza_burrata_saumon.jpeg",
    "Salade Burrata di Salmone": "salade_burrata_saumon.webp",
    "Salade Burrata di Parma": "salade_burrata_parma.webp",
}


def afficher_image_plat(plat: str, images_dict: dict):
    """Affiche l'image du plat ou l'image par défaut."""
    image_path = f'images/{images_dict.get(plat, "default.jpg")}'
    if not os.path.exists(image_path):
        image_path = "images/default.jpg"
    st.image(image_path, use_container_width=True)


def generer_detailed_breakdown(plat, composition_finale, cout_matiere, prix_affiche):
    """
    Génère une chaîne de texte expliquant le calcul.
    """
    breakdown = f"**Détails du calcul pour {plat}**\n\n"
    for idx, row in composition_finale.iterrows():
        breakdown += f"- {row['ingredient']}: {row['Coût (€)']:.2f} €\n"
    breakdown += f"\n**Coût Matière (ingrédients + pâte)**: {cout_matiere:.2f} €\n"
    return breakdown


def optimize_grammages_linprog(df_ing, prix_affiche, marge_cible, q_min=5):
    """
    Linprog minimise ∑ dᵢ avec qᵢ ≥ q_min, dᵢ ≥ |qᵢ–q0ᵢ|,
    sous ∑(qᵢ·prix_kgᵢ/1000) ≤ budget.
    Exclut toute pâte de l'optimisation (reste fixe).
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
    en pourcentage sur l'ensemble des ingrédients.
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
    Optimisation en deux phases:
    1. Minimiser les changements avec contrainte de marge minimale
    2. Ajuster proportionnellement pour atteindre exactement la marge cible
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

  
# Chargement des données
recettes, ingredients = load_data()
if recettes is None or ingredients is None:
    st.error("Impossible de charger les données. Veuillez réessayer ou contacter le support.")
    st.stop()

# Navigation simplifiée dans la sidebar (sans en-tête)
# Ajout d'un style global pour une barre latérale plus sobre et compacte
st.markdown("""
<style>
.sidebar .block-container {
    padding-top: 0.3rem;
    padding-bottom: 0.5rem;
}
.sidebar h4 {
    margin-top: 0.2rem;
    margin-bottom: 0.2rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: #334155;
}
.sidebar .stRadio > label {
    display: none;
}
.sidebar .stSelectbox > label {
    font-size: 0.85rem;
    padding-bottom: 0rem;
    margin-bottom: 0rem;
}
.sidebar .stCheckbox > label {
    font-size: 0.85rem;
    margin-bottom: 0rem;
}
.sidebar .stSlider > label {
    font-size: 0.85rem;
    margin-bottom: 0rem;
}
.sidebar [data-testid="stVerticalBlock"] > div {
    padding-top: 0.1rem !important;
    padding-bottom: 0.1rem !important;
}
.sidebar .stMarkdown {
    margin-bottom: 0.2rem !important;
}
.sidebar .stContainer {
    margin-bottom: 0.2rem !important;
}
.sidebar div.row-widget.stRadio > div {
    margin-top: 0.1rem !important;
    margin-bottom: 0.1rem !important;
}
.sidebar div.row-widget.stSelectbox > div[data-baseweb="select"] {
    margin-top: 0.1rem !important;
    margin-bottom: 0.2rem !important;
}
.sidebar .stCaption {
    margin-top: -0.2rem !important;
    font-size: 0.75rem !important;
    line-height: 1.2 !important;
}
.sidebar div.stButton > button {
    padding: 0.2rem 0.5rem !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar.container():
    # Titre plus petit pour la navigation
    st.markdown("""
    <div style="
        font-size: 1rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 0.3rem;
        border-left: 3px solid #D92332;
        padding-left: 8px;
        display: flex;
        align-items: center;
    ">Navigation</div>
    """, unsafe_allow_html=True)
    
    mode_analysis = st.radio("", options=[
        "Analyse d'un plat",
        "Analyse comparative",
        "Modifier un plat"
    ], key="mode_navigation", 
    label_visibility="collapsed")

# Séparateur plus discret
st.sidebar.markdown("""
<div style="
    height: 1px;
    background: rgba(49, 51, 63, 0.1);
    margin: 0.2rem 0 0.2rem;
"></div>
""", unsafe_allow_html=True)

with st.sidebar.container():
    affichage_prix = st.radio(
        "Format d'affichage", 
        ["TTC", "HT"], 
        horizontal=True, 
        key="affichage_prix",
        help="TTC inclut toutes les taxes, HT est utilisé pour les calculs de rentabilité"
    )


# Supprime tout affichage non conditionnel du header avant ce bloc !

# Suppression de l'en-tête qui contenait "Chez Antoine"

# PRINCIPAL : GESTION DES DIFFÉRENTS MODES 

if mode_analysis == "Analyse d'un plat":
    # Séparateur simple
    st.sidebar.markdown("""
    <div style="
        height: 1px;
        background: rgba(49, 51, 63, 0.1);
        margin: 0.4rem 0 0.4rem;
    "></div>
    """, unsafe_allow_html=True)
    
    # Réorganisation: Coefficient d'ajustement en premier
    with st.sidebar.container():
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 0.3rem;">
            <div style="font-size: 1rem; font-weight: 600; color: #334155;">Majoration coût généreux</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Coefficient d'ajustement avec badge de pourcentage
        coeff_surplus = st.slider(
            "", 
            1.0, 2.0, 1.3, 0.05,
            help="Majore le coût des ingrédients pour obtenir le coût généreux (1.3 = +30%)",
            label_visibility="collapsed"
        )
        
        # Affichage du pourcentage sous forme de badge
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            margin-top: -0.8rem;
            margin-bottom: 0.5rem;
        ">
            <div style="
                background: rgba(217, 35, 50, 0.1);
                color: #D92332;
                font-size: 0.75rem;
                font-weight: 600;
                padding: 0.2rem 0.5rem;
                border-radius: 4px;
            ">
                +{(coeff_surplus - 1)*100:.0f}% pour coût généreux
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Séparateur entre les sections
    st.sidebar.markdown("""
    <div style="
        height: 1px;
        background: rgba(49, 51, 63, 0.1);
        margin: 0.5rem 0 0.5rem;
    "></div>
    """, unsafe_allow_html=True)
    
    # Section de sélection du plat simplifiée
    with st.sidebar.container():
        st.markdown("#### Sélection du plat")
        
        # Sélection de la catégorie
        categorie_choisie = st.selectbox(
            "Catégorie", 
            ["Tout"] + sorted(list(recettes["categorie"].unique())), 
            key="categorie_analyse"
        )

        # 2️⃣ Liste des plats selon la catégorie
        if categorie_choisie == "Tout":
            plats_dispo = recettes["plat"].unique()
        else:
            plats_dispo = recettes[recettes["categorie"] == categorie_choisie]["plat"].unique()

        # 3️⃣ Sélection du plat avec une meilleure description
        plat = st.selectbox(
            "Plat", 
            plats_dispo, 
            key="plat_unique",
            help="Sélectionnez le plat que vous souhaitez analyser"
        )
    
    # Options simplifiées - Section supprimée car coefficient d'ajustement déplacé en haut
    
    # ️ Récupération de la catégorie du plat pour l'affichage
    plat_info = recettes[recettes['plat'] == plat].iloc[0] if len(recettes[recettes['plat'] == plat]) > 0 else None
    categorie_plat = plat_info['categorie'] if plat_info is not None else "Non définie"
    
    # 🎯 Gérer la portion si catégorie = "Pâtes" (déplacé dans la sidebar)
    portion_faim = "Petite Faim"  # Par défaut
    if categorie_plat.lower() == "pâtes":
        # Séparateur pour section pâtes
        st.sidebar.markdown("""
        <div style="
            height: 1px;
            background: rgba(49, 51, 63, 0.1);
            margin: 0.4rem 0 0.4rem;
        "></div>
        """, unsafe_allow_html=True)
        
        # Section Options Spécifiques Pâtes
        with st.sidebar.container():
            # On crée un div avec un ID unique pour cibler uniquement ce radio button
            st.markdown('<div id="portion_faim_container"></div>', unsafe_allow_html=True)
            portion_container = st.container()
            
            # Style CSS ciblant spécifiquement notre container
            option_style = """
            <style>
            /* Styles pour le conteneur des portions */
            #portion_faim_container + div div[data-testid="stRadio"] > div {
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }
            #portion_faim_container + div div[data-testid="stRadio"] > div:first-child {
                font-size: 0.85rem;
            }
            #portion_faim_container + div div[data-testid="stRadio"] > div > label {
                cursor: pointer;
                background: white;
                border: 1px solid #e2e8f0;
                padding: 0.3rem 0.5rem;
                border-radius: 4px;
                font-size: 0.8rem;
                transition: all 0.2s;
                color: #333;
            }
            #portion_faim_container + div div[data-testid="stRadio"] > div > label:hover {
                border-color: #D92332;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            </style>
            """
            st.markdown(option_style, unsafe_allow_html=True)
            
            # Placer le radio button dans le container spécifique
            with portion_container:
                portion_faim = st.radio(
                    "Taille de portion 🍝",
                    options=["Petite Faim", "Grosse Faim (+3€)"],
                    horizontal=True,
                    key="portion_faim_radio",
                    help="La portion 'Grosse Faim' augmente la quantité de pâtes (+40-52%) et le prix (+3€)"
                )
                
                # Indication discrète pour la portion sélectionnée
                if portion_faim.startswith("Grosse"):
                    st.markdown("<div style='font-size:0.7rem; color:#6b7280; margin-top:-0.2rem;'>Portion XL : +40-52% de pâtes selon le plat</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='font-size:0.7rem; color:#6b7280; margin-top:-0.2rem;'>Portion standard</div>", unsafe_allow_html=True)
    
    # En-tête premium pour "Analyse d'un plat" (style harmonisé avec l'analyse comparative)
    # Style plus compact avec marge supérieure réduite
    st.markdown(f"""
    <div style="
        margin: 0.6rem 0 1rem;
        background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
        border: 1px solid #e2e8f0;
        border-left: 3px solid #D92332;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        padding: 0.9rem 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        border-radius: 7px;
        position: relative;
    ">
        <span style="
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 32px;
            height: 32px;
            border-radius: 6px;
            background: rgba(217, 35, 50, 0.05);
        ">
            <svg width="18" height="18" fill="none" style="display:block;" xmlns="http://www.w3.org/2000/svg">
                <path d="M4 4h16M4 8h6m4 0h6M4 12h6m4 0h6M4 16h16" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 8.5v7" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 6.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                <path d="M17 16.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
            </svg>
        </span>
        <div style="display: flex; flex-direction: column;">
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 1.05rem;
                font-weight: 600;
                color: #1e293b;
                letter-spacing: -0.01em;
                margin-bottom: 0.2rem;
            ">
                Analyse d'un plat
            </div>
            <div style="
                color: #64748b;
                font-size: 0.85rem;
                line-height: 1.3;
                font-weight: 400;
            ">
                Visualisez la composition et les métriques détaillées du plat sélectionné
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # — Interface du plat créative mais plus compacte —
    st.markdown(f"""
    <div style="
        background: #fff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 0.5rem 0.9rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    ">
        <span style="
            font-family: 'Inter', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: #1e293b;
            margin-right: 0.5rem;
        ">{plat}</span>
        <span style="
            background: rgba(217, 35, 50, 0.07);
            color: #D92332;
            font-size: 0.7rem;
            font-weight: 500;
            padding: 0.1rem 0.45rem;
            border-radius: 4px;
        ">{categorie_plat}</span>
    </div>
    """, unsafe_allow_html=True)


    # 1. Filtrer les ingrédients du plat sélectionné
    ingr_plat = ingredients[ingredients['plat'].str.lower() == plat.lower()].copy()


    # 2. 🔢 Quantités spécifiques pour chaque plat (Grosse Faim)
    quantites_grosse_faim = {
        "bolognaise": 330,
        "truffe": 330,
        "saumon": 350,
        "carbonara": 350,
        "fermière": 330,
        "3 fromages": 350,
        "napolitaine": 350,
        "sicilienne": 330,
        "arrabiata": 350,
        "arrabiata poulet": 330,
    }

 
    # 3. Adapter la quantité de pâtes si besoin
    if categorie_plat.lower() == "pâtes":
        plat_key = plat.lower().strip()
        mask_pate = ingr_plat["ingredient"].str.lower().str.contains("spaghetti|penné|pâtes")


        # Adapter la quantité de pâtes si besoin
        if portion_faim.startswith("Grosse"):
            if plat_key in quantites_grosse_faim and mask_pate.any():
                nouvelle_quantite = quantites_grosse_faim[plat_key]
                ingr_plat.loc[mask_pate, "quantite_g"] = nouvelle_quantite
               
        else:
            # Ne rien modifier : on garde les quantités de base (Petite Faim)
            pass


    # 4. Recalcul du coût matière avec les quantités à jour
    ingr_plat = calculer_cout(ingr_plat)


    # 5. Ajustement du prix de vente pour les pâtes en Grosse Faim
    prix_affiche = prix_vente_dict.get(plat, None)
    if categorie_plat.lower() == "pâtes" and portion_faim.startswith("Grosse"):
        prix_affiche += 3  # Ajoute 3€ pour Grosse Faim
   


    # Taux de TVA applicable (ajuste-le si besoin)
    taux_tva = 0.10

    # Sauvegarde du prix TTC pour référence
    prix_ttc = prix_affiche
    
    # Calcul dynamique selon mode d'affichage
    if affichage_prix == "HT" and prix_affiche:
        # Conversion de TTC vers HT
        prix_affiche = prix_affiche / (1 + taux_tva)

   




    salades_avec_pain = [
    "salade burrata di parma",
    "salade burrata di salmone",
    "salade césar",
    "salade chèvre",
    "salade végétarienne"
]
    if plat.lower() in salades_avec_pain:
        ingr_plat = pd.concat([
        ingr_plat,
        pd.DataFrame([{
            "ingredient": "Pain aux herbes",
            "quantite_g": 0,
            "prix_kg": 0,
            "Coût (€)": 0.21,
            "ingredient_lower": "pain aux herbes"
        }])
    ], ignore_index=True)


    # 2. Coût matière initial + pâte
    cout_matiere = ingr_plat["Coût (€)"].sum() + get_dough_cost(plat)
    composition_finale = ingr_plat.copy()
   
    # 3. Ajouter la pâte à pizza si nécessaire
    pate_cost = get_dough_cost(plat)
    if pate_cost > 0:
        composition_finale = pd.concat([
            composition_finale,
            pd.DataFrame([{
                "ingredient": "Pâte à pizza",
                "quantite_g": 0,
                "prix_kg": 0,
                "Coût (€)": pate_cost,
                "ingredient_lower": "pâte à pizza"
            }])
        ], ignore_index=True)
   
    # 4. Traitement spécifique Panini Pizz
    if plat.lower() == "panini pizz":
        # Section panini avec séparateur simple
        st.sidebar.markdown("""
        <div style="height: 1px; background: rgba(49, 51, 63, 0.1); margin: 0.4rem 0;"></div>
        """, unsafe_allow_html=True)
        
        with st.sidebar.container():
            st.markdown("#### Options Panini")
            
            # Calcul des coûts
            cost_creme = ingr_plat.loc[ingr_plat["ingredient"].str.lower() == "crème", "Coût (€)"].sum()
            cost_sauce = ingr_plat.loc[ingr_plat["ingredient"].str.lower() == "sauce tomate", "Coût (€)"].sum()
            
            # Interface optimisée pour le panini
            st.markdown("""
            <style>
            /* Réduire l'espacement des widgets panini */
            div[data-testid="stRadio"] > div:first-child {
                margin-bottom: 0.2rem;
            }
            /* Réduire marge entre checkbox et label */
            div[data-testid="stCheckbox"] > label > div {
                margin-top: 0.1rem;
                margin-bottom: 0.1rem;
            }
            /* Réduire les marges des selectbox */
            div[data-testid="stSelectbox"] {
                margin-bottom: 0.3rem;
            }
            /* Réduire la taille des labels d'ingrédients */
            div[data-testid="stSelectbox"] > label > div {
                font-size: 0.85rem;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Titre compacte
            st.markdown('<div style="font-size:0.9rem; font-weight:500; margin-bottom:0.3rem; margin-top:-0.4rem;">Type de base:</div>', unsafe_allow_html=True)
            
            # Sélection de base simplifiée
            base_selection = st.radio(
                "Base", 
                ["Crème", "Sauce Tomate"], 
                index=0, 
                horizontal=True,
                key="base_panini"
            )
            
            # Option de personnalisation
            st.markdown('<div style="font-size:0.9rem; font-weight:500; margin-bottom:0.1rem; margin-top:0.3rem;">Options avancées:</div>', unsafe_allow_html=True)
            mode_avance = st.checkbox(
                "Personnaliser les ingrédients", 
                key="mode_avance",
                help="Permet de choisir les ingrédients spécifiques du panini"
            )
            
            # Calcul des ingrédients additionnels
            additional = ingr_plat[~ingr_plat["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
            avg_add = additional["Coût (€)"].mean() if not additional.empty else 0.0
            
            if mode_avance:
                # Préparation des données pour les sélecteurs
                already_included = ["crème", "sauce tomate"]
                additional_clean = additional.drop_duplicates(subset=["ingredient"])
                all_ingrs = list(additional_clean.loc[~additional_clean["ingredient"].str.lower().isin(already_included), "ingredient"].unique())
                all_ingrs.sort()
                
                # Ingrédients en disposition compacte
                st.markdown('<div style="font-size:0.9rem; font-weight:500; margin-top:0.4rem; margin-bottom:0.3rem;">Choix des ingrédients:</div>', unsafe_allow_html=True)
                
                slot1 = st.selectbox(
                    "Ingrédient #1", 
                    ["Aucun"] + all_ingrs, 
                    key="slot1"
                )
                
                slot2 = st.selectbox(
                    "Ingrédient #2", 
                    ["Aucun"] + all_ingrs, 
                    key="slot2"
                )
                
                # Astuce discrète
                st.markdown("<div style='font-size:0.7rem; color:#6b7280; margin-top:0.2rem'>💡 Vous pouvez choisir 2× le même ingrédient</div>", unsafe_allow_html=True)
                
                # Résumé visuel pour référence rapide
                st.markdown('<div style="margin-top:0.5rem; padding:0.5rem; background-color:#f8f9fa; border-radius:4px; font-size:0.8rem;">' +
                           f'<div style="font-weight:500;">Composition:</div>' +
                           f'<div>Base: <span style="color:#1E90FF">{base_selection}</span></div>' +
                           f'<div>Ingr. #1: <span style="color:#1E90FF">{slot1 if slot1 != "Aucun" else "-"}</span></div>' +
                           f'<div>Ingr. #2: <span style="color:#1E90FF">{slot2 if slot2 != "Aucun" else "-"}</span></div>' +
                           '</div>', unsafe_allow_html=True)
            
            # Définition du coût de base selon la sélection
            cost_base = cost_creme if base_selection == "Crème" else cost_sauce
            
            # Cette logique est maintenant intégrée dans la sidebar
            if base_selection == "Crème":
                composition_candidates = ingr_plat[ingr_plat["original_plat"].str.contains("base crème", case=False, na=False)].copy()
            else:
                composition_candidates = ingr_plat[ingr_plat["original_plat"].str.contains("base tomate", case=False, na=False)].copy()


            if not mode_avance:
                # Mode simple : utiliser la moyenne des ingrédients additionnels
                cout_panini = cost_base + 2 * avg_add
                df_fake_avg = pd.DataFrame()
                if not additional.empty:
                    row_avg = {
                        "ingredient": "Moyenne suppl",
                        "quantite_g": 0,
                        "prix_kg": 0,
                        "Coût (€)": avg_add,
                        "ingredient_lower": "moyenne suppl"
                    }
                    df_fake_avg = pd.DataFrame([row_avg, row_avg])
                if base_selection == "Crème":
                    df_base = composition_candidates[composition_candidates["ingredient"].str.lower() == "crème"]
                else:
                    df_base = composition_candidates[composition_candidates["ingredient"].str.lower() == "sauce tomate"]
                composition_finale = pd.concat([df_base, df_fake_avg], ignore_index=True)
            else:
                # Mode personnalisé - utiliser les sélections de la sidebar
                additional_clean = additional.drop_duplicates(subset=["ingredient"])
                
                # Calcul des coûts des ingrédients sélectionnés
                cost_slot1 = additional_clean.loc[additional_clean["ingredient"] == slot1, "Coût (€)"].iloc[0] if slot1 != "Aucun" else 0
                cost_slot2 = additional_clean.loc[additional_clean["ingredient"] == slot2, "Coût (€)"].iloc[0] if slot2 != "Aucun" else 0
                cout_panini = cost_base + cost_slot1 + cost_slot2

                # Construction de la composition finale personnalisée
                composition_finale = pd.DataFrame(columns=composition_candidates.columns)
                if base_selection == "Crème":
                    df_base = composition_candidates.loc[composition_candidates["ingredient"].str.lower() == "crème"].iloc[[0]]
                else:
                    df_base = composition_candidates.loc[composition_candidates["ingredient"].str.lower() == "sauce tomate"].iloc[[0]]
                composition_finale = pd.concat([composition_finale, df_base], ignore_index=True)
                
                # Ajout des ingrédients sélectionnés
                if slot1 != "Aucun":
                    ingr1 = additional_clean.loc[additional_clean["ingredient"] == slot1].copy()
                    if not ingr1.empty:
                        # Ajouter un identifiant unique si l'ingrédient est sélectionné deux fois
                        if slot1 == slot2:
                            ingr1["ingredient_id"] = f"{slot1}_1"
                        composition_finale = pd.concat([composition_finale, ingr1], ignore_index=True)
                
                if slot2 != "Aucun":
                    ingr2 = additional_clean.loc[additional_clean["ingredient"] == slot2].copy()
                    if not ingr2.empty:
                        # Ajouter un identifiant unique si l'ingrédient est sélectionné deux fois
                        if slot1 == slot2:
                            ingr2["ingredient_id"] = f"{slot2}_2"
                        composition_finale = pd.concat([composition_finale, ingr2], ignore_index=True)
            
            # Vérifier si la mozzarella est sélectionnée dans les ingrédients
            mozza_count = 0
            
            if mode_avance:
                mozza_count = (slot1 == "Mozzarella") + (slot2 == "Mozzarella")
            
            # Pour garantir que la mozzarella n'est pas présente en double quand elle est sélectionnée
            composition_finale = composition_finale[composition_finale["ingredient"].str.lower() != "mozzarella"]
            
            cost_mozza = 0.234  # Coût final pour 40g de mozzarella
            cost_pate_panini = 0.12  # Coût de la pâte à panini

        # Toujours ajouter une mozzarella de base, même si elle est aussi sélectionnée comme ingrédient
        row_mozza = pd.DataFrame([{
            "ingredient": "Mozzarella",
            "quantite_g": 40,
            "prix_kg": 5.85,
            "Coût (€)": cost_mozza,
            "ingredient_lower": "mozzarella"
        }])
        composition_finale = pd.concat([composition_finale, row_mozza], ignore_index=True)
        
        # Si la mozzarella a été sélectionnée comme ingrédient, on l'ajoute à nouveau (pour la double portion)
        if mozza_count > 0:
            for i in range(mozza_count):
                row_mozza_extra = pd.DataFrame([{
                    "ingredient": "Mozzarella (extra)",
                    "quantite_g": 40,
                    "prix_kg": 5.85,
                    "Coût (€)": cost_mozza,
                    "ingredient_lower": "mozzarella extra"
                }])
                composition_finale = pd.concat([composition_finale, row_mozza_extra], ignore_index=True)

        # Ajout de la pâte à panini
        row_pate = pd.DataFrame([{
            "ingredient": "Pâte à panini",
            "quantite_g": 0,
            "prix_kg": 0,
            "Coût (€)": cost_pate_panini,
            "ingredient_lower": "pâte à panini"
        }])

        # Ajouter la pâte à la composition finale
        composition_finale = pd.concat([composition_finale, row_pate], ignore_index=True)

        # S'assurer que le coût matière inclut tous les éléments
        cout_matiere = composition_finale["Coût (€)"].sum()
        
    # 5. Calcul du coût généreux (avec coefficient)
    # Calcul de la marge basée sur le coût généreux
    # 5. Calculs
    cout_genereux = cout_matiere * coeff_surplus
    marge_generuse = prix_affiche - cout_genereux
    taux_generuse = (marge_generuse / prix_affiche * 100) if prix_affiche and prix_affiche > 0 else None


    marge_brute = prix_affiche - cout_matiere if prix_affiche is not None else None
    taux_marge = (marge_brute / prix_affiche * 100) if marge_brute is not None and prix_affiche and prix_affiche > 0 else None


    # 6. Regroupement final
    my_agg = {
        "quantite_g": "sum",
        "prix_kg": "mean",
        "Coût (€)": "sum",
        "original_plat": "first"
    }
    grouped_finale = composition_finale.groupby("ingredient", as_index=False).agg(my_agg)


    # 7. Texte explicatif
    detailed_breakdown = generer_detailed_breakdown(plat, grouped_finale, cout_matiere, prix_affiche)


    # 🔥 Affichage des KPI fusionnés (format compact)
    st.markdown("<div style='margin-bottom:-0.5rem;'></div>", unsafe_allow_html=True)
    cols = st.columns(5)


    # Bloc 0 : Prix Vente
    with cols[0]:
        val = f"{prix_affiche:.2f}€" if prix_affiche else "N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Prix Vente</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 1 : Coût Matière
    with cols[1]:
        val = f"{cout_matiere:.2f}€"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Coût Matière</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 2 : Coût Généreux + Marge Généreuse + Taux dans la même carte
    with cols[2]:
        val_gen = f"{cout_genereux:.2f}€"
        val_marge = f"{marge_generuse:.2f}€"
        val_taux = f"{taux_generuse:.1f}%" if taux_generuse is not None else "N/A"
        percent_text = f"(+{(coeff_surplus - 1)*100:.0f}%)"
       
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val_gen}</div>"
            f"<div style='font-size:12px; color: #999; line-height:1.1;'>{percent_text}</div>"
            f"<div class='metric-title'>Coût Généreux</div>"
            f"<div style='font-size:12px; margin-top:6px;'>"
            f"💸 Marge : <strong>{val_marge}</strong><br>"
            f"📈 Taux : <strong>{val_taux}</strong>"
            f"</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 3 : Marge Brute
    with cols[3]:
        val = f"{marge_brute:.2f}€" if marge_brute is not None else "N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Marge Brute</div>"
            f"</div>", unsafe_allow_html=True
        )


    # Bloc 4 : Taux de Marge
    with cols[4]:
        val = f"{taux_marge:.1f}%" if taux_marge is not None else"N/A"
        st.markdown(
            f"<div class='metric-card'>"
            f"<div class='metric-value'>{val}</div>"
            f"<div class='metric-title'>Taux de Marge</div>"
            f"</div>", unsafe_allow_html=True
        )
    
    # Réduction de l'espace avant l'affichage de l'image
    st.markdown("<div style='margin-top:-1rem;'></div>", unsafe_allow_html=True)


    # Affichage de l'image et des détails
    col1, col2 = st.columns([1, 2])
    with col1:
        afficher_image_plat(plat, images_plats)
    with col2:
        if not grouped_finale.empty:
            top_ing = grouped_finale.sort_values("Coût (€)", ascending=False).iloc[0]
            part = (top_ing["Coût (€)"] / cout_matiere) * 100 if cout_matiere > 0 else 0
            st.markdown(f"""
<div style="
    background: white;
    border-radius: 10px;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #D92332;
    padding: 1.1rem 1.4rem;
    margin: 1rem 0;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.04);
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle at top right, 
            rgba(217, 35, 50, 0.03) 0%, 
            rgba(217, 35, 50, 0.01) 30%,
            transparent 70%);
        pointer-events: none;
    "></div>
    <div style="
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        margin-bottom: 0.7rem;
    ">
        <div style="
            width: 34px;
            height: 34px;
            min-width: 34px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(217, 35, 50, 0.08);
            border-radius: 7px;
            margin-top: 2px;
        ">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 21L16.65 16.65" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M11 8V14" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 11H14" stroke="#D92332" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="flex: 1;">
            <div style="
                color: #1e293b;
                font-weight: 600;
                font-size: 1rem;
                letter-spacing: -0.01em;
                margin-bottom: 0.6rem;
                display: flex;
                align-items: center;
                gap: 0.4rem;
            ">
                <span>Focus Ingrédient Principal</span>
                <div style="
                    width: 3px;
                    height: 3px;
                    border-radius: 50%;
                    background-color: #D92332;
                    opacity: 0.7;
                    margin-top: 1px;
                "></div>
            </div>
            <div style="
                color: #475569;
                font-size: 0.9rem;
                line-height: 1.5;
                position: relative;
                padding-left: 0;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            ">
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <span style="
                        font-weight: 600;
                        color: #D92332;
                    ">{top_ing['ingredient']}</span>
                    <div style="
                        height: 4px;
                        width: 4px;
                        background: #cbd5e1;
                        border-radius: 50%;
                    "></div>
                    <span>
                        représente <strong>{part:.1f}%</strong> du coût matière
                    </span>
                </div>
                <div style="
                    background: #f8fafc;
                    border-radius: 6px;
                    padding: 0.5rem 0.7rem;
                    font-size: 0.85rem;
                    color: #64748b;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                ">
                    <span>Coût de cet ingrédient:</span>
                    <span style="
                        font-weight: 600;
                        color: #334155;
                        font-variant-numeric: tabular-nums;
                    ">{top_ing['Coût (€)']:.2f} €</span>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    if taux_marge is not None:
        if taux_marge >= 70:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #f0fdf4 0%, #f8fff5 100%);
    border: 1px solid #bbf7d0;
    border-left: 3px solid #22c55e;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 0.8rem;
    box-shadow: 0 1px 3px rgba(34, 197, 94, 0.07);
    position: relative;
    overflow: hidden;
">
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(34, 197, 94, 0.1);
            border-radius: 6px;
        ">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17L4 12" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="
            color: #16a34a;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
        ">
            <span>Ce plat est <strong>très rentable</strong></span>
            <span style="
                font-size: 0.8rem;
                opacity: 0.9;
                font-weight: 400;
                margin-top: 0.1rem;
            ">Marge supérieure à 70% ({taux_marge:.1f}%)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        elif taux_marge >= 50:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #fffbeb 0%, #fffdf5 100%);
    border: 1px solid #fde68a;
    border-left: 3px solid #f59e0b;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 0.8rem;
    box-shadow: 0 1px 3px rgba(245, 158, 11, 0.07);
    position: relative;
    overflow: hidden;
">
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(245, 158, 11, 0.1);
            border-radius: 6px;
        ">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 9V13" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 17.01L12.01 16.9989" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="
            color: #d97706;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
        ">
            <span>Rentabilité <strong>correcte</strong> mais améliorable</span>
            <span style="
                font-size: 0.8rem;
                opacity: 0.9;
                font-weight: 400;
                margin-top: 0.1rem;
            ">Marge entre 50% et 70% ({taux_marge:.1f}%)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #fef2f2 0%, #fff5f5 100%);
    border: 1px solid #fecaca;
    border-left: 3px solid #ef4444;
    border-radius: 8px;
    padding: 0.6rem 0.9rem;
    margin: 0.5rem 0 0.8rem;
    box-shadow: 0 1px 3px rgba(239, 68, 68, 0.07);
    position: relative;
    overflow: hidden;
">
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
    ">
        <div style="
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(239, 68, 68, 0.1);
            border-radius: 6px;
        ">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div style="
            color: #dc2626;
            font-size: 0.9rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
        ">
            <span>Rentabilité <strong>faible</strong> à optimiser</span>
            <span style="
                font-size: 0.8rem;
                opacity: 0.9;
                font-weight: 400;
                margin-top: 0.1rem;
            ">Marge inférieure à 50% ({taux_marge:.1f}%)</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


    # CSS pour réduire les espaces entre les sections
    st.markdown("""
    <style>
    /* Réduire l'espace avant et après les graphiques */
    .stPlotlyChart {
        margin-top: -1rem;
        margin-bottom: -1rem;
    }
    /* Réduire la taille des titres des sections */
    .modern-subheader {
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
        padding: 0.3rem 0.6rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<div class="modern-subheader">
  <span class="emoji">🛒</span>
  Composition du Plat
</div>
""", unsafe_allow_html=True)
    affichage_final = grouped_finale[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]].copy()
    affichage_final.rename(columns={
        'ingredient': 'Ingrédient',
        'quantite_g': 'Quantité (g)',
        'prix_kg': 'Prix (€/kg)',
        'Coût (€)': 'Coût (€)'
    }, inplace=True)
    st.dataframe(affichage_final, use_container_width=True, hide_index=True)
   
    st.markdown("""
<div class="modern-subheader">
  <span class="emoji">📉</span>
  Répartition des coûts par Ingrédient
</div>
""", unsafe_allow_html=True)
    # Réduire la hauteur du graphique circulaire
    fig_pie = px.pie(grouped_finale, values="Coût (€)", names="ingredient", hole=0.4, height=300)
    st.plotly_chart(fig_pie, use_container_width=True)
   
    st.markdown("""
<div class="modern-subheader">
  <span class="emoji">📈</span>
  Coût Matière par Ingrédient
</div>
""", unsafe_allow_html=True)
    # Réduire la hauteur du graphique à barres
    fig_bar = px.bar(grouped_finale, x="ingredient", y="Coût (€)", height=300)
    st.plotly_chart(fig_bar, use_container_width=True)


elif mode_analysis == "Analyse comparative":
    # En-tête principal - Design plus raffiné
    st.markdown("""
    <div style="
        margin: 1.8rem 0 1.3rem;
        background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
        border: 1px solid #e2e8f0;
        border-left: 3px solid #D92332;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        padding: 1.1rem 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.9rem;
        border-radius: 7px;
        position: relative;
    ">
        <span style="
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 36px;
            height: 36px;
            border-radius: 7px;
            background: rgba(217, 35, 50, 0.05);
        ">
            <svg width="20" height="20" fill="none" style="display:block;" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 3v18h18" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <rect x="6" y="9" width="3" height="9" rx="1" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                <rect x="11" y="6" width="3" height="12" rx="1" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
                <rect x="16" y="11" width="3" height="7" rx="1" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.5"/>
            </svg>
        </span>
        <div style="display: flex; flex-direction: column;">
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                font-weight: 600;
                color: #1e293b;
                letter-spacing: -0.01em;
                margin-bottom: 0.3rem;
            ">
                Analyse comparative
            </div>
            <div style="
                color: #64748b;
                font-size: 0.875rem;
                line-height: 1.4;
                font-weight: 400;
            ">
                Comparez les performances de vos plats et identifiez les leviers d'optimisation
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Définition de affichage_ht déplacée avant la création de l'interface utilisateur
    affichage_ht = (affichage_prix == "HT")
    
    # Menu de navigation interne - version compacte et épurée
    st.markdown("""
    <div id="navigation-menu" style="
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 7px;
        padding: 0.85rem 1.15rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    ">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.4rem;
            margin-bottom: 0.6rem;
        ">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 12h18M3 6h18M3 18h18" stroke="#64748b" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="
                font-weight: 600;
                color: #374151;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">Navigation Rapide</span>
        </div>
        <div style="
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        ">
            <a href="#section-kpis" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 1.2rem;
                    height: 1.2rem;
                    font-size: 1.1rem;
                    position: relative;
                ">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M3 3v18h18" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <rect x="6" y="13" width="3" height="5" rx="0.5" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                        <rect x="11" y="9" width="3" height="9" rx="0.5" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
                        <rect x="16" y="5" width="3" height="13" rx="0.5" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.5"/>
                    </svg>
                </span>
                <div>
                    <div style="font-weight: 500;">Indicateurs de Performance</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Marges et rentabilité</div>
                </div>
            </a>
            <a href="#section-top-flop" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="font-size: 1.1rem;">🏆</span>
                <div>
                    <div style="font-weight: 500;">Top & Flop 5</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Meilleurs et pires</div>
                </div>
            </a>
            <a href="#section-tableau" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="font-size: 1.1rem;">📋</span>
                <div>
                    <div style="font-weight: 500;">Tableau Détaillé</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Données complètes</div>
                </div>
            </a>
            <a href="#section-graphique" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="font-size: 1.1rem;">📈</span>
                <div>
                    <div style="font-weight: 500;">Graphiques</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Visualisation</div>
                </div>
            </a>
            <a href="#section-ingredients" style="
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 0.6rem 1rem;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                text-align: left;
                font-family: inherit;
                font-size: 0.85rem;
                color: #64748b;
                text-decoration: none;
            ">
                <span style="font-size: 1.1rem;">🎯</span>
                <div>
                    <div style="font-weight: 500;">Ingrédients Critiques</div>
                    <div style="font-size: 0.75rem; opacity: 0.8;">Analyse poussée</div>
                </div>
            </a>
        </div>
        <style>
        a:hover {
            background-color: #D92332 !important;
            color: white !important;
            border-color: #D92332 !important;
            transform: translateY(-1px);
        }
        a:hover * {
            color: white !important;
        }
        </style>
        <div style="
            padding: 0.5rem;
            background: rgba(217, 35, 50, 0.05);
            border-radius: 4px;
            text-align: center;
            font-size: 0.8rem;
            color: #64748b;
        ">
            💡 <strong>Astuce :</strong> Utilisez les boutons "Retour au menu" en bas de chaque section pour naviguer facilement
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Information sur les prix HT/TTC placée juste après le menu de navigation - design élégant et moderne
    price_mode = "<b>HT</b>" if affichage_ht else "<b>TTC</b>"
    price_badge = "HT" if affichage_ht else "TTC"
    
    st.markdown(f"""
    <div style="
        margin: 0 0 0.8rem; 
        padding: 0.4rem 0.9rem;
        border: 1px solid #e9ecef;
        background: linear-gradient(to right, rgba(255, 255, 255, 0.9), rgba(250, 250, 252, 0.97));
        border-radius: 6px;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(to bottom, #D92332, rgba(217, 35, 50, 0.7));
        "></div>
        <div style="
            background: rgba(217, 35, 50, 0.08);
            color: #D92332;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            margin-right: 0.6rem;
            letter-spacing: 0.03em;
        ">{price_badge}</div>
        <span style="
            color: #475569;
            font-size: 0.8rem;
            font-weight: 400;
            letter-spacing: 0.01em;
        ">Tous les prix sont affichés en {price_mode}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # CSS et animations pour la navigation
    st.markdown("""
    <style>
    /* Animation et transitions fluides */
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes underlineGrow {
        from { width: 0; }
        to { width: 50%; }
    }
    
    /* Navigation fluide et comportement de défilement */
    html {
        scroll-behavior: smooth;
    }
    
    /* Ajustement des ancres pour éviter que les titres soient masqués par le header fixe */
    [id] {
        scroll-margin-top: 70px;
    }
    
    /* Style des liens de navigation */
    a {
        transition: all 0.2s ease;
        text-decoration: none;
    }
    a:hover {
        background-color: #D92332 !important;
        color: white !important;
        border-color: #D92332 !important;
        transform: translateY(-1px);
    }
    a:hover * {
        color: white !important;
    }
    
    /* Responsive design */
    @media (max-width: 600px) {
        .section-title-minimal {
            margin: 1.5rem 0 1.5rem !important;
            padding: 1rem 1.2rem !important;
            gap: 0.8rem !important;
        }
        .section-title-minimal > span:first-child {
            width: 36px !important;
            height: 36px !important;
        }
        .section-title-minimal > div span:first-child {
            font-size: 1rem !important;
        }
        .section-title-minimal > div span:last-child {
            font-size: 0.8rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    all_plats = recettes["plat"].unique()

    # Séparateur simple
    st.sidebar.markdown("""
    <div style="height: 1px; background: rgba(49, 51, 63, 0.1); margin: 0.4rem 0;"></div>
    """, unsafe_allow_html=True)
    
    # Section de sélection des plats simplifiée
    with st.sidebar.container():
        st.markdown("#### Sélection des plats")
        
        categories = recettes["categorie"].unique()
        categories = ["Tout"] + list(categories)  # Ajoute 'Tout' tout en haut

        categorie_comp = st.selectbox(
            "Filtrer par catégorie", 
            categories, 
            key="cat_comp"
        )

        if categorie_comp == "Tout":
            plats_cat = recettes["plat"].unique()
        else:
            plats_cat = recettes[recettes["categorie"] == categorie_comp]["plat"].unique()

        selected_plats = st.multiselect(
            "Plats à comparer", 
            plats_cat, 
            key="selected_plats"
        )
    
    # Section des paramètres d'analyse simplifiée
    with st.sidebar.container():
        st.markdown("#### Paramètres")
        
        seuil_marge = st.slider(
            "Seuil de rentabilité (%)", 
            40, 90, 70
        )
        
        classement_par = st.radio(
            "Classement par", 
            ["Marge (€)", "Taux (%)"]
        )
        
        filtre_sous_seuil = st.checkbox(
            "Plats sous le seuil uniquement"
        )
    
    # Informations complémentaires regroupées
    with st.sidebar.expander("💡 Comprendre les métriques"):
        st.markdown("#### Pourquoi afficher en HT ?")
        st.markdown("""
        • En restauration, la TVA est <b>reversée à l'État</b>, donc ne constitue pas un gain
        • Il est plus juste de calculer les marges en <b>hors taxes (HT)</b>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Pourquoi 70% est un bon seuil ?")
        st.markdown("""
        En restauration, on vise un taux de marge matière de 70% ou plus.
        
        Cela signifie que 30% du prix est consacré aux ingrédients, le reste couvre :
        - ✅ Main d'œuvre
        - ✅ Charges (loyer, énergie...)
        - ✅ Bénéfices
        
        � **Niveaux de rentabilité :**
        - < 50% = souvent à perte  
        - 50–70% = à surveiller  
        - ≥ 70% = bon rendement
        
        *Source: École Hôtelière de Lausanne*
        """)
        
        st.markdown("#### Quel critère choisir ?")
        st.markdown("""
        - **Marge (€)** : met en avant les plats qui rapportent le plus d'argent brut
        - **Taux (%)** : montre les plats les plus efficaces proportionnellement
        """)


    with st.sidebar.expander("ℹ️ Quel critère choisir ?"):
        st.markdown("""
        - **Marge (€)** : met en avant les plats qui rapportent le plus d'argent brut.
        - **Taux (%)** : montre les plats les plus efficaces proportionnellement (rentabilité relative).


        👉 Exemple : un plat pas cher peut avoir un taux élevé mais une petite marge en valeur.
        """)


        def analyse_plat(plat, seuil_marge, affichage_ht=True):
            ingr = ingredients[ingredients['plat'].str.lower() == plat.lower()].copy()
            ingr = calculer_cout(ingr)
            base_cost = ingr["Coût (€)"].sum()
            dough = get_dough_cost(plat)

            if plat.lower() == "panini pizz":
                # Coût moyen des bases (crème et sauce tomate)
                bases = ingr[ingr["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
                mean_base = bases["Coût (€)"].mean() if not bases.empty else 0.0
                avg_add = 0.246  # Moyenne figée des suppléments
                cost_mozza = 0.234  # 40g de mozzarella
                cost_dough = 0.12   # pâte à panini
                total_cost = mean_base + 2 * avg_add + cost_mozza + cost_dough
            else:   
                total_cost = base_cost + dough

            prix_ttc = prix_vente_dict.get(plat, 0)
            taux_tva = 0.10
            prix_affiche = prix_ttc / (1 + taux_tva) if affichage_ht else prix_ttc

            marge = prix_affiche - total_cost
            taux = (marge / prix_affiche * 100) if prix_affiche > 0 else None

            if taux is None:
                note = "❓ Données manquantes"  
            elif taux >= 70 and marge >= 5:
                note = "🔝 Excellent — très rentable"
            elif taux >= 70:
                note = "💡 Bon rendement — petit gain"
            elif taux >= 50 and marge >= 5:
                note = "👍 Correct — à surveiller"  
            elif taux >= 50:    
                note = "⚠️ Faible gain — améliorable"   
            else:
                note = "❌ À revoir — non rentable"

            prix_conseille = total_cost / (1 - seuil_marge / 100) if seuil_marge < 100 else None
            delta_prix = prix_conseille - prix_affiche if prix_conseille else None
            delta_pct = (delta_prix / prix_affiche * 100) if prix_affiche > 0 and delta_prix else None

            if delta_pct is None:
                ajustement = "❓"
            elif delta_pct <= 10:
                ajustement = "✅ raisonnable"
            elif delta_pct <= 25:
                ajustement = "⚠️ à étudier"
            else:
                ajustement = "❌ trop écarté"

            return {
                "Plat": plat,
                "Prix (€)": round(prix_affiche, 2),
                "Coût (€)": round(total_cost, 2),
                "Marge (€)": round(marge, 2),
                "Taux (%)": round(taux, 1) if taux else None,
                "Note": note,
                "Prix conseillé (€)": round(prix_conseille, 2) if prix_conseille else None,
                "Delta (€)": round(delta_prix, 2) if delta_prix else None,
                "Delta (%)": round(delta_pct, 1) if delta_pct else None,
                "Ajustement": ajustement
            }

    plats_analyzes = selected_plats if selected_plats else plats_cat

    # La définition de affichage_ht a été déplacée plus haut pour qu'elle soit disponible pour l'interface
    df = pd.DataFrame([analyse_plat(p, seuil_marge, affichage_ht=affichage_ht) for p in plats_analyzes])




    marge_moy = df["Marge (€)"].mean()
    taux_moy = df["Taux (%)"].mean()
    
    # Calcul d'indicateurs supplémentaires
    nb_plats_analysés = len(df)
    nb_plats_rentables = len(df[df["Taux (%)"] >= seuil_marge])
    pct_plats_rentables = (nb_plats_rentables / nb_plats_analysés * 100) if nb_plats_analysés > 0 else 0
    
    # Aucun KPI à afficher ici car ils ont été remontés en haut de la page
    
    # === SECTION KPIs GLOBAUX === (style harmonisé)
    st.markdown('<div id="section-kpis"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 0.4rem 0 0.8rem;">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.8rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 34px;
                height: 34px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 7px;
            ">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3v18h18" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <rect x="6" y="13" width="3" height="5" rx="0.5" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                    <rect x="11" y="9" width="3" height="9" rx="0.5" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
                    <rect x="16" y="5" width="3" height="13" rx="0.5" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.5"/>
                    <path d="M7.5 10L10 7.5M10 7.5L7.5 5M10 7.5H5M10 7.5V2.5" stroke="#D92332" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <span style="
                    font-weight: 600;
                    color: #1e293b;
                    font-size: 1.05rem;
                ">
                    Indicateurs de Performance
                </span>
                <span style="
                    font-size: 0.8rem;
                    color: #64748b;
                    font-weight: 400;
                    display: block;
                ">
                    Vue d'ensemble des marges et rentabilité
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mise en page en une rangée de trois colonnes pour les KPIs avec style élégant et professionnel
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    
    # KPI 1: Marge Moyenne - Design élégant et professionnel
    with row1_col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(150deg, #ffffff 0%, #fcfcfc 100%);
            border-radius: 8px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.01);
            overflow: hidden;
            position: relative;
            transition: all 0.3s ease;
            height: 110px;
            width: 100%;
            display: flex;
            flex-direction: column;
        ">
            <div style="
                border-left: 3px solid #D92332;
                padding: 0.8rem 1.1rem;
                height: 100%;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 0.7rem;
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 28px;
                        height: 28px;
                        background: rgba(217, 35, 50, 0.08);
                        border-radius: 6px;
                    ">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3 3v18h18" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <rect x="6" y="9" width="3" height="9" rx="1" fill="#D92332" fill-opacity="0.2" stroke="#D92332" stroke-width="1.5"/>
                            <rect x="11" y="6" width="3" height="12" rx="1" fill="#D92332" fill-opacity="0.3" stroke="#D92332" stroke-width="1.5"/>
                            <rect x="16" y="11" width="3" height="7" rx="1" fill="#D92332" fill-opacity="0.15" stroke="#D92332" stroke-width="1.5"/>
                        </svg>
                    </div>
                    <span style="
                        color: #4b5563;
                        font-weight: 600;
                        font-size: 0.95rem;
                        letter-spacing: -0.01em;
                    ">Marge Moyenne</span>
                </div>
                <div style="display: flex; align-items: baseline;">
                    <span style="
                        font-size: 1.65rem;
                        font-weight: 700;
                        color: #1e293b;
                        letter-spacing: -0.02em;
                        display: inline-block;
                        margin-right: 0.5rem;
                        font-feature-settings: 'tnum';
                    ">{marge_moy:.2f} €</span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 500;
                    ">par plat</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 2: Taux de Marge Moyen - Design élégant et professionnel
    with row1_col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(150deg, #ffffff 0%, #fcfcfc 100%);
            border-radius: 8px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.01);
            overflow: hidden;
            position: relative;
            transition: all 0.3s ease;
            height: 110px;
            width: 100%;
            display: flex;
            flex-direction: column;
        ">
            <div style="
                border-left: 3px solid #0369a1;
                padding: 0.8rem 1.1rem;
                height: 100%;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 0.7rem;
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 28px;
                        height: 28px;
                        background: rgba(3, 105, 161, 0.08);
                        border-radius: 6px;
                    ">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M23 6l-9.5 9.5-5-5L1 18" stroke="#0369a1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M17 6h6v6" stroke="#0369a1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <span style="
                        color: #4b5563;
                        font-weight: 600;
                        font-size: 0.95rem;
                        letter-spacing: -0.01em;
                    ">Taux de Marge Moyen</span>
                </div>
                <div style="display: flex; align-items: baseline;">
                    <span style="
                        font-size: 1.65rem;
                        font-weight: 700;
                        color: #1e293b;
                        letter-spacing: -0.02em;
                        display: inline-block;
                        margin-right: 0.5rem;
                        font-feature-settings: 'tnum';
                    ">{taux_moy:.1f} %</span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 500;
                    ">rentabilité</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI 3: Performance du menu - Plats rentables
    with row1_col3:
        st.markdown(f"""
        <div style="
            background: linear-gradient(150deg, #ffffff 0%, #fcfcfc 100%);
            border-radius: 8px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.01);
            overflow: hidden;
            position: relative;
            transition: all 0.3s ease;
            height: 110px;
            width: 100%;
            display: flex;
            flex-direction: column;
        ">
            <div style="
                border-left: 3px solid #10B981;
                padding: 0.8rem 1.1rem;
                height: 100%;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 0.7rem;
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 28px;
                        height: 28px;
                        background: rgba(16, 185, 129, 0.08);
                        border-radius: 6px;
                    ">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M9 12l2 2 4-4M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="#10B981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <span style="
                        color: #4b5563;
                        font-weight: 600;
                        font-size: 0.95rem;
                        letter-spacing: -0.01em;
                    ">Performance menu</span>
                </div>
                <div style="display: flex; align-items: baseline;">
                    <span style="
                        font-size: 1.65rem;
                        font-weight: 700;
                        color: #1e293b;
                        letter-spacing: -0.02em;
                        display: inline-block;
                        margin-right: 0.5rem;
                        font-feature-settings: 'tnum';
                    ">{pct_plats_rentables:.1f} %</span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 500;
                    ">plats rentables</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Bouton retour au menu après la section KPIs
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0 2rem; padding-top: 0.5rem;">
        <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
            <span class="back-to-top-line"></span>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </a>
    </div>
    <style>
    .back-to-top {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.85);
        border-radius: 8px;
        color: #94a3b8;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        border: none;
        cursor: pointer;
        text-decoration: none;
        position: relative;
        backdrop-filter: blur(4px);
        transform-origin: center;
    }
    .back-to-top::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 8px;
        padding: 1.5px;
        background: linear-gradient(45deg, rgba(217, 35, 50, 0.06), rgba(255, 255, 255, 0.1));
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    .back-to-top-line {
        position: absolute;
        top: -6px;
        width: 10px;
        height: 2px;
        background: #D92332;
        border-radius: 4px;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        opacity: 0;
    }
    .back-to-top:hover {
        background: rgba(255, 255, 255, 0.95);
        color: #D92332;
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 16px rgba(217, 35, 50, 0.12);
    }
    .back-to-top:hover .back-to-top-line {
        width: 20px;
        opacity: 1;
    }
    .back-to-top:active {
        transform: translateY(0) scale(0.98);
        box-shadow: 0 2px 8px rgba(217, 35, 50, 0.08);
    }
    .back-to-top svg {
        width: 18px;
        height: 18px;
    }
    .back-to-top svg path {
        stroke: currentColor;
        stroke-width: 1.5;
        stroke-linecap: round;
        stroke-linejoin: round;
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # Styling for back-to-menu buttons
    st.markdown("""
    <style>
    .back-to-menu-dot {
        height: 5px;
        background-color: #D92332;
        border-radius: 50%;
        display: inline-block;
        transition: all 0.2s ease;
    }
    .back-to-menu:hover {
        background: #f1f5f9;
        color: #475569;
        opacity: 1;
        transform: translateY(-1px);
    }
    .back-to-menu:hover .back-to-menu-dot {
        transform: scale(1.3);
    }
    </style>
    """, unsafe_allow_html=True)




    classement_key = "Marge (€)" if classement_par == "Marge (€)" else "Taux (%)"


    if not selected_plats:
        # === SECTION TOP & FLOP 5 ===
        st.markdown('<div id="section-top-flop"></div>', unsafe_allow_html=True)
        top5 = df[df["Taux (%)"] >= seuil_marge].sort_values(classement_key, ascending=False).head(5)
        flop5 = df[df["Taux (%)"] < seuil_marge].sort_values(classement_key, ascending=True).head(5)

        # Section Top 5 et Flop 5 harmonisée avec le style Comparaison Visuelle
        st.markdown("""
        <div style="
            margin: 1.5rem 0;
        ">
        """, unsafe_allow_html=True)
        
        # En-tête Top 5 Plats - Style harmonisé avec Comparaison Visuelle
        st.markdown("""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1rem;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 36px;
                    height: 36px;
                    background: rgba(16, 185, 129, 0.08);
                    border-radius: 8px;
                ">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8.21 13.89L7 23l4.5-2.5L16 23l-1.21-9.11" stroke="#10b981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M15 7a3 3 0 11-6 0 3 3 0 016 0z" stroke="#10b981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M21 10h-4a2 2 0 100 4h1a2 2 0 110 4h-5M3 18h4a2 2 0 100-4H6a2 2 0 110-4h5" stroke="#10b981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div>
                    <span style="
                        font-weight: 600;
                        color: #1e293b;
                        font-size: 1.15rem;
                    ">
                        Top 5 Plats
                    </span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 400;
                        display: block;
                    ">
                        Classement par """ + f"{classement_key}" + """
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Affichage du dataframe Top 5 dans un conteneur stylisé
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.03) 0%, rgba(16, 185, 129, 0.01) 100%);
                border: 1px solid rgba(16, 185, 129, 0.15);
                border-radius: 8px;
                padding: 0.5rem;
                margin-bottom: 1.5rem;
            ">
        """, unsafe_allow_html=True)
        
        st.dataframe(top5, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # En-tête Flop 5 Plats - Style harmonisé avec Comparaison Visuelle
        st.markdown("""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin: 1.5rem 0 1rem 0;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 36px;
                    height: 36px;
                    background: rgba(244, 63, 94, 0.08);
                    border-radius: 8px;
                ">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 9v2M12 15h.01" stroke="#f43f5e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="#f43f5e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div>
                    <span style="
                        font-weight: 600;
                        color: #1e293b;
                        font-size: 1.15rem;
                    ">
                        Flop 5 Plats
                    </span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 400;
                        display: block;
                    ">
                        À optimiser en priorité
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Affichage du dataframe Flop 5 dans un conteneur stylisé
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, rgba(244, 63, 94, 0.03) 0%, rgba(244, 63, 94, 0.01) 100%);
                border: 1px solid rgba(244, 63, 94, 0.15);
                border-radius: 8px;
                padding: 0.5rem;
                margin-bottom: 1rem;
            ">
        """, unsafe_allow_html=True)
        
        st.dataframe(flop5, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Bouton retour au menu après la section Top/Flop
        st.markdown("""
        <div style="text-align: center; margin: 1.5rem 0 2rem; padding-top: 0.5rem;">
            <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
                <span class="back-to-top-line"></span>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </a>
        </div>
        """, unsafe_allow_html=True)


        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1rem;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 36px;
                    height: 36px;
                    background: rgba(217, 35, 50, 0.06);
                    border-radius: 8px;
                ">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L16 4m0 13V4m0 0L9 7" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div>
                    <span style="
                        font-weight: 600;
                        color: #1e293b;
                        font-size: 1.15rem;
                    ">
                        Stratégies d'optimisation
                    </span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 400;
                        display: block;
                    ">
                        Analyse comparative des plats sous-performants
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not flop5.empty:
            st.markdown("""
            <div style="margin-bottom: 0.5rem;">
            """, unsafe_allow_html=True)
            
            for _, row in flop5.iterrows():
                taux = row['Taux (%)']
                ecart = seuil_marge - taux
                
                # Définir la criticité avec les couleurs de la charte graphique
                # Définir les styles en fonction de l'écart
                if ecart >= 10:
                    bg_color = "#FEECEE"  # Rouge très clair
                    icon = "⚠️"
                    text_color = "#D92332"  # Rouge de la charte
                    icon_color = "#D92332"  # Rouge de la charte
                    border_color = "rgba(217, 35, 50, 0.25)"
                    status_text = "critique"
                elif ecart >= 5:
                    bg_color = "#FEF6EC"  # Orange très clair
                    icon = "✏️"
                    text_color = "#F97316"  # Orange
                    icon_color = "#F97316"  # Orange
                    border_color = "rgba(249, 115, 22, 0.25)"
                    status_text = "à surveiller"
                else:
                    bg_color = "#F0F9FF"  # Bleu très clair
                    icon = "ℹ️"
                    text_color = "#0F76D9"  # Bleu de la charte
                    icon_color = "#0F76D9"  # Bleu de la charte
                    border_color = "rgba(15, 118, 217, 0.25)"
                    status_text = "à améliorer"
                
                # Calcul du coût actuel et du prix
                plat_name = row['Plat']
                coût_actuel = row.get('Coût denrées', 0)
                prix_vente = row.get('Prix de vente', 0)
                
                st.markdown(f"""
                <div style="
                    background-color: {bg_color};
                    padding: 1rem;
                    margin-bottom: 0.75rem;
                    border-radius: 8px;
                    display: flex;
                    align-items: flex-start;
                    gap: 0.75rem;
                    border: 1px solid {border_color};
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                ">
                    <div style="
                        font-size: 1.1rem;
                        color: {icon_color};
                        padding-top: 0.1rem;
                        min-width: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">{icon}</div>
                    <div style="flex-grow: 1;">
                        <div style="
                            font-weight: 600;
                            color: {text_color};
                            font-size: 0.95rem;
                            margin-bottom: 0.25rem;
                        ">"{plat_name}"</div>
                        <div style="
                            color: {text_color};
                            opacity: 0.9;
                            font-size: 0.85rem;
                            margin-bottom: 0.25rem;
                        ">Marge actuelle: {taux:.1f}% (objectif: {seuil_marge:.1f}%)</div>
                        <div style="
                            color: {text_color};
                            font-size: 0.85rem;
                            font-weight: 500;
                        ">
                            <span style="display: inline-block; margin-right: 4px;">⟶</span>
                            <strong>Écart au seuil: {ecart:.1f}%</strong> - Statut: {status_text}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="
                background-color: #EBF9F1;
                padding: 1rem;
                margin-bottom: 0.75rem;
                border-radius: 8px;
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                border: 1px solid rgba(16, 185, 129, 0.25);
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <div style="
                    font-size: 1.1rem;
                    color: #10B981;
                    padding-top: 0.1rem;
                    min-width: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">✓</div>
                <div style="flex-grow: 1;">
                    <div style="
                        font-weight: 600;
                        color: #10B981;
                        font-size: 0.95rem;
                        margin-bottom: 0.1rem;
                    ">Excellent!</div>
                    <div style="
                        color: #10B981;
                        opacity: 0.9;
                        font-size: 0.85rem;
                    ">Tous les plats analysés sont au-dessus du seuil de rentabilité.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

    # === SECTION TABLEAU DÉTAILLÉ ===
    st.markdown('<div id="section-tableau"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 1.5rem 0;">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 8px;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H7" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <span style="
                    font-weight: 600;
                    color: #1e293b;
                    font-size: 1.15rem;
                ">
                    Détail des plats sélectionnés
                </span>
                <span style="
                    font-size: 0.85rem;
                    color: #64748b;
                    font-weight: 400;
                    display: block;
                ">
                    Analyse complète des plats
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        df.sort_values(classement_key, ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Bouton retour au menu après le tableau
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0 2rem; padding-top: 0.5rem;">
        <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
            <span class="back-to-top-line"></span>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # === SECTION COMPARAISON VISUELLE ===
    st.markdown('<div id="section-graphique"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 2rem 0 1rem;">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 8px;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3v18h18M9 9l3-3 4 4-3 3-4-4z" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <span style="
                    font-weight: 600;
                    color: #1e293b;
                    font-size: 1.15rem;
                ">
                    Comparaison Visuelle
                </span>
                <span style="
                    font-size: 0.85rem;
                    color: #64748b;
                    font-weight: 400;
                    display: block;
                ">
                    Prix vs Coût vs Marge
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Préparer le DataFrame pour le chart
    df_chart = df[["Plat", "Prix (€)", "Coût (€)", "Marge (€)", "Taux (%)"]].dropna()

    # Filtrer si demandé
    if filtre_sous_seuil:
        df_chart = df_chart[df_chart["Taux (%)"] < seuil_marge]

    # Restructurer pour Plotly
    df_melt = df_chart.melt(
        id_vars="Plat",
        value_vars=["Prix (€)", "Coût (€)", "Marge (€)"],
        var_name="Type", value_name="Valeur (€)"
    )
    fig = px.bar(
        df_melt,
        x="Plat", y="Valeur (€)",
        color="Type", barmode="group",
        color_discrete_map={
            "Prix (€)": "#0F76D9", 
            "Coût (€)": "#F43F5E", 
            "Marge (€)": "#10B981"
        }
    )
    
    # Amélioration du style du graphique
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Inter, sans-serif",
        legend=dict(
            orientation="h",
            y=1.1,
            title_text=""
        ),
        margin=dict(l=0, r=0, t=30, b=0),
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Bouton retour au menu après la comparaison visuelle
    st.markdown("""
    <div style="text-align: center; margin: 1.5rem 0 2rem;">
        <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
            <span class="back-to-top-line"></span>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </a>
    </div>
    """, unsafe_allow_html=True)

    # === SECTION ANALYSE DES INGRÉDIENTS CRITIQUES ===
    st.markdown('<div id="section-ingredients"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin: 2rem 0 1rem;">
        <div style="
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 8px;
            ">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 7L2 10l3 3M19 7l3 3-3 3" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 5l-7 14h14L12 5z" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 12v3M12 18h0.01" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <span style="
                    font-weight: 600;
                    color: #1e293b;
                    font-size: 1.15rem;
                ">
                    Analyse des Ingrédients Critiques
                </span>
                <span style="
                    font-size: 0.85rem;
                    color: #64748b;
                    font-weight: 400;
                    display: block;
                ">
                    Ingrédients avec le plus d'impact sur vos coûts
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyse des ingrédients critiques
    def analyser_ingredients_critiques(plats_analyses):
        """Analyse les ingrédients qui pèsent le plus sur les coûts globaux"""
        tous_ingredients = []
        
        for plat_nom in plats_analyses:
            # Récupérer les ingrédients du plat
            ingr_plat = ingredients[ingredients['plat'].str.lower() == plat_nom.lower()].copy()
            
            if not ingr_plat.empty:
                # Calculer les coûts
                ingr_plat = calculer_cout(ingr_plat)
                
                # Ajouter le coût de la pâte si applicable
                cout_pate = get_dough_cost(plat_nom)
                if cout_pate > 0:
                    ingr_plat = pd.concat([
                        ingr_plat,
                        pd.DataFrame([{
                            "ingredient": "Pâte à pizza",
                            "plat": plat_nom,
                            "quantite_g": 250,  # Estimation moyenne
                            "prix_kg": cout_pate * 4,  # Approximation du prix/kg
                            "Coût (€)": cout_pate
                        }])
                    ], ignore_index=True)
                
                # Gestion spéciale pour Panini Pizz
                if plat_nom.lower() == "panini pizz":
                    # Remplacer par les coûts moyens calculés
                    bases = ingr_plat[ingr_plat["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
                    mean_base = bases["Coût (€)"].mean() if not bases.empty else 0.0
                    avg_add = 0.246  # Moyenne des suppléments
                    
                    # Nettoyer et reconstruire
                    ingr_plat = pd.DataFrame([
                        {"ingredient": "Base (moyenne)", "plat": plat_nom, "quantite_g": 50, "prix_kg": mean_base * 20, "Coût (€)": mean_base},
                        {"ingredient": "Suppléments (moyenne)", "plat": plat_nom, "quantite_g": 100, "prix_kg": avg_add * 10, "Coût (€)": avg_add * 2},
                        {"ingredient": "Mozzarella", "plat": plat_nom, "quantite_g": 40, "prix_kg": 5.85, "Coût (€)": 0.234},
                        {"ingredient": "Pâte à panini", "plat": plat_nom, "quantite_g": 120, "prix_kg": 1.0, "Coût (€)": 0.12}
                    ])
                
                # Ajouter le nom du plat pour traçabilité
                ingr_plat["plat_origine"] = plat_nom
                tous_ingredients.append(ingr_plat)
        
        if not tous_ingredients:
            return pd.DataFrame()
        
        # Combiner tous les ingrédients
        df_ingredients = pd.concat(tous_ingredients, ignore_index=True)
        
        # Grouper par ingrédient et calculer les totaux
        analyse_ingredients = df_ingredients.groupby("ingredient").agg({
            "Coût (€)": ["sum", "count", "mean"],
            "quantite_g": "sum",
            "prix_kg": "mean",
            "plat_origine": lambda x: list(set(x))
        }).round(3)
        
        # Aplatir les colonnes multi-niveaux
        analyse_ingredients.columns = [
            "Coût Total (€)", "Nb Plats", "Coût Moyen (€)", 
            "Quantité Totale (g)", "Prix Moyen (€/kg)", "Plats Concernés"
        ]
        
        # Calculer les pourcentages
        cout_total_global = analyse_ingredients["Coût Total (€)"].sum()
        analyse_ingredients["% du Coût Total"] = (
            analyse_ingredients["Coût Total (€)"] / cout_total_global * 100
        ).round(1)
        
        # Trier par impact financier
        analyse_ingredients = analyse_ingredients.sort_values("Coût Total (€)", ascending=False)
        
        return analyse_ingredients.reset_index()
    
    # Effectuer l'analyse
    ingredients_critiques = analyser_ingredients_critiques(plats_analyzes)
    
    if not ingredients_critiques.empty:
        # Affichage des top 10 ingrédients critiques
        top_ingredients = ingredients_critiques.head(10)
        
        # KPIs des ingrédients critiques
        col1, col2, col3 = st.columns(3)
        
        with col1:
            impact_top3 = top_ingredients.head(3)["% du Coût Total"].sum()
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(217, 35, 50, 0.03) 0%, rgba(217, 35, 50, 0.01) 100%);
                border: 1px solid rgba(217, 35, 50, 0.15);
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            ">
                <div style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin-bottom: 0.25rem;">
                    {impact_top3:.1f}%
                </div>
                <div style="font-size: 0.8rem; color: #64748b; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px;">
                    Impact Top 3
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            ingredient_le_plus_cher = top_ingredients.iloc[0]
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(3, 105, 161, 0.03) 0%, rgba(3, 105, 161, 0.01) 100%);
                border: 1px solid rgba(3, 105, 161, 0.15);
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            ">
                <div style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin-bottom: 0.25rem;">
                    {ingredient_le_plus_cher['Coût Total (€)']:.2f}€
                </div>
                <div style="font-size: 0.8rem; color: #64748b; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px;">
                    Coût le Plus Élevé
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; font-style: italic;">
                    {ingredient_le_plus_cher['ingredient']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            nb_ingredients_significatifs = len(ingredients_critiques[ingredients_critiques["% du Coût Total"] >= 5])
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.03) 0%, rgba(16, 185, 129, 0.01) 100%);
                border: 1px solid rgba(16, 185, 129, 0.15);
                border-radius: 8px;
                padding: 1rem;
                text-align: center;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            ">
                <div style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin-bottom: 0.25rem;">
                    {nb_ingredients_significatifs}
                </div>
                <div style="font-size: 0.8rem; color: #64748b; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px;">
                    Ingrédients à > 5%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Tableau des ingrédients critiques
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(217, 35, 50, 0.03) 0%, rgba(217, 35, 50, 0.01) 100%);
            border: 1px solid rgba(217, 35, 50, 0.15);
            border-radius: 8px;
            padding: 0.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        ">
        """, unsafe_allow_html=True)
        
        # Préparer le dataframe pour l'affichage
        df_affichage = top_ingredients[["ingredient", "Coût Total (€)", "% du Coût Total", "Nb Plats", "Prix Moyen (€/kg)"]].copy()
        df_affichage.columns = ["Ingrédient", "Coût Total (€)", "% Impact", "Nb Plats", "Prix (€/kg)"]
        
        st.dataframe(df_affichage, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Graphique en secteurs des ingrédients critiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Répartition des coûts par ingrédient**")
            # Prendre les 8 premiers + regrouper le reste
            top_8 = top_ingredients.head(8)
            autres_cout = ingredients_critiques.iloc[8:]["Coût Total (€)"].sum() if len(ingredients_critiques) > 8 else 0
            
            if autres_cout > 0:
                pie_data = pd.concat([
                    top_8[["ingredient", "Coût Total (€)"]],
                    pd.DataFrame([{"ingredient": "Autres", "Coût Total (€)": autres_cout}])
                ])
            else:
                pie_data = top_8[["ingredient", "Coût Total (€)"]]
            
            fig_pie = px.pie(
                pie_data, 
                values="Coût Total (€)", 
                names="ingredient", 
                hole=0.4,
                color_discrete_sequence=[
                    "#D92332", "#0369a1", "#10b981", "#f59e0b", "#8b5cf6", 
                    "#ef4444", "#06b6d4", "#84cc16", "#f97316"
                ]
            )
            fig_pie.update_layout(
                font_family="Inter, sans-serif",
                showlegend=True,
                legend=dict(orientation="v", y=0.5, font=dict(size=11)),
                margin=dict(l=0, r=0, t=30, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("**Top 10 - Impact financier**")
            # Créer une palette de couleurs dégradée basée sur la charte
            colors = [f"rgba(217, 35, 50, {0.9 - i*0.08})" for i in range(len(top_ingredients.head(10)))]
            
            fig_bar = px.bar(
                top_ingredients.head(10),
                x="% du Coût Total",
                y="ingredient",
                orientation="h",
                color="% du Coût Total",
                color_continuous_scale=[[0, "#fef2f2"], [0.5, "#fca5a5"], [1, "#D92332"]]
            )
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_family="Inter, sans-serif",
                yaxis=dict(categoryorder="total ascending", tickfont=dict(size=11)),
                xaxis=dict(tickfont=dict(size=11)),
                coloraxis_showscale=False,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            fig_bar.update_traces(
                marker_line_color='rgba(217, 35, 50, 0.3)',
                marker_line_width=1
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Recommandations basées sur l'analyse
        st.markdown("""
        <div style="margin: 1.5rem 0;">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 1rem;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 36px;
                    height: 36px;
                    background: rgba(217, 35, 50, 0.06);
                    border-radius: 8px;
                ">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div>
                    <span style="
                        font-weight: 600;
                        color: #1e293b;
                        font-size: 1.15rem;
                    ">
                        Insights stratégiques
                    </span>
                    <span style="
                        font-size: 0.85rem;
                        color: #64748b;
                        font-weight: 400;
                        display: block;
                    ">
                        Actions prioritaires pour améliorer la rentabilité
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Générer des recommandations intelligentes
        recommandations = []
        
        # Recommandation sur l'ingrédient le plus impactant
        top_ingredient = top_ingredients.iloc[0]
        if top_ingredient["% du Coût Total"] > 15:
            recommandations.append(f"🎯 **{top_ingredient['ingredient']}** représente {top_ingredient['% du Coût Total']:.1f}% de vos coûts. Négociez avec vos fournisseurs ou cherchez des alternatives.")
        
        # Recommandation sur les ingrédients très présents
        ingredients_frequents = top_ingredients[top_ingredients["Nb Plats"] >= len(plats_analyzes) * 0.6]
        if len(ingredients_frequents) > 0:
            ing_freq = ingredients_frequents.iloc[0]
            recommandations.append(f"📊 **{ing_freq['ingredient']}** est utilisé dans {ing_freq['Nb Plats']} plats. Optimiser son prix peut avoir un impact global.")
        
        # Recommandation sur les prix élevés
        ingredients_chers = top_ingredients[top_ingredients["Prix Moyen (€/kg)"] > 10]
        if len(ingredients_chers) > 0:
            ing_cher = ingredients_chers.iloc[0]
            recommandations.append(f"💰 **{ing_cher['ingredient']}** coûte {ing_cher['Prix Moyen (€/kg)']:.2f}€/kg. Vérifiez s'il existe des substituts moins chers.")
        
        # Recommandation générale
        if impact_top3 > 50:
            recommandations.append(f"⚡ Les 3 premiers ingrédients représentent {impact_top3:.1f}% de vos coûts. Concentrez vos efforts d'optimisation sur ces postes.")
        
        # Afficher les recommandations
        for i, rec in enumerate(recommandations):
            # Définir les couleurs selon la charte graphique
            if i % 4 == 0:
                couleur = "#0F76D9"  # Bleu de la charte
                bg_color = "#F0F9FF"
                border_color = "rgba(15, 118, 217, 0.25)"
            elif i % 4 == 1:
                couleur = "#10B981"  # Vert de la charte
                bg_color = "#EBF9F1"
                border_color = "rgba(16, 185, 129, 0.25)"
            elif i % 4 == 2:
                couleur = "#F97316"  # Orange
                bg_color = "#FEF6EC"
                border_color = "rgba(249, 115, 22, 0.25)"
            else:
                couleur = "#D92332"  # Rouge de la charte
                bg_color = "#FEECEE"
                border_color = "rgba(217, 35, 50, 0.25)"
                
            st.markdown(f"""
            <div style="
                background-color: {bg_color};
                padding: 1rem;
                margin-bottom: 0.75rem;
                border-radius: 8px;
                border: 1px solid {border_color};
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <div style="color: {couleur};">
                    {rec}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Bouton retour au menu après les ingrédients critiques
        st.markdown("""
        <div style="text-align: center; margin: 1.5rem 0 2rem;">
            <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
                <span class="back-to-top-line"></span>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                </svg>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.warning("Aucune donnée d'ingrédients disponible pour l'analyse.")
        
        # Bouton retour au menu même en cas d'absence de données
        st.markdown("""
        <div style="text-align: center; margin: 1.5rem 0 2rem;">
            <a href="#navigation-menu" class="back-to-top" aria-label="Retour au menu">
                <span class="back-to-top-line"></span>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.6568 15.6569L12 10L6.34314 15.6569" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                </svg>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
elif mode_analysis == "Modifier un plat":
    # === CSS MODERNE ET HARMONISÉ POUR LE MODE GESTION DES PLATS ===
    st.markdown("""
    <style>
    /* Variables CSS pour cohérence */
    :root {
        --primary: #D92332;
        --primary-light: rgba(217, 35, 50, 0.1);
        --primary-dark: #b41c29;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
        --neutral-50: #f8fafc;  
        --neutral-100: #f1f5f9;
        --neutral-200: #e2e8f0;
        --neutral-300: #cbd5e1;
        --neutral-400: #94a3b8;
        --neutral-500: #64748b;
        --neutral-600: #475569;
        --neutral-700: #334155;
        --neutral-800: #1e293b;
        --neutral-900: #0f172a;
        --radius: 8px;
        --radius-lg: 12px;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --transition: all 0.25s cubic-bezier(0.25, 1, 0.5, 1);
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Masquer l'en-tête principal pour une interface plus épurée */
    .creative-header {
        display: none !important;
    }
    
    /* Navigation moderne par onglets */
    .dish-nav-tabs {
        display: flex;
        background: var(--neutral-50);
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        padding: 0.5rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-sm);
        overflow-x: auto;
        gap: 0.25rem;
    }
    
    .dish-nav-tab {
        flex: 1;
        min-width: 140px;
        padding: 0.75rem 1rem;
        background: transparent;
        color: var(--neutral-600);
        border: none;
        border-radius: var(--radius);
        font-weight: 500;
        font-size: 0.875rem;
        cursor: pointer;
        transition: var(--transition);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        text-decoration: none;
        white-space: nowrap;
    }
    
    .dish-nav-tab:hover {
        background: rgba(255, 255, 255, 0.7);
        color: var(--primary);
    }
    
    .dish-nav-tab.active {
        background: white;
        color: var(--primary);
        box-shadow: var(--shadow-sm);
        font-weight: 600;
    }
    
    .dish-nav-tab.disabled {
        opacity: 0.5;
        cursor: not-allowed;
        color: var(--neutral-400);
    }
    
    /* Header moderne */
    .dish-header-modern {
        background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
        border: 1px solid var(--neutral-200);
        border-left: 3px solid var(--primary);
        box-shadow: var(--shadow-sm);
        border-radius: var(--radius);
        padding: 1.25rem 1.5rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .dish-header-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: var(--primary-light);
        border-radius: var(--radius);
        flex-shrink: 0;
    }
    
    .dish-header-content h1 {
        font-family: var(--font-sans);
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 0.25rem 0;
        letter-spacing: -0.01em;
    }
    
    .dish-header-content p {
        color: var(--neutral-500);
        font-size: 0.875rem;
        margin: 0;
        line-height: 1.4;
    }
    
    /* Cards des plats - Style minimaliste ultra moderne */
    .dish-card-modern {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.5);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    
    .dish-card-modern::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: var(--neutral-200);
        transition: var(--transition);
    }
    
    /* Styles minimalistes pour chaque statut */
    .dish-card-modern.excellent {
        border-left: 4px solid var(--success);
        background: white;
    }
    
    .dish-card-modern.good {
        border-left: 4px solid var(--warning);
        background: white;
    }
    
    .dish-card-modern.poor {
        border-left: 4px solid var(--danger);
        background: white;
    }
    
    .dish-card-modern.excellent::before { 
        content: none;
    }
    .dish-card-modern.good::before { 
        content: none;
    }
    .dish-card-modern.poor::before { 
        content: none;
    }
    
    .dish-card-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
        border-color: rgba(203, 213, 225, 0.9);
    }
    
    .dish-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1.2rem;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    
    .dish-card-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 0.35rem 0;
        line-height: 1.3;
        letter-spacing: -0.01em;
    }
    
    .dish-card-base {
        font-size: 0.8rem;
        color: var(--neutral-500);
        padding: 0;
        display: inline-block;
        font-weight: 400;
    }
    
    .dish-card-status {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.6rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        border: none;
        position: relative;
        transition: all 0.2s ease;
    }
    
    .dish-card-status::before {
        display: none;
    }
    
    .dish-card-status.excellent {
        background: rgba(16, 185, 129, 0.1);
        color: var(--success);
    }
    
    .dish-card-status.good {
        background: rgba(245, 158, 11, 0.1);
        color: var(--warning);
    }
    
    .dish-card-status.poor {
        background: rgba(244, 63, 94, 0.1);
        color: var(--danger);
    }
    
    .dish-card-metrics {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
        padding: 1.25rem;
        background: var(--neutral-50);
        border-radius: var(--radius);
        border: 1px solid var(--neutral-200);
    }
    
    .dish-metric {
        text-align: center;
    }
    
    .dish-metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--neutral-800);
        margin-bottom: 0.25rem;
        line-height: 1;
    }
    
    .dish-metric-label {
        font-size: 0.75rem;
        color: var(--neutral-500);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    .dish-card-actions {
        display: flex;
        gap: 0.75rem;
        margin-top: 1.5rem;
    }
    
    /* Boutons modernes */
    .btn-modern {
        flex: 1;
        padding: 0.75rem 1rem;
        border-radius: var(--radius);
        font-weight: 500;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        transition: var(--transition);
        cursor: pointer;
        border: 1px solid;
        text-decoration: none;
    }
    
    .btn-primary {
        background: white;
        color: var(--primary);
        border-color: var(--primary);
    }
    
    .btn-primary:hover {
        background: var(--primary);
        color: white;
        box-shadow: 0 4px 12px rgba(217, 35, 50, 0.25);
        transform: translateY(-1px);
    }
    
    .btn-secondary {
        background: white;
        color: var(--neutral-500);
        border-color: var(--neutral-200);
    }
    
    .btn-secondary:hover {
        background: var(--danger);
        color: white;
        border-color: var(--danger);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
        transform: translateY(-1px);
    }
    
    /* Formulaires modernes */
    .form-modern {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-sm);
    }
    
    .form-section-modern {
        margin-bottom: 2rem;
    }
    
    .form-section-modern h3 {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--neutral-200);
    }
    
    .form-section-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: var(--primary-light);
        border-radius: var(--radius);
        color: var(--primary);
    }
    
    /* Métriques de prévisualisation */
    .preview-metrics-modern {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .preview-metric {
        background: var(--neutral-50);
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius);
        padding: 1.25rem;
        text-align: center;
        transition: var(--transition);
    }
    
    .preview-metric:hover {
        border-color: var(--primary);
        box-shadow: var(--shadow-sm);
    }
    
    .preview-metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--neutral-800);
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .preview-metric-label {
        font-size: 0.875rem;
        color: var(--neutral-500);
        font-weight: 500;
    }
    
    /* Interface d'édition avancée */
    .edit-interface-modern {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    .edit-interface-header {
        background: linear-gradient(135deg, var(--neutral-50) 0%, var(--neutral-100) 100%);
        padding: 2rem;
        border-bottom: 1px solid var(--neutral-200);
    }
    
    .edit-interface-content {
        padding: 2rem;
    }
    
    /* Tableau d'ingrédients moderne */
    .ingredients-table-modern {
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius);
        overflow: hidden;
        margin-bottom: 2rem;
    }
    
    .ingredients-header {
        background: var(--neutral-50);
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--neutral-200);
        font-weight: 600;
        color: var(--neutral-700);
        font-size: 0.875rem;
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr auto;
        gap: 1rem;
        align-items: center;
    }
    
    .ingredient-row-modern {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--neutral-100);
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr auto;
        gap: 1rem;
        align-items: center;
        transition: var(--transition);
    }
    
    .ingredient-row-modern:last-child {
        border-bottom: none;
    }
    
    .ingredient-row-modern:hover {
        background: var(--neutral-50);
    }
    
    .ingredient-name-modern {
        font-weight: 500;
        color: var(--neutral-800);
    }
    
    .ingredient-cost-modern {
        font-weight: 600;
        color: var(--primary);
    }
    
    /* États vides */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: white;
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        margin: 2rem 0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        opacity: 0.6;
    }
    
    .empty-state h3 {
        color: var(--neutral-800);
        margin-bottom: 0.75rem;
        font-weight: 600;
        font-size: 1.25rem;
    }
    
    .empty-state p {
        color: var(--neutral-500);
        margin: 0;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .dish-nav-tabs {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .dish-nav-tab {
            min-width: auto;
        }
        
        .dish-card-metrics, .preview-metrics-modern {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .ingredients-header, .ingredient-row-modern {
            grid-template-columns: 1fr;
            gap: 0.5rem;
            text-align: left;
        }
        
        .dish-card-actions {
            flex-direction: column;
        }
        
        .form-modern {
            padding: 1.5rem;
        }
    }
    
    /* Animations modernes et subtiles */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(6px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    @keyframes subtlePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .dish-card-status:hover {
        transform: translateY(-1px);
    }
    
    .animate-slide-up {
        animation: slideInUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        will-change: transform, opacity;
    }
    
    .animate-fade-in {
        animation: fadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        will-change: transform, opacity;
    }
    
    .dish-card-modern.excellent:hover {
        box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.2), 0 3px 8px rgba(0, 0, 0, 0.06);
    }
    
    .dish-card-modern.good:hover {
        box-shadow: 0 0 0 1px rgba(245, 158, 11, 0.2), 0 3px 8px rgba(0, 0, 0, 0.06);
    }
    
    .dish-card-modern.poor:hover {
        box-shadow: 0 0 0 1px rgba(244, 63, 94, 0.2), 0 3px 8px rgba(0, 0, 0, 0.06);
    }
    
    /* Interface d'édition premium */
    .edit-interface-premium {
        background: white;
        border-radius: 16px;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.05),
            0 1px 3px rgba(0, 0, 0, 0.03);
        border: 1px solid var(--neutral-200);
        margin-bottom: 2rem;
        overflow: hidden;
    }
    
    .edit-interface-premium-header {
        padding: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(to right, #ffffff, #fcfcfc);
        border-bottom: 1px solid var(--neutral-100);
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .edit-dish-main {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .edit-dish-icon {
        width: 48px;
        height: 48px;
        background: var(--primary-light);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(217, 35, 50, 0.1);
    }
    
    .edit-dish-info h1 {
        font-size: 1.35rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.01em;
    }
    
    .edit-dish-subtitle {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: var(--neutral-500);
        font-size: 0.875rem;
    }
    
    .edit-dish-base {
        font-weight: 500;
    }
    
    .edit-dish-divider {
        width: 3px;
        height: 3px;
        background: var(--neutral-300);
        border-radius: 50%;
    }
    
    .edit-dish-id {
        font-size: 0.75rem;
        color: var(--neutral-400);
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    
    .edit-dish-status {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .status-icon {
        font-size: 1.25rem;
    }
    
    .status-content {
        display: flex;
        flex-direction: column;
    }
    
    .status-text {
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-value {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    /* Métriques premium */
    .edit-metrics-premium {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0;
        border-bottom: 1px solid var(--neutral-100);
        background: linear-gradient(to bottom, #ffffff, #f9fafc);
    }
    
    .edit-metric {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        border-right: 1px solid var(--neutral-100);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .edit-metric:last-child {
        border-right: none;
    }
    
    .edit-metric:hover {
        background: linear-gradient(to bottom, #ffffff, #f0f4f8);
        transform: translateY(-2px);
    }
    
    .edit-metric-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        font-size: 0.85rem;
        color: var(--neutral-500);
        font-weight: 500;
    }
    
    .edit-metric-header svg {
        color: var(--neutral-400);
        transition: transform 0.3s ease;
    }
    
    .edit-metric:hover .edit-metric-header svg {
        transform: scale(1.1);
        color: var(--primary);
    }
    
    .edit-metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--neutral-800);
        margin-bottom: 0.75rem;
        transition: color 0.3s ease;
    }
    
    .edit-metric:hover .edit-metric-value {
        color: var(--primary);
    }
    
    .edit-metric-footer {
        margin-top: auto;
    }
    
    .edit-metric-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.35rem 0.75rem;
        background: var(--neutral-100);
        color: var(--neutral-600);
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        transition: all 0.3s ease;
    }
    
    .edit-metric:hover .edit-metric-badge {
        background: var(--primary-light);
        color: var(--primary);
    }
    
    /* Badge container */
    .edit-badge-container {
        padding: 0.75rem 1.25rem;
        background: var(--neutral-50);
        display: flex;
        justify-content: flex-end;
    }
    
    .edit-badge {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        color: var(--neutral-500);
        font-size: 0.75rem;
    }
    
    /* Onglets d'édition modernes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: var(--neutral-50) !important;
        padding: 0.5rem !important;
        border-radius: 10px !important;
        border: 1px solid var(--neutral-200) !important;
        margin-bottom: 1rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        color: var(--neutral-600) !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: var(--primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: var(--primary) !important;
        font-weight: 600 !important;
        border: 1px solid var(--neutral-200) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Form sections premium */
    .form-section-premium {
        margin-bottom: 1.5rem;
        background: white;
        border-radius: 12px;
        border: 1px solid var(--neutral-200);
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        padding: 1.25rem;
    }
    
    .form-section-header {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--neutral-100);
        padding-bottom: 1rem;
    }
    
    .form-section-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        background: var(--primary-light);
        border-radius: 8px;
        color: var(--primary);
        flex-shrink: 0;
    }
    
    .form-section-title h3 {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--neutral-800);
        margin: 0 0 0.25rem 0;
    }
    
    .form-section-title p {
        color: var(--neutral-500);
        font-size: 0.85rem;
        margin: 0;
    }
    
    .form-section-content {
        padding: 0 0 0.5rem 0;
    }
    
    .form-section-hint {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        background-color: rgba(99, 179, 237, 0.1);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        border-left: 3px solid rgba(99, 179, 237, 0.6);
        margin-bottom: 1rem;
    }
    
    .hint-icon {
        font-size: 1rem;
    }
    
    .hint-text {
        font-size: 0.85rem;
        color: #3182CE;
        line-height: 1.4;
    }
    
    /* Champs de saisie plus modernes */
    [data-testid="stTextInput"] input, 
    [data-testid="stNumberInput"] input {
        border-radius: 8px !important;
        border: 1px solid var(--neutral-200) !important;
        padding: 0.6rem 0.75rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stTextInput"] input:focus, 
    [data-testid="stNumberInput"] input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(217, 35, 50, 0.1) !important;
    }
    
    /* Style pour les sélecteurs */
    [data-testid="stSelectbox"] [data-baseweb="select"] {
        border-radius: 8px !important;
        border-color: var(--neutral-200) !important;
    }
    
    [data-testid="stSelectbox"] [data-baseweb="select"]:hover {
        border-color: var(--neutral-300) !important;
    }
    
    /* Responsive design pour l'interface d'édition */
    @media (max-width: 768px) {
        .edit-interface-premium-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1rem;
        }
        
        .edit-dish-status {
            align-self: stretch;
        }
        
        .edit-metrics-premium {
            grid-template-columns: 1fr;
        }
        
        .edit-metric {
            border-right: none;
            border-bottom: 1px solid var(--neutral-100);
        }
        
        .edit-metric:last-child {
            border-bottom: none;
        }
        
        .form-section-premium {
            padding: 1rem;
        }
    }
    
    .dish-nav-tabs::-webkit-scrollbar-track {
        background: var(--neutral-100);
        border-radius: 2px;
    }
    
    .dish-nav-tabs::-webkit-scrollbar-thumb {
        background: var(--neutral-300);
        border-radius: 2px;
    }
    
    .dish-nav-tabs::-webkit-scrollbar-thumb:hover {
        background: var(--neutral-400);
    }
    </style>
    """, unsafe_allow_html=True)

    # === INITIALISATION ET CONFIGURATION ===
    # Initialisation des états
    if "brouillons" not in st.session_state:
        st.session_state.brouillons = load_drafts()
    if "plat_actif" not in st.session_state:
        st.session_state.plat_actif = None
    if "suggestions" not in st.session_state:
        st.session_state.suggestions = None
    if "edit_view" not in st.session_state:
        st.session_state.edit_view = "liste"
    if "show_success" not in st.session_state:
        st.session_state.show_success = False

    # Configuration
    affichage_ht_edit = (affichage_prix == "HT")
    taux_tva = 0.10
    seuil_marge_perso = st.sidebar.slider("🎯 Objectif de marge (%)", 40, 90, 70, 1, key="objectif_marge_edit")

    # === HEADER PREMIUM ===
    
    # Déterminer l'étape actuelle pour la navigation
    current_view = st.session_state.edit_view
    current_dish = st.session_state.plat_actif["nom"] if st.session_state.plat_actif else ""
    
    # En-tête principal avec style harmonisé avec l'analyse comparative
    st.markdown(f"""
    <div style="
        margin: 1.5rem 0 1.5rem;
        background: linear-gradient(to right, #ffffff 0%, #fcfcfc 100%);
        border: 1px solid #e2e8f0;
        border-left: 3px solid #D92332;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        padding: 1.2rem 1.3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 8px;
        position: relative;
    ">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                background: rgba(217, 35, 50, 0.06);
                border-radius: 8px;
            ">
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 3h18v18H3V3z" stroke="#D92332" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M9 9h6M9 13h6M9 17h6" stroke="#D92332" stroke-width="1.2" stroke-linecap="round"/>
                </svg>
            </div>
            <div>
                <span style="
                    font-weight: 600;
                    color: #1e293b;
                    font-size: 1.15rem;
                ">
                    Gestion des plats personnalisés
                </span>
                <span style="
                    font-size: 0.85rem;
                    color: #64748b;
                    font-weight: 400;
                    display: block;
                ">
                    Créez, modifiez et optimisez vos recettes avec une analyse de rentabilité en temps réel
                </span>
            </div>
        </div>
        <div style="
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.9rem;
            background: rgba(217, 35, 50, 0.03);
            border: 1px solid rgba(217, 35, 50, 0.1);
            border-radius: 7px;
        ">
            <span style="
                font-size: 1.25rem;
                font-weight: 700;
                color: #D92332;
                margin-right: 0.2rem;
            ">{len(st.session_state.brouillons)}</span>
            <span style="
                font-size: 0.75rem;
                color: #64748b;
                font-weight: 500;
            ">plats enregistrés</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Ajout de styles premium pour le header et le fil d'Ariane
    st.markdown("""
    <style>
    
    /* Header premium avec effets visuels améliorés */
    .dish-header-premium {
        display: flex;
        background: linear-gradient(150deg, #ffffff 0%, #fcfcfc 100%);
        border-radius: 12px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }
    
    .dish-header-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(to bottom, #D92332, rgba(217, 35, 50, 0.7));
        border-radius: 8px 0 0 8px;
    }
    
    .dish-header-premium:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }
    
    .dish-header-left {
        display: flex;
        align-items: center;
    }
    
    .dish-header-right {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .dish-header-stats {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .dish-header-stat {
        text-align: center;
        padding: 0.75rem 1.25rem;
        background: rgba(217, 35, 50, 0.03);
        border: 1px solid rgba(217, 35, 50, 0.1);
        border-radius: 10px;
        min-width: 100px;
    }
    
    .stat-value {
        display: block;
        font-size: 1.5rem;
        font-weight: 700;
        color: #D92332;
        line-height: 1.2;
    }
    
    .stat-label {
        display: block;
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    .dish-header-icon {
        background: rgba(217, 35, 50, 0.1);
        border-radius: 12px;
        width: 54px;
        height: 54px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1.25rem;
        box-shadow: 0 4px 10px rgba(217, 35, 50, 0.15);
    }
    
    .dish-header-content h1 {
        color: #1e293b;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.2;
        position: relative;
    }
    
    .dish-header-content h1::after {
        content: '';
        display: block;
        width: 40px;
        height: 3px;
        background: linear-gradient(to right, #D92332, rgba(217, 35, 50, 0.4));
        margin-top: 0.5rem;
        border-radius: 2px;
    }
    
    .dish-header-content p {
        color: #64748b;
        font-size: 1rem;
        margin: 0.5rem 0 0;
        max-width: 80%;
        line-height: 1.5;
    }
    
    /* Animations */
    .animate-slide-up {
        animation: slideUp 0.5s ease-out;
    }
    
    .animate-fade-in {
        animation: fadeIn 0.4s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Navigation par boutons uniquement
    st.markdown("""
    <div class="nav-buttons">
    """, unsafe_allow_html=True)
    
    # Conteneur pour les boutons de navigation minimalistes
    st.markdown("""
    <div class="nav-buttons">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # Liste des plats - Premier onglet - Bouton Streamlit fonctionnel
    with col1:
        liste_active = st.session_state.edit_view == "liste"
        
        # Style conditionnel pour le bouton actif
        button_type = "primary" if liste_active else "secondary"
        
        if st.button(
            "📋 Liste des plats",
            key="nav_liste",
            type=button_type,
            use_container_width=True,
            help="Voir tous les plats disponibles"
        ):
            st.session_state.edit_view = "liste"
            st.rerun()
    
    # Créer un plat - Deuxième onglet - Bouton Streamlit fonctionnel
    with col2:  
        creation_active = st.session_state.edit_view == "creation"
        
        # Style conditionnel pour le bouton actif
        button_type = "primary" if creation_active else "secondary"
        
        if st.button(
            "➕ Créer un plat",
            key="nav_creation",
            type=button_type,
            use_container_width=True,
            help="Créer une nouvelle recette"
        ):
            st.session_state.edit_view = "creation"
            st.rerun()
    
    # Messages contextuels améliorés et personnalisés pour guider l'utilisateur
    if st.session_state.edit_view == "liste":
        context_title = "Liste des plats"
        context_message = "Consultez et sélectionnez un plat pour le modifier ou créez une nouvelle recette personnalisée."
    elif st.session_state.edit_view == "creation":
        context_title = "Création de plat"
        context_message = "Configurez votre nouvelle recette en choisissant une base et en ajustant les ingrédients selon vos besoins."
    else:
        plat_name = st.session_state.plat_actif["nom"] if st.session_state.plat_actif else "plat"
        context_title = f"Édition: {plat_name}"
        context_message = f"Personnalisez les ingrédients et ajustez les coûts pour optimiser la rentabilité de votre recette."
    
    # Préparation de l'indicateur d'étape visuel
    if st.session_state.edit_view == "liste":
        step_indicator = "1/3"
    elif st.session_state.edit_view == "creation":
        step_indicator = "2/3"
    else:
        step_indicator = "3/3"
        
    # Affichage du message contextuel avec un design amélioré et indicateur d'étape
    st.markdown(f"""
    <div class="context-message">
        <div class="step-badge">{step_indicator}</div>
        <div class="context-content">
            <div class="context-title">{context_title}</div>
            <div class="context-text">{context_message}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CSS pour les boutons de navigation minimalistes et le message contextuel
    st.markdown("""
    <style>
    /* Style pour les boutons de navigation */
    .nav-buttons {
        margin-bottom: 0.75rem;
    }
    
    [data-testid="baseButton-primary"] {
        background: rgba(217, 35, 50, 0.08) !important;
        border: 1px solid rgba(217, 35, 50, 0.2) !important;
        color: #D92332 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="baseButton-primary"]:hover {
        background: rgba(217, 35, 50, 0.12) !important;
        border-color: rgba(217, 35, 50, 0.3) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
    }
    
    [data-testid="baseButton-secondary"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        color: #64748b !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        border-color: #cbd5e1 !important;
        color: #475569 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03) !important;
    }
    
    [data-testid="baseButton-secondary"]:disabled {
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Style pour le message contextuel - design élégant et moderne */
    .context-message {
        display: flex;
        align-items: flex-start;
        background: linear-gradient(145deg, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin: 0.9rem 0 1.7rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        transition: all 0.25s ease;
        animation: fadeIn 0.5s ease;
        position: relative;
        overflow: hidden;
    }
    
    /* Style pour le badge d'indicateur d'étape */
    .step-badge {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        background-color: #D92332;
        color: white;
        font-weight: 700;
        font-size: 0.75rem;
        border-radius: 50%;
        margin-right: 1rem;
        flex-shrink: 0;
        box-shadow: 0 2px 5px rgba(217, 35, 50, 0.2);
    }
    
    .context-message:hover {
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
        transform: translateY(-1px);
    }
    
    .context-message::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100%;
        background: linear-gradient(to left, rgba(241, 245, 249, 0.7), rgba(241, 245, 249, 0));
        pointer-events: none;
    }
    

    
    .context-content {
        flex: 1;
    }
    
    .context-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.2rem;
        letter-spacing: 0.01em;
    }
    
    .context-text {
        font-size: 0.825rem;
        color: #64748b;
        line-height: 1.4;
        letter-spacing: 0.01em;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modifier un plat - Troisième onglet - Bouton Streamlit fonctionnel
    with col3:
        edition_active = st.session_state.edit_view == "edition"
        
        # Déterminer le texte du bouton et tronquer le nom si nécessaire
        if st.session_state.plat_actif:
            plat_name = st.session_state.plat_actif["nom"]
            if len(plat_name) > 15:
                edit_btn_label = f"✏️ {plat_name[:12]}..."
            else:
                edit_btn_label = f"✏️ {plat_name}"
            btn_title = f"Modifier : {plat_name}"
        else:
            edit_btn_label = "✏️ Modifier un plat"
            btn_title = "Sélectionnez d'abord un plat à modifier"
            
        edit_btn_disabled = not st.session_state.plat_actif
        
        # Style conditionnel pour le bouton actif
        button_type = "primary" if edition_active else "secondary"
        
        if st.button(
            edit_btn_label,
            key="nav_edition",
            type=button_type,
            use_container_width=True,
            help=btn_title,
            disabled=edit_btn_disabled
        ):
            if st.session_state.plat_actif:
                st.session_state.edit_view = "edition"
                st.rerun()
        
        # Ajouter un indicateur visuel simple pour l'onglet actif
        if edition_active:
            st.markdown("""
            <div style="text-align: center; color: #D92332; font-size: 0.8rem; margin-top: 0.3rem;">
                ⚡ Mode édition actif
            </div>
            """, unsafe_allow_html=True)
    
    # Fermeture de la div nav-buttons après tous les boutons
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    # Style CSS premium pour les boutons
    st.markdown("""
    <style>
    /* Style pour les boutons de navigation avec apparence premium */
    [data-testid="baseButton-primary"] {
        background: rgba(217, 35, 50, 0.08) !important;
        border: 1px solid rgba(217, 35, 50, 0.3) !important;
        color: #D92332 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(217, 35, 50, 0.05) !important;
        transition: all 0.2s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="baseButton-primary"]::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
        transition: all 0.6s ease !important;
    }
    
    [data-testid="baseButton-primary"]:hover::before {
        left: 100% !important;
    }
    
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(217, 35, 50, 0.15) !important;
        background: rgba(217, 35, 50, 0.12) !important;
    }
    
    [data-testid="baseButton-secondary"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        color: #64748b !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        border-color: #cbd5e1 !important;
        color: #475569 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 6px rgba(0,0,0,0.03) !important;
    }
    
    [data-testid="baseButton-secondary"]:disabled {
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # === CONTENU SELON LA VUE ACTIVE ===
    if st.session_state.edit_view == "liste":
        # === VUE LISTE DES PLATS ===
        # Message d'information sur les prix
        price_mode = "<b>HT</b>" if affichage_ht_edit else "<b>TTC</b>"
        price_badge = "HT" if affichage_ht_edit else "TTC"
        
        st.markdown(f"""
        <div style="
            margin: 0 0 0.8rem; 
            padding: 0.4rem 0.9rem;
            border: 1px solid #e9ecef;
            background: linear-gradient(to right, rgba(255, 255, 255, 0.9), rgba(250, 250, 252, 0.97));
            border-radius: 6px;
            display: flex;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 3px;
                background: linear-gradient(to bottom, #D92332, rgba(217, 35, 50, 0.7));
            "></div>
            <div style="
                background: rgba(217, 35, 50, 0.08);
                color: #D92332;
                font-size: 0.7rem;
                font-weight: 600;
                padding: 0.15rem 0.4rem;
                border-radius: 4px;
                margin-right: 0.6rem;
                letter-spacing: 0.03em;
            ">{price_badge}</div>
            <span style="
                color: #475569;
                font-size: 0.8rem;
                font-weight: 400;
                letter-spacing: 0.01em;
            ">Tous les prix sont affichés en {price_mode} • Objectif de marge : <span style="font-weight: 600; color: #10b981;">{seuil_marge_perso}%</span></span>
        </div>
        """, unsafe_allow_html=True)
        
        # CSS pour la grille responsive des cards
        st.markdown("""
        <style>
        .plat-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }
        
        @media (max-width: 768px) {
            .plat-grid-container {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
        }
        
        .empty-state {
            background: white;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
            padding: 2.5rem 1.5rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
            animation: fadeInUp 0.5s ease-out forwards;
            grid-column: 1 / -1;
        }
        
        .empty-state-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            opacity: 0.8;
        }
        
        .empty-state h3 {
            font-size: 1.1rem;
            font-weight: 600;
            color: #334155;
            margin-bottom: 0.5rem;
        }
        
        .empty-state p {
            color: #64748b;
            font-size: 0.9rem;
            max-width: 300px;
            margin: 0 auto;
            line-height: 1.5;
        }
        
        .streamlit-button-container {
            margin-top: 0.5rem;
            padding: 0.5rem;
            background-color: white;
            border-radius: 0 0 10px 10px;
        }
        
        /* Style pour les boutons Streamlit dans les cards */
        .streamlit-button-container [data-testid="stHorizontalBlock"] {
            gap: 0.5rem;
        }
        
        .streamlit-button-container [data-testid="baseButton-primary"],
        .streamlit-button-container [data-testid="baseButton-secondary"] {
            border-radius: 6px;
            font-size: 0.75rem !important;
            min-height: 2rem !important;
            height: auto !important;
            font-weight: 500;
            padding: 0.4rem 0.5rem !important;
            transition: all 0.15s ease;
        }
        
        .streamlit-button-container [data-testid="baseButton-primary"] {
            background-color: #D92332 !important;
            border-color: #D92332 !important;
        }
        
        .streamlit-button-container [data-testid="baseButton-primary"]:hover {
            background-color: #C02130 !important;
            box-shadow: 0 2px 5px rgba(217, 35, 50, 0.2) !important;
            transform: translateY(-1px);
        }
        
        .streamlit-button-container [data-testid="baseButton-secondary"] {
            background-color: #f8fafc !important;
            border-color: #e2e8f0 !important;
            color: #64748b !important;
        }
        
        .streamlit-button-container [data-testid="baseButton-secondary"]:hover {
            background-color: #f1f5f9 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05) !important;
            transform: translateY(-1px);
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Début du conteneur de grille
        st.markdown('<div class="plat-grid-container">', unsafe_allow_html=True)
        
        if not st.session_state.brouillons:
            # État vide
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🍽️</div>
                <h3>Aucun plat personnalisé</h3>
                <p>Commencez par créer votre premier plat personnalisé pour optimiser votre menu</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Liste des plats
            nb_plats = len(st.session_state.brouillons)
            
            for i, plat in enumerate(st.session_state.brouillons):
                # Calculs pour la carte
                ingr = pd.DataFrame(plat["composition"])
                if "Coût (€)" not in ingr.columns:
                    ingr["Coût (€)"] = (ingr["prix_kg"] * ingr["quantite_g"]) / 1000
                
                cout_matiere = ingr["Coût (€)"].sum()
                prix = plat.get('prix_affiche', 0)
                prix_affiche = prix / (1 + taux_tva) if affichage_ht_edit and not plat.get("affichage_ht", False) else prix
                marge = prix_affiche - cout_matiere
                taux_marge = (marge / prix_affiche * 100) if prix_affiche > 0 else 0

                # Statut
                if taux_marge >= seuil_marge_perso:
                    status_class = "excellent"
                    status_text = "Excellent"
                    status_icon = "✓"
                    bg_status = "rgba(16, 185, 129, 0.1)"
                    color_status = "rgb(16, 122, 68)"
                    badge_bg = "#ecfdf5"
                    badge_color = "#065f46"
                elif taux_marge >= seuil_marge_perso - 10:
                    status_class = "good" 
                    status_text = "Correct"
                    status_icon = "⚖️"
                    bg_status = "rgba(245, 158, 11, 0.1)"
                    color_status = "rgb(146, 94, 6)"
                    badge_bg = "#fffbeb"
                    badge_color = "#92400e"
                else:
                    status_class = "poor"
                    status_text = "À optimiser"
                    status_icon = "⚠️"
                    bg_status = "rgba(244, 63, 94, 0.1)"
                    color_status = "rgb(159, 18, 57)"
                    badge_bg = "#fef2f2"
                    badge_color = "#b91c1c"

                # HTML de la card
                card_structure = f"""
                <div class="plat-card animate-fade-in" data-plat-id="{i}">
                    <div class="card-accent {status_class}"></div>
                    <div class="card-content">
                        <div class="card-header">
                            <div class="card-title-container">
                                <h3 class="card-title">{plat['nom']}</h3>
                                <div class="card-subtitle">{plat['base']}</div>
                            </div>
                            <div class="card-badges">
                                <div class="marge-badge" style="background: {badge_bg}; color: {badge_color};">{taux_marge:.0f}%</div>
                                <div class="status-badge" style="background: {bg_status}; color: {color_status};">{status_icon} {status_text}</div>
                            </div>
                        </div>
                        <div class="card-metrics">
                            <div class="metric">
                                <div class="metric-value">{prix_affiche:.2f} €</div>
                                <div class="metric-label">Prix <span class="price-badge">{price_badge}</span></div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">{cout_matiere:.2f} €</div>
                                <div class="metric-label">Coût matière</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value" style="color: {color_status};">{marge:.2f} €</div>
                                <div class="metric-label">Marge brute</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">{len(ingr)}</div>
                                <div class="metric-label">Ingrédients</div>
                            </div>
                        </div>
                    </div>
                </div>
                """
                
                # CSS pour les cards
                card_css = f"""
                <style>
                .plat-card {{
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
                    overflow: hidden;
                    position: relative;
                    display: flex;
                    border: 1px solid #e5e7eb;
                    height: 100%;
                    animation: fadeIn 0.4s ease-out forwards;
                    animation-delay: calc({i} * 0.05s);
                    opacity: 0;
                }}

                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                
                .card-accent {{
                    width: 5px;
                    flex-shrink: 0;
                }}
                
                .card-accent.excellent {{ background: linear-gradient(to bottom, #10b981, #059669); }}
                .card-accent.good {{ background: linear-gradient(to bottom, #f59e0b, #d97706); }}
                .card-accent.poor {{ background: linear-gradient(to bottom, #f43f5e, #e11d48); }}
                
                .card-content {{
                    flex: 1;
                    padding: 1.25rem;
                    display: flex;
                    flex-direction: column;
                }}
                
                .card-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-bottom: 1rem;
                }}
                
                .card-title-container {{
                    flex: 1;
                }}
                
                .card-title {{
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: #1e293b;
                    margin: 0 0 0.3rem 0;
                    line-height: 1.3;
                }}
                
                .card-subtitle {{
                    font-size: 0.8rem;
                    color: #64748b;
                    line-height: 1.4;
                }}
                
                .card-badges {{
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                    align-items: flex-end;
                }}
                
                .marge-badge {{
                    font-size: 0.7rem;
                    font-weight: 600;
                    padding: 0.15rem 0.4rem;
                    border-radius: 12px;
                    letter-spacing: 0.03em;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .status-badge {{
                    font-size: 0.7rem;
                    font-weight: 500;
                    padding: 0.2rem 0.5rem;
                    border-radius: 4px;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.3rem;
                    white-space: nowrap;
                }}
                
                .card-metrics {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 1rem;
                    padding: 1rem;
                    background: #f8fafc;
                    border-radius: 8px;
                    margin-bottom: 0;
                    border: 1px solid #f1f5f9;
                }}
                
                @media (min-width: 640px) {{
                    .card-metrics {{
                        grid-template-columns: repeat(4, 1fr);
                        gap: 0.75rem;
                    }}
                }}
                
                .metric {{
                    text-align: center;
                }}
                
                .metric-value {{
                    font-size: 1rem;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 0.2rem;
                    line-height: 1.2;
                }}
                
                .metric-label {{
                    font-size: 0.7rem;
                    color: #64748b;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.3rem;
                }}
                
                .price-badge {{
                    background: rgba(100, 116, 139, 0.1);
                    color: #64748b;
                    font-size: 0.65rem;
                    font-weight: 600;
                    padding: 0.05rem 0.25rem;
                    border-radius: 3px;
                }}
                
                /* Style personnalisé pour les boutons Streamlit */
                [data-testid="stHorizontalBlock"] {{
                    gap: 0.5rem;
                    margin-top: 0.5rem;
                }}
                
                [data-testid="baseButton-primary"] {{
                    background-color: #D92332 !important;
                    border-color: #D92332 !important;
                    font-size: 0.8rem !important;
                    padding: 0.4rem 0.5rem !important;
                    transition: all 0.15s ease !important;
                }}
                
                [data-testid="baseButton-primary"]:hover {{
                    background-color: #C02130 !important;
                    border-color: #C02130 !important;
                    transform: translateY(-1px) !important;
                    box-shadow: 0 2px 5px rgba(217, 35, 50, 0.2) !important;
                }}
                
                [data-testid="baseButton-secondary"] {{
                    font-size: 0.8rem !important;
                    padding: 0.4rem 0.5rem !important;
                    border-color: #e2e8f0 !important;
                    color: #64748b !important;
                    transition: all 0.15s ease !important;
                }}
                
                [data-testid="baseButton-secondary"]:hover {{
                    background-color: #f1f5f9 !important;
                    transform: translateY(-1px) !important;
                }}
                </style>
                """
                
                # Affichage du CSS et du HTML
                st.markdown(card_css, unsafe_allow_html=True)
                st.markdown(card_structure, unsafe_allow_html=True)

                # Conteneur pour les boutons d'action Streamlit - visible et intégré à la card
                st.markdown('<div class="streamlit-button-container">', unsafe_allow_html=True)
                
                # Boutons d'action Streamlit
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Modifier", key=f"edit_{i}", help="Modifier ce plat", use_container_width=True, type="primary"):
                        plat_modifie = plat.copy()
                        plat_modifie["nom_original"] = plat["nom"]
                        st.session_state.plat_actif = plat_modifie
                        st.session_state.edit_view = "edition"
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Supprimer", key=f"delete_{i}", help="Supprimer ce plat", use_container_width=True):
                        st.session_state.brouillons = [b for b in st.session_state.brouillons if b["nom"] != plat["nom"]]
                        save_drafts(st.session_state.brouillons)
                        st.success(f"✅ '{plat['nom']}' supprimé avec succès")
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Fermeture du conteneur de grille
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.edit_view == "creation":
        # === VUE CRÉATION D'UN PLAT ===
        # === VUE CRÉATION D'UN PLAT ===
        st.markdown("""
        <div class="form-modern animate-slide-up" style="padding: 1rem; margin-bottom: 1rem;">
            <div class="form-section-modern" style="margin-bottom: 0.75rem;">
                <h3 style="font-size: 1rem; padding-bottom: 0.5rem; margin-bottom: 0.5rem;">
                    <div class="form-section-icon" style="width: 24px; height: 24px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 6v12M6 12h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    Choix de la base
                </h3>
                <p style="color: var(--neutral-500); margin-bottom: 0.75rem; font-size: 0.85rem;">Sélectionnez un plat existant comme base pour votre création</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            categories = ["Tout"] + sorted(list(recettes["categorie"].unique()))
            categorie_filtre = st.selectbox("🏷️ Catégorie", categories, key="cat_creation")

        with col2:
            if categorie_filtre == "Tout":
                plats_filtres = sorted(recettes["plat"].unique())
            else:
                plats_filtres = sorted(recettes[recettes["categorie"] == categorie_filtre]["plat"].unique())
            plat_selectionne = st.selectbox("🍽️ Plat de base", plats_filtres, key="base_creation")

        # Configuration du plat
        st.markdown("""
        <div class="form-section-modern">
            <h3>
                <div class="form-section-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                Configuration du plat
            </h3>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            nom_plat = st.text_input("📝 Nom du plat", value=f"{plat_selectionne} personnalisé", key="nom_plat")
        
        # Traitement des ingrédients
        filtered_ingredients = ingredients[ingredients['plat'].str.lower() == plat_selectionne.lower()].copy()
        
        if filtered_ingredients.empty:
            st.error(f"❌ Aucun ingrédient trouvé pour {plat_selectionne}")
            st.stop()

        ingr_base = calculer_cout(filtered_ingredients.copy())
        
        # Traitement spécial panini
        # Traitement spécial pour Panini Pizz
        if plat_selectionne.lower() == "panini pizz":
            # Configuration du panini - Version sobre
            st.markdown("""
            <div style="
                margin-bottom: 1rem;
                padding: 0.6rem 0.8rem;
                border: 1px solid #e5e7eb;
                border-left: 3px solid #D92332;
                border-radius: 6px;
                background-color: #fafafa;
            ">
                <div style="font-weight: 600; color: #334155; font-size: 0.95rem; margin-bottom: 0.5rem;">
                    Configuration du panini
                </div>
            """, unsafe_allow_html=True)
            
            # Mode simple vs avancé
            mode_avance = st.checkbox("Personnaliser les ingrédients", key="mode_avance", 
                                      help="Activez cette option pour personnaliser votre panini")
            
            if mode_avance:
                # Mode avancé: choix des composants de manière plus sobre
                # Choix de la base (crème ou sauce tomate)
                base_selection = st.radio(
                    "Base",
                    ["Crème", "Sauce Tomate"],
                    horizontal=True,
                    key="base_panini"
                )
                # Convertir la sélection pour correspondre à la base de données
                base_key = "crème" if base_selection == "Crème" else "sauce tomate"
                
                # Ingrédients de base pour un panini
                composition = []
                
                # Ajouter la base sélectionnée
                base_matches = filtered_ingredients[filtered_ingredients["ingredient"].str.lower() == base_key]
                if not base_matches.empty:
                    composition.append(base_matches.iloc[0])
                
                # Calcul des ingrédients additionnels
                additional = filtered_ingredients[~filtered_ingredients["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
                if not additional.empty and "Coût (€)" not in additional.columns:
                    additional = calculer_cout(additional)
                
                # Préparation des options d'ingrédients
                if not additional.empty:
                    additional_clean = additional.drop_duplicates(subset=["ingredient"])
                    all_ingrs = sorted(list(additional_clean["ingredient"].unique()))
                    
                    # Sélection des ingrédients côte à côte
                    col1, col2 = st.columns(2)
                    with col1:
                        slot1 = st.selectbox("Ingrédient #1", ["Aucun"] + all_ingrs, key="slot1")
                    with col2:
                        slot2 = st.selectbox("Ingrédient #2", ["Aucun"] + all_ingrs, key="slot2")
                    
                    # Ingrédients supplémentaires selon sélection
                    for i, slot in enumerate([slot1, slot2]):
                        if slot != "Aucun":
                            slot_matches = additional[additional["ingredient"] == slot]
                            if not slot_matches.empty:
                                # Créer une copie de la série pour éviter les références partagées
                                ingr_row = slot_matches.iloc[0].copy()
                                # Ajouter un suffixe unique pour différencier les ingrédients identiques
                                if slot in [ing.get("ingredient") for ing in composition]:
                                    ingr_row["ingredient_id"] = f"{slot}_{i+1}"
                                composition.append(ingr_row)
                else:
                    # En cas d'absence d'ingrédients additionnels
                    st.warning("Aucun ingrédient supplémentaire disponible pour ce panini")
                    # Valeurs par défaut pour la moyenne
                    avg_qty = 30
                    avg_price = 8.0
                    avg_cost = 0.24
                    
                    # Ajouter deux ingrédients "moyens" avec des valeurs calculées correctement
                    for _ in range(2):
                        composition.append(pd.Series({
                            "ingredient": "Moyenne suppl",
                            "quantite_g": avg_qty,
                            "prix_kg": avg_price,
                            "Coût (€)": avg_cost
                        }))
            else:
                # Mode simple: configuration automatique - message plus sobre
                st.caption("Configuration standard avec sauce tomate et ingrédients moyens")
                
                # Ingrédients de base pour un panini
                composition = []
                
                # Base par défaut (sauce tomate)
                base_key = "sauce tomate"
                base_matches = filtered_ingredients[filtered_ingredients["ingredient"].str.lower() == base_key]
                if not base_matches.empty:
                    composition.append(base_matches.iloc[0])
                
                # Calcul des ingrédients additionnels
                additional = filtered_ingredients[~filtered_ingredients["ingredient"].str.lower().isin(["crème", "sauce tomate"])]
                # S'assurer que la colonne "Coût (€)" existe dans additional
                if not additional.empty and "Coût (€)" not in additional.columns:
                    additional = calculer_cout(additional)
                
                # Calcul des moyennes pour les ingrédients supplémentaires
                if not additional.empty:
                    avg_qty = additional["quantite_g"].mean()
                    avg_price = additional["prix_kg"].mean() 
                    avg_cost = additional["Coût (€)"].mean()
                else:
                    avg_qty = 30  # Valeur par défaut raisonnable
                    avg_price = 8.0  # Valeur par défaut raisonnable
                    avg_cost = 0.24  # Valeur par défaut raisonnable (environ 30g à 8€/kg)
                
                # Ajouter deux ingrédients "moyens" avec des valeurs calculées correctement
                for _ in range(2):
                    composition.append(pd.Series({
                        "ingredient": "Moyenne suppl",
                        "quantite_g": avg_qty,
                        "prix_kg": avg_price,
                        "Coût (€)": avg_cost
                    }))
            
            # Fermer le div principal
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            # Ajout mozzarella et pâte (commun aux deux modes)
            composition.extend([
                pd.Series({"ingredient": "Mozzarella", "quantite_g": 40, "prix_kg": 5.85, "Coût (€)": 0.234}),
                pd.Series({"ingredient": "Pâte à panini", "quantite_g": 0, "prix_kg": 0, "Coût (€)": 0.12})
            ])
            
            ingr_base = pd.DataFrame(composition)
            
            # Gestion des ingrédients identiques: conserver l'ingrédient original pour l'affichage
            if 'ingredient_id' in ingr_base.columns:
                ingr_base['ingredient_original'] = ingr_base['ingredient']
                ingr_base.loc[ingr_base['ingredient_id'].notna(), 'ingredient'] = ingr_base.loc[ingr_base['ingredient_id'].notna(), 'ingredient_id']
            
            # S'assurer que le DataFrame a bien la colonne "Coût (€)"
            ingr_base = calculer_cout(ingr_base)

        # Ajout pâte pour pizzas
        elif any(s in plat_selectionne.lower() for s in ["pizza", " s", " m"]):
            pate_cost = get_dough_cost(plat_selectionne)
            if pate_cost > 0:
                pate_row = pd.DataFrame([{
                    "ingredient": "Pâte à pizza",
                    "quantite_g": 0,
                    "prix_kg": 0,
                    "Coût (€)": pate_cost
                }])
                ingr_base = pd.concat([ingr_base, pate_row], ignore_index=True)

        cout_initial = ingr_base["Coût (€)"].sum()
        
        # Prix suggéré
        prix_conseille = cout_initial / (1 - seuil_marge_perso/100) if seuil_marge_perso < 100 else None
        prix_base = prix_vente_dict.get(plat_selectionne, prix_conseille or 10.0)
        prix_base_affiche = prix_base / (1 + taux_tva) if affichage_ht_edit else prix_base

        with col2:
            prix_nouveau = st.number_input(
                f"💰 Prix de vente ({'HT' if affichage_ht_edit else 'TTC'})",
                min_value=1.0,
                value=prix_base_affiche,
                step=0.5,
                key="prix_nouveau",
                help=f"Prix recommandé : {prix_conseille:.2f}€ pour {seuil_marge_perso}% de marge" if prix_conseille else ""
            )

        # Aperçu financier
        marge_estimee = prix_nouveau - cout_initial
        taux_estime = (marge_estimee / prix_nouveau * 100) if prix_nouveau > 0 else 0

        # Statut coloré pour la prévisualisation
        if taux_estime >= seuil_marge_perso:
            preview_status = "excellent"
            preview_color = "#22c55e"
        elif taux_estime >= seuil_marge_perso - 10:
            preview_status = "good" 
            preview_color = "#f59e0b"
        else:
            preview_status = "poor"
            preview_color = "#ef4444"

        st.markdown("""
        <div class="form-section-modern">
            <h3>
                <div class="form-section-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                Aperçu financier
            </h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="preview-metrics-modern">
            <div class="preview-metric">
                <div class="preview-metric-value">{cout_initial:.2f} €</div>
                <div class="preview-metric-label">Coût matière</div>
            </div>
            <div class="preview-metric">
                <div class="preview-metric-value" style="color: {preview_color};">{marge_estimee:.2f} €</div>
                <div class="preview-metric-label">Marge brute</div>
            </div>
            <div class="preview-metric">
                <div class="preview-metric-value" style="color: {preview_color};">{taux_estime:.0f}%</div>
                <div class="preview-metric-label">Taux de marge</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Composition détaillée
        with st.expander("📋 Voir la composition détaillée", expanded=False):
            # Préparer le DataFrame pour l'affichage
            display_df = ingr_base.copy()
            
            # Si nous avons des noms d'ingrédients modifiés pour la gestion des doublons,
            # restaurer le nom original pour l'affichage tout en gardant la valeur unique pour les calculs
            if 'ingredient_original' in display_df.columns:
                display_df['ingredient'] = display_df['ingredient_original']
                display_df = display_df.drop(columns=['ingredient_original', 'ingredient_id'], errors='ignore')
            
            # Afficher le DataFrame avec les colonnes voulues
            st.dataframe(
                display_df[["ingredient", "quantite_g", "prix_kg", "Coût (€)"]],
                use_container_width=True,
                hide_index=True
            )

        # Actions
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        
        if col1.button("❌ Annuler", use_container_width=True, key="cancel_creation"):
            st.session_state.edit_view = "liste"
            st.rerun()
        
        if col2.button("🚀 Créer et personnaliser", use_container_width=True, type="primary", key="create_dish"):
            # Validation du nom
            if any(plat["nom"] == nom_plat for plat in st.session_state.brouillons):
                st.error(f"❌ Un plat nommé '{nom_plat}' existe déjà. Choisissez un autre nom.")
            else:
                st.session_state.plat_actif = {
                    "nom": nom_plat,
                    "base": plat_selectionne,
                    "composition": ingr_base.to_dict(orient="records"),
                    "prix_affiche": prix_nouveau,
                    "affichage_ht": affichage_ht_edit,
                    "nom_original": None  # Marquer comme nouveau plat
                }
                st.session_state.edit_view = "edition"
                st.rerun()

    else:
        # === VUE ÉDITION D'UN PLAT ===
        plat_data = st.session_state.plat_actif
        
        # Stocker une copie de l'état initial du plat si ce n'est pas déjà fait
        if "plat_initial" not in st.session_state:
            st.session_state.plat_initial = copy.deepcopy(plat_data)

        # Traitement des données
        try:
            ingr_modifie = pd.DataFrame(plat_data["composition"])
            if "Coût (€)" not in ingr_modifie.columns:
                ingr_modifie["Coût (€)"] = (ingr_modifie["prix_kg"] * ingr_modifie["quantite_g"]) / 1000
            ingr_modifie = calculer_cout(ingr_modifie)
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement : {e}")
            if st.button("🔄 Retour à la liste"):
                st.session_state.edit_view = "liste"
                st.session_state.plat_actif = None
                st.rerun()
            st.stop()

        # Gestion HT/TTC
        ancien_affichage_ht = plat_data.get("affichage_ht", False)
        prix_affiche = plat_data.get("prix_affiche", 10.0)
        if affichage_ht_edit != ancien_affichage_ht:
            prix_affiche = prix_affiche / (1 + taux_tva) if affichage_ht_edit else prix_affiche * (1 + taux_tva)
            plat_data["affichage_ht"] = affichage_ht_edit
            plat_data["prix_affiche"] = prix_affiche
            st.session_state.plat_actif = plat_data
            st.rerun()

        # Métriques
        cout_matiere = ingr_modifie["Coût (€)"].sum()
        marge_brute = prix_affiche - cout_matiere
        taux_marge = (marge_brute / prix_affiche * 100) if prix_affiche > 0 else 0

        # Statut
        if taux_marge >= seuil_marge_perso:
            status_class = "excellent"
            status_text = "Excellente rentabilité"
            status_icon = "🟢"
            status_color = "#22c55e"
        elif taux_marge >= seuil_marge_perso - 10:
            status_class = "good"
            status_text = "Rentabilité correcte"
            status_icon = "🟠"
            status_color = "#f59e0b"
        else:
            status_class = "poor"
            status_text = "À optimiser"
            status_icon = "🔴"
            status_color = "#ef4444"

        # Interface d'édition simplifiée
        # Style pour l'interface d'édition sans le titre principal
        st.markdown("""
        <style>
            /* Style pour les étiquettes de champ */
            [data-testid="stTextInput"] label, [data-testid="stNumberInput"] label {
                font-weight: 600 !important;
                color: #334155 !important;
                font-size: 0.95rem !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Style pour les champs numériques */
            [data-testid="stNumberInput"] > div > div > input {
                border-radius: 5px !important;
                border: 1px solid #e2e8f0 !important;
                padding: 0.75rem 1rem !important;
                font-size: 0.95rem !important;
                transition: all 0.2s ease !important;
            }
            
            [data-testid="stNumberInput"] > div > div > input:focus {
                border-color: #D92332 !important;
                box-shadow: 0 0 0 3px rgba(217, 35, 50, 0.1) !important;
                transform: translateY(-1px);
            }
            
            /* Style pour les boutons primaires */
            button[data-testid="baseButton-primary"] {
                background-color: #D92332 !important;
                border-color: #D92332 !important;
                transition: all 0.2s ease !important;
            }
            
            button[data-testid="baseButton-primary"]:hover {
                background-color: #C02130 !important;
                border-color: #C02130 !important;
                transform: translateY(-1px);
                box-shadow: 0 2px 5px rgba(217, 35, 50, 0.2) !important;
            }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        /* Style simplifié pour l'interface d'édition */
        .edit-header {
            background-color: #fff;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Style pour les champs de saisie */
        input[type="text"], input[type="number"] {
            font-size: 1rem !important;
            border-radius: 6px !important;
            border: 1px solid #e2e8f0 !important;
            padding: 10px 12px !important;
            transition: all 0.2s ease;
        }
        
        input[type="text"]:focus, input[type="number"]:focus {
            border-color: #D92332 !important;
            box-shadow: 0 0 0 3px rgba(217, 35, 50, 0.1) !important;
            transform: translateY(-1px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        
        # Champs principaux côte à côte
        col1, col2 = st.columns(2)
        
        with col1:
            nouveau_nom = st.text_input("Nom du plat", value=plat_data["nom"], key="edit_nom")
            # Mise à jour du nom dans la session state (sans sauvegarde automatique)
            if nouveau_nom != plat_data["nom"]:
                plat_data["nom"] = nouveau_nom
                st.session_state.plat_actif = plat_data
        
        with col2:
            prix_affiche = st.number_input(
                f"Prix de vente ({'HT' if affichage_ht_edit else 'TTC'})",
                min_value=1.0,
                value=prix_affiche,
                step=0.5,
                key="edit_prix"
            )
            # Mise à jour du prix dans la session state (sans sauvegarde automatique)
            if prix_affiche != plat_data.get("prix_affiche", 0):
                plat_data["prix_affiche"] = prix_affiche
                st.session_state.plat_actif = plat_data

        # Interface épurée - mise en page à deux colonnes
        
        # Onglets pour la navigation entre les différentes fonctionnalités
        edit_tab, optim_tab = st.tabs(["📋 Édition des ingrédients", "⚡ Optimisation"])
        
        # Tab 1: Édition des ingrédients
        with edit_tab:            # Réorganisation : deux colonnes principales (gauche: ingrédients, droite: métriques)
            # Répartition optimisée pour le tableau à gauche et les métriques à droite
            tab_col1, tab_col2 = st.columns([2, 1])
            
            with tab_col1:
                # Style moderne et compact pour le tableau des ingrédients - harmonisé avec les métriques
                st.markdown("""
                <style>
                    .ingredient-table {
                        background-color: white;
                        border-radius: 5px;
                        border: 1px solid #e2e8f0;
                        margin-bottom: 0.7rem;
                        padding: 0.5rem 0.5rem 0.4rem 0.5rem;
                        font-size: 0.85rem;
                        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
                    }
                    .ingredient-header {
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                        background-color: #f8fafc;
                        padding: 0.4rem 0.5rem;
                        border-radius: 4px;
                        margin-bottom: 0.4rem;
                        font-weight: 600;
                        font-size: 0.75rem;
                        color: #1e293b;
                        border-bottom: 1px solid #f1f5f9;
                    }
                    .ingredient-header::before {
                        content: "";
                        width: 3px;
                        height: 16px;
                        background-color: #D92332;
                        border-radius: 1px;
                        margin-right: 0.4rem;
                    }
                    .ingredient-row {
                        display: flex;
                        flex-direction: row;
                        align-items: center;
                        padding: 0.4rem 0.5rem;
                        border-bottom: 1px solid #f1f5f9;
                        margin-bottom: 0.15rem;
                        font-size: 0.8rem;
                        border-radius: 3px;
                        transition: background-color 0.15s ease;
                    }
                    .ingredient-row:hover {
                        background-color: #f8fafc;
                    }
                    .ingredient-row:last-child {
                        border-bottom: none;
                        margin-bottom: 0;
                    }
                    .ingredient-name {
                        flex: 1.5;
                        font-weight: 500;
                        font-size: 0.85rem;
                        color: #334155;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        padding-left: 0.1rem;
                    }
                    .ingredient-quantity {
                        flex: 0.6;
                        text-align: center;
                    }
                    .ingredient-cost {
                        flex: 0.6;
                        text-align: right;
                        font-weight: 500;
                        font-size: 0.85rem;
                        padding-right: 0.1rem;
                    }
                    .ingredient-action {
                        flex: 0.4;
                        text-align: center;
                    }
                    .ingredient-header-item {
                        padding: 0 0.1rem;
                    }
                    /* Style compact pour les champs numériques */
                    [data-testid="stNumberInput"] > div {
                        width: 100% !important;
                    }
                    [data-testid="stNumberInput"] > div > div > input {
                        padding: 0.3rem 0.4rem !important;
                        font-size: 0.8rem !important;
                        border: 1px solid #e2e8f0 !important;
                        border-radius: 4px !important;
                        transition: border-color 0.15s ease, box-shadow 0.15s ease;
                        width: 100% !important;
                        text-align: center !important;
                    }
                    [data-testid="stNumberInput"] > div > div > input:focus {
                        border-color: #D92332 !important;
                        box-shadow: 0 0 0 1px rgba(217, 35, 50, 0.1) !important;
                    }
                    /* Réduire l'espace autour des boutons */
                    button[data-testid="baseButton-secondary"] {
                        padding: 0.2rem 0.3rem !important;
                        min-height: unset !important;
                        height: auto !important;
                        font-size: 0.8rem !important;
                        border-radius: 4px !important;
                        transition: background-color 0.15s ease, transform 0.1s ease;
                        width: 100% !important;
                    }
                    button[data-testid="baseButton-secondary"]:hover {
                        transform: translateY(-1px);
                    }
                    /* Réduire l'espace autour des selectbox */
                    [data-testid="stSelectbox"] {
                        min-height: unset !important;
                        line-height: 1.2 !important;
                    }
                    [data-testid="stSelectbox"] > div {
                        line-height: 1.2 !important;
                    }
                </style>
                <div class="ingredient-table">
                    <div class="ingredient-header">
                        <div class="ingredient-header-item" style="flex: 1.5;">Ingrédients</div>
                        <div class="ingredient-header-item" style="flex: 0.6; text-align: center;">Qté (g)</div>
                        <div class="ingredient-header-item" style="flex: 0.6; text-align: right;">Coût</div>
                        <div class="ingredient-header-item" style="flex: 0.4; text-align: center;">Action</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Variables pour stocker les modifications
                ingredients_to_delete = []
                quantity_updates = {}

                for i, (idx, row) in enumerate(ingr_modifie.iterrows()):
                    # Afficher une ligne d'ingrédient avec style amélioré
                    ing_name = row['ingredient']
                    cout = row['Coût (€)']
                    cout_color = "#22c55e" if cout < 1.0 else "#f59e0b" if cout < 2.0 else "#ef4444"
                    
                    # Configuration des colonnes pour le tableau
                    ing_col, qty_col, cost_col, action_col = st.columns([1.5, 0.6, 0.6, 0.4])
                    
                    with ing_col:
                        st.markdown(f"""<div class="ingredient-name">{ing_name}</div>""", unsafe_allow_html=True)
                    
                    with qty_col:
                        new_qty = st.number_input(
                            "",
                            min_value=0.0,
                            value=float(row["quantite_g"]),
                            step=5.0,
                            key=f"qty_edit_{i}_{idx}",
                            label_visibility="collapsed",
                            format="%.0f"
                        )
                    
                    with cost_col:
                        # Affichage du coût avec style harmonisé et élégant
                        st.markdown(f"""<div class="ingredient-cost" style="color: {cout_color};">{cout:.2f}€</div>""", unsafe_allow_html=True)
                    
                    with action_col:
                        # Bouton supprimer avec style amélioré et élégant
                        if st.button("🗑️", key=f"del_edit_{i}_{idx}", help="Supprimer cet ingrédient", use_container_width=True):
                            ingredients_to_delete.append(idx)
                    
                    # Stocker les mises à jour de quantité
                    if new_qty != row["quantite_g"]:
                        quantity_updates[idx] = new_qty
                        # Mise à jour immédiate pour affichage
                        ingr_modifie.loc[idx, "quantite_g"] = new_qty
                        ingr_modifie.loc[idx, "Coût (€)"] = (new_qty * ingr_modifie.loc[idx, "prix_kg"]) / 1000

                # Appliquer les modifications
                if ingredients_to_delete or quantity_updates:
                    # Supprimer les ingrédients
                    for idx in ingredients_to_delete:
                        ingr_modifie = ingr_modifie.drop(idx)
                    
                    # Mettre à jour les quantités
                    for idx, new_qty in quantity_updates.items():
                        if idx in ingr_modifie.index:
                            ingr_modifie.loc[idx, "quantite_g"] = new_qty
                            ingr_modifie.loc[idx, "Coût (€)"] = (new_qty * ingr_modifie.loc[idx, "prix_kg"]) / 1000
                    
                    # Mettre à jour les modifications dans la session state (sans sauvegarde automatique)
                    st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
                    if ingredients_to_delete:
                        st.success(f"✅ {len(ingredients_to_delete)} ingrédient(s) supprimé(s)", icon="✅")
                    if quantity_updates:
                        st.success(f"✅ {len(quantity_updates)} quantité(s) mise(s) à jour", icon="✅")
                    st.rerun()
                
                # Fermeture du div pour le tableau
                st.markdown("</div>", unsafe_allow_html=True)

                # Ajout d'ingrédient avec style harmonisé avec le tableau et les métriques
                st.markdown("""
                <div class="form-section-modern" style="
                    padding: 0.5rem 0.6rem;
                    background-color: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 5px;
                    margin: 0.7rem 0 0.5rem 0;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
                ">
                    <div style="
                        display: flex; 
                        align-items: center; 
                        margin: 0 0 0.5rem 0; 
                        padding-bottom: 0.4rem;
                        border-bottom: 1px solid #f1f5f9;
                    ">
                        <div style="
                            width: 3px; 
                            height: 16px; 
                            background-color: #D92332; 
                            border-radius: 1px; 
                            margin-right: 0.4rem;
                        "></div>
                        <h3 style="
                            margin: 0; 
                            font-size: 0.85rem; 
                            font-weight: 600; 
                            color: #1e293b;
                        ">
                            Ajouter un ingrédient
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1.5, 0.6, 0.8])
                
                ingr_dispo = sorted([ing for ing in ingredients["ingredient"].unique() if ing not in ingr_modifie["ingredient"].values])
                
                if ingr_dispo:
                    nouvel_ing = col1.selectbox("Ingrédient", ingr_dispo, key="new_ing", 
                                               label_visibility="collapsed")
                    qty_nouvelle = col2.number_input("Quantité (g)", min_value=5.0, value=50.0, step=5.0, 
                                                    key="new_qty", label_visibility="collapsed")
                    
                    if col3.button("Ajouter", key="add_ing", type="primary", use_container_width=True):
                        data_ing = ingredients[ingredients["ingredient"] == nouvel_ing]
                        prix_kg = data_ing.iloc[0]["prix_kg"] if not data_ing.empty else 0.0
                        
                        new_row = pd.DataFrame([{
                            "ingredient": nouvel_ing,
                            "quantite_g": qty_nouvelle,
                            "prix_kg": prix_kg,
                            "Coût (€)": (qty_nouvelle * prix_kg) / 1000
                        }])
                        
                        ingr_modifie = pd.concat([ingr_modifie, new_row], ignore_index=True)
                        st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
                        st.success(f"✅ Ingrédient ajouté avec succès", icon="✅")
                        st.rerun()
                else:
                    st.info("Tous les ingrédients disponibles sont déjà ajoutés à ce plat.")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Fonction pour afficher les métriques en temps réel
            def afficher_metriques():
                cout_actuel = ingr_modifie["Coût (€)"].sum()
                marge_actuelle = prix_affiche - cout_actuel
                taux_marge_actuel = (marge_actuelle / prix_affiche * 100) if prix_affiche > 0 else 0
                margin_color = "#22c55e" if taux_marge_actuel >= seuil_marge_perso else "#f59e0b" if taux_marge_actuel >= seuil_marge_perso - 10 else "#ef4444"
                
                # En-tête des métriques - design sobre et minimaliste
                st.markdown("""
                <div style="background-color: white; border-radius: 6px; border: 1px solid #e2e8f0; padding: 0.6rem; margin-bottom: 0.7rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="display: flex; align-items: center; margin-bottom: 0.3rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.3rem;">
                        <div style="width: 3px; height: 16px; background-color: #D92332; border-radius: 1px; margin-right: 0.4rem;"></div>
                        <h3 style="margin: 0; font-size: 0.85rem; font-weight: 600; color: #1e293b;">
                            Métriques
                        </h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Métriques de coût et prix - design unifié et épuré
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 0.6rem;">
                    <div style="display: flex; align-items: center; padding: 0.5rem; background-color: white; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;">
                        <div style="margin-right: 0.5rem; width: 22px; text-align: center;">
                            <span style="color: #64748b; font-size: 0.85rem;">💰</span>
                        </div>
                        <div>
                            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.1rem; font-weight: 500;">Coût matière</div>
                            <div style="font-size: 1rem; font-weight: 600; color: #1e293b;">{cout_actuel:.2f} €</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background-color: white; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;">
                        <div style="margin-right: 0.5rem; width: 22px; text-align: center;">
                            <span style="color: #64748b; font-size: 0.85rem;">💵</span>
                        </div>
                        <div>
                            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.1rem; font-weight: 500;">Prix de vente</div>
                            <div style="font-size: 1rem; font-weight: 600; color: #1e293b;">{prix_affiche:.2f} €</div>
                        </div>
                    </div>
                </div>
                
                <!-- Métriques de marge - design avec indication visuelle par couleur -->
                <div style="display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 0.6rem;">
                    <div style="display: flex; align-items: center; padding: 0.5rem; background-color: white; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; border-left: 3px solid {margin_color};">
                        <div style="margin-right: 0.5rem; width: 22px; text-align: center;">
                            <span style="color: {margin_color}; font-size: 0.85rem;">📈</span>
                        </div>
                        <div style="flex-grow: 1;">
                            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.1rem; font-weight: 500;">Marge brute</div>
                            <div style="font-size: 1rem; font-weight: 600; color: {margin_color};">{marge_actuelle:.2f} €</div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; padding: 0.5rem; background-color: white; border-radius: 5px; box-shadow: 0 1px 2px rgba(0,0,0,0.03); border: 1px solid #e2e8f0; border-left: 3px solid {margin_color};">
                        <div style="margin-right: 0.5rem; width: 22px; text-align: center;">
                            <span style="color: {margin_color}; font-size: 0.85rem;">%</span>
                        </div>
                        <div style="flex-grow: 1;">
                            <div style="font-size: 0.7rem; color: #64748b; margin-bottom: 0.1rem; font-weight: 500;">Taux de marge</div>
                            <div style="font-size: 1rem; font-weight: 600; color: {margin_color};">{taux_marge_actuel:.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Barre de progression minimaliste et élégante
                progress_pct = min(taux_marge_actuel / seuil_marge_perso, 1.0)
                st.markdown(f"""
                <div style="background-color: white; border-radius: 5px; padding: 0.5rem; margin-bottom: 0.6rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem; font-size: 0.7rem; color: #64748b;">
                        <div style="font-weight: 500;">Progression</div>
                        <div>{taux_marge_actuel:.1f}% / {seuil_marge_perso}%</div>
                    </div>
                    <div style="height: 5px; width: 100%; background-color: #f1f5f9; border-radius: 3px; overflow: hidden;">
                        <div style="height: 100%; width: {progress_pct * 100}%; background-color: {margin_color}; border-radius: 3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Message de statut compact et informatif
                icon = "✅" if taux_marge_actuel >= seuil_marge_perso else "⚠️" if taux_marge_actuel >= seuil_marge_perso - 10 else "❌"
                color = "#22c55e" if taux_marge_actuel >= seuil_marge_perso else "#f59e0b" if taux_marge_actuel >= seuil_marge_perso - 10 else "#ef4444"
                status = "Objectif atteint" if taux_marge_actuel >= seuil_marge_perso else "Proche de l'objectif" if taux_marge_actuel >= seuil_marge_perso - 10 else "À optimiser"
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 0.4rem 0.5rem; border-radius: 4px; background-color: white; border: 1px solid #e2e8f0; border-left: 3px solid {color}; margin-bottom: 0.6rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="color: {color}; font-size: 0.85rem; margin-right: 0.4rem;">{icon}</div>
                    <div style="color: #1e293b; font-size: 0.75rem; font-weight: 500;">{status}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with tab_col2:
                # Métriques dans l'onglet Édition
                afficher_metriques()
        
        # Tab 2: Optimisation
        with optim_tab:
            # En-tête stylisé de l'optimisation
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f8fafc, #f0f9ff); border-radius: 10px; border: 1px solid #e2e8f0; padding: 1rem; margin-bottom: 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                <h3 style="margin-top: 0; margin-bottom: 0.5rem; font-size: 1.1rem; color: #1e293b; display: flex; align-items: center; gap: 0.5rem; letter-spacing: 0.01em; text-shadow: 0 1px 1px rgba(255,255,255,0.8);">
                    <span style="font-size: 1.2rem;">⚡</span> Optimiser les grammages
                </h3>
                <p style="margin: 0; font-size: 0.9rem; color: #64748b;">
                    Ajustez automatiquement les quantités pour optimiser la marge tout en respectant les proportions du plat.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Remplacer l'encadré par un expander Streamlit
            with st.expander("ℹ️ Comprendre la méthodologie d'optimisation"):
                st.markdown("""
                <h4 style="margin-top: 0.5rem; margin-bottom: 0.8rem; font-size: 1.05rem; color: #0369a1;">Comment fonctionne l'optimisation ?</h4>
                
                <p style="margin: 0 0 0.7rem 0; font-size: 0.9rem; color: #334155; line-height: 1.5;">
                    Notre algorithme utilise une approche <b>minimax équilibrée</b> qui répartit les ajustements de quantités de manière équitable entre les ingrédients :
                </p>
                
                <ul style="margin: 0 0 0.8rem 0; padding-left: 1.2rem; font-size: 0.9rem; color: #334155;">
                    <li style="margin-bottom: 0.4rem;">Les pâtes et bases sont préservées (coûts fixes)</li>
                    <li style="margin-bottom: 0.4rem;">Chaque ingrédient est réduit proportionnellement au minimum nécessaire</li>
                    <li style="margin-bottom: 0.4rem;">L'objectif est d'atteindre la marge cible de <b>{seuil_marge_perso}%</b> en minimisant l'impact sur la recette</li>
                    <li style="margin-bottom: 0.4rem;">Les proportions entre ingrédients sont respectées autant que possible</li>
                </ul>
                
                <div style="background-color: rgba(56, 189, 248, 0.1); border-left: 3px solid #0ea5e9; padding: 0.6rem; margin-top: 0.5rem; border-radius: 4px;">
                    <p style="margin: 0; font-size: 0.85rem; color: #0369a1; font-style: italic;">
                        <b>Note :</b> L'algorithme garantit un grammage minimum de 5g pour chaque ingrédient variable pour préserver le goût et l'intégrité de la recette.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Deux colonnes pour l'optimisation et les métriques
            optim_col1, optim_col2 = st.columns([3, 1])
            
            with optim_col1:
                # Section optimisation avec style amélioré
                if st.button("🚀 Analyser et optimiser les grammages", key="optimize", type="primary", use_container_width=True):
                    with st.spinner("Analyse en cours..."):
                        try:
                            df_opt = optimize_grammages_balanced(ingr_modifie, prix_affiche, seuil_marge_perso)
                            
                            suggestions = []
                            for _, row in ingr_modifie.iterrows():
                                ing = row["ingredient"]
                                old_q = row["quantite_g"]
                                matching = df_opt[df_opt["ingredient"] == ing]
                                new_q = float(matching["new_qty"].iloc[0]) if not matching.empty else old_q
                                if abs(new_q - old_q) > 1:  # Seulement si changement significatif
                                    suggestions.append((ing, old_q, new_q))
                            
                            if suggestions:
                                st.session_state.suggestions = suggestions
                                st.session_state.no_optimization_found = False
                                st.success(f"✅ {len(suggestions)} suggestion(s) d'optimisation trouvée(s)")
                            else:
                                st.session_state.no_optimization_found = True
                                st.session_state.suggestions = None
                                st.info("Aucune optimisation significative trouvée")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erreur d'optimisation : {e}")
                
                # Afficher les suggestions si disponibles
                if hasattr(st.session_state, 'suggestions') and st.session_state.suggestions:
                    st.markdown("""
                    <div style="background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; padding: 1rem; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <h3 style="margin-top: 0; margin-bottom: 0.75rem; font-size: 1.1rem; color: #334155; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span style="font-size: 1.1rem;">💡</span> Suggestions d'optimisation
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Tableau des suggestions avec style amélioré
                    data = []
                    for ing, old_q, new_q in st.session_state.suggestions:
                        diff = new_q - old_q
                        diff_pct = (diff / old_q * 100) if old_q > 0 else 0
                        data.append({
                            "Ingrédient": ing,
                            "Quantité actuelle (g)": f"{old_q:.1f}",
                            "Nouvelle quantité (g)": f"{new_q:.1f}",
                            "Variation": f"{diff_pct:+.1f}%"
                        })
                    
                    df = pd.DataFrame(data)
                    
                    # Style amélioré pour le dataframe
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Ingrédient": st.column_config.TextColumn(
                                "Ingrédient",
                                width="medium",
                                help="Nom de l'ingrédient"
                            ),
                            "Quantité actuelle (g)": st.column_config.NumberColumn(
                                "Quantité actuelle (g)",
                                format="%.1f g",
                                width="small"
                            ),
                            "Nouvelle quantité (g)": st.column_config.NumberColumn(
                                "Nouvelle quantité (g)",
                                format="%.1f g",
                                width="small"
                            ),
                            "Variation": st.column_config.TextColumn(
                                "Variation",
                                width="small"
                            )
                        }
                    )
                    
                    # Bouton d'application stylisé
                    st.markdown("""
                    <div style="margin: 1rem 0;">
                        <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.75rem;">
                            Appliquer ces suggestions permettra d'optimiser la marge tout en respectant les proportions du plat.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("✅ Appliquer toutes les suggestions", type="primary", use_container_width=True):
                        for ing, _, new_q in st.session_state.suggestions:
                            mask = ingr_modifie["ingredient"] == ing
                            if mask.any():
                                ingr_modifie.loc[mask, "quantite_g"] = new_q
                                ingr_modifie.loc[mask, "Coût (€)"] = (new_q * ingr_modifie.loc[mask, "prix_kg"]) / 1000
                        
                        st.session_state.plat_actif["composition"] = ingr_modifie.to_dict(orient="records")
                        st.session_state.suggestions = None
                        st.success("✅ Toutes les optimisations ont été appliquées!")
                        st.rerun()
                        
                elif hasattr(st.session_state, 'no_optimization_found') and st.session_state.no_optimization_found:
                    st.markdown("""
                    <div style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; padding: 1rem; margin: 1rem 0;">
                        <p style="margin: 0; display: flex; align-items: center; gap: 0.5rem; color: #64748b;">
                            <span style="font-size: 1.2rem;">🔍</span>
                            <span>Les grammages semblent déjà optimisés pour ce plat.</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with optim_col2:
                # Métriques dans l'onglet Optimisation
                afficher_metriques()
        # Finalisation avec style cohérent avec la charte
        st.markdown("---")
        st.markdown("""
        <div style="background-color: white; border-radius: 8px; border: 1px solid #e2e8f0; padding: 1rem; margin: 1.5rem 0 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h3 style="margin-top: 0; margin-bottom: 0.5rem; font-size: 1.1rem; color: #334155; display: flex; align-items: center; gap: 0.5rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.5rem;">
                <span style="font-size: 1.2rem;">✅</span> Finalisation
            </h3>
            <p style="margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #64748b;">
                Sauvegardez vos modifications ou revenez en arrière.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialisation des états de confirmation si nécessaire
        if "confirm_delete_dish" not in st.session_state:
            st.session_state.confirm_delete_dish = False
        if "confirm_reset_dish" not in st.session_state:
            st.session_state.confirm_reset_dish = False
        
        # Zone d'actions avec style moderne
        st.markdown("""
        <div style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; padding: 0.75rem; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 0.85rem; color: #64748b;">
                <span style="font-weight: 500;">Note:</span> Les modifications ne sont pas sauvegardées automatiquement. Utilisez le bouton ci-dessous pour enregistrer vos changements.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Boutons d'action stylisés
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        # Bouton Sauvegarder (mis en évidence)
        with col1:
            # Condition de sauvegarde
            save_button_disabled = "save_success_time" in st.session_state
            
            save_clicked = st.button(
                "💾 Sauvegarder les modifications", 
                use_container_width=True, 
                type="primary", 
                key="save_dish",
                disabled=save_button_disabled
            )
            
            # Affichage du message de succès juste sous le bouton
            if "save_success_time" in st.session_state:
                current_time = time.time()
                # Afficher le message pendant 3 secondes
                if current_time - st.session_state.save_success_time < 3:
                    # Message de succès stylisé
                    st.markdown("""
                    <div style="
                        background-color: rgba(34, 197, 94, 0.1);
                        border: 1px solid rgba(34, 197, 94, 0.3);
                        border-radius: 6px;
                        padding: 0.6rem 0.8rem;
                        margin: 0.5rem 0 0.5rem 0;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        animation: fadeInUp 0.3s ease-out;
                    ">
                        <div style="color: #22c55e; font-size: 1rem;">✅</div>
                        <div style="color: #166534; font-weight: 500; font-size: 0.85rem;">Plat sauvegardé avec succès !</div>
                    </div>
                    
                    <style>
                    @keyframes fadeInUp {
                        from { opacity: 0; transform: translateY(5px); }
                        to { opacity: 1; transform: translateY(0); }
                    }
                    </style>
                    """, unsafe_allow_html=True)
                else:
                    # Supprimer la variable après 3 secondes pour faire disparaître le message
                    del st.session_state.save_success_time
                    st.rerun()
            
            if save_clicked:
                try:
                    # Validation du nom
                    nom_original = st.session_state.plat_actif.get("nom_original", plat_data["nom"])
                    
                    # Vérifier si le nom existe déjà (sauf pour le plat actuel)
                    nom_existe = any(
                        plat["nom"] == nouveau_nom and plat["nom"] != nom_original 
                        for plat in st.session_state.brouillons
                    )
                    
                    if nom_existe:
                        st.error(f"Un plat nommé '{nouveau_nom}' existe déjà. Choisissez un autre nom.")
                    else:
                        # Mise à jour des données du plat
                        plat_data["nom"] = nouveau_nom
                        plat_data["prix_affiche"] = prix_affiche
                        plat_data["composition"] = ingr_modifie.to_dict(orient="records")
                        plat_data["affichage_ht"] = affichage_ht_edit
                        
                        # Trouver et remplacer le plat existant ou l'ajouter
                        plat_trouve = False
                        for i, plat in enumerate(st.session_state.brouillons):
                            if plat["nom"] == nom_original:
                                st.session_state.brouillons[i] = plat_data
                                plat_trouve = True
                                break
                        
                        if not plat_trouve:
                            st.session_state.brouillons.append(plat_data)
                        
                        # Sauvegarder dans le fichier
                        save_drafts(st.session_state.brouillons)
                        
                        # Créer une clé d'état pour le message de succès
                        st.session_state.save_success_time = time.time()
                        
                        # Mise à jour du nom_original pour les futures sauvegardes
                        plat_data["nom_original"] = plat_data["nom"]
                        st.session_state.plat_actif = plat_data
                        
                        # Rechargement de la page pour afficher le message
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Erreur lors de la sauvegarde : {str(e)}")
        
        # Bouton Réinitialiser
        with col2:
            if not st.session_state.confirm_reset_dish:
                if st.button("🔄 Réinitialiser le plat", use_container_width=True, key="reset_dish"):
                    st.session_state.confirm_reset_dish = True
                    st.rerun()
            else:
                st.warning("Toutes les modifications seront annulées et le plat sera restauré à son état initial. Continuer ?")
                
                col_cancel, col_confirm = st.columns(2)
                with col_cancel:
                    if st.button("Annuler", use_container_width=True, key="cancel_reset"):
                        st.session_state.confirm_reset_dish = False
                        st.rerun()
                with col_confirm:
                    if st.button("Confirmer", use_container_width=True, key="confirm_reset", type="secondary"):
                        # Réinitialiser aux valeurs d'origine stockées
                        if "plat_initial" in st.session_state:
                            # Restaurer directement à partir de la copie initiale
                            st.session_state.plat_actif = copy.deepcopy(st.session_state.plat_initial)
                        else:
                            # Fallback au cas où plat_initial n'existe pas
                            nom_original = st.session_state.plat_actif.get("nom_original")
                            if nom_original:
                                # Trouver le plat original dans les brouillons
                                for plat in st.session_state.brouillons:
                                    if plat["nom"] == nom_original:
                                        st.session_state.plat_actif = plat.copy()
                                        st.session_state.plat_actif["nom_original"] = nom_original
                                        break
                        
                        st.session_state.confirm_reset_dish = False
                        st.info("Modifications annulées - plat réinitialisé à son état initial")
                        st.rerun()
                        st.rerun()
        
        # Bouton Supprimer avec confirmation
        with col3:
            if not st.session_state.confirm_delete_dish:
                if st.button("🗑️ Supprimer", use_container_width=True, key="delete_dish"):
                    st.session_state.confirm_delete_dish = True
                    st.rerun()
            else:
                st.error("Confirmer la suppression ?")
                
                col_cancel, col_confirm = st.columns(2)
                with col_cancel:
                    if st.button("Annuler", use_container_width=True, key="cancel_delete"):
                        st.session_state.confirm_delete_dish = False
                        st.rerun()
                with col_confirm:
                    if st.button("Supprimer", use_container_width=True, key="confirm_delete", type="secondary"):
                        try:
                            nom_a_supprimer = st.session_state.plat_actif.get("nom_original", plat_data["nom"])
                            
                            # Supprimer le plat des brouillons
                            st.session_state.brouillons = [
                                b for b in st.session_state.brouillons 
                                if b["nom"] != nom_a_supprimer
                            ]
                            
                            # Sauvegarder la liste mise à jour
                            save_drafts(st.session_state.brouillons)
                            
                            # Réinitialiser les états
                            st.session_state.plat_actif = None
                            if "plat_initial" in st.session_state:
                                del st.session_state.plat_initial
                            st.session_state.edit_view = "liste"
                            st.session_state.confirm_delete_dish = False
                            
                            st.success(f"Plat '{nom_a_supprimer}' supprimé avec succès !")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Erreur lors de la suppression : {str(e)}")
        
        # Bouton Retour avec confirmation
        with col4:
            if "confirm_back" not in st.session_state:
                st.session_state.confirm_back = False
                
            if not st.session_state.confirm_back:
                if st.button("⬅️ Retour", use_container_width=True, key="back_to_list"):
                    st.session_state.confirm_back = True
                    st.rerun()
            else:
                st.warning("Les modifications non sauvegardées seront perdues. Continuer ?")
                col_cancel_back, col_confirm_back = st.columns(2)
                
                with col_cancel_back:
                    if st.button("Annuler", use_container_width=True, key="cancel_back"):
                        st.session_state.confirm_back = False
                        st.rerun()
                        
                with col_confirm_back:
                    if st.button("Confirmer", use_container_width=True, key="btn_confirm_back"):
                        # Nettoyer les variables de session utilisées pour l'édition
                        st.session_state.plat_actif = None
                        if "plat_initial" in st.session_state:
                            del st.session_state.plat_initial
                        st.session_state.edit_view = "liste"
                        st.session_state.confirm_back = False
                        st.rerun()