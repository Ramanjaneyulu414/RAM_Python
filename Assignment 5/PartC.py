


# Step 1: Load dataset (use latin1 encoding for this file)
df = pd.read_csv("sales_data_sample.csv", encoding="latin1")

# Step 2: Clean missing values (drop rows where key columns are missing)
df_clean = df.dropna(subset=["QUANTITYORDERED", "PRICEEACH", "ORDERDATE"])

# Step 3: Create new column TotalAmount = Quantity × Price
df_clean["TotalAmount"] = df_clean["QUANTITYORDERED"] * df_clean["PRICEEACH"]

# Step 4: Group data by Product and calculate total revenue per product
revenue_per_product = df_clean.groupby("PRODUCTCODE")["TotalAmount"].sum().reset_index()

print("Revenue per Product:")
print(revenue_per_product.head())

# Step 5: Find the month with the highest sales
sales_per_month = df_clean.groupby(["YEAR_ID", "MONTH_ID"])["TotalAmount"].sum().reset_index()
best_month = sales_per_month.loc[sales_per_month["TotalAmount"].idxmax()]
print("\nMonth with Highest Sales:")
print(best_month)

