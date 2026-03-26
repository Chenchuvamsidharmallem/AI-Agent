# Step 4: Document Knowledge Layer with RAG and ChromaDB

## Overview

This step adds the unstructured knowledge layer for policies, summaries, and product notes.

## Objective

- Create sample business documents.
- Convert them into embeddings.
- Store them in a Chroma vector database.

## Components Involved

- `data/business_notes/*.txt`
- `src/build_vector_store.py`
- OpenAI embeddings
- ChromaDB

## Workflow

1. Write business notes as text files.
2. Load the files as LangChain documents.
3. Split long text into chunks.
4. Create embeddings for each chunk.
5. Save the embedded chunks into ChromaDB.

## Commands Used

```bash
python src/build_vector_store.py
```

## Outputs Produced

- Business note text files
- Persisted Chroma vector store in `data/chroma_store`

## Architecture Notes

This layer gives the project access to semantic search. It is used when the user asks for context that is not stored in SQL tables.

## Troubleshooting Notes

- If the build script fails, verify `OPENAI_API_KEY` is present.
- If the vector store directory is missing later, rerun the build script.

## Terminology Learned

- RAG
- Embedding
- Chunking
- Similarity search
- Vector store

## Summary

Step 4 enables semantic retrieval, which is how the project answers note-based and policy-based questions.
