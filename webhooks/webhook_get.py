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

def organisation_network(dashboard):
    # Get all networks for the organization
    try:
        response = dashboard.organizations.getOrganizationNetworks(ORGANISATION_ID, total_pages='all')
        return response
    except meraki.APIError as error:
        print (error.status)
        print (error.reason)
        print (error.message)

def list_networks(org_networks):
    network_ids = []
    for network in org_networks:
        network_ids.append(network['id'])  # Add network IDs to the list
    return network_ids

def required_user_input():
    name = input("Please provide a relavant name for the webhook: ")  # Name of the webhook server
    url = input("Please provide the relevant URL for the webhook: ")  # URL of the webhook server
    return name , url

def webhook_getter(network_ids):
    webhook_dict={}
    #name , url = required_user_input()
    for netid in network_ids:
        # Create a webhook HTTP server for each network
        try:
            response = dashboard.networks.getNetworkWebhooksHttpServers(
               netid)
            #print (response)
            for webhook in response:
                webhook_dict[webhook["name"]] = {"name": webhook["name"] , "id": webhook["id"]}
            return (webhook_dict)
        except meraki.APIError as error:
            print (f"Webhook NOT created for {netid}")
            print (error.status)
            print (error.reason)
            print (error.message) 

def webhooktableprint(dict):
    table_data = [[key, value['id']] for key, value in dict.items()]
    print(tabulate(table_data, headers=["Name", "ID"], tablefmt="grid"))

dashboard = meraki_session()
org_networks = organisation_network(dashboard)
network_id_list = list_networks(org_networks)
dict_of_webhooks = webhook_getter(network_id_list)
webhooktableprint(dict_of_webhooks)
