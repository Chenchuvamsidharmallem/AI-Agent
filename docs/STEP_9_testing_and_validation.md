# Step 9: Testing and Validation

## Overview

This step explains how to manually validate the SQL path, the RAG path, and the hybrid path.

## Objective

- Confirm that each layer works independently.
- Confirm that the full end-to-end flow works together.

## Components Involved

- `src/create_database.py`
- `src/build_vector_store.py`
- `src/agent.py`
- `app.py`

## Workflow

1. Build the database.
2. Build the vector store.
3. Test SQL-only questions.
4. Test RAG-only questions.
5. Test hybrid questions.
6. Inspect tool outputs when answers look wrong.

## Commands Used

```bash
python src/create_database.py
python src/build_vector_store.py
python src/agent.py --question "Show total revenue by region."
python src/agent.py --question "What does the refund policy say about onboarding blockers?"
python src/agent.py --question "Which product had the most returns, and do the notes explain why?"
streamlit run app.py
```

## Outputs Produced

- Validated SQL answers
- Validated RAG answers
- Validated hybrid answers

## Sample Questions

- SQL only: "Which region generated the highest total revenue?"
- SQL only: "How many returned orders were recorded?"
- RAG only: "What is the refund timeline for enterprise customers?"
- RAG only: "What is the Q2 priority for Dashboard Plus?"
- Hybrid: "Which product has return issues, and is there any note explaining the cause?"

## Troubleshooting Notes

- If SQL answers are wrong, inspect the generated query.
- If RAG answers are weak, inspect the retrieved note chunks.
- If both layers work independently but the final answer is poor, adjust the synthesis prompt.

## Terminology Learned

- Validation
- Debugging
- Test prompt
- Hybrid query

## Summary

Step 9 teaches how to verify the system like an engineer instead of assuming the agent is correct because it sounds fluent.
