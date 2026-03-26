"""Database helper functions for safe SQL generation and execution."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
BLOCKED_SQL_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "ATTACH",
    "PRAGMA",
    "VACUUM",
    "REINDEX",
}


class SQLGenerationResult(BaseModel):
    """Structured output returned by the SQL-generation model."""

    reasoning: str = Field(description="Short explanation of why this query answers the question.")
    sql_query: str = Field(description="A single read-only SQLite query.")


def resolve_database_url() -> str:
    """Return the configured database URL, or a sensible default."""
    default_path = BASE_DIR / "data" / "sales.db"
    return os.getenv("DATABASE_URL", f"sqlite:///{default_path.as_posix()}")


def get_engine():
    """Create a SQLAlchemy engine for the project database."""
    return create_engine(resolve_database_url())


def ensure_openai_api_key() -> None:
    """Raise a clear error when the OpenAI API key is missing."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError(
            "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
        )


def get_sales_schema_description() -> str:
    """Describe the sales table for prompt grounding."""
    return """
Table: sales

Columns:
- id: integer primary key
- order_date: text in YYYY-MM-DD format
- region: sales region such as North, South, East, West
- product_name: sold product name
- category: product category
- sales_rep: account owner
- customer_segment: SMB, Mid-Market, or Enterprise
- units_sold: number of units sold
- unit_price: price per unit before discount
- discount_pct: decimal discount such as 0.10 for 10 percent
- total_revenue: final revenue after discount
- returned: boolean where 1 means returned and 0 means not returned
- return_reason: optional text reason for returned orders

Rules:
- Only query the sales table.
- Use read-only SQL.
- Prefer total_revenue for revenue questions.
- Use COUNT(*) for counts and AVG(...) for averages.
- For ranking questions, use ORDER BY with LIMIT.
- For return analysis, returned = 1 means true.
""".strip()


def generate_sql_query(question: str) -> SQLGenerationResult:
    """Use an LLM to convert a business question into SQL."""
    ensure_openai_api_key()

    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    llm = ChatOpenAI(model=model_name, temperature=0)
    structured_llm = llm.with_structured_output(SQLGenerationResult)

    prompt = f"""
You are a careful SQL analyst working with SQLite.
Create exactly one read-only SQL query that answers the user's question.

Schema:
{get_sales_schema_description()}

Safety rules:
- Return only a SELECT query or a WITH...SELECT query.
- Never modify the database.
- Do not reference tables or columns outside the provided schema.
- Use SQLite-compatible SQL.
- Keep the query easy to read.

User question:
{question}
""".strip()

    return structured_llm.invoke(prompt)


def validate_sql_query(sql_query: str) -> str:
    """Reject unsafe or malformed SQL before execution."""
    cleaned_query = sql_query.strip().rstrip(";")
    upper_query = cleaned_query.upper()

    if ";" in cleaned_query:
        raise ValueError("Only single-statement SQL queries are allowed.")

    if not (upper_query.startswith("SELECT") or upper_query.startswith("WITH")):
        raise ValueError("Only read-only SELECT queries are allowed.")

    blocked_terms = [keyword for keyword in BLOCKED_SQL_KEYWORDS if keyword in upper_query]
    if blocked_terms:
        raise ValueError(f"Unsafe SQL detected. Blocked terms: {', '.join(blocked_terms)}")

    return cleaned_query


def execute_sql_query(sql_query: str) -> list[dict[str, Any]]:
    """Run a validated SQL query and return rows as dictionaries."""
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(text(sql_query))
        rows = result.mappings().all()
        return [dict(row) for row in rows]


def format_sql_rows(rows: list[dict[str, Any]]) -> str:
    """Convert query rows into a readable plain-text block."""
    if not rows:
        return "No rows were returned."

    formatted_lines = []
    for index, row in enumerate(rows, start=1):
        formatted_lines.append(f"Row {index}: {row}")
    return "\n".join(formatted_lines)


def run_sql_analysis(question: str) -> dict[str, Any]:
    """Generate SQL, validate it, execute it, and package the result."""
    sql_plan = generate_sql_query(question)
    safe_query = validate_sql_query(sql_plan.sql_query)
    rows = execute_sql_query(safe_query)

    return {
        "question": question,
        "reasoning": sql_plan.reasoning,
        "sql_query": safe_query,
        "row_count": len(rows),
        "rows": rows,
        "formatted_rows": format_sql_rows(rows),
    }
