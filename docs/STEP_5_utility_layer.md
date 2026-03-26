# Step 5: Utility Layer for Reusable Database and Retrieval Logic

## Overview

This step creates reusable helper functions so the rest of the system does not have to manage raw database or vector-store logic directly.

## Objective

- Separate low-level logic from agent orchestration.
- Add safe SQL validation and reusable retrieval helpers.

## Components Involved

- `src/db_utils.py`
- `src/rag_utils.py`

## Workflow

1. Add database connection helpers.
2. Add SQL prompt generation and validation.
3. Add SQL execution and result formatting.
4. Add Chroma loading and document retrieval helpers.

## Commands Used

No new build command is required for this step, but the utilities are used indirectly by the tool layer and agent layer.

## Outputs Produced

- Safe SQL-generation workflow
- Reusable RAG lookup functions
- Cleaner module boundaries

## Architecture Notes

This is a separation-of-concerns step. The utilities own the implementation details of SQL and retrieval, while higher layers only call them.

## Troubleshooting Notes

- If SQL generation fails, inspect the prompt and the returned query.
- If RAG lookup fails, confirm that the persisted Chroma store exists.

## Terminology Learned

- Utility module
- Separation of concerns
- Validation
- Reusable abstraction

## Summary

Step 5 makes the codebase easier to maintain and easier to explain because each layer has a focused responsibility.
