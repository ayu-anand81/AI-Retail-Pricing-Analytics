import pandas as pd # type: ignore
import sqlite3


conn = sqlite3.connect("pricing_analytics.db")

# ============================================================
# 1. PRICING ANALYSIS
# ============================================================

# Retrieve data and calculate pricing metrics
query = """
SELECT
    product_id,
    product_category_name,
    month_year,
    unit_price,
    qty,
    customers,
    product_score,
    comp_1,
    comp_2,
    comp_3,

    -- Average competitor price
    (comp_1 + comp_2 + comp_3) / 3.0 AS competitor_benchmark,

    -- Difference between our price and competitor benchmark
    unit_price - ((comp_1 + comp_2 + comp_3) / 3.0)
        AS price_variance,

    -- Percentage price difference
    ((unit_price - ((comp_1 + comp_2 + comp_3) / 3.0))
        / ((comp_1 + comp_2 + comp_3) / 3.0)) * 100
        AS variance_pct

FROM retail_price;
"""

result = pd.read_sql_query(query, conn)
conn.close()

# ------------------------------------------------------------
# 1.1 Price Classification
# ------------------------------------------------------------

result["price_flag"] = result["variance_pct"].apply(
    lambda x:
        "Potentially High" if x > 15
        else "Potentially Low" if x < -15
        else "Within Range"
)

# ------------------------------------------------------------
# 1.2 Product-Level Pricing Analysis
# ------------------------------------------------------------

result.sort_values(
    by="variance_pct",
    ascending=False,
    inplace=True
)

print("\nTop Products by Price Variance:")
print(
    result[[
            "product_id",
            "product_category_name",
            "unit_price",
            "comp_1",
            "comp_2",
            "comp_3",
            "qty",
            "product_score",
            "month_year",
            "variance_pct"]
    ].head(10)
)

# ------------------------------------------------------------
# 1.3 Category-Level Pricing Analysis
# ------------------------------------------------------------

