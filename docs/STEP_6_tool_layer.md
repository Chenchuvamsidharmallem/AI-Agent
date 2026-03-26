# Step 6: Tool Layer with LangChain Tools

## Overview

This step wraps the SQL and RAG workflows as tools that the language model can call.

## Objective

- Turn the utility functions into named tools.
- Give the LLM clear choices for structured and unstructured retrieval.

## Components Involved

- `src/tools.py`
- LangChain `@tool`

## Workflow

1. Create a SQL tool that accepts a business question.
2. Create a RAG tool that accepts a business question.
3. Return readable tool output that can be passed into a final answer prompt.

## Commands Used

Example test command:

```bash
python -m src.agent --question "Show total revenue by region."
```

## Outputs Produced

- `sql_analyst_tool`
- `policy_notes_tool`

## Architecture Notes

This step is where the project becomes agent-friendly. The model is no longer forced to answer directly; it can decide to call one of the available tools.

## Troubleshooting Notes

- If the wrong tool is selected, improve the tool descriptions or routing prompt.
- If the SQL tool works but the RAG tool fails, verify the vector store build step completed.

## Terminology Learned

- Tool
- Tool description
- Tool invocation
- Tool output

## Summary

Step 6 creates the action layer the agent can use. This is a key shift from plain prompting to tool-augmented reasoning.
