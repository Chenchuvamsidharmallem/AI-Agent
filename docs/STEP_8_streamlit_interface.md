# Step 8: Streamlit Interface

## Overview

This step adds the user-facing application layer.

## Objective

- Create a simple interface for asking business questions.
- Show answers and debugging details in one place.

## Components Involved

- `app.py`
- Streamlit

## Workflow

1. User enters a question in the chat input.
2. Streamlit calls the analyst agent.
3. The agent returns the final answer and evidence details.
4. The UI renders both the conversation and optional debug information.

## Commands Used

```bash
streamlit run app.py
```

## Outputs Produced

- Interactive web app
- Chat history in session state
- Tool-call and evidence details for debugging

## Architecture Notes

This step does not change the data logic. It adds a presentation layer on top of the existing agent workflow.

## Troubleshooting Notes

- If the app starts but answers fail, inspect the error shown in the chat window.
- If imports fail, make sure the virtual environment is active before launching Streamlit.

## Terminology Learned

- Front end
- Session state
- Chat interface
- Presentation layer

## Summary

Step 8 turns the backend workflow into a user-friendly demo application that is suitable for GitHub screenshots and project demos.
