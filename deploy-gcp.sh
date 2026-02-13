#!/bin/bash

# GCP Deployment Script for Construction Management System
# This script deploys the application to Google Cloud Run

# Exit on error
set -e

# Configuration
PROJECT_ID="your-gcp-project-id"
REGION="asia-south1"  # Change to your preferred region
SERVICE_NAME="construction-management"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "======================================"
echo "GCP Deployment Script"
echo "======================================"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI is not installed."
    echo "Please install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set the project
echo "Setting GCP project to: ${PROJECT_ID}"
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo ""
echo "Enabling required GCP APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the Docker image
echo ""
echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:latest .

# Push to Container Registry
echo ""
echo "Pushing image to Google Container Registry..."
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
echo ""
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME}:latest \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 1 \
  --port 8080 \
  --set-env-vars "FLASK_ENV=production,DEBUG=False,PORT=8080" \
  --set-secrets "SECRET_KEY=construction-secret-key:latest,MONGODB_HOST=construction-mongodb-uri:latest"

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Your application is now running on Google Cloud Run."
echo "To view your service:"
echo "  gcloud run services describe ${SERVICE_NAME} --region ${REGION}"
echo ""
echo "To view logs:"
echo "  gcloud run services logs read ${SERVICE_NAME} --region ${REGION}"
