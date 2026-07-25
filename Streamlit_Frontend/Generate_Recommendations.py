# import streamlit as st
# from random import uniform as rnd
# from ImageFinder.ImageFinder import get_images_links as find_image

# # Nutritional fields
# nutritions_values = [
#     'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
#     'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent'
# ]

# # ----- Person class -----
# class Person:
#     def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
#         self.age = age
#         self.height = height
#         self.weight = weight
#         self.gender = gender
#         self.activity = activity
# #         self.meals_calories_perc = meals_calories_perc
# #         self.weight_loss = weight_loss

# #     def calculate_bmi(self):
# #         return round(self.weight / ((self.height / 100) ** 2), 2)

# #     def display_result(self):
# #         bmi = self.calculate_bmi()
# #         bmi_string = f'{bmi} kg/m²'
# #         if bmi < 18.5:
# #             category, color = 'Underweight', 'Red'
# #         elif bmi < 25:
# #             category, color = 'Normal', 'Green'
# #         elif bmi < 30:
# #             category, color = 'Overweight', 'Yellow'
# #         else:
# #             category, color = 'Obesity', 'Red'
# #         return bmi_string, category, color

# #     def calculate_bmr(self):
# #         if self.gender == 'Male':
# #             return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
# #         else:
# #             return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

# #     def calories_calculator(self):
# #         activities = ['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)',
# #                       'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
# #         weights = [1.2, 1.375, 1.55, 1.725, 1.9]
# #         weight_factor = weights[activities.index(self.activity)]
# #         return self.calculate_bmr() * weight_factor

# #     def generate_recommendations(self):
# #         """Generate multiple random recipes per meal with nutrition values"""
# #         total_calories = self.weight_loss * self.calories_calculator()
# #         recommendations = {}

# #         for meal, perc in self.meals_calories_perc.items():
# #             meal_calories = perc * total_calories
# #             meal_recipes = []

# #             # Generate 2-3 recipes per meal
# #             for i in range(2):
# #                 recipe_name = f"{meal.capitalize()} Recipe {i+1}"
# #                 ingredients = [f"Ingredient {j+1}" for j in range(5)]
# #                 instructions = [f"Step {j+1}" for j in range(3)]

# #                 # Generate random nutrition values
# #                 if meal in ['breakfast', 'morning snack']:
# #                     nutritions = [
# #                         meal_calories, rnd(10,30), rnd(0,4), rnd(0,30), rnd(0,400),
# #                         rnd(40,75), rnd(4,10), rnd(0,10), rnd(30,100)
# #                     ]
# #                 elif meal in ['lunch', 'afternoon snack', 'dinner']:
# #                     nutritions = [
# #                         meal_calories, rnd(20,40), rnd(0,4), rnd(0,30), rnd(0,400),
# #                         rnd(40,75), rnd(4,20), rnd(0,10), rnd(50,175)
# #                     ]
# #                 else:
# #                     nutritions = [meal_calories] + [rnd(0,10) for _ in range(8)]

# #                 recipe = {
# #                     "RecipeName": recipe_name,
# #                     "Ingredients": ingredients,
# #                     "Instructions": instructions,
# #                     **{key: value for key, value in zip(nutritions_values, nutritions)}
# #                 }

# #                 # Add image link (if available)
# #                 recipe['image_link'] = find_image(recipe_name)
# #                 meal_recipes.append(recipe)

# #             recommendations[meal] = meal_recipes

# #         return recommendations


# # # ----- Display class -----
# # class Display:
# #     def __init__(self):
# #         self.plans = ["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
# #         self.weights = [1, 0.9, 0.8, 0.6]
# #         self.losses = ['-0 kg/week','-0.25 kg/week','-0.5 kg/week','-1 kg/week']

# #     def display_bmi(self, person):
# #         st.header('BMI CALCULATOR')
# #         bmi_string, category, color = person.display_result()
# #         st.metric(label="Body Mass Index (BMI)", value=bmi_string)
# #         st.markdown(f'<p style="color:{color}; font-size:25px;">{category}</p>', unsafe_allow_html=True)
# #         st.markdown("Healthy BMI range: 18.5 kg/m² - 25 kg/m².")

# #     def display_calories(self, person):
# #         st.header('CALORIES CALCULATOR')
# #         maintain_calories = person.calories_calculator()
# #         for plan, weight, loss, col in zip(self.plans, self.weights, self.losses, st.columns(4)):
# #             with col:
# #                 st.metric(label=plan, value=f'{round(maintain_calories*weight)} Calories/day', delta=loss, delta_color="inverse")

# #     def display_recommendation(self, person, recommendations):
# #         st.header('DIET RECOMMENDATIONS')
# #         if not recommendations:
# #             st.warning("No recommendations available.")
# #             return

