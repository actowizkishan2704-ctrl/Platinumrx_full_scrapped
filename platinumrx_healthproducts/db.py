import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="platinumrx"
)

query = "SELECT * FROM platinumrx_healthproduct_pdp"
first = True

for chunk in pd.read_sql(query, conn, chunksize=5000):

    chunk.to_csv(
        "platinumrx_health_product_pdp.csv",
        mode="w" if first else "a",
        index=False,
        header=first,
        encoding="utf-8-sig"
    )

    first = False
    print("Exported:", len(chunk))

conn.close()

print("Export completed successfully")