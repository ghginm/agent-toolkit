import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

from config import CONFIG


def predict(df):
    """Inference path. NOTE: preprocessing duplicated here, not shared with training."""
    with open(CONFIG["model_path"], "rb") as f:
        model = pickle.load(f)
    num_cols = ["tenure_months", "monthly_spend", "support_tickets", "usage_score"]
    X = df[num_cols].copy()
    X["avg_spend_per_ticket"] = df["monthly_spend"] / (df["support_tickets"] + 1)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)          # fits on the *inference batch* — different transform than training
    probs = model.predict_proba(X)[:, 1]
    return (probs > CONFIG["score_threshold"]).astype(int)  # threshold hardcoded in config, never validated
