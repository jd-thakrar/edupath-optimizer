#!/bin/bash

# EduPath Optimizer - Cloud Run Deployment Script

echo "================================================"
echo "EduPath Optimizer - Cloud Run Deployment"
echo "================================================"

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
SERVICE_NAME="edupath-optimizer"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI not found. Please install Google Cloud SDK."
    exit 1
fi

# Set project
echo "Setting GCP project..."
gcloud config set project $PROJECT_ID

# Build Docker image
echo ""
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Push to Google Container Registry
echo ""
echo "Pushing image to GCR..."
docker push $IMAGE_NAME

# Deploy to Cloud Run
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 0 \
    --max-instances 10 \
    --timeout 300 \
    --set-env-vars "FLASK_ENV=production"

echo ""
echo "================================================"
echo "Deployment Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Configure environment variables in Cloud Run console"
echo "2. Upload Firebase credentials as secret"
echo "3. Set GEMINI_API_KEY in environment variables"
echo "4. Update frontend API_BASE_URL to Cloud Run URL"
echo ""
