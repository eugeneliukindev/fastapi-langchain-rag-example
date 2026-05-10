from langchain_ollama import ChatOllama

from config import settings

ollama_llm = ChatOllama(
    model=settings.llm.ollama.model,
    base_url=settings.llm.ollama.base_url,
)
