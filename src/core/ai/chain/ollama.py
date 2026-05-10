from langchain_core.output_parsers import StrOutputParser

from core.ai.llm.ollama import ollama_llm
from core.ai.prompt.prompt_template import prompt_template

chain = prompt_template | ollama_llm | StrOutputParser()
