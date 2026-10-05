import os
import sys

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

sys.path.append(".")
from preprocess import clean_text

df = pd.read_csv("data/notifications.csv")

# Include user feedback if it exists
if os.path.exists("data/feedback.csv"):
    fb = pd.read_csv("data/feedback.csv")
    df = pd.concat([df, fb, fb, fb], ignore_index=True)  # weight feedback higher
    print("Using", len(fb), "feedback rows")

df["clean"] = df["text"].apply(clean_text)

for target in ["category", "priority"]:
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df[target], test_size=0.2, random_state=42
    )
    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)),
        MultinomialNB(),
    )
    model.fit(X_train, y_train)
    print(f"\n=== {target.upper()} MODEL ===")
    print(classification_report(y_test, model.predict(X_test)))
    model.fit(df["clean"], df[target])  # final fit on all data
    joblib.dump(model, f"model/{target}_model.pkl")

print("Models saved in model/")