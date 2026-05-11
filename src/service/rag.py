from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader

from core.ai.chain.ollama import chain
from core.ai.documents.text_splitter import splitter
from core.ai.embeddings.hf import hf_embeddings
from core.db.manager import SessionDep
from exception.rag import RagContentTypeException
from repo.rag import RagRepoDep
from tmp import create_tmp_file_from_bytes


class RagService:
    def __init__(self, session: SessionDep, repo: RagRepoDep):
        self.session = session
        self.repo = repo

    async def upload_pdf(self, file: UploadFile) -> None:
        if file.content_type != "application/pdf":
            raise RagContentTypeException

        file_bytes = await file.read()
        with create_tmp_file_from_bytes(file_bytes, "pdf") as tmp_file:
            documents = PyPDFLoader(tmp_file).load()
            for doc in documents:
                doc.metadata["filename"] = file.filename

            document_chunks = splitter.split_documents(documents)

            texts = [chunk.page_content for chunk in document_chunks]
            embeddings = hf_embeddings.embed_documents(texts)
            metadatas = [chunk.metadata for chunk in document_chunks]

            await self.repo.add_documents(
                texts=texts,
                embeddings=embeddings,
                metadatas=metadatas,
            )
            await self.session.commit()

    async def ask_pdf(self, query: str) -> str:
        embedding = hf_embeddings.embed_query(query)
        chunks = await self.repo.similar_documents(embedding)

        context = "\n\n".join(chunk.content for chunk in chunks)
        print(context)
        response = await chain.ainvoke(
            {
                "context": context,
                "query": query,
            }
        )
        return response
