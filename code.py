import streamlit as st
import requests
import os

# --- Partie 1 : Fonctions API Spoonacular ---
API_KEY = os.getenv("SPOONACULAR_API_KEY", "15743483325f40568a65c786ba9d74bc")

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

# --- Partie 2 : Affichage des recettes ---

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

# --- Partie 3 : Interface Utilisateur Streamlit ---

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
