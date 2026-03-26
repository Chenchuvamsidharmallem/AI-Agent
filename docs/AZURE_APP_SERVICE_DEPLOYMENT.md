# Azure Deployment Guide

## Recommended Azure Target

Deploy this project to **Azure App Service on Linux**.

This is the simplest fit for the current repository because:

- the app is a standard Python project with `requirements.txt`
- Azure App Service can install Python dependencies automatically
- the project only needs a custom startup command for Streamlit
- the Azure portal can connect directly to the existing GitHub repository

## Why This Project Needs a Custom Startup Command

Azure App Service auto-detects Flask and Django apps, but this project is a Streamlit app. Because of that, Azure needs an explicit startup command.

This repository includes a deployment startup script:

```bash
bash startup.sh
```

The script:

1. ensures the SQLite database exists
2. ensures the Chroma vector store exists
3. starts Streamlit on the Azure-provided port

## Required Azure App Settings

Set these in **Azure Portal > App Service > Settings > Configuration > Application settings**:

- `OPENAI_API_KEY`
- `OPENAI_MODEL=gpt-4o-mini`
- `EMBEDDING_MODEL=text-embedding-3-small`
- `DATABASE_URL=sqlite:////home/data/ai_data_analyst_agent/sales.db`
- `CHROMA_PERSIST_DIRECTORY=/home/data/ai_data_analyst_agent/chroma_store`
- `TOP_K_RESULTS=3`
- `WEBSITES_ENABLE_APP_SERVICE_STORAGE=true`

## Required Azure General Settings

Under **Azure Portal > App Service > Settings > Configuration > General settings**:

- Runtime stack: `Python 3.11`
- Startup Command: `bash startup.sh`

## Deployment Flow

### Option 1: Deploy from GitHub in Azure Portal

1. Create a new **Web App** in Azure.
2. Choose:
   - Publish: `Code`
   - Runtime stack: `Python 3.11`
   - Operating System: `Linux`
3. After the app is created, open **Deployment Center**.
4. Choose **GitHub** as the source.
5. Connect the repository:
   - Organization: your GitHub account
   - Repository: `AI-Agent`
   - Branch: `main`
6. Save the deployment settings.
7. Open **Configuration** and add the app settings listed above.
8. Set **Startup Command** to `bash startup.sh`.
9. Restart the app.

### Option 2: Deploy with Azure CLI

If Azure CLI is installed locally, the flow is:

```bash
az login
az group create --name ai-agent-rg --location eastus
az appservice plan create --name ai-agent-plan --resource-group ai-agent-rg --sku B1 --is-linux
az webapp create --resource-group ai-agent-rg --plan ai-agent-plan --name <your-app-name> --runtime "PYTHON|3.11"
az webapp config set --resource-group ai-agent-rg --name <your-app-name> --startup-file "bash startup.sh"
az webapp config appsettings set --resource-group ai-agent-rg --name <your-app-name> --settings \
OPENAI_API_KEY="<your-key>" \
OPENAI_MODEL="gpt-4o-mini" \
EMBEDDING_MODEL="text-embedding-3-small" \
DATABASE_URL="sqlite:////home/data/ai_data_analyst_agent/sales.db" \
CHROMA_PERSIST_DIRECTORY="/home/data/ai_data_analyst_agent/chroma_store" \
TOP_K_RESULTS="3" \
WEBSITES_ENABLE_APP_SERVICE_STORAGE="true"
```

Then configure deployment from GitHub in the portal or use ZIP deployment.

## What Happens on First Startup

On the first successful deployment:

1. `startup.sh` runs
2. `src/bootstrap.py` checks for `sales.db`
3. if missing, it runs `src/create_database.py`
4. it checks for `chroma.sqlite3`
5. if missing, it runs `src/build_vector_store.py`
6. Streamlit starts and serves the app

## Important Operational Notes

- The first startup may take longer because embeddings must be created.
- OpenAI billing and quota must be active, or the vector-store build will fail.
- This deployment keeps SQLite and Chroma data under `/home/data/...`, which is the persistent storage path intended for Linux App Service.
- If you redeploy and keep the same persistent storage, the app should not need to rebuild the database or embeddings unless those files are deleted.

## Troubleshooting

- `401 invalid_api_key`: the `OPENAI_API_KEY` value in Azure App Settings is wrong.
- `429 insufficient_quota`: the OpenAI project has no remaining quota.
- Streamlit starts but shows default Azure page: the startup command was not set correctly.
- Startup loops: check App Service log stream to confirm whether the bootstrap step is failing.
- Repeated vector-store rebuilds: confirm `WEBSITES_ENABLE_APP_SERVICE_STORAGE=true` and the Chroma path is under `/home`.
