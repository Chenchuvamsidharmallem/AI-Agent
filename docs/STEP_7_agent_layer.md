# Step 7: Agent Layer and Grounded Answer Synthesis

## Overview

This step creates the reasoning layer that decides whether to use SQL, RAG, or both.

## Objective

- Route the user question intelligently.
- Execute the selected tools.
- Synthesize a grounded final answer.

## Components Involved

- `src/agent.py`
- LangChain `bind_tools`
- OpenAI chat model

## Workflow

1. Send the user question and available tools to the model.
2. Read the returned tool calls.
3. Execute each selected tool.
4. Send the tool outputs into a synthesis prompt.
5. Return the final grounded response.

## Commands Used

Single question:

```bash
python src/agent.py --question "Which product had the most returns?"
```

Interactive mode:

```bash
python src/agent.py
```

## Outputs Produced

- Tool-call plan
- Evidence collected from tools
- Final grounded answer

## Architecture Notes

This is the orchestration layer. It does not store data itself. Its job is to choose the right path and combine evidence safely.

## Troubleshooting Notes

- If no tool calls appear, inspect the routing prompt or fallback heuristics.
- If one tool fails, the current implementation records the error and still allows synthesis.

## Terminology Learned

- Agent reasoning
- Routing
- Orchestration
- Grounded answer

## Summary

Step 7 is the core AI behavior of the project. It is the layer that makes the application feel like an intelligent analyst rather than a simple database script.
