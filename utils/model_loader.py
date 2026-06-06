from joblib import load
#Loads model once and shares everywhere.
MODEL = load("models/stacking_model.joblib")
TRAINING_COLUMNS = load("models/training_columns.pkl")