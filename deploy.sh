#!/bin/bash

# Deployment Script for Construction App
# Using docker-compose.prod.yml

echo "Starting Deployment..."

# 1. Pull latest changes from Git
echo "Pulling latest code..."
git pull origin main

# 2. Build and start containers
echo "Building and restarting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# 3. Clean up unused images
echo "Cleaning up..."
docker image prune -f

echo "Deployment Complete! App should be running on port 80."