# #         for meal, meal_recipes in recommendations.items():
# #             st.subheader(meal.capitalize())
# #             if not meal_recipes:
# #                 st.info("No recipes available for this meal.")
# #                 continue

# #             for recipe in meal_recipes:
# #                 recipe_name = recipe.get('RecipeName', 'Unknown Recipe')
# #                 ingredients = recipe.get('Ingredients', [])
# #                 instructions = recipe.get('Instructions', [])

# #                 expander = st.expander(recipe_name)
# #                 if recipe.get('image_link'):
# #                     expander.markdown(
# #                         f'<div><center><img src="{recipe["image_link"]}" alt="{recipe_name}" width="250"></center></div>',
# #                         unsafe_allow_html=True
# #                     )

# #                 nutritions_df = {key: [recipe.get(key, 0)] for key in nutritions_values}
# #                 expander.markdown("**Nutritional Values (g / kcal):**")
# #                 expander.dataframe(nutritions_df)

# #                 if ingredients:
# #                     expander.markdown("**Ingredients:**")
# #                     for ing in ingredients:
# #                         expander.markdown(f"- {ing}")

# #                 if instructions:
# #                     expander.markdown("**Instructions:**")
# #                     for step in instructions:
# #                         expander.markdown(f"- {step}")

# #                 expander.markdown("---")


# import requests
# from ImageFinder.ImageFinder import get_images_links as find_image

# class Generator:
#     """
#     Handles recipe generation from backend and normalizes the output.
#     """

#     def __init__(self, ingredients=None, meal_type=None, params=None):
#         self.ingredients = ingredients or []
#         self.meal_type = meal_type
#         self.params = params or {"n_neighbors": 5}

#     def set_request(self, ingredients, meal_type, params):
#         self.ingredients = ingredients
#         self.meal_type = meal_type
#         self.params = params

#     def generate(self):
#         """
#         Sends a POST request to the backend and returns normalized recipe data.
#         """
#         request = {
#             "ingredients": self.ingredients,
#             "meal_type": self.meal_type,
#             "params": self.params
#         }

#         try:
#             response = requests.post("http://backend:8080/predict/", json=request)
#             response.raise_for_status()
#             data = response.json()
# #             return self._normalize_recipes(data.get("output", []))

# #         except Exception as e:
# #             return {"error": str(e)}

# #     def _normalize_recipes(self, recipes):
# #         """
# #         Standardizes recipe fields and adds image links.
# #         Ensures consistent keys for Streamlit display.
# #         """
# #         normalized = []
# #         for r in recipes:
# #             recipe = {
# #                 "RecipeName": r.get("RecipeName") or r.get("RecipeNameHindi") or "Unknown Recipe",
# #                 "Ingredients": r.get("Ingredients") or r.get("RecipeIngredientParts") or [],
# #                 "Instructions": r.get("Instructions") or r.get("RecipeInstructions") or [],
# #                 "PrepTime": r.get("PrepTime") or r.get("PrepTimeInMins"),
# #                 "CookTime": r.get("CookTime") or r.get("CookTimeInMins"),
# #                 "TotalTime": r.get("TotalTime") or r.get("TotalTimeInMins"),
# #                 "Servings": r.get("Servings") or 1,
# #                 "Cuisine": r.get("Cuisine") or "Unknown",
# #                 "Course": r.get("Course") or "Unknown",
# #                 "Diet": r.get("Diet") or "Unknown",
# #                 "MealType": r.get("MealType") or self.meal_type or "Any",
# #                 "image_link": r.get("image_link") or find_image(r.get("RecipeName") or "")
# #             }
# #             normalized.append(recipe)

# #         # Group recipes by MealType for Streamlit display
# #         grouped = {"breakfast": [], "lunch": [], "dinner": [], "other": []}
# #         for rec in normalized:
# #             meal = rec["MealType"].lower() if rec["MealType"] else "other"
# #             if meal in grouped:
# #                 grouped[meal].append(rec)
# #             else:
# #                 grouped["other"].append(rec)

# #         return grouped


# import pandas as pd
# from random import sample
# from ImageFinder.ImageFinder import get_images_links as find_image

# class Generator:
#     """
#     Generates recipes directly from dataset CSV and normalizes for Streamlit.
#     """

#     def __init__(self, dataset_path="recipes.csv", n_per_meal=3):
#         self.dataset_path = dataset_path
#         self.n_per_meal = n_per_meal
#         self.df = pd.read_csv(self.dataset_path)
#         # Ensure MealType exists
#         if 'MealType' not in self.df.columns:
#             self.df['MealType'] = self.df['Course'].apply(self._map_course_to_meal)

#     def _map_course_to_meal(self, course):
#         course = str(course).lower()
#         if "breakfast" in course:
#             return "breakfast"
#         elif "lunch" in course or "main" in course:
#             return "lunch"
#         elif "dinner" in course or "side" in course:
#             return "dinner"
#         else:
#             return "other"

