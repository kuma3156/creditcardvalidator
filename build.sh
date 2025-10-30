#!/usr/bin/env bash
set -e  # Exit on first error

# ===== CONFIG =====
LOCAL_RUN=true   # Always run locally with uvicorn
APP_MODULE="app.main:app"  # Adjust if your main FastAPI app is in a different file
HOST="127.0.0.1"
PORT="8000"

# ===== PYTHON BUILD & TEST =====
echo "🚀 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt pytest pytest-cov datamodel-code-generator uvicorn

echo "🧬 Generating OpenAPI models..."
datamodel-codegen --input openapi.yaml --input-file-type openapi --output ./app/models/generated_models

echo "🧪 Running tests with coverage..."
# Add project root to PYTHONPATH so 'app' imports work
export PYTHONPATH=$(pwd)
pytest --cov=app --cov-report=term-missing -v

# ===== RUN LOCAL SERVER =====
if [ "$LOCAL_RUN" = true ]; then
    echo "🚀 Starting FastAPI app locally with Uvicorn..."
    uvicorn $APP_MODULE --host $HOST --port $PORT --reload
fi

deactivate
