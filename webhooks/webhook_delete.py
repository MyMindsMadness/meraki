import meraki  # Import the Meraki SDK
import os # Import os library
from dotenv import load_dotenv # import python-dotenv library
import inquirer

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
    name = input("Please provide a relavant id for the webhook: ")  # ID of the webhook server
    return name

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

def webhook_inquiry(dict_of_webhooks):
    webhook_name_list = []
    for webhook in dict_of_webhooks:
        webhook_name_list.append(webhook)
    questions = [
    inquirer.List('choice', 
                  message="Select an option:", 
                  choices=webhook_name_list),
    ]
    answers = inquirer.prompt(questions)
    selected_option = answers['choice']
    #print(f"Selected option: {selected_option}")

    if selected_option in dict_of_webhooks:
        select = dict_of_webhooks[selected_option]
        return select["id"]

def webhook_deleter(network_ids, webhook_id):
    for netid in network_ids:
        # Create a webhook HTTP server for each network
        try:
            response = dashboard.networks.deleteNetworkWebhooksHttpServer(
               netid, webhook_id
            )
            print (f"Webhook deleted for {netid}")
        except meraki.APIError as error:
            print (f"Webhook NOT deleted for {netid}")
            print (error.status)
            print (error.reason)
            print (error.message) 

dashboard = meraki_session()
org_networks = organisation_network(dashboard)
network_id_list = list_networks(org_networks)
dict_of_webhooks = webhook_getter(network_id_list)
webhook_id = webhook_inquiry(dict_of_webhooks)
webhook_deleter(network_id_list,webhook_id)
