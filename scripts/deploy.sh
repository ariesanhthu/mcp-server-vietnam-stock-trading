#!/bin/bash

# Deploy script for vnstock-mcp-server
# Usage: ./scripts/deploy.sh [platform] [options]

set -e

PLATFORM=${1:-local}
IMAGE_NAME=${IMAGE_NAME:-vnstock-mcp-server}
IMAGE_TAG=${IMAGE_TAG:-latest}
TRANSPORT=${TRANSPORT:-sse}

echo "🚀 Deploying vnstock-mcp-server to $PLATFORM..."

case $PLATFORM in
  local)
    echo "📦 Building Docker image..."
    docker build -t $IMAGE_NAME:$IMAGE_TAG .
    
    echo "🏃 Starting container..."
    docker-compose up -d
    
    echo "✅ Server started on http://localhost:8000"
    echo "📊 View logs: docker-compose logs -f"
    ;;
    
  gcp)
    # Google Cloud Run deployment
    PROJECT_ID=${GCP_PROJECT_ID:-$(gcloud config get-value project)}
    REGION=${GCP_REGION:-asia-southeast1}
    SERVICE_NAME=${SERVICE_NAME:-vnstock-mcp-server}
    
    if [ -z "$PROJECT_ID" ]; then
      echo "❌ Error: GCP_PROJECT_ID not set"
      exit 1
    fi
    
    echo "📦 Building and pushing to GCR..."
    gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME:$IMAGE_TAG .
    
    echo "🚀 Deploying to Cloud Run..."
    gcloud run deploy $SERVICE_NAME \
      --image gcr.io/$PROJECT_ID/$SERVICE_NAME:$IMAGE_TAG \
      --platform managed \
      --region $REGION \
      --allow-unauthenticated \
      --port 8000 \
      --memory 512Mi \
      --cpu 1 \
      --timeout 300 \
      --max-instances 10 \
      --set-env-vars TRANSPORT=$TRANSPORT,MOUNT_PATH=/
    
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
    echo "✅ Service deployed: $SERVICE_URL"
    ;;
    
  aws)
    # AWS ECS/Fargate deployment
    AWS_REGION=${AWS_REGION:-ap-southeast-1}
    AWS_ACCOUNT_ID=${AWS_ACCOUNT_ID:-$(aws sts get-caller-identity --query Account --output text)}
    ECR_REPO=${ECR_REPO:-vnstock-mcp-server}
    
    if [ -z "$AWS_ACCOUNT_ID" ]; then
      echo "❌ Error: AWS_ACCOUNT_ID not set"
      exit 1
    fi
    
    echo "🔐 Logging into ECR..."
    aws ecr get-login-password --region $AWS_REGION | \
      docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    
    echo "📦 Building and pushing to ECR..."
    docker build -t $ECR_REPO:$IMAGE_TAG .
    docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
    
    echo "✅ Image pushed to ECR"
    echo "ℹ️  Use AWS Console or CLI to create ECS service with the image"
    ;;
    
  azure)
    # Azure Container Instances deployment
    AZURE_RESOURCE_GROUP=${AZURE_RESOURCE_GROUP:-vnstock-rg}
    AZURE_REGISTRY=${AZURE_REGISTRY:-vnstockregistry}
    SERVICE_NAME=${SERVICE_NAME:-vnstock-mcp-server}
    
    echo "📦 Building and pushing to ACR..."
    az acr build --registry $AZURE_REGISTRY --image $SERVICE_NAME:$IMAGE_TAG .
    
    echo "🚀 Deploying to Container Instances..."
    az container create \
      --resource-group $AZURE_RESOURCE_GROUP \
      --name $SERVICE_NAME \
      --image $AZURE_REGISTRY.azurecr.io/$SERVICE_NAME:$IMAGE_TAG \
      --cpu 1 \
      --memory 1 \
      --registry-login-server $AZURE_REGISTRY.azurecr.io \
      --ip-address Public \
      --ports 8000 \
      --environment-variables TRANSPORT=$TRANSPORT MOUNT_PATH=/
    
    echo "✅ Service deployed"
    ;;
    
  *)
    echo "❌ Unknown platform: $PLATFORM"
    echo "Available platforms: local, gcp, aws, azure"
    exit 1
    ;;
esac

echo "🎉 Deployment complete!"

