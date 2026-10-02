import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import joblib
from preprocess import load_and_prepare

def train():
    df = load_and_prepare()

    y = df["won"]
    X = df.drop(columns=["won", "match_id"])

    model = RandomForestClassifier(n_estimators=200, random_state=42)

    # Dataset kecil -> pakai cross-validation daripada single train/test split
    if len(df) >= 5:
        scores = cross_val_score(model, X, y, cv=min(5, len(df)))
        print("Cross-validation scores:", scores)
        print("Rata-rata akurasi:", scores.mean())
    else:
        print("Dataset terlalu kecil untuk cross-validation, skip evaluasi.")

    # Train di seluruh data (karena data sedikit, kita pakai semua buat training final)
    model.fit(X, y)

    joblib.dump(model, "models/model.pkl")
    joblib.dump(list(X.columns), "models/columns.pkl")
    print("Model saved to models/model.pkl")

if __name__ == "__main__":
    train()