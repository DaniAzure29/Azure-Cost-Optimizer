Azure Cost Optimization Tool
Overview

A Python tool that queries the Azure Cost Management API to track and optimize cloud spend.
It authenticates via either DefaultAzureCredential (az login) or a Service Principal fallback, retrieves recent cost data, transforms it into clean reports, and detects cost anomalies.

Features

🔐 Flexible Authentication: Uses az login if available, otherwise falls back to Service Principal (azure_sp.json).

💰 Cost Queries: Pulls subscription-level spend using the official CostManagementClient.

📊 Data Transformation: Converts raw API results into Pandas DataFrame.

💾 Export: Saves reports to CSV (and optionally Markdown).

🚨 Spike Detection: Flags sudden cost increases (e.g., >30% compared to rolling average).

File Structure

azure-cost-optimizer/
│── src/
│ └── main.py # Our Python entry point
│── config/
│ └── azure-credentials.json # Service principal creds (gitignored)
│── output/
│ └── reports/ # Cost reports (CSV/Markdown)
│── README.md
│── .gitignore
│── requirements.txt

Usage

1. Install dependencies
   pip install -r requirements.txt

2. Authenticate

   Option A: Login interactively

   az login

Option B: Provide Service Principal JSON (azure_sp.json)

    {
    "tenantId": "xxxx-xxxx-xxxx",
    "clientId": "xxxx-xxxx-xxxx",
    "clientSecret": "xxxx-xxxx-xxxx",
    "subscriptionId": "xxxx-xxxx-xxxx"
    }

3. Run the script
   python main.py

4. Output

azure_costs_YYYYMMDD.csv → cost breakdown for last 7 days
