# AI-Powered Data Analyst Agent

This project is a beginner-friendly but resume-ready AI application that answers business questions using both structured and unstructured data sources.

It combines:

- Python for the application logic
- SQLite and SQLAlchemy for structured sales data
- OpenAI for language reasoning and embeddings
- LangChain for tool calling and orchestration
- ChromaDB for vector search over business notes
- Streamlit for the user interface

## What the project does

A user asks a natural-language business question such as:

- "Which region generated the highest revenue?"
- "What does the refund policy say about onboarding issues?"
- "Which product had the most returns, and is there any note explaining why?"

The agent then decides whether it should:

1. query the SQLite database with SQL,
2. search business notes with RAG,
3. or use both paths together.

## Architecture Diagram

```text
User Question
    |
    v
Streamlit UI or Terminal
    |
    v
LangChain + OpenAI Analyst Agent
    |
    +--> SQL Tool --> SQL Generator --> SQLAlchemy --> SQLite sales.db
    |
    +--> RAG Tool --> OpenAI Embeddings --> ChromaDB --> business_notes/*.txt
    |
    v
Grounded Final Answer
```

## End-to-End Workflow

1. The user submits a business question.
2. The agent inspects the question and decides which tool or tools to call.
3. The SQL tool converts the question into a safe read-only SQL query and runs it on SQLite.
4. The RAG tool runs similarity search over embedded business notes stored in ChromaDB.
5. The agent combines the evidence from SQL, RAG, or both.
6. The final answer is returned in grounded natural language.

## Project Structure

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
|   |   |-- refund_policy.txt
|   |   |-- quarterly_summary.txt
|   |   |-- product_notes.txt
|-- src/
|   |-- create_database.py
|   |-- build_vector_store.py
|   |-- db_utils.py
|   |-- rag_utils.py
|   |-- tools.py
|   |-- agent.py
```

## Setup Instructions

### 1. Create and activate a virtual environment

Python 3.11 is recommended because the AI and vector database dependencies are more stable on it.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Create your environment file

```bash
cp .env.example .env
```

Then open `.env` and add your OpenAI API key.

### 4. Build the database

```bash
python src/create_database.py
```

### 5. Build the vector store

```bash
python src/build_vector_store.py
```

### 6. Start the app

```bash
streamlit run app.py
```

## Key Concepts

### Structured vs unstructured data

- Structured data fits into rows and columns. In this project, the sales table is structured data.
- Unstructured data is free-form text such as policy notes or quarterly summaries.

### SQL vs RAG

- SQL is best when the user needs numbers, filters, counts, comparisons, or aggregations.
- RAG is best when the user needs policy context, explanations, or text knowledge not stored in tables.

### What an AI agent is

An AI agent is an LLM-driven system that can decide what action to take next. In this project, the agent decides whether it needs SQL, RAG, or both.

### What tool calling is

Tool calling lets an LLM choose from predefined functions. Here, the model can call a SQL tool or a RAG tool instead of answering from memory.

### What embeddings are

Embeddings are numerical representations of text. Similar meanings produce similar vectors, which helps the system find relevant notes even when the wording changes.

### What a vector database is

A vector database stores embeddings and supports similarity search. ChromaDB helps this project retrieve the most relevant business note chunks for a question.

## Usage Examples

### SQL-only questions

- "Show total revenue by region."
- "Which product generated the most revenue?"
- "How many returned orders do we have?"

### RAG-only questions

- "What does the refund policy say about onboarding blockers?"
- "What are the Q2 priorities?"
- "What should sales mention for Dashboard Plus onboarding?"

### Hybrid questions

- "Which product had the most returns, and is there any note explaining why?"
- "Which region looks strongest, and what does the quarterly summary say about it?"

## Testing Guidance

### Terminal testing

```bash
python src/agent.py --question "Which region generated the highest revenue?"
```

### Interactive testing

```bash
python src/agent.py
```

### Streamlit testing

```bash
streamlit run app.py
```

## Troubleshooting

- Missing `OPENAI_API_KEY`: add it to `.env`.
- `sales.db` not found: run `python src/create_database.py`.
- Chroma store not found: run `python src/build_vector_store.py`.
- Import errors: confirm the virtual environment is activated and dependencies are installed.
- Weak answers: inspect the SQL query or retrieved documents in the app's debug expander.

## Future Improvements

- Add chat memory for follow-up questions
- Support CSV upload for custom datasets
- Add charts and visual analytics
- Move the backend to FastAPI
- Add Docker for deployment
- Add observability and evaluation
- Add authentication and guardrails
- Explore multi-agent orchestration

## Resume-Ready Project Summary

Built an AI-powered data analyst application that routes natural-language business questions across SQL analytics and RAG-based document retrieval, using LangChain, OpenAI, SQLite, SQLAlchemy, ChromaDB, and Streamlit.

## Suggested Resume Bullet Points

- Built an AI data analyst agent that converted natural-language business questions into grounded answers using SQL automation and retrieval-augmented generation.
- Designed a modular architecture with a SQLite sales database, Chroma vector store, LangChain tools, and a Streamlit interface.
- Implemented safe SQL generation, semantic document retrieval, and answer synthesis with OpenAI models.
