import os
import subprocess
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


HERE = os.path.dirname(os.path.abspath(__file__))   
ROOT = os.path.dirname(HERE)                        

load_dotenv(os.path.join(ROOT, ".env"))
engine = create_engine(os.environ["DATABASE_URL"])


def banner(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_python_script(filename):
    """Run a pipeline script with the project root as the
    working directory, so its relative paths (like data/raw/...)
    resolve correctly."""
    script_path = os.path.join(HERE, filename)
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=ROOT, 
    )
    if result.returncode != 0:
        print(f"FAILED: {filename} — stopping pipeline.")
        sys.exit(1)


def run_sql_file(filename, show_results):
    """Execute every statement in a SQL file. If show_results is
    True, print the rows each SELECT returns."""
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


banner("STEP 1/4: Load raw CSV into PostgreSQL")
run_python_script("load_raw.py")

banner("STEP 2/4: Transform raw -> clean (in-database)")
run_python_script("transform.py")

banner("STEP 3/4: Create semantic views")
run_sql_file("views.sql", show_results=False)
print("Views created: v_sales_by_region, v_monthly_trend,")
print("          v_product_performance, v_segment_summary")

banner("STEP 4/4: Data-quality evidence (from dqa.sql)")
run_sql_file("dqa.sql", show_results=True)

banner("PIPELINE COMPLETE")