#     def generate(self, meal_type=None):
#         """
#         Returns grouped recipes by meal type.
#         """
#         grouped = {"breakfast": [], "lunch": [], "dinner": [], "other": []}

#         if meal_type:
# #             df_filtered = self.df[self.df['MealType'].str.lower() == meal_type.lower()]
# #         else:
# #             df_filtered = self.df

# #         for meal in grouped.keys():
# #             meal_df = df_filtered[df_filtered['MealType'].str.lower() == meal]
# #             if len(meal_df) == 0:
# #                 grouped[meal] = []
# #                 continue

# #             # Pick up to n_per_meal random recipes
# #             n_pick = min(self.n_per_meal, len(meal_df))
# #             sampled = meal_df.sample(n=n_pick, random_state=None)

# #             recipes = []
# #             for _, r in sampled.iterrows():
# #                 recipe = {
# #                     "RecipeName": r.get("RecipeName", "Unknown Recipe"),
# #                     "Ingredients": r.get("Ingredients", "").split(","),
# #                     "Instructions": r.get("Instructions", "").split(". "),
# #                     "PrepTime": r.get("PrepTimeInMins"),
# #                     "CookTime": r.get("CookTimeInMins"),
# #                     "TotalTime": r.get("TotalTimeInMins"),
# #                     "Servings": r.get("Servings", 1),
# #                     "Cuisine": r.get("Cuisine", "Unknown"),
# #                     "Course": r.get("Course", "Unknown"),
# #                     "Diet": r.get("Diet", "Unknown"),
# #                     "MealType": meal,
# #                     "image_link": find_image(r.get("RecipeName", ""))
# #                 }
# #                 recipes.append(recipe)

# #             grouped[meal] = recipes

# #         return grouped


# import pandas as pd
# from ImageFinder.ImageFinder import get_images_links as find_image

# class Generator:
#     def __init__(self, n_per_meal=3):
#         self.n_per_meal = n_per_meal
#         # Load dataset
#         self.dataset = pd.read_csv("recipes_dataset.csv")
#         # Clean meal_type column
#         if "MealType" not in self.dataset.columns:
#             self.dataset["MealType"] = "other"
#         else:
#             self.dataset["MealType"] = self.dataset["MealType"].astype(str).str.strip().str.lower()

#     def generate(self):
#         grouped = {"breakfast": [], "lunch": [], "dinner": [], "other": []}

#         for meal in grouped.keys():
#             df = self.dataset[self.dataset["MealType"] == meal]
#             if df.empty:
#                 continue
#             df_sample = df.sample(min(self.n_per_meal, len(df)))  # random sample
#             for _, row in df_sample.iterrows():
#                 recipe = {
#                     "RecipeName": row.get("RecipeName", "Unknown Recipe"),
#                     "Ingredients": str(row.get("Ingredients", "")).split(","),
#                     "Instructions": str(row.get("Instructions", "")).split(". "),
#                     "PrepTimeInMins": row.get("PrepTimeInMins"),
#                     "CookTimeInMins": row.get("CookTimeInMins"),
#                     "TotalTimeInMins": row.get("TotalTimeInMins"),
#                     "Servings": row.get("Servings", 1),
#                     "Cuisine": row.get("Cuisine", "Unknown"),
#                     "Course": row.get("Course", "Unknown"),
#                     "Diet": row.get("Diet", "Unknown"),
#                     "MealType": meal,
#                     "image_link": find_image(row.get("RecipeName", "")),
#                     # Dummy nutrition values (or you can parse from CSV if available)
#                     "Calories": 100,
#                     "FatContent": 5,
#                     "SaturatedFatContent": 2,
#                     "CholesterolContent": 0,
#                     "SodiumContent": 50,
#                     "CarbohydrateContent": 20,
#                     "FiberContent": 5,
#                     "SugarContent": 5,
#                     "ProteinContent": 10
#                 }
#                 grouped[meal].append(recipe)
#         return grouped


# import pandas as pd
# from ImageFinder.ImageFinder import get_images_links as find_image
# import os

# class Generator:
#     def __init__(self, n_per_meal=3, dataset_path=None):
#         self.n_per_meal = n_per_meal

#         # Default relative path to dataset
#         if dataset_path is None:
#             dataset_path = os.path.join("Data", "dataset.csv")  # relative to app root

#         # Try to load CSV, fallback to demo data if missing
#         if os.path.exists(dataset_path):
#             self.dataset = pd.read_csv(dataset_path)
#         else:
#             # Minimal demo dataset to avoid crashing
#             self.dataset = pd.DataFrame([{
#                 "RecipeName": "Demo Oatmeal",
#                 "Ingredients": "Oats, Milk",
#                 "Instructions": "Boil oats in milk",
#                 "PrepTimeInMins": 5,
#                 "CookTimeInMins": 10,
#                 "TotalTimeInMins": 15,
#                 "Servings": 1,
#                 "Cuisine": "American",
#                 "Course": "Breakfast",
#                 "Diet": "Vegetarian",
#                 "MealType": "breakfast"
#             }])

