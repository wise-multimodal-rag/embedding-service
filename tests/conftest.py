import pytest

from app.src.model_handling import save_model

embedding_model_name = "distiluse-base-multilingual-cased-v1"


@pytest.fixture(scope="session", autouse=True)
def embedding_model_save():
    save_model(embedding_model_name)


@pytest.fixture(scope="session")
def single_docs_example():
    return "여러 문서를 동시에 임베딩하여 리스트 형태로 받아볼 수 있습니다."


@pytest.fixture(scope="session")
def batch_docs_example():
    return [
        "임베딩을 진행할 텍스트입니다. 어떻게 임베딩되는지 확인해볼까요?",
        "여러 문서를 동시에 임베딩하여 리스트 형태로 받아볼 수 있습니다."
    ]
