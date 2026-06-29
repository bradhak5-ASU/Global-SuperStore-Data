# Global Superstore — Data Engineering Pipeline

A raw to clean ingestion pipeline for the Global Superstore dataset.
Loads the raw CSV into PostgreSQL, then builds a cleaned, query-ready
table with normalized column names, proper date types, and data-quality
validation between layers.

Stack: Python, pandas, SQLAlchemy, PostgreSQL
Data: Global Superstore dataset (~12MB, public, from Kaggle),
included in `data/raw/` so the pipeline runs out of the box.