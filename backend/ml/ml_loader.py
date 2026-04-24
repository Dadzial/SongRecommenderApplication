import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "knn_model.pkl")

class MLLoader:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                print("Model KNN was loaded.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f" Warning {MODEL_PATH}")

ml_loader = MLLoader()
