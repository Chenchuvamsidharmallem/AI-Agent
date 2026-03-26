"""Bootstrap runtime assets before starting the deployed application."""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.build_vector_store import build_vector_store, resolve_persist_directory
from src.create_database import create_database, resolve_database_path

load_dotenv()


def ensure_runtime_assets() -> None:
    """Create the SQLite database and Chroma store only when they are missing."""
    database_path = resolve_database_path()
    if database_path.exists():
        print(f"Database already available at: {database_path}")
    else:
        print("Database not found. Creating SQLite database...")
        create_database(overwrite=False)

    persist_directory = resolve_persist_directory()
    chroma_file = persist_directory / "chroma.sqlite3"
    if chroma_file.exists():
        print(f"Chroma vector store already available at: {persist_directory}")
    else:
        persist_directory.parent.mkdir(parents=True, exist_ok=True)
        print("Vector store not found. Building Chroma vector store...")
        build_vector_store()


if __name__ == "__main__":
    ensure_runtime_assets()
