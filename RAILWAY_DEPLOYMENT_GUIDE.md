# Railway Deployment Guide

Deploying to **Railway.app** is incredibly simple because it directly integrates with your GitHub repository and automatically manages the PostgreSQL database and reverse proxy (so you don't even need Nginx).

Follow these exact steps to successfully deploy the application on Railway.

---

### Step 1: Ensure your code is on GitHub
Railway pulls your code directly from a visual dashboard. Make sure your latest code is pushed to your GitHub repository.

### Step 2: Create a PostgreSQL Database on Railway
1. Go to [Railway.app](https://railway.app/) and log in with your GitHub account.
2. Click **New Project** -> **Provision PostgreSQL**.
3. Wait about 30 seconds for the database to spin up.

### Step 3: Deploy your Code
1. In the same project dashboard, click the **+ Create** button (or **+ New**).
2. Select **GitHub Repo** and choose your `Construction` repository.
3. Railway will start cloning the repo.

### Step 4: Configure the Deployment settings
Because your project has multiple files and a custom Dockerfile name, you need to tell Railway where to look.

1. Click on your newly created web service box in the Railway dashboard.
2. Go to the **Settings** tab.
3. Scroll down to the **Build** section:
   - Change the **Builder** to `Dockerfile`.
   - Set the **Dockerfile Path** to `/Dockerfile.backend`.
4. Scroll down to the **Deploy** section:
   - Under **Start Command**, leave it blank (it will use the `CMD` from your Dockerfile).
   - Under **Custom Domain**, click **Generate Domain** to get a free `x.up.railway.app` URL for your site.

### Step 5: Configure Environment Variables
Railway needs the same secret variables you use locally, plus a connection to the newly created database.

1. Still on your web service, go to the **Variables** tab.
2. Click **New Variable** -> **Add Reference** -> Select the `DATABASE_URL` from your PostgreSQL plugin. Railway will automatically link the database!
3. Add the following additional variables manually:
   - `SECRET_KEY`: (Enter any secret string, e.g., `my-production-secret-key`)
   - `DEBUG`: `False`
   - `PORT`: `8000` *(Very Important: Since your `Dockerfile.backend` explicitly binds gunicorn to port 8000, you must tell Railway to listen on port 8000).*

### Step 6: Wait for the Build and Migrate DB
Whenever you update settings or variables, Railway triggers a new deployment.
Wait for it to show a green **Success** badge.

Once deployed, you need to create your database tables:
1. In the Railway dashboard for your web service, click the **Terminal** tab or the `>_` icon.
2. Run the migration and create a superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
```

**That's it!** You can now visit the custom URL generated in Step 4, and your app will be live with full SSL and a connected database.

---
### *Need to Restore Data?*
If you want to move your local data to Railway:
1. Railway explicitly provides the PostgreSQL connection details (Host, Port, User, Password, DB Name) in the Database service's "Variables" tab.
2. Run this command on your **local computer**, replacing the caps with the Railway database variables:
```bash
pg_restore -U PGUSER -h PGHOST -p PGPORT -d PGDATABASE -v --no-owner --no-acl construction_dump.dump
```
