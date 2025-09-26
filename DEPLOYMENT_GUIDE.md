## Deployment Guide - Sustainable Supply Chain Optimizer

This guide outlines multiple deployment paths. Pick the one that matches your hackathon constraints and future goals.

### 1. Local (Fast) - Docker Compose
```bash
docker compose build
docker compose up -d
curl http://localhost:5000/health
```

### 2. Single Docker Image (Manual Run)
```bash
docker build -t supply-chain-optimizer:latest .
docker run --rm -p 5000:5000 \
  -e AWS_REGION=us-east-1 \
  -e STRANDS_API_KEY=$STRANDS_API_KEY \
  supply-chain-optimizer:latest
```

### 3. Push to Amazon ECR
```bash
AWS_REGION=us-east-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO=supply-chain-optimizer
aws ecr create-repository --repository-name $REPO || true
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker tag supply-chain-optimizer:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest
```

### 4. Run on AWS ECS (Fargate) - High Level
1. Create ECS Cluster
2. Register Task Definition using ECR image
3. Set environment variables in task (AWS_REGION, STRANDS_API_KEY, USE_AWS_AGENTCORE)
4. Create Service (Fargate) with Load Balancer mapping port 5000 → 80
5. Test endpoint `/health` then `/api/sustainability/test`

### 5. Kubernetes (EKS or any cluster)
Edit `deployment.yml`:
```yaml
data:
  api-key: <base64 STRANDS_API_KEY>
```
Apply:
```bash
kubectl apply -f deployment.yml
kubectl get pods
kubectl port-forward svc/supply-chain-optimizer-service 8080:80
curl http://localhost:8080/health
```

### 6. Lambda + API Gateway (Minimal Packaging)
If you want serverless:
1. Create Lambda Layer (optional) for dependencies.
2. Zip project core (exclude large dev files) or refactor API into a handler: `lambda_handler(event, context)`.
3. Use API Gateway HTTP API → Integrate with Lambda.
4. Map routes: `/api/sustainability/analyze`, `/health`.

### 7. (Planned) AWS AgentCore Integration
Current status: `orchestration/agentcore_adapter.py` provides a simulation layer.
To make it live when AgentCore SDK is accessible:
1. Install SDK (placeholder): `pip install aws-agentcore`
2. Replace placeholder import + implement `create_workflow`, `submit_run`, `poll_run`.
3. Add env vars:
```bash
USE_AWS_AGENTCORE=1
AGENTCORE_PROJECT_NAME=supply-chain-optimizer
AGENTCORE_REGION=us-east-1
```
4. Expose new endpoint: (planned) `POST /api/agentcore/analyze`.

### 8. Environment Variables
| Variable | Purpose | Default |
|----------|---------|---------|
| AWS_REGION | AWS service region | us-east-1 |
| STRANDS_API_KEY | Strands Agents access | (none) |
| USE_AWS_AGENTCORE | Toggle AgentCore adapter | 0 |
| AGENTCORE_PROJECT_NAME | Logical workflow namespace | supply-chain-optimizer |
| AGENTCORE_WORKFLOW_ID | Pre-created workflow id | (empty) |

### 9. Health + Smoke Tests
```bash
curl http://localhost:5000/health
curl http://localhost:5000/api/sustainability/test
```

### 10. Production Hardening Checklist
- Add WAF / rate limiting (API Gateway / ALB)
- Add CloudWatch log retention + metrics
- Add tracing (X-Ray / OpenTelemetry)
- Externalize secrets to AWS Secrets Manager
- Add CI pipeline (GitHub Actions) building + pushing image + scanning

### 11. CI/CD (GitHub Actions Skeleton)
```yaml
name: build-and-push
on: [push]
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - name: Login to ECR
        run: |
          aws ecr get-login-password --region us-east-1 | \
          docker login --username AWS --password-stdin ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com
      - name: Build
        run: docker build -t supply-chain-optimizer:latest .
      - name: Tag & Push
        run: |
          docker tag supply-chain-optimizer:latest ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/supply-chain-optimizer:latest
          docker push ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/supply-chain-optimizer:latest
```

### 12. Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| 404 /favicon.ico | Favicon missing | Ignore or add file |
| Bedrock errors | Missing credentials or permission | Export AWS creds & IAM policy |
| Strands fallback message | SDK not installed / key missing | Set STRANDS_API_KEY |
| AgentCore not used | Env flag off or SDK absent | Set USE_AWS_AGENTCORE=1 |

---
Need an automated script for one-click deployment? Ask to generate `deploy.sh` or a GitHub Actions workflow extension.
