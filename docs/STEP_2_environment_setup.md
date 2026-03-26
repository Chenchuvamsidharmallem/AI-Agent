# Step 2: Local Environment and Configuration

## Overview

This step prepares the local Python environment, dependency list, secret management, and repository hygiene.

## Objective

- Install the project dependencies.
- Store secrets safely with `.env`.
- Keep the repository clean with `.gitignore`.

## Components Involved

- `requirements.txt`
- `.env.example`
- `.gitignore`

## Workflow

1. Create and activate the virtual environment.
2. Install the project packages.
3. Copy `.env.example` to `.env`.
4. Add the OpenAI API key and model configuration.

## Commands Used

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Outputs Produced

- Isolated Python environment
- Installed dependencies
- Local configuration file for API access

## Troubleshooting Notes

- If `pip install` fails, confirm the virtual environment is active.
- If `OPENAI_API_KEY` is missing, the agent and vector build scripts will stop with a clear error.

## Terminology Learned

- Virtual environment
- Dependency management
- Environment variables
- Secret management

## Summary

Step 2 makes the project runnable on a real machine and introduces the configuration layer that other modules depend on.
