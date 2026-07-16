# Setup and running

## What you need

Python 3.11 or newer, and one of the two database options below.

## 1. Clone and install

```
git clone https://github.com/bradhak5-ASU/Global-SuperStore-Data.git
cd Global-SuperStore-Data
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Database, pick one

**Option A, Docker (easiest).** Needs Docker Desktop installed, nothing else.

```
cp .env.example .env
docker compose up -d --wait
```

That starts PostgreSQL in a container with the user, password and database
already created. The default DATABASE_URL in .env.example points at it, so
there is nothing to edit.

**Option B, your own PostgreSQL.** Create an empty database, then copy
.env.example to .env and change DATABASE_URL to your own connection string,
for example:

```
DATABASE_URL=postgresql://youruser@localhost:5432/yourdb
```

## 3. Run the pipeline

```
python src/run_pipeline.py
```

One command does everything: loads the raw CSV into PostgreSQL, runs the
in-database transform, creates the four views, prints the data quality
evidence, and exports the views to data/exports/ as CSV and Excel for BI
tools. Safe to rerun any number of times.

## 4. Chatbot (optional)

The chatbot needs a Google Gemini API key. Get a free one at
aistudio.google.com and add it to .env:

```
GEMINI_API_KEY=...
```

Then:

```
python app/chatbot.py
```

The pipeline and the dashboard work without a key. Only the chatbot needs it.

## Stopping the Docker database

```
docker compose down        # stop it, keep the data
docker compose down -v     # stop it and wipe the data
```