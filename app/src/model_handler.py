import logging
from pathlib import Path

import tensorflow_hub as hub
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import common_texts
from sentence_transformers import SentenceTransformer

from app.src.exception.service import NotExistModelError, InvalidModelError, UnknownError

default_model_dir = "models"


def embedding_model_validator(func):
    def wrapper(*args, **kwargs):
        # model path exist check
        if not Path(default_model_dir).exists():
            logging.warning(f"{default_model_dir} does not exist. Make directory.")
            Path(default_model_dir).mkdir()
        # model load check
        embedding_model_name = args[1]  # embedding model name
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            raise NotExistModelError(embedding_model_name, ve)
        except OSError as oe:
            raise InvalidModelError(embedding_model_name, oe)
        except Exception as exc:
            raise UnknownError(exc)

    return wrapper


def save_doc2vec_model(model_name):
    """단위테스트용 함수"""
    # model path exist check
    if not Path(default_model_dir).exists():
        logging.warning(f"{default_model_dir} does not exist. Make directory.")
        Path(default_model_dir).mkdir()
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(common_texts)]
    model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)
    model.save(str(Path(default_model_dir).joinpath(model_name).resolve()))


def load_use_model(model_url: str):
    """단위테스트용 함수"""
    # model path exist check
    if not Path(default_model_dir).exists():
        logging.warning(f"{default_model_dir} does not exist. Make directory.")
        Path(default_model_dir).mkdir()
    model = hub.load(model_url)
    return model


def save_sbert_model(model_name):
    """단위테스트용 함수"""
    # model path exist check
    if not Path(default_model_dir).exists():
        logging.warning(f"{default_model_dir} does not exist. Make directory.")
        Path(default_model_dir).mkdir()
    modelPath = f"{default_model_dir}/{model_name}"
    model = SentenceTransformer(model_name)
    model.save(modelPath)


def get_saved_model_path(model_name: str):
    model_resolve_path = str(Path(default_model_dir).joinpath(model_name).resolve())
    logging.debug(f"{model_resolve_path=}")
    return model_resolve_path
