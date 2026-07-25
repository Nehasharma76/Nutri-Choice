# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# import pandas as pd
# from model import recommend, output_recommended_recipes

# # Load dataset inside Docker container
# dataset = pd.read_csv('/app/Data/dataset.csv')

# app = FastAPI()


# # -----------------------------
# # Request Models
# # -----------------------------

# class Params(BaseModel):
#     n_neighbors: int = 5


# class PredictionIn(BaseModel):
#     ingredients: List[str] = []   # Simple & matched with frontend
#     params: Optional[Params] = None


# # -----------------------------
# # Response Models
# # -----------------------------

# class RecipeOut(BaseModel):
#     RecipeName: str
#     Ingredients: List[str]
#     Instructions: List[str]
#     PrepTimeInMins: Optional[int] = None
#     CookTimeInMins: Optional[int] = None
#     TotalTimeInMins: Optional[int] = None
#     Servings: Optional[int] = None
#     Cuisine: Optional[str] = None
#     Course: Optional[str] = None
#     Diet: Optional[str] = None
#     URL: Optional[str] = None


# class PredictionOut(BaseModel):
#     output: Optional[List[RecipeOut]] = None


# # -----------------------------
# # Routes
# # -----------------------------

# @app.get("/")
# def home():
#     return {"health_check": "OK"}


# @app.post("/predict/", response_model=PredictionOut)
# def predict_handler(pred: PredictionIn):

#     params = pred.params or Params()
#     ingredients = pred.ingredients or []

#     # core recommendation (nutrition removed)
#     df_reco = recommend(
#         dataset,
#         None,  # nutrition removed
#         ingredients,
#         {"n_neighbors": params.n_neighbors}
#     )

#     # convert to list of RecipeOut dicts
#     output = output_recommended_recipes(df_reco, top_k=params.n_neighbors)

#     if not output:
#         return {"output": None}

#     return {"output": output}


# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# import pandas as pd
# from model import recommend, output_recommended_recipes

# # Load dataset inside Docker container
# dataset = pd.read_csv('/app/Data/dataset.csv')

# app = FastAPI()


# # -----------------------------
# # Request Models
# # -----------------------------

# class Params(BaseModel):
#     n_neighbors: int = 5


# class PredictionIn(BaseModel):
#     ingredients: List[str] = []
#     meal_type: Optional[str] = None      # NEW FIELD
#     params: Optional[Params] = None


# # -----------------------------
# # Response Models
# # -----------------------------

# class RecipeOut(BaseModel):
#     RecipeName: str
#     Ingredients: List[str]
#     Instructions: List[str]
#     PrepTimeInMins: Optional[int] = None
#     CookTimeInMins: Optional[int] = None
#     TotalTimeInMins: Optional[int] = None
#     Servings: Optional[int] = None
#     Cuisine: Optional[str] = None
#     Course: Optional[str] = None
#     Diet: Optional[str] = None
#     URL: Optional[str] = None


# class PredictionOut(BaseModel):
#     output: Optional[List[RecipeOut]] = None


# # -----------------------------
# # Routes
# # -----------------------------

# @app.get("/")
# def home():
#     return {"health_check": "OK"}


# @app.post("/predict/", response_model=PredictionOut)
# def predict_handler(pred: PredictionIn):

#     params = pred.params or Params()
#     ingredients = pred.ingredients or []
#     meal_type = pred.meal_type

#     # Filter by meal type
#     if meal_type:
#         df_filtered = dataset[dataset["meal_type"].str.lower() == meal_type.lower()]
#         if df_filtered.empty:
#             return {"output": None}
#     else:
#         df_filtered = dataset

#     # Run recommendation
#     df_reco = recommend(
#         df_filtered,
#         None,
#         ingredients,
#         {"n_neighbors": params.n_neighbors}
#     )

#     # Convert to RecipeOut list
#     output = output_recommended_recipes(df_reco, top_k=params.n_neighbors)

#     if not output:
#         return {"output": None}

#     return {"output": output}

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Optional
# import pandas as pd
# from model import recommend, output_recommended_recipes

# # Load dataset inside Docker container
# dataset = pd.read_csv('/app/Data/dataset.csv')

