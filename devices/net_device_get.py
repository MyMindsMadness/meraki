import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library
import subprocess
import json

# Run script to set Organisation
# script_path = "organisations/organisation_select.py"
# subprocess.call(['python', script_path])

# Run script to set Network
# script_path = "networks/network_select.py"
# subprocess.call(['python', script_path])

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable
NETWORK_ID = os.getenv('NETWORK_ID') # Get the Organisation ID from environment variable


def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def get_org_devices():
    dictofdevices = {}
    response = dashboard.networks.getNetworkDevices(NETWORK_ID)
    print(json.dumps(response,indent=4))
    for device in response:
        dictofdevices[device["name"]] = {"name":device["name"], 
                                        "serial":device["serial"],
                                        "firmware":device["firmware"],
                                        "mac":device["mac"],
                                        "model":device["model"]
                                        }
        if "lanIP" in device:
            print (device["lanIp"])
    return dictofdevices
        #print (json.dumps(device, indent=4))

def device_table_print(data):
    # Create a list of lists containing network details
    table_data = [[key,
                   value['serial'],
                   value['firmware'], 
                   value['mac'], 
                   value['model'],
                   ] 
                   for key, value in data.items()]
    
    # Print the device details in a tabular format
    print(tabulate(table_data, headers=["Name", "Serial", "firmware", "Mac", "Model"], tablefmt="grid"))
    
    #print(tabulate(table_data, headers=["Name", "ID"], tablefmt="grid"))

dashboard = meraki_session()
org_devices = get_org_devices()
device_table_print(org_devices)