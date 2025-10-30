#!/usr/bin/env bash
set -e  # Exit on first error

# ===== CONFIG =====
IMAGE_NAME="creditcardvalidatorapi"
TF_DIR="./terraform"
LOCAL_RUN=false   # Set to true to run Docker locally for testing

# ===== INPUT AWS KEYS =====
echo "Enter your AWS Access Key ID:"
read -r AWS_ACCESS_KEY_ID
echo "Enter your AWS Secret Access Key:"
read -rs AWS_SECRET_ACCESS_KEY
echo ""

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION="us-east-1"

# ===== PYTHON BUILD & TEST =====
echo "🚀 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt pytest pytest-cov datamodel-code-generator

echo "🧬 Generating OpenAPI models..."
datamodel-codegen --input openapi.yaml --input-file-type openapi --output ./app/models/generated_models

echo "🧪 Running tests with coverage..."
# Add project root to PYTHONPATH so 'app' imports work
export PYTHONPATH=$(pwd)
pytest --cov=app --cov-report=term-missing -v

deactivate

# ===== DOCKER BUILD =====
echo "🐳 Building Docker image locally..."
docker build -t "${IMAGE_NAME}:latest" .

if [ "$LOCAL_RUN" = true ]; then
    echo "✅ Running Docker container locally for testing..."
    docker run -d -p 8000:8000 "${IMAGE_NAME}:latest"
    sleep 5
    docker ps | grep "${IMAGE_NAME}" && echo "Container is running successfully!"
fi

# ===== TERRAFORM DEPLOY =====
echo "🌍 Deploying to AWS via Terraform..."
cd "${TF_DIR}"

terraform init
terraform fmt
terraform validate
terraform plan -out=tfplan
terraform apply -auto-approve tfplan

cd ..

echo "🎉 Deployment complete!"
