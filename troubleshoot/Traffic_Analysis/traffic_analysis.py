import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library
import subprocess
import inquirer
import json

### UNDER CONSTRUCTION ###


# Run script to set Organisation
script_path = "organisations/organisations_select.py"
subprocess.call(['python', script_path])

# Run script to set Network
script_path = "networks/network_select.py"
subprocess.call(['python', script_path])

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable
NETWORK_ID = os.getenv('NETWORK_ID') # Get the Network ID from environment variable

def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def traffic_analysis(dashboard, net_id):
    try:
        response = dashboard.networks.getNetworkTrafficAnalysis(
        net_id
        )
        print (response)
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

dashboard = meraki_session()
traffic_analysis(dashboard, NETWORK_ID)