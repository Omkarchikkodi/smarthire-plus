import pandas as pd
import lightgbm as lgb
import pickle
import os

DATA_PATH = "ml/data/train_pairs.csv"
MODEL_PATH = "ml/models/ranker_lightgbm.pkl"

def main():
    print("Loading training data...")
    df = pd.read_csv(DATA_PATH)

    print("Preparing feature matrix...")
    FEATURES = ["cos_sim", "skill_overlap", "title_match"]
    TARGET = "label"

    X = df[FEATURES]
    y = df[TARGET]

    print("Computing resume-wise groups...")
    # group = number of job pairs per resume (required for ranking)
    groups = df.groupby("resume_id").size().tolist()

    # ================================
    # LightGBM Ranker (Optimized)
    # ================================
    print("Training LightGBM ranking model...")

    ranker = lgb.LGBMRanker(
        objective="lambdarank",
        boosting_type="gbdt",
        num_leaves=63,
        learning_rate=0.05,
        n_estimators=300,
        subsample=0.9,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=0.1,
        random_state=42,
    )

    ranker.fit(
        X, 
        y,
        group=groups,
        eval_at=[5, 10, 20],
    )

    os.makedirs("ml/models", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(ranker, f)

    print(f"\n✔ Model trained and saved to {MODEL_PATH}\n")


if __name__ == "__main__":
    main()
