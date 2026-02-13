# GCP Setup Script for Construction Management System
# Run this AFTER installing Google Cloud SDK

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "GCP Setup for Construction Management" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Your project details
$PROJECT_ID = "project-918d244d-a3b7-4309-8b9"
$REGION = "asia-south1"

Write-Host "Step 1: Setting up project..." -ForegroundColor Green
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION

Write-Host ""
Write-Host "Step 2: Enabling required APIs..." -ForegroundColor Green
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com

Write-Host ""
Write-Host "Step 3: Creating secrets..." -ForegroundColor Green

# Generate random secret key
$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object { [char]$_ })
Write-Host "Generated SECRET_KEY: $SECRET_KEY" -ForegroundColor Yellow

# Create secret for SECRET_KEY
echo $SECRET_KEY | gcloud secrets create construction-secret-key --data-file=-
Write-Host "✓ Created construction-secret-key" -ForegroundColor Green

# Prompt for MongoDB URI
Write-Host ""
Write-Host "Please enter your MongoDB Atlas connection string:" -ForegroundColor Yellow
Write-Host "Format: mongodb+srv://username:password@cluster.xxxxx.mongodb.net/construction_db?retryWrites=true&w=majority" -ForegroundColor Gray
$MONGODB_URI = Read-Host "MongoDB URI"

# Create secret for MongoDB URI
echo $MONGODB_URI | gcloud secrets create construction-mongodb-uri --data-file=-
Write-Host "✓ Created construction-mongodb-uri" -ForegroundColor Green

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project ID: $PROJECT_ID" -ForegroundColor White
Write-Host "Region: $REGION" -ForegroundColor White
Write-Host ""
Write-Host "Secrets created:" -ForegroundColor White
Write-Host "  - construction-secret-key" -ForegroundColor White
Write-Host "  - construction-mongodb-uri" -ForegroundColor White
Write-Host ""
Write-Host "Next step: Run .\deploy-gcp.ps1 to deploy your application!" -ForegroundColor Yellow
