from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryDataset, QueryTimePeriod
import pandas as pd
from datetime import datetime, timedelta, timezone
import json
import os
import sys

def get_credentials():
    """
    Try DefaultAzureCredential first (az login, VS Code login, managed identity).
    If that fails, fall back to Service Principal JSON file.
    """
    try:
        # First try default credentials (developer-friendly)
        cred = DefaultAzureCredential()
        # Fetch subscription ID from current context
        sub_client = SubscriptionClient(cred)
        subs = list(sub_client.subscriptions.list())

        if not subs:
            raise Exception("No active subscription found with DefaultAzureCredential.")
        
        subscription_id = subs[0].subscription_id
        print("✅ Using DefaultAzureCredential  (az login / managed identity)")
        return cred, subscription_id
    
    #falling back to service principal
    except Exception as e:
        print(f"{e}.⚠️ Default credentials not available, falling back to JSON file...")

        # Load creds from JSON
        with open(os.path.join("config", "azure-credentials.json")) as f:
            creds = json.load(f)

        cred = ClientSecretCredential(
            tenant_id=creds["tenantId"],
            client_id=creds["clientId"],
            client_secret=creds["clientSecret"],
        )
        subscription_id = creds["subscriptionId"]
        print("✅ Using Service Principal credentials")
        return cred, subscription_id
    
def query_costs(cred, subscription_id):
    # Initialize the client
    client = CostManagementClient(credential=cred)

    # Scope is at subscription level
    scope = f"subscriptions/{subscription_id}"

    # Define timeframe: last 7 days for testing
    time_period = QueryTimePeriod(
        from_property=(datetime.now(timezone.utc) - timedelta(days=7)),
        to=datetime.now(timezone.utc)
    )

    query_definition = QueryDefinition(
        type="Usage",
        timeframe="Custom",
        time_period=time_period,
        dataset=QueryDataset(
            granularity="Daily",
            aggregation={
                "totalCost": {
                    "name": "PreTaxCost",
                    "function": "Sum"
                }
            }
        )
    )

    # Run the query
    result = client.query.usage(scope=scope, parameters=query_definition)

    # Inspect the raw result (rows + columns)
    print("Columns:", [col.name for col in result.columns])
    for row in result.rows:
        print(row)

    return result


def costs_to_dataframe(result):
    # Extract column names
    columns = [col.name for col in result.columns]

    # Build DataFrame
    df = pd.DataFrame(result.rows, columns=columns)

    print("✅ Converted costs to DataFrame")
    print(df.head())  # quick peek
    return df

def main():
    # Step 1: Authenticate
    try: 
        cred, subscription_id = get_credentials()
        print("🎉 Authentication successful!")
        # Step 2: Query costs (last 7 days)
        result = query_costs(cred, subscription_id)
        # Step 3: Convert to DataFrame
        df = costs_to_dataframe(result)
        today = datetime.now().strftime("%Y%m%d")

        # Step 4: Save to CSV (basic export for now)
        filename = f"output/reports/azure_costs{today}.csv"
        df.to_csv(filename, index=False)
        print(f"💾 Saved costs to {filename}")
    except Exception as err:
        print("❌ Authentication failed:", err)
        sys.exit(1)



if __name__ == "__main__":
    main()