# # Convert Ingredients string → list
# dataset["Ingredients"] = dataset["Ingredients"].apply(
#     lambda x: [i.strip() for i in str(x).split(',')]
# )

# app = FastAPI()

# # -----------------------------
# # Request Models
# # -----------------------------

# class Params(BaseModel):
#     n_neighbors: int = 5


# class PredictionIn(BaseModel):
#     ingredients: List[str] = []
#     meal_type: Optional[str] = None       # Breakfast / Lunch / Dinner
#     params: Optional[Params] = None


# # -----------------------------
# # Response Models
# # -----------------------------

# class RecipeOut(BaseModel):
#     RecipeName: str
#     Ingredients: List[str]
#     Instructions: List[str]
#     PrepTimeInMins: Optional[int] = None
#     CookTimeInMins: Optional[int] = None
#     TotalTimeInMins: Optional[int] = None
#     Servings: Optional[int] = None
#     Cuisine: Optional[str] = None
#     Course: Optional[str] = None
#     Diet: Optional[str] = None
#     URL: Optional[str] = None


# class PredictionOut(BaseModel):
#     output: Optional[List[RecipeOut]] = None


# # -----------------------------
# # Routes
# # -----------------------------

# @app.get("/")
# def home():
#     return {"health_check": "OK"}


# @app.post("/predict/", response_model=PredictionOut)
# def predict_handler(pred: PredictionIn):

#     params = pred.params or Params()
#     ingredients = pred.ingredients or []
#     meal_type = pred.meal_type

#     # -----------------------------
#     # Filter Meal Type using "Course" column from your dataset
#     # -----------------------------
#     if meal_type:
#         df_filtered = dataset[
#             dataset["Course"].astype(str).str.lower() == meal_type.lower()
#         ]
#         if df_filtered.empty:
#             return {"output": None}
#     else:
#         df_filtered = dataset

#     # -----------------------------
#     # Run Recommendation
#     # -----------------------------
#     df_reco = recommend(
#         df_filtered,
#         None,                    # nutrition removed
#         ingredients,
#         {"n_neighbors": params.n_neighbors}
#     )

#     # Convert recommended rows to RecipeOut format
#     output = output_recommended_recipes(df_reco, top_k=params.n_neighbors)

#     if not output:
#         return {"output": None}

#     return {"output": output}

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from model import recommend, output_recommended_recipes

# Load dataset
dataset = pd.read_csv('/app/Data/dataset.csv')

# Make meal_type consistent: lowercase and stripped
dataset["meal_type"] = dataset["meal_type"].astype(str).str.strip().str.lower()

app = FastAPI()

# -----------------------------
# Request Models
# -----------------------------

class Params(BaseModel):
    n_neighbors: int = 5

class PredictionIn(BaseModel):
    ingredients: List[str] = []
    meal_type: Optional[str] = None
    params: Optional[Params] = None

# -----------------------------
# Response Models
# -----------------------------

class RecipeOut(BaseModel):
    RecipeName: str
    Ingredients: List[str]
    Instructions: List[str]
    PrepTimeInMins: Optional[int] = None
    CookTimeInMins: Optional[int] = None
    TotalTimeInMins: Optional[int] = None
    Servings: Optional[int] = None
    Cuisine: Optional[str] = None
    Course: Optional[str] = None
    Diet: Optional[str] = None
    URL: Optional[str] = None

class PredictionOut(BaseModel):
    output: List[RecipeOut] = []

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/predict/", response_model=PredictionOut)
def predict_handler(pred: PredictionIn):
    params = pred.params or Params()
    ingredients = pred.ingredients or []
    meal_type = pred.meal_type.lower().strip() if pred.meal_type else None

    # Filter by meal_type
    if meal_type:
        df_filtered = dataset[dataset["meal_type"] == meal_type]
        if df_filtered.empty:
            return {"output": []}
    else:
        df_filtered = dataset

    # Run recommendation
    df_reco = recommend(
        df_filtered,
        None,
        ingredients,
        {"n_neighbors": params.n_neighbors}
    )

    output = output_recommended_recipes(df_reco, top_k=params.n_neighbors)

    return {"output": output or []}
