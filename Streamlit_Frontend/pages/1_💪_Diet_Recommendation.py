import streamlit as st
import pandas as pd
from random import uniform as rnd
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts

# st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="💪", layout="wide")

nutritions_values = [
    'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent',
    'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent'
]

# Streamlit states initialization
if 'person' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None
    st.session_state.person = None
    st.session_state.weight_loss_option = None

# ----- Person class -----
class Person:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss

    def calculate_bmi(self):
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi

    def display_result(self):
        bmi = self.calculate_bmi()
        bmi_string = f'{bmi} kg/m²'
        if bmi < 18.5:
            category, color = 'Underweight', 'Red'
        elif 18.5 <= bmi < 25:
            category, color = 'Normal', 'Green'
        elif 25 <= bmi < 30:
            category, color = 'Overweight', 'Yellow'
        else:
            category, color = 'Obesity', 'Red'
        return bmi_string, category, color

    def calculate_bmr(self):
        if self.gender == 'Male':
            return 10*self.weight + 6.25*self.height - 5*self.age + 5
        else:
            return 10*self.weight + 6.25*self.height - 5*self.age - 161

    def calories_calculator(self):
        activities = ['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)',
                      'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight_factor = weights[activities.index(self.activity)]
        maintain_calories = self.calculate_bmr() * weight_factor
        return maintain_calories

    def generate_recommendations(self):
        total_calories = self.weight_loss * self.calories_calculator()
        recommendations = []
        for meal in self.meals_calories_perc:
            meal_calories = self.meals_calories_perc[meal] * total_calories
            if meal == 'breakfast':
                recommended_nutrition = [meal_calories, rnd(10,30), rnd(0,4), rnd(0,30), rnd(0,400), rnd(40,75), rnd(4,10), rnd(0,10), rnd(30,100)]
            elif meal == 'lunch':
                recommended_nutrition = [meal_calories, rnd(20,40), rnd(0,4), rnd(0,30), rnd(0,400), rnd(40,75), rnd(4,20), rnd(0,10), rnd(50,175)]
            elif meal == 'dinner':
                recommended_nutrition = [meal_calories, rnd(20,40), rnd(0,4), rnd(0,30), rnd(0,400), rnd(40,75), rnd(4,20), rnd(0,10), rnd(50,175)]
            else:
                recommended_nutrition = [meal_calories, rnd(10,30), rnd(0,4), rnd(0,30), rnd(0,400), rnd(40,75), rnd(4,10), rnd(0,10), rnd(30,100)]
            generator = Generator(recommended_nutrition)
            recommended_recipes = generator.generate().get('output', [])
            for recipe in recommended_recipes:
                recipe['image_link'] = find_image(recipe.get('RecipeName', ''))
            recommendations.append(recommended_recipes)
        return recommendations

# ----- Display class -----
class Display:
    def __init__(self):
        self.plans = ["Maintain weight","Mild weight loss","Weight loss","Extreme weight loss"]
        self.weights = [1, 0.9, 0.8, 0.6]
        self.losses = ['-0 kg/week','-0.25 kg/week','-0.5 kg/week','-1 kg/week']

    def display_bmi(self, person):
        st.header('BMI CALCULATOR')
        bmi_string, category, color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        st.markdown(f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>', unsafe_allow_html=True)
        st.markdown("Healthy BMI range: 18.5 kg/m² - 25 kg/m².")

    def display_calories(self, person):
        st.header('CALORIES CALCULATOR')
        maintain_calories = person.calories_calculator()
        for plan, weight, loss, col in zip(self.plans, self.weights, self.losses, st.columns(4)):
            with col:
                st.metric(label=plan, value=f'{round(maintain_calories*weight)} Calories/day', delta=loss, delta_color="inverse")

    def display_recommendation(self, person, recommendations):
        st.header('DIET RECOMMENDATIONS')
        if not recommendations:
            st.warning("No recommendations available.")
            return

        for meal_recommendations in recommendations:
            for recipe in meal_recommendations:
                recipe_name = recipe.get('RecipeName', 'Unknown Recipe')
                ingredients = recipe.get('RecipeIngredientParts', recipe.get('Ingredients', []))
                instructions = recipe.get('RecipeInstructions', recipe.get('Instructions', []))
                prep_time = recipe.get('PrepTime', recipe.get('PrepTimeInMins'))
                cook_time = recipe.get('CookTime', recipe.get('CookTimeInMins'))
                total_time = recipe.get('TotalTime', recipe.get('TotalTimeInMins'))
                servings = recipe.get('Servings', 1)
                cuisine = recipe.get('Cuisine', 'Unknown')
                course = recipe.get('Course', 'Unknown')
                diet = recipe.get('Diet', 'Unknown')
                recipe_img = recipe.get('image_link') or find_image(recipe_name)

                expander = st.expander(recipe_name)
                if recipe_img:
                    expander.markdown(f'<div><center><img src="{recipe_img}" alt="{recipe_name}" width="250"></center></div>', unsafe_allow_html=True)

                nutritions_df = pd.DataFrame({value: [recipe.get(value, 0)] for value in nutritions_values})
                expander.markdown("**Nutritional Values (g / kcal):**")
                expander.dataframe(nutritions_df)

                if ingredients:
                    expander.markdown("**Ingredients:**")
                    for ing in ingredients:
                        expander.markdown(f"- {ing}")

                if instructions:
                    expander.markdown("**Instructions:**")
                    for step in instructions:
                        expander.markdown(f"- {step}")

                info = []
                if prep_time: info.append(f"Prep: {prep_time} min")
                if cook_time: info.append(f"Cook: {cook_time} min")
                if total_time: info.append(f"Total: {total_time} min")
                if servings: info.append(f"Servings: {servings}")
                info.extend([f"Cuisine: {cuisine}", f"Course: {course}", f"Diet: {diet}"])
                expander.markdown(" | ".join(info))
                expander.markdown("---")

# ----- Streamlit app -----
display = Display()
st.markdown("<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>", unsafe_allow_html=True)

with st.form("recommendation_form"):
    st.write("Modify the values and click Generate")
    age = st.number_input('Age', min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)', min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)', min_value=10, max_value=300, step=1)
    gender = st.radio('Gender', ('Male','Female'))
    activity = st.select_slider('Activity', options=[
        'Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)',
        'Very active (6-7 days/wk)', 'Extra active (very active & physical job)'
    ])
    option = st.selectbox('Choose your weight loss plan:', display.plans)
    st.session_state.weight_loss_option = option
    weight_loss = display.weights[display.plans.index(option)]
    number_of_meals = st.slider('Meals per day', min_value=3, max_value=5, step=1, value=3)

    if number_of_meals == 3:
        meals_calories_perc = {'breakfast':0.35,'lunch':0.40,'dinner':0.25}
    elif number_of_meals == 4:
        meals_calories_perc = {'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'dinner':0.25}
    else:
        meals_calories_perc = {'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'afternoon snack':0.05,'dinner':0.20}

    generated = st.form_submit_button("Generate")

if generated:
    st.session_state.generated = True
    person = Person(age, height, weight, gender, activity, meals_calories_perc, weight_loss)
    st.session_state.person = person
    with st.spinner('Generating recommendations...'):
        recommendations = person.generate_recommendations()
        st.session_state.recommendations = recommendations

if st.session_state.generated:
    display.display_bmi(st.session_state.person)
    display.display_calories(st.session_state.person)
    display.display_recommendation(st.session_state.person, st.session_state.recommendations)
