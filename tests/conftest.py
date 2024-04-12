import pytest

from app.src.model_handler import save_sbert_model, save_doc2vec_model

doc2vec_default_model_name = "my_doc2vec_model"
sbert_default_model_name = "distiluse-base-multilingual-cased-v1"
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"


@pytest.fixture(scope="session", autouse=True)
def doc2vec_model_save():
    save_doc2vec_model(doc2vec_default_model_name)


@pytest.fixture(scope="session", autouse=True)
def sbert_model_save():
    save_sbert_model(sbert_default_model_name)


@pytest.fixture(scope="session")
def single_docs_example():
    return "한 문서를 임베딩하여 스트링 형태로 받아볼 수 있습니다."


@pytest.fixture(scope="session")
def batch_docs_example():
    return [
        "임베딩을 진행할 텍스트입니다. 어떻게 임베딩되는지 확인해볼까요?",
        "여러 문서를 동시에 임베딩하여 리스트 형태로 받아볼 수 있습니다."
    ]
