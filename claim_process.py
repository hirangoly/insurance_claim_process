import pandas as pd
import requests
import json

def calculate_net_fee(provider_fees, member_coinsurance, member_copay, allowed_fees):
    """
    Calculate the net fee based on provider fee, member coinsurance, member copay and allowed fees.
    """
    net_fee = provider_fees + member_coinsurance + member_copay - allowed_fees

    return net_fee

def process_csv(input_csv):
    """
    Process the CSV file to calculate net fees and return processed data.
    """
    # Read the input CSV file
    df = pd.read_csv(input_csv)

    
    # Calculate the net fee for each row
    df['net_fee'] = df.apply(lambda row: calculate_net_fee(float(row['provider fees'].split('$')[1]), float(row['member coinsurance'].split('$')[1]), float(row['member copay'].split('$')[1]), float(row['Allowed fees'].split('$')[1])), axis=1)
    
    # Group by provider NPI and aggregate claims
    provider_data = df.groupby('Provider NPI')['net_fee'].sum().reset_index()

    # Return relevant columns, user defined columns
    return provider_data.rename(columns={'Provider NPI':'provider_npi'})[['provider_npi', 'net_fee']].to_dict(orient='records')

def send_to_downstream_service(provider_data):
    """
    Send the processed provider data to the downstream FastAPI service.
    """
    url = 'http://localhost:8000/api/payments'  # FastAPI service endpoint
    response = requests.post(url, json=provider_data)
    
    if response.status_code == 200:
        print("Data successfully sent to downstream service!")
    else:
        print(f"Error: {response.status_code}")

# Example usage
input_csv = 'Desktop/Python/claim_process/claim_1234.csv'  # Path to your CSV file
provider_data = process_csv(input_csv)
print(provider_data)
send_to_downstream_service(provider_data)
