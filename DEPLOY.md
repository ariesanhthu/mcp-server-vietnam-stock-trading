# Hướng dẫn Deploy vnstock-mcp-server lên Cloud

## Tổng quan

vnstock-mcp-server hỗ trợ deploy lên các cloud platforms với Docker. Server hỗ trợ 3 transport modes:

- **stdio**: Cho desktop MCP clients
- **sse**: Server-Sent Events (phù hợp cho web apps và cloud)
- **streamable-http**: HTTP streaming (phù hợp cho API services)

## Yêu cầu

- Docker và Docker Compose đã cài đặt
- Tài khoản cloud platform (Google Cloud, AWS, Azure, etc.)

## Build Docker Image

### Build local

```bash
# Build image
docker build -t vnstock-mcp-server:latest .

# Hoặc dùng Dockerfile đơn giản hơn
docker build -f Dockerfile.simple -t vnstock-mcp-server:latest .
```

### Test local

```bash
# Chạy với docker-compose
docker-compose up

# Hoặc chạy trực tiếp
docker run -p 8000:8000 vnstock-mcp-server:latest

# Test health check
curl http://localhost:8000/health
```

## Deploy lên Google Cloud Run

### 1. Setup Google Cloud CLI

```bash
# Install gcloud CLI (nếu chưa có)
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

### 2. Build và Push Image

```bash
# Set variables
export PROJECT_ID=your-project-id
export SERVICE_NAME=vnstock-mcp-server
export REGION=asia-southeast1

# Build và push image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

# Hoặc build local rồi push
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest
```

### 3. Deploy lên Cloud Run

```bash
# Deploy với các settings cơ bản
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars TRANSPORT=sse,MOUNT_PATH=/

# Hoặc deploy với file config
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --cpu 1
```

### 4. Test Deployment

```bash
# Lấy URL của service
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

# Test
curl $SERVICE_URL/health
```

## Deploy lên AWS ECS/Fargate

### 1. Build và Push Image lên ECR

```bash
# Set variables
export AWS_REGION=ap-southeast-1
export AWS_ACCOUNT_ID=your-account-id
export SERVICE_NAME=vnstock-mcp-server

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name $SERVICE_NAME --region $AWS_REGION

# Build và push
docker build -t $SERVICE_NAME:latest .
docker tag $SERVICE_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$SERVICE_NAME:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$SERVICE_NAME:latest
```

### 2. Tạo Task Definition

Tạo file `task-definition.json`:

```json
{
  "family": "vnstock-mcp-server",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "vnstock-mcp-server",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/vnstock-mcp-server:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "TRANSPORT",
          "value": "sse"
        },
        {
          "name": "MOUNT_PATH",
          "value": "/"
        }
      ],
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "curl -f http://localhost:8000/health || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 40
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/vnstock-mcp-server",
          "awslogs-region": "ap-southeast-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### 3. Deploy

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create cluster (nếu chưa có)
aws ecs create-cluster --cluster-name vnstock-cluster

# Create service
aws ecs create-service \
  --cluster vnstock-cluster \
  --service-name vnstock-mcp-server \
  --task-definition vnstock-mcp-server \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

## Deploy lên Azure Container Instances

### 1. Build và Push Image

```bash
# Set variables
export AZURE_RESOURCE_GROUP=vnstock-rg
export AZURE_REGISTRY=vnstockregistry
export SERVICE_NAME=vnstock-mcp-server

# Create resource group
az group create --name $AZURE_RESOURCE_GROUP --location southeastasia

# Create container registry
az acr create --resource-group $AZURE_RESOURCE_GROUP --name $AZURE_REGISTRY --sku Basic

# Login to ACR
az acr login --name $AZURE_REGISTRY

# Build và push
az acr build --registry $AZURE_REGISTRY --image $SERVICE_NAME:latest .
```

### 2. Deploy Container Instance

```bash
# Deploy
az container create \
  --resource-group $AZURE_RESOURCE_GROUP \
  --name $SERVICE_NAME \
  --image $AZURE_REGISTRY.azurecr.io/$SERVICE_NAME:latest \
  --cpu 1 \
  --memory 1 \
  --registry-login-server $AZURE_REGISTRY.azurecr.io \
  --ip-address Public \
  --ports 8000 \
  --environment-variables TRANSPORT=sse MOUNT_PATH=/
```

## Deploy với Docker Compose (VPS/VM)

### 1. Setup trên VPS

```bash
# Install Docker và Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone repository
git clone <repository-url>
cd vnstock-mcp-server
```

### 2. Deploy

```bash
# Chạy với docker-compose production
docker-compose -f docker-compose.prod.yml up -d

# Xem logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

### 3. Setup Nginx Reverse Proxy (Optional)

Tạo file `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream vnstock {
        server vnstock-mcp-server:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        location / {
            proxy_pass http://vnstock;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }
}
```

## Environment Variables

- `TRANSPORT`: Transport mode (`stdio`, `sse`, `streamable-http`) - default: `sse`
- `MOUNT_PATH`: Mount path cho SSE transport - default: `/`
- `PORT`: Port để listen (cho SSE/HTTP) - default: `8000`

## Health Check

Server hỗ trợ health check endpoint tại `/health` (nếu transport là SSE/HTTP).

```bash
curl http://localhost:8000/health
```

## Monitoring và Logging

### Cloud Run

```bash
# Xem logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=vnstock-mcp-server" --limit 50
```

### AWS ECS

```bash
# Xem logs
aws logs tail /ecs/vnstock-mcp-server --follow
```

### Docker Compose

```bash
# Xem logs
docker-compose logs -f vnstock-mcp-server
```

## Troubleshooting

### Container không start

```bash
# Check logs
docker logs vnstock-mcp-server

# Check container status
docker ps -a
```

### Port đã được sử dụng

```bash
# Thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Map host port 8001 to container port 8000
```

### Health check failed

- Kiểm tra server có chạy đúng transport mode không
- Kiểm tra port có đúng không
- Kiểm tra firewall/security groups

## Best Practices

1. **Sử dụng non-root user**: Dockerfile đã config user `appuser`
2. **Health checks**: Đã config health check trong Dockerfile
3. **Resource limits**: Set limits trong docker-compose.prod.yml
4. **Logging**: Sử dụng JSON logging driver
5. **Security**:
   - Sử dụng private container registry
   - Enable authentication cho Cloud Run (nếu cần)
   - Sử dụng secrets management cho sensitive data

## CI/CD Integration

### GitHub Actions Example

Tạo `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Google Cloud
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}

      - name: Build and Push
        run: |
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/vnstock-mcp-server:latest

      - name: Deploy
        run: |
          gcloud run deploy vnstock-mcp-server \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/vnstock-mcp-server:latest \
            --platform managed \
            --region asia-southeast1 \
            --allow-unauthenticated
```

## Support

Nếu gặp vấn đề, vui lòng mở issue trên repository.
