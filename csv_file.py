import pandas as pd

input_file = r"C:\Users\kishan.prajapati\Desktop\platinumrx_pdp.csv"
output_file = r"C:\Users\kishan.prajapati\Desktop\platinumrx_pdp_unique.csv"

df = pd.read_csv(input_file)

print("Total rows:", len(df))
print("Duplicate URLs:", df["product_url"].duplicated().sum())

df = df.drop_duplicates(
    subset=["product_url"],
    keep="first"
)

df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Final rows:", len(df))
print("Saved:", output_file)