from numpy import ndarray

from app.src.embedding import sbert_embedding
from tests.conftest import embedding_model_name


def test_sbert_embedding_single(single_docs_example):
    embeddings = sbert_embedding(single_docs_example, embedding_model_name)
    assert isinstance(embeddings, ndarray)
    assert all(-1 <= embedding <= 1 for embedding in embeddings)


def test_sbert_embedding_batch(batch_docs_example):
    embeddings = sbert_embedding(batch_docs_example, embedding_model_name)
    assert isinstance(embeddings, ndarray)
    assert isinstance(embeddings[0], ndarray)
    assert all(-1 <= em <= 1 for embedding in embeddings for em in embedding)
