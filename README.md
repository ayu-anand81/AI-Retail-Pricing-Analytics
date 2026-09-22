# AI Retail Pricing Analytics

An end-to-end retail pricing analytics project that combines **Python, SQL-based analysis, Power BI, and Generative AI** to identify pricing anomalies, analyze product performance, and generate business insights.

## Project Overview

Retail businesses need to balance product pricing, competitor prices, demand, and revenue. This project analyzes retail pricing data to identify products that may be **overpriced or underpriced**, understand category-level performance, and generate actionable pricing insights.

The project uses Python for data processing and analysis, SQLite for database-based querying, Power BI for interactive visualization, and Gemini Generative AI for automated business reporting.

## Project Structure

```text
AI-Retail-Pricing-Analytics/
│
├── Data/
│   └── retail_price.csv
│
├── Python/
│   ├── retail_inspect.py
│   ├── load_database.py
│   ├── query_database.py
│   └── ai_report.py
│
├── PowerBI/
│   └── retail_pricing_dashboard.pbix
│
└── powerbi_retail_analysis.csv
```

## Technologies Used

* **Python**
* **Pandas**
* **SQLite**
* **SQL**
* **Power BI**
* **DAX**
* **Google Gemini API**
* **Generative AI**
* **CSV Data Processing**

## Project Workflow

```text
Retail Dataset
      ↓
Data Inspection with Python
      ↓
Load Data into SQLite
      ↓
Pricing & Product Analysis
      ↓
Export Analytics Dataset
      ↓
Power BI Dashboard
      ↓
Gemini AI Business Report
```

## Key Analysis

### 1. Competitive Pricing Analysis

The project compares product prices against competitor prices using a competitor benchmark.

The benchmark is calculated from the available competitor price fields:

```text
Competitor Benchmark =
(Competitor 1 + Competitor 2 + Competitor 3) / 3
```

Price variance is then used to identify products whose prices differ significantly from the competitor benchmark.

Products are classified as:

* **Potentially High**
* **Potentially Low**
* **Within Range**

### 2. Revenue Analysis

The project analyzes revenue at product and category levels to identify products and categories contributing significantly to overall revenue.

### 3. Demand Analysis

Product quantity and customer-related metrics are analyzed to understand demand patterns across categories.

### 4. Product Performance

Products are classified using revenue and demand-related metrics into performance groups such as:

* High Performer
* Revenue Opportunity
* High-Value / Lower Volume
* Low Performer

### 5. Pricing Alerts

Products with unusually high or low pricing variance are highlighted as potential pricing alerts for further business investigation.

## Power BI Dashboard

The Power BI dashboard provides an interactive view of:

* Total Revenue
* Total Quantity
* Average Pricing Variance
* Potentially High-Priced Products
* Revenue by Category
* Demand by Category
* Pricing Position
* Pricing Trends
* Top Pricing Alerts

Users can explore the analysis using category, product, and time-based filters.

## Generative AI Integration

The project uses **Google Gemini** to interpret the analytical results and generate a structured business report.

The AI layer does not replace the underlying calculations. Instead, it receives the already-calculated analytical results and converts them into business-oriented insights.

The generated report covers:

* Executive Summary
* Revenue Insights
* Demand Insights
* Pricing Insights
* Pricing Alerts and Risks
* Product Performance
* Business Recommendations
* Management Summary

The Gemini API key is stored through an environment variable rather than directly inside the source code.

## Example Business Insight

The analysis identified significant pricing deviations for certain products when compared with competitor benchmarks.

For example, the product **health5** showed a substantially higher price variance than the competitor benchmark, making it a product that warrants further pricing review.

This type of analysis can help businesses investigate whether pricing differences are justified by factors such as product positioning, demand, product characteristics, or competitive strategy.

## Project Objective

The main objective is to demonstrate how a retail pricing dataset can be transformed into a practical **pricing intelligence workflow** using:

**Data → Analysis → Visualization → AI-generated Business Insights**

## Skills Demonstrated

* Data Cleaning and Exploration
* Python Data Analysis
* Pandas
* SQL and SQLite
* Pricing Analytics
* Competitive Benchmarking
* Business Intelligence
* Power BI Dashboard Development
* DAX
* Generative AI Integration
* Gemini API
* Business Insight Generation
* Data-driven Decision Support

## Future Improvements

Potential extensions include:

* Automated price recommendation models
* Price elasticity analysis
* Time-series price forecasting
* Automated dashboard refresh
* ML-based demand prediction
* Dynamic pricing recommendations
* Deployment as an analytics application

## Author

**Ayushi Sahu**

Data Analytics | Data Science | Machine Learning | Generative AI

