from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
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
        # Quick test: try to get a token
        cred.get_token("https://management.azure.com/.default")
        print("✅ Using DefaultAzureCredential (az login / managed identity)")
        return cred
    except Exception as e:
        print("⚠️ Default credentials not available, falling back to JSON file...")

        # Load creds from JSON
        with open(os.path.join("config", "azure-credentials.json")) as f:
            creds = json.load(f)

        cred = ClientSecretCredential(
            tenant_id=creds["tenantId"],
            client_id=creds["clientId"],
            client_secret=creds["clientSecret"],
        )
        print("✅ Using Service Principal credentials")
        return cred, creds["subscriptionId"]

if __name__ == "__main__":
    try:
        result = get_credentials()
        print("🎉 Authentication successful!")
    except Exception as err:
        print("❌ Authentication failed:", err)
        sys.exit(1)
