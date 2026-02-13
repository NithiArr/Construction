# GCP Deployment Script for Construction Management System (Windows PowerShell)
# This script deploys the application to Google Cloud Run

# Configuration
$PROJECT_ID = "your-gcp-project-id"
$REGION = "asia-south1"  # Change to your preferred region
$SERVICE_NAME = "construction-management"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "GCP Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
try {
    gcloud version | Out-Null
} catch {
    Write-Host "ERROR: gcloud CLI is not installed." -ForegroundColor Red
    Write-Host "Please install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Set the project
Write-Host "Setting GCP project to: $PROJECT_ID" -ForegroundColor Green
gcloud config set project $PROJECT_ID

# Enable required APIs
Write-Host ""
Write-Host "Enabling required GCP APIs..." -ForegroundColor Green
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the Docker image
Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Green
docker build -t ${IMAGE_NAME}:latest .

# Push to Container Registry
Write-Host ""
Write-Host "Pushing image to Google Container Registry..." -ForegroundColor Green
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
Write-Host ""
Write-Host "Deploying to Cloud Run..." -ForegroundColor Green
gcloud run deploy $SERVICE_NAME `
  --image ${IMAGE_NAME}:latest `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --memory 512Mi `
  --cpu 1 `
  --max-instances 10 `
  --min-instances 1 `
  --port 8080 `
  --set-env-vars "FLASK_ENV=production,DEBUG=False,PORT=8080" `
  --set-secrets "SECRET_KEY=construction-secret-key:latest,MONGODB_HOST=construction-mongodb-uri:latest"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your application is now running on Google Cloud Run." -ForegroundColor Green
Write-Host "To view your service:" -ForegroundColor Yellow
Write-Host "  gcloud run services describe $SERVICE_NAME --region $REGION"
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  gcloud run services logs read $SERVICE_NAME --region $REGION"
