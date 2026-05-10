from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful assistant that answers questions based strictly on the provided context. "
            "If the answer cannot be found in the context, say that you don't know. "
            "Do not make up information or use knowledge outside the context.",
        ),
        ("user", "Context: {context}\nQuery: {query}"),
    ],
    input_variables=["context", "query"],
)
