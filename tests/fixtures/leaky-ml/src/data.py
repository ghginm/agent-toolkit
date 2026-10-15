import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from config import CONFIG


def load_data():
    df = pd.read_csv(CONFIG["data_path"])
    # monthly usage; 'month' column defines time order of records
    df = df.sort_values("month").reset_index(drop=True)
    df = df.fillna(0)  # blanket imputation, silently drops the NaN signal
    return df


def build_dataset(df):
    num_cols = ["tenure_months", "monthly_spend", "support_tickets", "usage_score"]
    X = df[num_cols].copy()
    X["avg_spend_per_ticket"] = df["monthly_spend"] / (df["support_tickets"] + 1)
    y = df["churned_next_month"]

    # NOTE: scaling everything first for convenience
    scaler = StandardScaler()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=CONFIG["test_size"], random_state=CONFIG["random_state"]
    )  # shuffle=True default on time-ordered data
    return X_tr, X_te, y_tr, y_te
