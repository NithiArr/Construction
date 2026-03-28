# Runpod Deployment Guide

Deploying a multi-container application (like your Django + Nginx + PostgreSQL setup) to Runpod requires a **Docker-in-Docker (DinD)** environment, as Runpod provisions standalone containers rather than full virtual machines by default.

Here is the step-by-step method to deploy your application to a Runpod Pod:

## 1. Top-up Your Account
As seen in your screenshot, make sure you have added a payment method and loaded some credits in the **Billing** section of the Runpod console.

## 2. Deploy a Docker-in-Docker Pod
Since your app uses `docker-compose` to manage 3 containers, you'll need an environment that allows running Docker inside Docker.

1. In the Runpod dashboard, go to **Pods** on the left menu.
2. Click **+ Deploy** (Choose either Secure Cloud or Community Cloud - Community is usually cheaper).
3. Find a suitable GPU or CPU. A basic CPU pod or the cheapest GPU (like RTX 3060 / 4000 Ada) is fine if you're just hosting a standard web app.
4. Click **Deploy**.
5. In the **Select a Template** screen, you need to use a Docker-in-Docker template. 
   - You can click **Customize Template**.
   - For the **Container Image**, enter: `crundy/runpod-dind:latest` (or any reliable Ubuntu DinD image). 
   - *Alternatively, you can just use the standard `runpod/base:0.4.0-cuda11.8.0` image and install docker inside it if it supports it, but `crundy/runpod-dind:latest` is pre-configured.*
6. Under **Expose External HTTP Ports**, enter `80`, since your Nginx frontend runs on port 80.
7. Click **Deploy On-Demand**.

## 3. Connect to your Pod
Once the Pod is running (Status will turn green):
1. Click the **Connect** button on your Pod.
2. Choose **Connect to Web Terminal** (or use the provided SSH command in your local terminal).

## 4. Install Dependencies (If needed)
If your container requires git or docker-compose to be manually installed, run this in the Pod's terminal:
```bash
apt-get update
apt-get install -y git docker-compose
```

## 5. Clone Your Code
Next, clone your application repository into the Pod:
```bash
# You may need to generate an SSH key (`ssh-keygen`) and add it to your GitHub/GitLab
# Or clone via HTTPS and type your username/password/PAT
git clone <URL_TO_YOUR_REPOSITORY>
cd Construction # or your repo name
```

## 6. Run the Application
Start your docker compose stack exactly the same way as you do locally:
```bash
docker compose up -d --build
```
This will build your `backend`, and pull the `postgres:15` and `nginx:alpine` images.

## 7. Setup the Database
Once the containers are running, run the Django migrations and optionally load your database dump (following the steps from your `DOCKER_SETUP.md`):
```bash
docker compose exec backend python manage.py migrate

# If you have a dump file to restore:
docker cp construction_dump.dump construction-db:/tmp/dump.dump
docker compose exec db pg_restore -U postgres -d construction_db -v --no-owner --no-acl /tmp/dump.dump
```

## 8. Access the App
Go back to your Runpod dashboard, click on your Pod, and look for the **Connect** button.
Under "HTTP Services", click the button corresponding to Port `80`. 
This will open your deployed application in a new browser tab.

---
### **Note on Persistent Storage**
Runpod wipes the main container storage upon termination unless you setup Network Volumes.
To ensure your Database never gets lost:
1. Create a **Network Volume** in Runpod.
2. When deploying the Pod, attach this Network Volume (e.g., mounted to `/workspace`).
3. Clone your code into `/workspace` instead of the root directory, so your Docker volumes (`postgres_data`) are stored safely in persistent storage.
