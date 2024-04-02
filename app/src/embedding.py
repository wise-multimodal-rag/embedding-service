import logging
from pathlib import Path
from typing import List, Literal

from sentence_transformers import SentenceTransformer

from app.src.exception.service import InvalidModelError, NotExistModelError
from app.src.model_handling import model_validator


@model_validator
def sbert_embedding(
        docs: List[str], embedding_model_name: str,
        encoding_format: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32") -> List[float]:
    try:
        model_path = str(Path("models").joinpath(embedding_model_name).resolve())
        logging.debug(f"{model_path=}")
        embedding_model = SentenceTransformer(model_path)
    except ValueError as ve:
        raise NotExistModelError(embedding_model_name, ve)
    except OSError as oe:
        raise InvalidModelError(embedding_model_name, oe)
    # embedding
    embeddings = embedding_model.encode(
        sentences=docs, precision=encoding_format
    )
    return embeddings  # type: ignore
