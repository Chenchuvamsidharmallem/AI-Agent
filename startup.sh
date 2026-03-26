#!/usr/bin/env bash
set -euo pipefail

echo "Bootstrapping runtime assets..."
python src/bootstrap.py

echo "Starting Streamlit on port ${PORT:-8000}..."
exec python -m streamlit run app.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT:-8000}" \
  --server.headless true
