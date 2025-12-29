# End-to-End-Data-BI-Pipeline
[Project Status](https://img.shields.io/badge/status-complete-green)
[Python](https://img.shields.io/badge/Python-3.10-blue)
[Snowflake](https://img.shields.io/badge/Snowflake-Data_Warehouse-blue)
[dbt](https://img.shields.io/badge/dbt-Transformation-orange)
[Power BI](https://img.shields.io/badge/Power_BI-Visualization-yellow)

Project Overview
This project is a full-stack Business Intelligence solution designed to analyze e-commerce sales performance. 
Unlike standard analysis projects, this focuses on the engineering architecture: extracting data from a REST API, loading it into a cloud data warehouse, transforming it using modern software engineering practices (dbt), and modeling it for high-performance reporting.

Architecture
Data Flow:`REST API (DummyJSON)` → `Python (Extraction)` → `Snowflake (Raw Layer)` → `dbt (Transformation/Modeling)` → `Power BI (Reporting)`

1. Extraction (EL)
Source:DummyJSON API (Products and Carts endpoints).
Tool:Python (Pandas + Snowflake Connector).
Logic: 
   Fetches data via HTTP requests.
   Handles data cleaning (column normalization).
   Uses `write_pandas` for efficient bulk loading into Snowflake.

2. Transformation (T)
Tool:dbt (Data Build Tool).
Modeling Strategy:Kimball Star Schema.
Key Models:
`dim_products`: Cleans raw product attributes.
`fct_orders`: Explodes nested JSON arrays using Snowflake's `FLATTEN` function to create a transactional fact table.

3. Visualization
Tool:Power BI.
Data Model:Star Schema (1-to-Many relationships).
Key Metrics:
`Total Revenue` (Calculated via DAX: `SUMX(Quantity * Price)`).
Sales by Category and Time.

 Dashboard Preview
The Executive Dashboard:
[Dashboard Screenshot](03_visualization/dashboard_screenshot.png)

The Data Model (Star Schema):
[Data Model](03_visualization/model_view.png)
