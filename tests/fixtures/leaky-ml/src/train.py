import pickle

from sklearn.linear_model import LogisticRegression

from config import CONFIG
from src.data import load_data, build_dataset


def train():
    df = load_data()
    X_tr, X_te, y_tr, y_te = build_dataset(df)
    model = LogisticRegression(max_iter=500)
    model.fit(X_tr, y_tr)
    score = model.score(X_te, y_te)  # accuracy only
    print(f"accuracy: {score:.4f}")
    with open(CONFIG["model_path"], "wb") as f:  # fixed path: runs clobber each other
        pickle.dump(model, f)
    return model, score


if __name__ == "__main__":
    train()
