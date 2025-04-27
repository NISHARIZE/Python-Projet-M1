---
marp: true
paginate: true
style: |
  section {
    font-size: 22px;
  }
---

# 🥗 Nutrition Recipe Finder

**Auteurs :**  
Jeancy Candela NISHARIZE, Lucie MATT, Ruiyue TONG


Ce projet utilise **l'API Spoonacular** et **Streamlit** pour proposer des recettes personnalisées selon les préférences alimentaires et les objectifs nutritionnels de l'utilisateur. Il s'agit d'une application interactive simple à utiliser, conçue en 3 parties principales.

---

##  Partie 1 : Récupération de Recettes 

Cette première partie gère la configuration de l'API et les appels à Spoonacular pour récupérer les recettes selon les critères choisis (régime, objectif, intolérances…).

```python
import streamlit as st
import requests
import os

API_KEY = os.getenv("SPOONACULAR_API_KEY", "YOUR_API_KEY_HERE")

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    return requests.get(url, params={"apiKey": API_KEY}).json()

def get_recipes(diet, goal, intolerances, keyword, number=5):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {"apiKey": API_KEY, "number": number, "addRecipeInformation": True}
    if diet.lower() != "indifférent": params["diet"] = diet.lower()
    if intolerances: params["intolerances"] = ",".join(intolerances)
    if keyword: params["query"] = keyword
    if goal.lower() == "perdre du poids": params["maxCalories"] = 400
    elif goal.lower() == "prendre du muscle": params["minProtein"] = 25
    return requests.get(url, params=params).json()
```

---

## Partie 2 : Traitement & Affichage des Résultats 
Cette partie extrait les ingrédients et ustensiles nécessaires à chaque recette, puis les affiche joliment à l’utilisateur dans l’application Streamlit.


```python
def afficher_recettes(recettes):
    if "results" not in recettes or not recettes["results"]:
        st.error("❌ Aucune recette trouvée."); return
    st.markdown("## 🍽️ Recettes trouvées :")
    for r in recettes["results"]:
        titre, image, id_recette = r['title'], r['image'], r['id']
        details = get_recipe_details(id_recette)
        st.markdown(f"### {titre}")
        col1, col2 = st.columns([1, 2])
        with col1: st.image(image, width=300)
        with col2:
            st.markdown("**🧂 Ingrédients :**")
            for i in details.get("extendedIngredients", []): st.write(f"- {i['original']}")
            utensils = {eq.get("name") for inst in details.get("analyzedInstructions", []) for step in inst.get("steps", []) for eq in step.get("equipment", [])}
            st.markdown("**🔧 Ustensiles :**")
            st.write(", ".join([u.capitalize() for u in utensils]) if utensils else "Non spécifiés")
```

---

## Partie 3 : Interface Utilisateur (Streamlit)
Cette dernière partie construit l'interface graphique Streamlit : les menus déroulants, les boutons, et l'affichage interactif en fonction des choix de l'utilisateur.

```python
st.set_page_config(page_title="Nutrition Recipe Finder", page_icon="🥗")
st.title("🥗 Nutrition Recipe Finder")
st.markdown("### Trouve des recettes adaptées à ton régime et tes objectifs nutritionnels !")

diet = st.selectbox("1️⃣ Quel est ton régime alimentaire ?", ["Indifférent", "Végétarien", "Vegan"])
goal = st.selectbox("2️⃣ Quel est ton objectif nutritionnel ?", ["Perdre du poids", "Prendre du muscle"])
intolerances = st.multiselect("3️⃣ Sélectionne des intolérances (optionnel) :", ["Lactose", "Gluten", "Porc", "Sucre", "Arachide"])
keyword = st.text_input("4️⃣ Entre un mot-clé pour filtrer les recettes (ex: curry, soupe...)")
number = st.slider("Combien de recettes veux-tu afficher ?", 1, 20, 5)

if st.button("🔍 Rechercher des recettes"):
    data = get_recipes(diet, goal, intolerances, keyword, number)
    afficher_recettes(data)

```
---

##  Analyse critique du projet

### Points forts

- **Simplicité d'utilisation** : Interface Streamlit claire, accessible sans compétence technique.
- **Tout en un seul fichier `app.py`** : Plus simple à exécuter et comprendre.
- **Choix d'une API externe adaptée** : Spoonacular est riche et suffisait largement pour réaliser ce projet sans passer par du scraping complexe.
- **Évite les problèmes de scraping** : Beaucoup de sites web utilisent du **JavaScript dynamique** (ex: chargement asynchrone), rendant difficile l'extraction directe. Spoonacular simplifie tout.
- **Streamlit > Widgets classiques** : Dans Google Colab ou Jupyter Notebook, les widgets étaient parfois instables. Streamlit recrée une interface web fluide et fonctionnelle.
---

##  Analyse critique du projet

###  Points faibles


- **Dépendance forte à Spoonacular** : Si l'API change, tout le projet est impacté.
- **Gestion d'erreurs basique** : Pas encore d'affichage spécifique pour erreur réseau, API key invalide, etc.
- **Pas de séparation des responsabilités** : Tout est dans `app.py` ; pour un projet très grand, ce serait difficile à maintenir.
- **Pas de sauvegarde locale** : Les recettes affichées ne sont pas enregistrées pour un usage ultérieur.

---

## Analyse critique du projet

### Axes d'amélioration possibles

- Ajouter une **gestion avancée des erreurs** : Détecter et informer mieux l'utilisateur en cas de problème réseau ou clé API incorrecte.
- Utiliser **`@st.cache_data`** pour limiter les appels API et rendre l'application plus rapide.
- Ajouter une **fonction d'export** (ex : PDF, TXT) pour sauvegarder les recettes.
- Permettre de **sauvegarder ses recettes favorites** dans une liste personnelle.

