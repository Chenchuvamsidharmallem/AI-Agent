"""Build the Chroma vector store from local business documents."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
NOTES_DIR = BASE_DIR / "data" / "business_notes"


def ensure_openai_api_key() -> None:
    """Raise a clear error when the OpenAI API key is missing."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )


def resolve_persist_directory() -> Path:
    """Return the configured Chroma persistence directory."""
    raw_path = os.getenv("CHROMA_PERSIST_DIRECTORY", "data/chroma_store")
    path = Path(raw_path)
    return path if path.is_absolute() else BASE_DIR / path


def load_documents() -> list[Document]:
    """Read all business note text files and wrap them as LangChain documents."""
    documents: list[Document] = []

    for file_path in sorted(NOTES_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")
        documents.append(
            Document(
                page_content=text,
                metadata={"source": file_path.name, "path": str(file_path)},
            )
        )

    if not documents:
        raise FileNotFoundError("No business note files were found in data/business_notes.")

    return documents


def build_vector_store() -> None:
    """Split documents, embed them, and persist them to Chroma."""
    ensure_openai_api_key()
    documents = load_documents()
    persist_directory = resolve_persist_directory()

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    split_documents = splitter.split_documents(documents)

    if persist_directory.exists():
        shutil.rmtree(persist_directory)

    embeddings = OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"))
    vector_store = Chroma(
        collection_name="business_notes",
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
    )
    vector_store.add_documents(split_documents)

    print(f"Loaded {len(documents)} source documents.")
    print(f"Created {len(split_documents)} chunks.")
    print(f"Vector store saved to: {persist_directory}")


if __name__ == "__main__":
    try:
        build_vector_store()
    except Exception as exc:
        print(f"Error: {exc}")
