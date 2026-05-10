from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate(
    [
        SystemMessage("You are helpful assistant"),
    ],
)
