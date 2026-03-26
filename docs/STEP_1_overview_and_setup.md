# Step 1: Full Project Overview, Architecture, and Folder Setup

## Overview

This step defines what the AI data analyst agent is, why it needs both SQL and RAG, and how the project should be organized before implementation starts.

## Objective

- Understand the full system before writing code.
- Learn the major concepts used by the project.
- Set up the initial project folder structure and local development environment.

## Components Involved

- Python application layer
- SQLite database for structured sales data
- Business note text files for unstructured context
- LangChain tool-calling layer
- OpenAI models for reasoning and embeddings
- ChromaDB for semantic retrieval
- Streamlit for the user interface

## Architecture

```text
User Question
    |
    v
Streamlit UI or Terminal
    |
    v
Analyst Agent (LangChain + OpenAI)
    |
    +--> SQL Tool --> SQLite sales database
    |
    +--> RAG Tool --> Chroma vector store --> business notes
    |
    v
Grounded Final Answer
```

## Workflow

1. A user asks a natural-language business question.
2. The agent decides whether the question needs SQL, RAG, or both.
3. SQL handles structured questions about sales numbers.
4. RAG handles policy and note retrieval from business documents.
5. The agent combines the collected evidence and produces a grounded answer.

## Prerequisites

- Python 3.11 recommended
- OpenAI API key
- Terminal access
- Basic familiarity with running `python`, `pip`, and `streamlit`

## Commands Used

```bash
mkdir ai_data_analyst_agent
cd ai_data_analyst_agent
python3.11 -m venv .venv
source .venv/bin/activate
```

## Initial Folder Structure

```text
ai_data_analyst_agent/
|-- app.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- docs/
|-- data/
|   |-- sales.db
|   |-- business_notes/
|-- src/
|   |-- create_database.py
|   |-- build_vector_store.py
|   |-- db_utils.py
|   |-- rag_utils.py
|   |-- tools.py
|   |-- agent.py
```

## Outputs Produced

- A defined system architecture
- A clear learning roadmap
- A standard project layout for GitHub

## Troubleshooting Notes

- If Python 3.11 is missing, install it before creating the virtual environment.
- If package compatibility becomes difficult on Python 3.14, use Python 3.11 for this project.

## Terminology Learned

- Structured data
- Unstructured data
- SQL
- RAG
- Embeddings
- Vector database
- Agent
- Tool calling

## Summary

Step 1 turns the project from an idea into a concrete architecture. It establishes what each layer is responsible for and prepares the repository for implementation.
