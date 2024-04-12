import pytest
from numpy import ndarray

from app.src.embedding import sbert_embedding, doc2vec_embedding, use_embedding
from tests.conftest import sbert_default_model_name, doc2vec_default_model_name


@pytest.mark.skip("모델 저장 이슈로 일단 스킵")
def test_use_embedding_batch(batch_docs_example):
    embeddings = use_embedding(batch_docs_example, "use-model")
    print(embeddings)
    assert isinstance(embeddings, list)


def test_doc2vec_embedding_batch(batch_docs_example):
    embeddings = doc2vec_embedding(batch_docs_example, doc2vec_default_model_name)
    assert isinstance(embeddings, list)
    assert isinstance(embeddings[0], ndarray)


def test_sbert_embedding_single(single_docs_example):
    embeddings = sbert_embedding(single_docs_example, sbert_default_model_name)
    assert isinstance(embeddings, ndarray)
    assert all(-1 <= embedding <= 1 for embedding in embeddings)


def test_sbert_embedding_batch(batch_docs_example):
    embeddings = sbert_embedding(batch_docs_example, sbert_default_model_name)
    assert isinstance(embeddings, ndarray)
    assert isinstance(embeddings[0], ndarray)
    assert all(-1 <= em <= 1 for embedding in embeddings for em in embedding)
