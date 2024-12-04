from typing import List, Literal

import tensorflow_hub as hub
from gensim.models.doc2vec import Doc2Vec
from sentence_transformers import SentenceTransformer

from app.schemas.models import EmbeddingResponse, EmbeddingData
from app.src.model_handler import embedding_model_validator, get_saved_model_path


def formatting_embedding_result(embeddings, model_name: str):
    """Formatting embedding result"""
    embedding_response = EmbeddingResponse(
        data=[EmbeddingData(embedding=emb, index=idx) for idx, emb in enumerate(embeddings)],
        model=model_name
    )
    return embedding_response


@embedding_model_validator
def doc2vec_embedding(docs: List[str], embedding_model_name: str):
    """Load model and embedding using doc2vec method"""
    # load model
    model_path = get_saved_model_path(embedding_model_name)
    model = Doc2Vec.load(model_path)
    # embedding
    vectors = []
    for doc in docs:
        vectors.append(model.infer_vector(doc.split()))  # pyright: ignore
    return vectors


@embedding_model_validator
def use_embedding(docs: List[str], embedding_model_name: str) -> List[List[float]]:
    """Load model and embedding using use method"""
    # load model
    model_path = get_saved_model_path(embedding_model_name)
    model = hub.load(model_path)
    # embedding
    sentence_embeddings = model(docs)  # pyright: ignore
    return sentence_embeddings.numpy().tolist()


@embedding_model_validator
def sbert_embedding(
        docs: List[str], embedding_model_name: str,
        encoding_format: Literal["float32", "int8", "uint8", "binary", "ubinary"] = "float32") -> List[float]:
    """Load model and Embedding"""
    model_path = get_saved_model_path(embedding_model_name)
    embedding_model = SentenceTransformer(model_path)
    embeddings = embedding_model.encode(
        sentences=docs, precision=encoding_format
    )
    return embeddings  # type: ignore
