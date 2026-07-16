import os

import pandas as pd
from dotenv import load_dotenv
from google import genai
from sqlalchemy import create_engine

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
engine = create_engine(os.environ["DATABASE_URL"])
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

view_map = {
    "v_sales_by_region": ["region", "market", "country", "where", "africa", "apac", "emea", "europe", "us", "canada", "latam"],
    "v_monthly_trend": ["month", "trend", "over time", "growth", "year", "when", "2011", "2012", "2013", "2014"],
    "v_product_performance": ["product", "category", "profit", "loss", "selling", "furniture", "office", "technology", "tables", "best", "worst"],
    "v_segment_summary": ["segment", "customer", "consumer", "corporate", "home office"],
}
def get_relevant_views(question):
    q = question.lower()
    matched = [v for v, words in view_map.items() if any(w in q for w in words)]
    return matched if matched else list(view_map)

def ask(question):
    views = get_relevant_views(question)
    context = ""
    for v in views:
        df = pd.read_sql(f"SELECT * FROM {v}", engine)
        context += f"\n--- {v} ---\n{df.to_csv(index=False)}"

    prompt = (
        "You are a data analyst for the Global Superstore dataset (2011-2014). "
        "Answer only from the data below. If it can't answer the question, say so. "
        "Dates are approximate to the week.\n"
        f"{context}\n"
        f"Question: {question}"
    )
    resp = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
    return resp.text, views

if __name__ == "__main__":
    print("Superstore chat. Ask about sales, products, regions, segments. 'q' to quit.")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("q", "quit", "exit"):
            break
        if not question:
            continue
        text, views = ask(question)
        print(f"\n{text}")
        print(f"(sources: {', '.join(views)})")