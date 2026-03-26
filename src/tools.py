"""LangChain tools used by the analyst agent."""

from __future__ import annotations

from langchain.tools import tool

from src.db_utils import run_sql_analysis
from src.rag_utils import run_rag_lookup


@tool
def sql_analyst_tool(question: str) -> str:
    """Use for structured questions about revenue, sales trends, returns, segments, or products."""
    result = run_sql_analysis(question)
    return "\n".join(
        [
            "SQL Analysis Result",
            f"Question: {result['question']}",
            f"Reasoning: {result['reasoning']}",
            "SQL Query:",
            result["sql_query"],
            f"Row Count: {result['row_count']}",
            "Rows:",
            result["formatted_rows"],
        ]
    )


@tool
def policy_notes_tool(question: str) -> str:
    """Use for refund policy, quarterly notes, product guidance, and other unstructured business context."""
    result = run_rag_lookup(question)
    return "\n".join(
        [
            "RAG Retrieval Result",
            f"Question: {result['question']}",
            f"Document Count: {result['document_count']}",
            "Retrieved Notes:",
            result["formatted_documents"],
        ]
    )
