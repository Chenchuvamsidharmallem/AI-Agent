"""RAG helper functions for retrieving business notes from Chroma."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]


def resolve_chroma_directory() -> Path:
    """Return the configured Chroma persistence directory."""
    raw_path = os.getenv("CHROMA_PERSIST_DIRECTORY", "data/chroma_store")
    path = Path(raw_path)
    return path if path.is_absolute() else BASE_DIR / path


def ensure_openai_api_key() -> None:
    """Raise a clear error when the OpenAI API key is missing."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )


def load_vector_store() -> Chroma:
    """Load the persisted Chroma collection from disk."""
    ensure_openai_api_key()
    persist_directory = resolve_chroma_directory()

    if not persist_directory.exists():
        raise FileNotFoundError(
            "Chroma vector store not found. Run python src/build_vector_store.py first."
        )

    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    return Chroma(
        collection_name="business_notes",
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
    )


def retrieve_business_notes(question: str, top_k: int | None = None):
    """Run similarity search against the business notes collection."""
    vector_store = load_vector_store()
    limit = top_k or int(os.getenv("TOP_K_RESULTS", "3"))
    return vector_store.similarity_search(question, k=limit)


def format_retrieved_documents(documents) -> str:
    """Convert retrieved documents into a readable text block."""
    if not documents:
        return "No relevant business notes were retrieved."

    blocks = []
    for index, document in enumerate(documents, start=1):
        blocks.append(
            "\n".join(
                [
                    f"Document {index}",
                    f"Source: {document.metadata.get('source', 'unknown')}",
                    f"Content: {document.page_content.strip()}",
                ]
            )
        )
    return "\n\n".join(blocks)


def run_rag_lookup(question: str) -> dict[str, Any]:
    """Retrieve relevant documents and package them for downstream prompts."""
    documents = retrieve_business_notes(question)

    return {
        "question": question,
        "document_count": len(documents),
        "documents": [
            {
                "source": document.metadata.get("source", "unknown"),
                "content": document.page_content,
            }
            for document in documents
        ],
        "formatted_documents": format_retrieved_documents(documents),
    }