#         # Normalize MealType column
#         if "MealType" not in self.dataset.columns:
#             self.dataset["MealType"] = "other"
#         else:
#             self.dataset["MealType"] = self.dataset["MealType"].astype(str).str.strip().str.lower()

#     def generate(self):
#         grouped = {"breakfast": [], "lunch": [], "dinner": [], "other": []}

#         for meal in grouped.keys():
#             df = self.dataset[self.dataset["MealType"] == meal]
#             if df.empty:
# #                 continue

# #             df_sample = df.sample(min(self.n_per_meal, len(df)))
# #             for _, row in df_sample.iterrows():
# #                 recipe_name = row.get("RecipeName", "Unknown Recipe")
# #                 image_links = find_image(recipe_name)
# #                 recipe = {
# #                     "RecipeName": recipe_name,
# #                     "Ingredients": str(row.get("Ingredients", "")).split(",") if pd.notna(row.get("Ingredients")) else [],
# #                     "Instructions": str(row.get("Instructions", "")).split(". ") if pd.notna(row.get("Instructions")) else [],
# #                     "PrepTimeInMins": row.get("PrepTimeInMins", 0),
# #                     "CookTimeInMins": row.get("CookTimeInMins", 0),
# #                     "TotalTimeInMins": row.get("TotalTimeInMins", 0),
# #                     "Servings": row.get("Servings", 1),
# #                     "Cuisine": row.get("Cuisine", "Unknown"),
# #                     "Course": row.get("Course", "Unknown"),
# #                     "Diet": row.get("Diet", "Unknown"),
# #                     "MealType": meal,
# #                     "image_link": image_links[0] if image_links else None,
# #                     "Calories": row.get("Calories", 100),
# #                     "FatContent": row.get("FatContent", 5),
# #                     "SaturatedFatContent": row.get("SaturatedFatContent", 2),
# #                     "CholesterolContent": row.get("CholesterolContent", 0),
# #                     "SodiumContent": row.get("SodiumContent", 50),
# #                     "CarbohydrateContent": row.get("CarbohydrateContent", 20),
# #                     "FiberContent": row.get("FiberContent", 5),
# #                     "SugarContent": row.get("SugarContent", 5),
# #                     "ProteinContent": row.get("ProteinContent", 10)
# #                 }
# #                 grouped[meal].append(recipe)

# #         return grouped

# import requests
# import json

# class Generator:
#     def __init__(self, ingredients=None, meal_type=None, params=None):
#         self.ingredients = ingredients or []
#         self.meal_type = meal_type
#         self.params = params or {"n_neighbors": 5}

#     def set_request(self, ingredients=None, meal_type=None, params=None):
#         self.ingredients = ingredients or []
#         self.meal_type = meal_type
#         self.params = params or {"n_neighbors": 5}

#     def generate(self):
#         payload = {
#             "ingredients": self.ingredients,
#             "meal_type": self.meal_type,
#             "params": self.params
#         }

#         try:
#             response = requests.post(
#                 url="http://backend:8080/predict/",
#                 data=json.dumps(payload),
#                 headers={"Content-Type": "application/json"}
#             )
#             response.raise_for_status()
#             return response.json()
#         except Exception as e:
#             print("API error:", e)
#             return {"output": []}


# frontend/Generate_Recommendations.py
import requests
import json
from typing import List, Dict, Any

class Generator:
    def __init__(self, nutrition_input: List[float], ingredients: List[str] = None, meal_type: str = None, params: Dict[str, Any]=None):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients or []
        self.meal_type = meal_type
        self.params = params or {"n_neighbors": 5}

    def set_request(self, nutrition_input: List[float], ingredients: List[str]=None, meal_type: str=None, params: Dict[str,Any]=None):
        self.nutrition_input = nutrition_input
        self.ingredients = ingredients or []
        self.meal_type = meal_type
        self.params = params or {"n_neighbors": 5}

    def generate(self):
        payload = {
            "nutrition_input": self.nutrition_input,
            "ingredients": self.ingredients,
            "meal_type": self.meal_type,
            "params": {"n_neighbors": self.params.get("n_neighbors", 5)}
        }
        try:
            # inside docker-compose frontend -> use 'http://backend:8080/predict/'
            url = "http://backend:8080/predict/"
            r = requests.post(url, data=json.dumps(payload), headers={"Content-Type":"application/json"}, timeout=10)
            r.raise_for_status()
            return r.json()    # returns dict with 'output' key
        except Exception as e:
            print("Error calling backend:", e)
            return {"output": []}
