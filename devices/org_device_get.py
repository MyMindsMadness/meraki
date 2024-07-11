import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library
import subprocess
import json

# Run script to set Organisation
#script_path = "organisations/organisation_select.py"
#subprocess.call(['python', script_path])

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable


def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def get_org_devices():
    dictofdevices = {}
    response = dashboard.organizations.getOrganizationDevices(
    ORGANISATION_ID, total_pages='all')
    for device in response:
        ip = ""
        dictofdevices[device["name"]] = {"name":device["name"], 
                                        "serial":device["serial"],
                                        "product":device["productType"],
                                        "mac":device["mac"],
                                        "model":device["model"]
                                        }
    return dictofdevices
        #print (json.dumps(device, indent=4))

def device_table_print(data):
    # Create a list of lists containing network details
    table_data = [[key,
                   value['serial'],
                   value['product'], 
                   value['mac'], 
                   value['model'],
                   ] 
                   for key, value in data.items()]
    
    # Print the device details in a tabular format
    print(tabulate(table_data, headers=["Name", "Serial", "Product", "Mac", "Model"], tablefmt="grid"))
    
    #print(tabulate(table_data, headers=["Name", "ID"], tablefmt="grid"))

dashboard = meraki_session()
org_devices = get_org_devices()
device_table_print(org_devices)