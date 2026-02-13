# DATA MIGRATION GUIDE

Your SQLite database is on your local machine, not in the Docker container.

## Option 1: Run Migration Locally (Recommended)

### Step 1: Install dependencies locally
```powershell
pip install mongoengine python-dotenv
```

### Step 2: Update .env to use localhost MongoDB
```
MONGODB_HOST=mongodb://localhost:27017/construction_db
```

### Step 3: Run the migration
```powershell
python migrate_simple.py
```

### Step 4: Update .env back to Docker MongoDB
```
MONGODB_HOST=mongodb://mongodb:27017/construction_db
```

## Option 2: Copy Database to Docker (Alternative)

Copy your SQLite database into the Docker container:

```powershell
docker cp instance/construction.db construction_app:/app/instance/construction.db
docker-compose exec app python migrate_simple.py
```

##Option 3: Use MongoDB Compass or Manual Entry

If migration is too complex, you can:
1. Install MongoDB Compass
2. Connect to your MongoDB Atlas
3. Manually recreate your data

OR simply start fresh with the new MongoDB-based system.

## Which database to use?

You have two SQLite databases:
- `instance/construction.db`
- `instance/construction_v2.db`

Which one has your actual data?
