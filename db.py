import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="platinumrx"
)

query = "SELECT * FROM platinumrx_pdp"

df = pd.read_sql(query, conn)

df.to_csv(
    "platinumrx_pdp.csv",
    index=False,
    encoding="utf-8-sig"
)

conn.close()

print("Export completed")
print("Total rows:", len(df))