import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_models", "knn_model.pkl")

class MLLoader:
    _instance = None
    model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLLoader, cls).__new__(cls)
            cls._instance.load_model()
        return cls._instance

    def load_model(self):
        
        if not os.path.exists(MODEL_PATH):
            return

        try:
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            
            if self.model is not None:
                print("ML model loaded successfully.")
            else:
                print("ML model is None after loading.")
                
        except Exception as e:
            print(f"Error loading ML model: {e}")
            self.model = None


ml_loader = MLLoader()
