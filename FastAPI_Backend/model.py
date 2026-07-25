import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def _safe_text(s):
    if pd.isna(s):
        return ""
    return str(s)

def _safe_int(v):
    try:
        if pd.isna(v):
            return None
        return int(v)
    except Exception:
        return None

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Ingredients_text"] = df["Ingredients"].fillna("").astype(str)
    df["Instructions_text"] = df["Instructions"].fillna("").astype(str)
    df["combined_text"] = df["Ingredients_text"] + " " + df["Instructions_text"]
    return df

def extract_ingredient_filtered_data(df: pd.DataFrame, ingredients: list):
    if not ingredients:
        return df
    tokens = [re.escape(t.strip()) for t in ingredients if t and str(t).strip()]
    if not tokens:
        return df
    regex_string = "(" + "|".join(tokens) + ")"
    mask = df["Ingredients_text"].str.contains(regex_string, case=False, regex=True, na=False)
    return df[mask]

def recommend(dataframe: pd.DataFrame, nutrition_input, ingredients: list, params: dict):
    df = preprocess(dataframe)
    candidates = extract_ingredient_filtered_data(df, ingredients)
    if candidates.empty:
        candidates = df

    tfidf = TfidfVectorizer(stop_words="english", max_features=20000)
    matrix = tfidf.fit_transform(candidates["combined_text"].values)

    n_neighbors = int(params.get("n_neighbors", 5)) if params else 5
    n_neighbors = max(1, n_neighbors)

    if ingredients and any(t.strip() for t in ingredients):
        query_text = " ".join(ingredients)
        query_vec = tfidf.transform([query_text])
        sim_scores = cosine_similarity(query_vec, matrix).flatten()
        candidates = candidates.copy()
        candidates["score"] = sim_scores
        candidates = candidates.sort_values(by="score", ascending=False)
    else:
        norms = np.asarray(matrix.power(2).sum(axis=1)).ravel()
        candidates = candidates.copy()
        candidates["score"] = norms
        candidates = candidates.sort_values(by="score", ascending=False)

    return candidates.head(n_neighbors)

def output_recommended_recipes(df: pd.DataFrame, top_k: int = 5):
    if df is None or df.empty:
        return []

    out = []
    for _, row in df.iterrows():
        ingredients_list = [i.strip() for i in str(row.get("Ingredients", "")).split(",") if i.strip()]
        instructions_text = str(row.get("Instructions", ""))
        instructions_list = [s.strip() for s in re.split(r'(?<=\.)\s+|\n', instructions_text) if s.strip()]

        item = {
            "RecipeName": row.get("RecipeName", ""),
            "Ingredients": ingredients_list,
            "Instructions": instructions_list,
            "PrepTimeInMins": _safe_int(row.get("PrepTimeInMins")),
            "CookTimeInMins": _safe_int(row.get("CookTimeInMins")),
            "TotalTimeInMins": _safe_int(row.get("TotalTimeInMins")),
            "Servings": _safe_int(row.get("Servings")),
            "Cuisine": row.get("Cuisine"),
            "Course": row.get("Course"),
            "Diet": row.get("Diet"),
            "URL": row.get("URL")
        }

        out.append(item)
        if len(out) >= top_k:
            break

    return out
