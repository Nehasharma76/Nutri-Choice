import streamlit as st
import requests

def display_recommendation(person, recommendations):
    if not recommendations or len(recommendations) == 0:
        st.warning("No recommendations found.")
        return

    for recipe in recommendations:
        recipe_name = recipe.get("RecipeName", "Unknown Recipe")
        ingredients = recipe.get("Ingredients", [])
        instructions = recipe.get("Instructions", [])
        prep_time = recipe.get("PrepTimeInMins")
        cook_time = recipe.get("CookTimeInMins")
        total_time = recipe.get("TotalTimeInMins")
        servings = recipe.get("Servings")
        cuisine = recipe.get("Cuisine", "Unknown")
        course = recipe.get("Course", "Unknown")
        diet = recipe.get("Diet", "Unknown")
        url = recipe.get("URL")

        st.subheader(recipe_name)
        if ingredients:
            st.markdown("**Ingredients:**")
            for ing in ingredients:
                st.write(f"- {ing}")
        if instructions:
            st.markdown("**Instructions:**")
            for step in instructions:
                st.write(f"- {step}")

        info = []
        if prep_time: info.append(f"Prep: {prep_time} min")
        if cook_time: info.append(f"Cook: {cook_time} min")
        if total_time: info.append(f"Total: {total_time} min")
        if servings: info.append(f"Servings: {servings}")
        info.extend([f"Cuisine: {cuisine}", f"Course: {course}", f"Diet: {diet}"])
        st.markdown(" | ".join(info))

        if url:
            st.markdown(f"[View Recipe]({url})")
        st.markdown("---")        

st.title("🍽️ Custom Food Recommendation")
ingredients_input = st.text_input("Enter ingredients (comma-separated)", "Karela")
n_recommend = st.number_input("Number of recipes", min_value=1, max_value=20, value=5)

if st.button("Get Recommendations"):
    st.info("Fetching recommendations...")
    try:
        payload = {
            "ingredients": [i.strip() for i in ingredients_input.split(",")],
            "params": {"n_neighbors": n_recommend}
        }
        # Note: use 'backend' instead of 'localhost' inside Docker
        response = requests.post("http://backend:8080/predict/", json=payload)
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("output", [])
            display_recommendation("User", recommendations)
        else:
            st.error(f"Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
