from langchain_ollama import ChatOllama

from config import settings

ollama_llm = ChatOllama(
    model=settings.ai.llm.ollama.model,
    base_url=settings.ai.llm.ollama.base_url,
)
