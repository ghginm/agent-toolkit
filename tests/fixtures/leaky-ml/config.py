# Central config. Global mutable dict, shared by all scripts.
CONFIG = {
    "data_path": "data/churn.csv",
    "model_path": "output/model.pkl",   # every run overwrites this
    "test_size": 0.2,
    "random_state": 42,
    "score_threshold": 0.5,
}
