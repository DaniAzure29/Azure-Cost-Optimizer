Azure Cost Optimizer
Overview

A Python tool that queries Azure Cost Management APIs to track and report cloud spend.
Authentication is handled via Default Azure Credentials (e.g. az login) with a Service Principal fallback for automation.

Project Structure

azure-cost-optimizer/
│── src/
│ └── main.py # Python entry point
│── config/
│ └── azure-credentials.json # Service Principal credentials (gitignored)
│── output/
│ └── reports/ # Cost reports (CSV/Markdown)
│── README.md
│── .gitignore
│── requirements.txt
│── .vpython/ # Virtual environment (local only, not committed)

Setup (Day 1)

1. Clone the repo & create virtual environment

python -m venv .venv
source .venv/bin/activate # Mac/Linux
.venv\Scripts\Activate # Windows

2.  Install dependencies
    pip install -r requirements.txt

3.  Authentication setup

    - Tool first tries DefaultAzureCredential (works if you ran az login).

    - If that fails, it falls back to a Service Principal JSON file.

    Create Service Principal (replace <SUBSCRIPTION_ID>):
    az ad sp create-for-rbac \
     --name "CostOptimizerSP" \
     --role "Cost Management Reader" \
     --scopes /subscriptions/<SUBSCRIPTION_ID>\
     --sdk-auth

    Save the JSON output to:
    config/azure-credentials.json

    Make sure .gitignore includes:
    config/azure-credentials.json

4.  Test authentication
    Run:

        python src/main.py

If logged in with az login:

    ✅ Using DefaultAzureCredential (az login / managed identity)
    🎉 Authentication successful!

If not logged in, falls back to Service Principal:

    ⚠️ Default credentials not available, falling back to JSON file...
    ✅ Using Service Principal credentials
    🎉 Authentication successful!

Current Status

Project structure set up.

Virtual environment configured.

Dependencies installed.

Authentication working with dual flow: Default creds → Service Principal fallback.

Next step: Query real cost data from Azure Cost Management API.