category_analysis = (
    result
    .groupby("product_category_name")["variance_pct"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Price Variance by Category:")
print(category_analysis)


# ============================================================
# 2. DEMAND ANALYSIS
# ============================================================

# ------------------------------------------------------------
# 2.1 Top 10 Products by Total Quantity Sold
# ------------------------------------------------------------

demand_query = """
SELECT
    product_id,
    SUM(qty) AS total_quantity
FROM retail_price
GROUP BY product_id
ORDER BY total_quantity DESC
LIMIT 10;
"""

top_products = pd.read_sql_query(
    demand_query,
    sqlite3.connect("pricing_analytics.db")
)

print("\nTop 10 Products by Total Quantity Sold:")
print(top_products)

# ------------------------------------------------------------
# 2.2 Demand by Product Category
# ------------------------------------------------------------

category_demand_query = """
SELECT
    product_category_name,
    SUM(qty) AS total_quantity,
    SUM(customers) AS total_customers,
    AVG(product_score) AS average_score
FROM retail_price
GROUP BY product_category_name
ORDER BY total_quantity DESC;
"""

category_demand = pd.read_sql_query(category_demand_query,sqlite3.connect("pricing_analytics.db"))

print("\nDemand by Product Category:")
print(category_demand)

# ------------------------------------------------------------
# 2.3 Product Score vs Demand
# ------------------------------------------------------------

product_demand_analysis = (
    result
    .groupby("product_id")
    .agg(
        average_score=("product_score", "mean"),
        total_quantity=("qty", "sum")
    )
    .sort_values(
        by="total_quantity",
        ascending=False
    )
)

print("\nProduct Score vs Demand:")
print(product_demand_analysis)

# ============================================================
# 3. REVENUE ANALYSIS
# ============================================================

# ------------------------------------------------------------
# 3.1 Revenue by Product
# ------------------------------------------------------------

revenue_query = """
SELECT PRODUCT_ID,
    PRODUCT_CATEGORY_NAME,
    SUM(UNIT_PRICE * QTY) AS TOTAL_REVENUE
FROM retail_price
GROUP BY PRODUCT_ID, PRODUCT_CATEGORY_NAME
ORDER BY TOTAL_REVENUE DESC;
"""

revenue_by_product = pd.read_sql_query(revenue_query, sqlite3.connect('pricing_analytics.db'))

print("\nRevenue by Product:")
print(revenue_by_product.head())

# ------------------------------------------------------------
# 3.1 Revenue by Product Category
# ------------------------------------------------------------

category_revenue_query = """
SELECT  PRODUCT_CATEGORY_NAME,
    SUM(UNIT_PRICE * QTY) AS TOTAL_REVENUE
FROM retail_price
GROUP BY PRODUCT_CATEGORY_NAME
ORDER BY TOTAL_REVENUE DESC;
"""

category_revenue = pd.read_sql_query(category_revenue_query, sqlite3.connect('pricing_analytics.db'))

print("\nRevenue by Product Category:")
print(category_revenue.head())

# ============================================================
# 4. BUSINESS PERFORMANCE ANALYSIS
# ============================================================

# ------------------------------------------------------------
# 4.1 Product Performance
# ------------------------------------------------------------

business_query = """
SELECT
    product_id,
    product_category_name,
    -- Demand
    SUM(qty) AS total_quantity,
    -- Revenue
    SUM(unit_price * qty) AS total_revenue,
    -- Pricing
    AVG(unit_price) AS average_price,
    AVG(comp_1) AS average_comp_1,
    AVG(comp_2) AS average_comp_2,
    AVG(comp_3) AS average_comp_3,
    -- Customer activity
    SUM(customers) AS total_customers,
    -- Product rating
    AVG(product_score) AS average_score
FROM retail_price
GROUP BY product_id, product_category_name
ORDER BY total_revenue DESC;
"""

business_performance = pd.read_sql_query(business_query, sqlite3.connect("pricing_analytics.db"))

print("\nProduct Business Performance:")
print(business_performance.head())

# ------------------------------------------------------------
# 4.2 Performance Classification
# ------------------------------------------------------------

demand_median = business_performance["total_quantity"].median()
revenue_median = business_performance["total_revenue"].median()

def classify_performance(row):
    if row['total_quantity'] >= demand_median and row['total_revenue'] >= revenue_median:
        return "High Performer"
    elif row['total_quantity'] >= demand_median and row['total_revenue'] < revenue_median:
        return "Revenue Opportunity"
    elif row['total_quantity'] < demand_median and row['total_revenue'] >= revenue_median:
        return "High-Value / Lower Volume"
    else:
        return "Low Performer"

business_performance['performance_class'] = (business_performance.apply(
    classify_performance, axis = 1)
)

print("\nPerformance Classification:")

print(
    business_performance[
        [
            "product_id",
            "product_category_name",
            "total_quantity",
            "total_revenue",
            "performance_class"
        ]
    ].head()
)

# ------------------------------------------------------------
# 4.3 Category Business Performance
# ------------------------------------------------------------

category_business = (
    business_performance.groupby("product_category_name").agg(
        total_quantity=("total_quantity", "sum"),
        total_revenue=("total_revenue", "sum"),
        average_score=("average_score", "mean")
    ).sort_values(by = 'total_revenue', ascending = False)
)

print("\nCategory Business Performance:")
print(category_business.head())

# ------------------------------------------------------------
# Power BI Dataset
# ------------------------------------------------------------

performance_class_lookup = business_performance[
    [
        "product_id",
        "performance_class"
    ]
].copy()

conn = sqlite3.connect('pricing_analytics.db')

power_bi_query = """
SELECT 
    product_id,
    product_category_name,
    month_year,
    qty,
    unit_price,
    customers,
    product_score,
    comp_1,
    comp_2,
    comp_3,

    -- Competitor benchmark
    (comp_1 + comp_2 + comp_3) / 3.0
        AS competitor_benchmark,

    -- Price variance
    unit_price -
    ((comp_1 + comp_2 + comp_3) / 3.0)
        AS price_variance,

    -- Percentage price variance
    (
        (unit_price -
        ((comp_1 + comp_2 + comp_3) / 3.0))
        /
        ((comp_1 + comp_2 + comp_3) / 3.0)
    ) * 100
        AS variance_pct,

    -- Revenue
    unit_price * qty AS revenue

FROM retail_price;
"""

power_bi_data = pd.read_sql_query(
    power_bi_query,
    conn
)

conn.close()

power_bi_data = power_bi_data.merge(
    performance_class_lookup,
    on="product_id",
    how="left"
)

power_bi_data["price_flag"] = power_bi_data["variance_pct"].apply(
    lambda x:
        "Potentially High" if x > 15
        else "Potentially Low" if x < -15
        else "Within Range"
)

power_bi_data.to_csv(
    'powerbi_retail_analysis.csv',
    index=False
)

print("Data exported to powerbi_retail_analysis.csv successfully.")

print(
    "Rows:",
    power_bi_data.shape[0],
    "Columns:",
    power_bi_data.shape[1]
)

print("\nPower BI Dataset:")
print(power_bi_data.head())