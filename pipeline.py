import requests
import pandas as pd
from snowflake.connector import connect
from snowflake.connector.pandas_tools import write_pandas

--- 1. CONFIGURATION ---
These match the settings you created in Snowflake
ACCOUNT_ID = 'yqjsgyp-xxc43108'
USER = 'sravyakganti'
PASSWORD = 'os.getenv("SNOWFLAKE_PASSWORD")'
WAREHOUSE = 'compute_wh'
DATABASE = 'retail_db'
SCHEMA = 'raw_data'
ROLE = 'data_loader_role'

--- 2. EXTRACT DATA FROM THE WEB (Using a more stable API) ---
print("Step 1: Fetching data from DummyJSON API...")

We are using dummyjson.com because it is faster and more reliable
Get Products
print("   -> Requesting Products...")
resp_prod = requests.get("https://dummyjson.com/products?limit=100")
data_prod = resp_prod.json()['products'] # This API puts data inside a 'products' key
df_products = pd.DataFrame(data_prod)

Get Carts (Orders)
print("   -> Requesting Carts...")
resp_carts = requests.get("https://dummyjson.com/carts?limit=100")
data_carts = resp_carts.json()['carts']   # This API puts data inside a 'carts' key
df_carts = pd.DataFrame(data_carts)

print(f"   -> Found {len(df_products)} products")
print(f"   -> Found {len(df_carts)} carts")

--- 3. CLEAN DATA FOR SNOWFLAKE ---
print("Step 2: Cleaning data...")

Snowflake loves UPPERCASE column names
df_products.columns = [c.upper() for c in df_products.columns]
df_carts.columns = [c.upper() for c in df_carts.columns]

Drop complex columns that might break the load (Lists/Dictionaries)
We keep it simple for your first project
cols_to_drop = ['IMAGES', 'THUMBNAIL', 'REVIEWS', 'META', 'DIMENSIONS', 'TAGS']
for col in cols_to_drop:
    if col in df_products.columns:
        df_products.drop(columns=[col], inplace=True)

--- 4. LOAD DATA TO SNOWFLAKE ---
print("Step 3: Connecting to Snowflake...")

try:
    # Create the connection
    conn = connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT_ID,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA,
        role=ROLE
    )

    print("   -> Uploading PRODUCTS table...")
    success, nchunks, nrows, _ = write_pandas(conn, df_products, "PRODUCTS", auto_create_table=True, overwrite=True)
    print(f"      Success! Loaded {nrows} rows.")

    print("   -> Uploading ORDERS table...")
    success, nchunks, nrows, _ = write_pandas(conn, df_carts, "ORDERS", auto_create_table=True, overwrite=True)
    print(f"      Success! Loaded {nrows} rows.")
    
    conn.close()
    print("ALL DONE! Go check Snowflake.")

except Exception as e:
    print("\nERROR CONNECTING TO SNOWFLAKE:")
    print(e)