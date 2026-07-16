import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.environ["DATABASE_URL"])

HERE = os.path.dirname(os.path.abspath(__file__))
SQL_PATH = os.path.join(HERE, "transform.sql")


with open(SQL_PATH,"r") as f:
    transform_sql = f.read()

with engine.begin() as connection:
    connection.execute(text(transform_sql))

with engine.connect() as connection:
    raw_count = connection.execute(
        text("SELECT COUNT(*) FROM raw_superstore")
    ).scalar()
    clean_count = connection.execute(
        text("SELECT COUNT(*) FROM clean_superstore")
    ).scalar()

print("raw_superstore rows: ", raw_count)
print("clean_superstore rows: ", clean_count)
print("Row counts match: ", raw_count == clean_count)