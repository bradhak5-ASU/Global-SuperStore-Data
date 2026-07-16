Global Superstore ELT Pipeline

An end to end ELT project. I take a messy public retail dataset, load it into PostgreSQL, clean and reshape it with SQL, and expose the results two ways: a Tableau dashboard for visuals and a small RAG chatbot that answers questions about the data in plain English.

The goal is simple: show the full journey of data from a raw file to something a business user can actually use, and document every data quality problem found along the way.

The data

Global Superstore, a public retail dataset from Kaggle. 51,290 order line items across 27 columns, covering 2011 to 2014: orders, products, customers, regions, sales, profit, discounts and shipping.

The copy in circulation is damaged. Both date columns contain the same corrupted string ('00:00.0') in every single row, there is a junk column that is just the number 1 repeated 51,290 times, and one column is a near duplicate of another. Instead of picking a cleaner dataset, I kept this one and treated the mess as the point of the project.

The pipeline

Refer: (architecture.png)


load_raw.py loads the CSV into PostgreSQL as raw_superstore. The raw layer is never modified.
transform.sql builds clean_superstore inside the database: snake_case column names, trimmed text, junk columns dropped, and order dates rebuilt at week level from the surviving year and week number columns (ship dates had no backup and are gone for good).
views.sql creates four aggregated views (region, monthly trend, product performance, customer segment). These views are the only thing the dashboard and the chatbot read.
dqa.sql holds one query per data quality finding, so anyone can rerun the evidence against the raw table.


Everything runs with one command:

python src/run_pipeline.py

It loads, transforms, builds the views, prints the data quality evidence, and exports the views to CSV and Excel for BI tools.

What was wrong with the data

FindingWhat I didAll 51,290 values in both date columns corrupted to '00:00.0'Dropped them, derived a week level order date from Year + weeknumYear embedded in every Order IDCross checked it against the Year column before trusting it (0 mismatches)ji_lu-shu column is the constant 1DroppedMarket2 duplicates Market except US and Canada roll into North AmericaKept, renamed market_groupRow ID unique, no nulls, no duplicate rowsUsed as primary key, no dedup needed

Run psql -d <yourdb> -f src/dqa.sql to see each of these prove itself.

Dashboard

Built in Tableau from the exported views: profit by sub category (Tables loses about 64K while everything else is profitable), monthly sales trend on the recovered dates, sales by market, and a segment breakdown, with a market filter wired across panels.

View it here: Tableau Public dashboard

Chatbot

app/chatbot.py is a small retrieval augmented generation loop. It picks the relevant view for your question, pulls those rows from PostgreSQL, and sends them to the OpenAI API with instructions to answer only from that data. Every answer shows which view it came from, and questions the data cannot answer get an honest refusal instead of a guess.

Running it yourself

pip install -r requirements.txt
# put your PostgreSQL connection string in .env as DATABASE_URL
# put your OpenAI key in .env as OPENAI_API_KEY (only needed for the chatbot)

python src/run_pipeline.py
python app/chatbot.py

Stack

Python, pandas, SQLAlchemy, PostgreSQL, SQL, Tableau, OpenAI API