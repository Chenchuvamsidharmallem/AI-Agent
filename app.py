"""Streamlit interface for the AI-powered data analyst agent."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.agent import AnalystAgent

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


@st.cache_resource
def load_agent() -> AnalystAgent:
    """Create one shared agent instance per Streamlit session."""
    return AnalystAgent()


def initialize_session_state() -> None:
    """Create session state containers the first time the app loads."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_sidebar() -> None:
    """Display quick project reminders in the sidebar."""
    st.sidebar.title("AI Data Analyst Agent")
    st.sidebar.markdown(
        """
        This demo answers business questions by combining:

        - SQL over a SQLite sales database
        - RAG over business and policy notes
        - A LangChain + OpenAI routing layer
        """
    )
    st.sidebar.markdown("**Setup checklist**")
    st.sidebar.code(
        "\n".join(
            [
                "1. Copy .env.example to .env",
                "2. Add your OPENAI_API_KEY",
                "3. Run python src/create_database.py",
                "4. Run python src/build_vector_store.py",
                "5. Start with streamlit run app.py",
            ]
        )
    )
    st.sidebar.markdown(f"Project root: `{BASE_DIR}`")


def render_chat_history() -> None:
    """Render the existing chat messages."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("details"):
                with st.expander("View tool usage details"):
                    st.json(message["details"])


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(page_title="AI Data Analyst Agent", layout="wide")
    initialize_session_state()
    render_sidebar()

    st.title("AI-Powered Data Analyst Agent")
    st.caption(
        "Ask business questions in natural language. The agent decides whether it "
        "needs SQL, policy retrieval, or both."
    )

    render_chat_history()

    question = st.chat_input("Ask a business question about sales or policies...")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        agent = load_agent()
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                result = agent.ask(question)
            st.markdown(result["final_answer"])
            with st.expander("View tool usage details"):
                st.json(
                    {
                        "tool_calls": result["tool_calls"],
                        "evidence": result["evidence"],
                    }
                )
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": result["final_answer"],
                "details": {
                    "tool_calls": result["tool_calls"],
                    "evidence": result["evidence"],
                },
            }
        )
    except Exception as exc:  # pragma: no cover - UI fallback
        error_message = f"Error: {exc}"
        with st.chat_message("assistant"):
            st.error(error_message)
        st.session_state.messages.append({"role": "assistant", "content": error_message})


if __name__ == "__main__":
    main()

