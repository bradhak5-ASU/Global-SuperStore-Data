import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
load_dotenv()

engine = create_engine(os.environ["DATABASE_URL"])

RAW = "data/raw/global_superstore.csv"
df = pd.read_csv(RAW, encoding="latin-1")
df.to_sql("raw_superstore",engine,if_exists="replace",index=False)
print("Loaded rows: ",df.shape[0])