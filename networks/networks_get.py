import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
from tabulate import tabulate # import tabulate library

# Load environment variables from the .env file
load_dotenv('venv/.env')
API_KEY = os.getenv('MERAKI_API_KEY')  # Get the Meraki API key from environment variable
ORGANISATION_ID = os.getenv('ORGANISATION_ID') # Get the Organisation ID from environment variable
WEBHOOK_SECRET = os.getenv('WEBHOOK_SHARED_SECRET')  # Get the webhook shared secret from environment variable


def meraki_session():
    # Create a Meraki dashboard API instance
    dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)
    return dashboard

def organisation_networks(dashboard):
    try:
        response = dashboard.organizations.getOrganizationNetworks(ORGANISATION_ID, total_pages='all')
        dictofnetworks = {}
        for network in response:
            #network_name = network["name"]
            dictofnetworks[network["name"]] = {"name":network["name"], 
                                            "id":network["id"],
                                            "products":network["productTypes"],
                                            "timezone":network["timeZone"],
                                            "tags":network["tags"],
                                            "url":network["url"]
                                            }
        return dictofnetworks
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

def network_table_print(dict):
    for key, value in dict.items():
        value['url'] = value['url'][:30]
        #value["id"] = value['id'][:25]
    table_data = [[key, value['id'], ', '.join(value['products']), 
                   value['timezone']] for key, value in dict.items()]
    print(tabulate(table_data, headers=["Name", "ID", "Products", "Timezone"], tablefmt="grid"))


dashboard = meraki_session()
org_networks = organisation_networks(dashboard)
network_table_print(org_networks)
