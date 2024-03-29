from pathlib import Path

from sentence_transformers import SentenceTransformer

model_path = "./models"


def save_model(model_name):
    modelPath = f"{model_path}/{model_name}"
    model = SentenceTransformer(model_name)
    model.save(modelPath)


def model_validator(func):
    def wrapper(*args, **kwargs):
        if not Path(model_path).exists():
            Path(model_path).mkdir()
        return func(*args, **kwargs)

    return wrapper
