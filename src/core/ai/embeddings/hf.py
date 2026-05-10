from langchain_huggingface import HuggingFaceEmbeddings

from config import settings

hf_embeddings = HuggingFaceEmbeddings(
    model_name=settings.ai.embedding.hf.model,
    model_kwargs={
        "device": settings.ai.embedding.hf.device,
    },
)
