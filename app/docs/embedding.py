from app.models import EmbeddingRequest

embedding_single_normal_example = {
    "summary": "싱글 임베딩 기본 예제",
    "description": "한 문서를 임베딩하는 예제",
    "value": {
        "input": "임베딩을 진행할 텍스트입니다. 어떻게 임베딩되는지 확인해볼까요?",
        "model": "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
    }
}

embedding_batch_normal_example = {
    "summary": "배치 임베딩 기본 예제",
    "description": "여러 문서를 동시에 임베딩하는 예제",
    "value": EmbeddingRequest(
        input=[
            "임베딩을 진행할 텍스트입니다. 어떻게 임베딩되는지 확인해볼까요?",
            "여러 문서를 동시에 임베딩하여 리스트 형태로 받아볼 수 있습니다."
        ],
        model="snunlp/KR-SBERT-V40K-klueNLI-augSTS"
    )
}

embedding_examples = {
    "single_normal": embedding_single_normal_example,
    "batch_normal": embedding_batch_normal_example
}
