# Credit Card Validator

**Author:** Kumaresh Easwaran

## Description
A FastAPI-based Credit Card Validator API that uses the Luhn algorithm to verify card numbers, identify card schemes (Visa, MasterCard, Amex), and provide error handling for invalid input.

---

## Table of Contents
- [Design](#design)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Design
The credit card validator API is based on a simple microservices pattern
that takes advantage of Python's FastAPI framework, with a EC2/docker infrastructure
to support it's deployment.

### Why FastAPI?
The reason for using FastAPI rather than a more robust framework is due to the scope
of the problem. Since we don't require the robust features of frameworks such as Django or Spring
and are more focused a incremental microservice that can deploy fast we aimed to use FastAPI.
In terms of development, we opted for a more contract based design generating our models/api
using OpenAPI provided services in order to ensure we adhere to a proper schema and maintain
consistency through our responses. Lastly, in terms of infra we make use of EC2 instance
for our docker containers deployed through Github CI/CD to support a simple architecture.
Preferably we'd like to use K8s to host our container clusters, however due to the small
scope we believe that EC2 is the right fit in terms of cost of compute.

---

## Features
- Validate credit card numbers using the Luhn algorithm
- Detect card scheme (Visa, MasterCard, Amex)
- Returns proper error responses for invalid cards
- Fully tested endpoints
- Can run locally or deployed via Docker/AWS

---

## Requirements
- Python 3.14+
- pip
- Docker (optional for containerized deployment)
- Terraform (optional for AWS deployment)

---

## Installation
```bash
# Clone the repo
git clone https://github.com/yourusername/project-name.git
cd project-name

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

or

chmod +x build.sh
./build.sh to run/build project
```
---

## Usage

### Run locally

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Example `curl` request

```bash
curl -X POST http://127.0.0.1:8000/api/validate \
     -H "Content-Type: application/json" \
     -d '{"number": "4111111111111111"}'
```

---

## Testing

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=term-missing -v
```

---

## API Endpoints

* **POST /api/validate** – Validate a credit card
  Request body:

  ```json
  { "number": "4111111111111111" }
  ```

  Response (valid card):

  ```json
  { "valid": true, "scheme": "visa", "message": "OK" }
  ```

  Response (invalid card):

  ```json
  { "code": "400", "error_message": "Credit card number must be 12-19 digits" }
  ```

* **GET /health** – Check API health
  Response:

  ```json
  { "status": "ok" }
  ```

---

## Deployment

### 1. Docker Deployment (Local / Server)

```bash
# Build the Docker image
docker build -t creditcardvalidatorapi .

# Run the Docker container
docker run -d -p 8000:8000 creditcardvalidatorapi

# Verify the container is running
docker ps
```

* The API will now be accessible at: `http://localhost:8000`
* Health check:

```bash
curl http://localhost:8000/health
```

### 2. AWS EC2 Deployment (via Terraform)

1. **Set AWS credentials as environment variables:**

```bash
export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="us-east-1"
```

2. **Navigate to the Terraform directory:**

```bash
cd terraform
```

3. **Initialize Terraform:**

```bash
terraform init
```

4. **Format and validate Terraform files:**

```bash
terraform fmt
terraform validate
```

5. **Plan the deployment:**

```bash
terraform plan -out=tfplan
```

6. **Apply the plan:**

```bash
terraform apply -auto-approve tfplan
```

* Terraform will create an EC2 instance, security groups, and deploy your Docker container with the API.
* The output will include the public IP of the EC2 instance.
* Health check example:

```bash
curl http://<EC2_PUBLIC_IP>:8000/health
```

### 3. GitHub Actions Deployment (Optional)

* Push to `main` branch triggers:

  1. Python build & tests
  2. Docker image build
  3. Terraform deployment to AWS
* Make sure **AWS credentials** are stored in GitHub Secrets:

  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY`
* Note when deploying, please wait 2-3 minutes once complete to give time to ec2 to execute docker commands

---

## Contributing

* Fork the repository
* Create a feature branch
* Submit pull requests for review