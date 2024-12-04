SUMMARY = "AI플랫폼팀 Embedding Service 🚀"
DESCRIPTION = "_클러스터 환경에서 MiniO에 저장된 모델을 사용하여 텍스트 임베딩 결과를 제공하는 서비스_ \n" \
              "- 현재 **On-Premise** 클러스터 환경의 공용 **MiniO**의 **'embeddings'** 버킷에 모델을 저장하여 사용이 가능하다. \n" \
              "- request body로 제공하는 모델명(`model`)은 버킷에 모델이 존재하는 경로 그대로 넣어주면 된다. \n" \
              "- huggingface에서 사용하는 모델명과 동일하게 넣어서 사용하면 된다. \n " \
              "- (ex) MiniO 모델 저장 경로: `embeddings/snunlp/KR-SBERT-V40K-klueNLI-augSTS` - model: `snunlp/KR-SBERT-V40K-klueNLI-augSTS`"

LICENSE_INFO = {
    "name": "Wisenut"
}
