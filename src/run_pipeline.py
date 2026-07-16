import os
import subprocess
import sys
 
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
 
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
 
load_dotenv(os.path.join(ROOT, ".env"))
 
if not os.environ.get("DATABASE_URL"):
    print("No DATABASE_URL found.")
    print("Copy .env.example to .env first. If you are using Docker, run:")
    print("  cp .env.example .env")
    print("  docker compose up -d --wait")
    raise SystemExit(1)
 
engine = create_engine(os.environ["DATABASE_URL"])
 
 
def banner(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
 
 
def run_python_script(filename):
    script_path = os.path.join(HERE, filename)
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=ROOT,
    )
    if result.returncode != 0:
        print(f"FAILED: {filename} -- stopping pipeline.")
        sys.exit(1)
 
 
def run_sql_file(filename, show_results):
    sql_path = os.path.join(HERE, filename)
    with open(sql_path, "r") as f:
        contents = f.read()
 
    statements = [s.strip() for s in contents.split(";") if s.strip()]
 
    with engine.begin() as connection:
        for statement in statements:
            result = connection.execute(text(statement))
            if show_results and result.returns_rows:
                for row in result.fetchall():
                    print("  ", row)
                print("  ---")
 
 
banner("STEP 1/5: Load raw CSV into PostgreSQL")
run_python_script("load_raw.py")
 
banner("STEP 2/5: Transform raw -> clean (in-database)")
run_python_script("transform.py")
 
banner("STEP 3/5: Create semantic views")
run_sql_file("views.sql", show_results=False)
print("Views created: v_sales_by_region, v_monthly_trend,")
print("               v_product_performance, v_segment_summary")
 
banner("STEP 4/5: Data-quality evidence (from dqa.sql)")
run_sql_file("dqa.sql", show_results=True)
 
banner("STEP 5/5: Export views for BI tools")
export_dir = os.path.join(ROOT, "data", "exports")
os.makedirs(export_dir, exist_ok=True)
view_names = [
    "v_sales_by_region",
    "v_monthly_trend",
    "v_product_performance",
    "v_segment_summary",
]
xlsx_path = os.path.join(export_dir, "superstore_views.xlsx")
with pd.ExcelWriter(xlsx_path) as writer:
    for v in view_names:
        df = pd.read_sql(f"SELECT * FROM {v}", engine)
        df.to_csv(os.path.join(export_dir, f"{v}.csv"), index=False)
        df.to_excel(writer, sheet_name=v, index=False)
        print(f"  {v}: {len(df)} rows")
print(f"  workbook: {xlsx_path}")
 
banner("PIPELINE COMPLETE")

