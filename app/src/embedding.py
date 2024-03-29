from pathlib import Path
from typing import List, Literal

from sentence_transformers import SentenceTransformer

from app.src.exception.service import InvalidModelNameError, NonexistModelError
from app.src.model_handling import model_validator


@model_validator
def sbert_embedding(docs: List[str], embedding_model_name: str,
                    encoding_format: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32") -> List[float]:
    try:
        embedding_model = SentenceTransformer(str(Path("models").joinpath(embedding_model_name).resolve()))
    except ValueError:
        raise NonexistModelError(embedding_model_name)
    except OSError:
        raise InvalidModelNameError(embedding_model_name)
    # embedding
    embeddings = embedding_model.encode(
        sentences=docs, precision=encoding_format
    )
    return embeddings  # type: ignore
