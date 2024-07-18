import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library
import subprocess
import inquirer
import json
from time import sleep


# # Run script to set Organisation
# script_path = "organisations/organisations_select.py"
# subprocess.call(['python', script_path])

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable

def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def organistation_devices(dashboard):
    dictofdevices = {}
    try:
        response = dashboard.organizations.getOrganizationDevicesAvailabilities(
        ORGANISATION_ID, total_pages='all')
        for device in response:
            if device['productType'] == "switch":
                dictofdevices[device['name']] = {'name':device['name'], 
                                                'serial':device['serial'], 
                                                'mac':device['mac'],
                                                'productType':device['productType'], 
                                                'network':device['network']
                                                }
        device_table_print(dictofdevices)
        return dictofdevices
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

def device_table_print(dict):
    table_data = [[key, value['serial'], value['mac'], 
                   value['productType']] for key, value in dict.items()]
    print(tabulate(table_data, headers=["Name", "Serial", "Mac Address", "productType"], tablefmt="grid"))

def arp_table_print(dict):
    table_data = [[key, value['mac'], 
                   value['lastTouch']] for key, value in dict.items()]
    print(tabulate(table_data, headers=["IP Address", "Mac Address", "Last Updated"], tablefmt="grid"))

def device_inquiry(dict_of_devices):
    # Create a list of organistation names
    device_serial_list = []

    # Create a list prompt for the user to select a network
    for net in dict_of_devices:
        device_serial_list.append(net)
    questions = [
    inquirer.List('choice', 
                  message="Select an option:", 
                  choices=device_serial_list),
    ]

    # Prompt the user and get the selected network
    answers = inquirer.prompt(questions)
    selected_option = answers['choice']

    # If the selected option is in the dictionary, return the network ID
    if selected_option in dict_of_devices:
        select = dict_of_devices[selected_option]
        return select["serial"]

def ARP_table(dashboard, serial):
    arp_dict = {}
    try:
        post_arp_table = dashboard.devices.createDeviceLiveToolsArpTable(
        serial
        )
        arptableid = post_arp_table['arpTableId']
        print ("Please Wait")
        sleep(10)
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)
        #print (json.dumps(response, indent=4))
    try:
        get_arp_table = dashboard.devices.getDeviceLiveToolsArpTable(
           serial, arptableid
            )
        arp_result = get_arp_table['entries']
        for entry in arp_result:
            arp_dict[entry['ip']] = {'ip':entry['ip'], 
                                            'mac':entry['mac'], 
                                            'lastTouch':entry['lastUpdatedAt']
                                            }
        arp_table_print(arp_dict)
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

dashboard = meraki_session()
dev_dict = organistation_devices(dashboard)
device_serial = device_inquiry(dev_dict)
ARP_table(dashboard, device_serial)