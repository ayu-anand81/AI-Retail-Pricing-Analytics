import os
import json
import pathlib
import pandas as pd 
from google import genai

PROJECT_DIR = pathlib.Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "powerbi_retail_analysis.csv"
REPORT_FILE = PROJECT_DIR / "ai_report.txt"

df = pd.read_csv(CSV_FILE)
required_columns = ["product_id", "product_category_name", "month_year", "qty", "revenue",
                    "variance_pct", "price_flag", "performance_class"]

def missing_columns(df, required_columns):
    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        raise ValueError(f'Missing value in required columns in powerbi_retail_analytics.dataset: {missing_cols}') 
    
    return missing_cols


analyze_columns = required_columns.copy()
analysis_data = df[analyze_columns].to_dict(orient='records')

#json.dumps(analysis_data, default = str)
prompt = f""" 
            You are Ai data analyst at an e_commerece company.
            The following is a dataset of retail analytics for the company and has already
            been analyzed using python, powerbi and sql.
            
            Follow the given instructions carefully:
            1. Do NOT recalculate the analytics.
            2. Do NOT invent numbers.
            3. Do NOT change price classifications.
            4. Do NOT create new variance calculations.
            5. Use only the supplied data.
            6. Treat price_flag and performance_class as already-validated
            classifications.
            7. Give practical business observations based on the data.Create a professional report with these sections:

            1. Executive Summary
            2. Revenue Insights
            3. Demand Insights
            4. Pricing Insights
            5. Pricing Alerts and Risks
            6. Product Performance
            7. Business Recommendations
            8. Management Summary

                For recommendations, suggest areas to investigate or monitor.
                Do not invent exact new product prices.

                ALREADY-CALCULATED ANALYTICAL DATA:

                {json.dumps(analysis_data, default=str)}
        """

api_key = os.getenv('GenAI_API_KEY')

if not api_key:
    raise RuntimeError("GenAI_API_KEY environment variable is not found.")

client = genai.Client(api_key = api_key)

#Sending prompt
chat = client.chats.create(model = 'gemini-3.8-flash')
response = chat.send_message(prompt)

ai_report = response.text

print(ai_report)

with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write("AI RETAIL PRICING ANALYTICS REPORT\n")
    file.write("=" * 70)
    file.write("\n\n")
    file.write(ai_report)