"""Agent layer that routes questions to SQL, RAG, or both tools."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.tools import policy_notes_tool, sql_analyst_tool

load_dotenv()


class AnalystAgent:
    """Simple tool-calling agent for business analytics questions."""

    def __init__(self) -> None:
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError(
                "OPENAI_API_KEY is missing. Copy .env.example to .env and add your key."
            )

        model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.tools = [sql_analyst_tool, policy_notes_tool]
        self.tool_map = {tool.name: tool for tool in self.tools}

    @property
    def routing_prompt(self) -> str:
        """System prompt for tool selection."""
        return """
You are an AI-powered business analyst.

Decide which tool or tools to call before answering:
- Use sql_analyst_tool for structured questions about numbers, totals, trends, rankings,
  regions, products, customer segments, sales reps, returns, and revenue.
- Use policy_notes_tool for refund policy, business notes, quarterly summaries,
  product guidance, and narrative context not stored in the database.
- Use both tools when the user needs quantitative data plus policy or note context.

Always gather evidence before the final answer.
Do not invent tool results.
If one tool fails, still use the other tool if it helps.
""".strip()

    @property
    def synthesis_prompt(self) -> str:
        """System prompt for answer generation after tool execution."""
        return """
You are preparing a grounded business answer for a user.

Rules:
- Use only the evidence provided.
- If SQL and RAG evidence both appear, combine them clearly.
- If the evidence is incomplete, say what is missing.
- Keep the answer concise but useful.
- End with a short 'Sources used' line that names the tools used.
""".strip()

    def plan_tool_calls(self, question: str):
        """Ask the model which tools should be used for the question."""
        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke(
            [SystemMessage(content=self.routing_prompt), HumanMessage(content=question)]
        )
        return response.tool_calls

    def fallback_tool_calls(self, question: str) -> list[dict[str, Any]]:
        """Choose a basic fallback route when the model returns no tool calls."""
        lowered_question = question.lower()
        policy_keywords = {
            "policy",
            "refund",
            "notes",
            "summary",
            "onboarding",
            "guidance",
            "quarterly",
        }
        sql_keywords = {
            "revenue",
            "sales",
            "count",
            "total",
            "average",
            "top",
            "region",
            "product",
            "returns",
        }

        use_policy = any(keyword in lowered_question for keyword in policy_keywords)
        use_sql = any(keyword in lowered_question for keyword in sql_keywords)

        fallback_calls = []
        if use_sql or not use_policy:
            fallback_calls.append({"name": "sql_analyst_tool", "args": {"question": question}})
        if use_policy:
            fallback_calls.append({"name": "policy_notes_tool", "args": {"question": question}})
        return fallback_calls

    def execute_tool_calls(self, tool_calls: list[dict[str, Any]], question: str) -> list[dict[str, Any]]:
        """Run the selected tools and collect their outputs."""
        if not tool_calls:
            tool_calls = self.fallback_tool_calls(question)

        evidence: list[dict[str, Any]] = []
        seen_calls: set[str] = set()

        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            args = tool_call.get("args", {}) or {"question": question}
            args.setdefault("question", question)

            dedupe_key = json.dumps({"name": tool_name, "args": args}, sort_keys=True)
            if dedupe_key in seen_calls:
                continue
            seen_calls.add(dedupe_key)

            tool = self.tool_map.get(tool_name)
            if tool is None:
                evidence.append(
                    {
                        "tool_name": tool_name,
                        "args": args,
                        "output": f"Tool '{tool_name}' is not registered in this project.",
                    }
                )
                continue

            try:
                output = tool.invoke(args)
            except Exception as exc:  # pragma: no cover - runtime fallback
                output = f"Tool execution error: {exc}"

            evidence.append({"tool_name": tool_name, "args": args, "output": output})

        return evidence

    def synthesize_answer(self, question: str, evidence: list[dict[str, Any]]) -> str:
        """Generate the final grounded answer from tool outputs."""
        evidence_text = "\n\n".join(
            [
                "\n".join(
                    [
                        f"Tool: {item['tool_name']}",
                        f"Arguments: {item['args']}",
                        f"Output:\n{item['output']}",
                    ]
                )
                for item in evidence
            ]
        )

        response = self.llm.invoke(
            [
                SystemMessage(content=self.synthesis_prompt),
                HumanMessage(
                    content=f"User question: {question}\n\nCollected evidence:\n{evidence_text}"
                ),
            ]
        )
        return response.content

    def ask(self, question: str) -> dict[str, Any]:
        """Run the full agent workflow for one business question."""
        tool_calls = self.plan_tool_calls(question)
        evidence = self.execute_tool_calls(tool_calls, question)
        final_answer = self.synthesize_answer(question, evidence)

        return {
            "question": question,
            "tool_calls": tool_calls,
            "evidence": evidence,
            "final_answer": final_answer,
        }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the AI data analyst agent.")
    parser.add_argument("--question", help="Ask one question and exit.")
    return parser.parse_args()


def run_terminal_chat() -> None:
    """Start an interactive terminal session for manual testing."""
    agent = AnalystAgent()
    print("AI Data Analyst Agent")
    print("Type a question, or type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        result = agent.ask(question)
        print("\nFinal Answer:")
        print(result["final_answer"])
        print("\nTool Calls:")
        for tool_call in result["tool_calls"]:
            print(tool_call)


def main() -> None:
    """Run either single-question mode or interactive mode."""
    try:
        args = parse_args()
        if args.question:
            agent = AnalystAgent()
            result = agent.ask(args.question)
            print(result["final_answer"])
            return

        run_terminal_chat()
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
