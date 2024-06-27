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

def networks_inquiry(dict_of_networks):
    network_name_list = []
    for network in dict_of_networks:
        network_name_list.append(network)
    questions = [
    inquirer.List('choice', 
                  message="Select an option:", 
                  choices=network_name_list),
    ]
    answers = inquirer.prompt(questions)
    selected_option = answers['choice']
    #print(f"Selected option: {selected_option}")

    if selected_option in dict_of_networks:
        select = dict_of_networks[selected_option]
        return select["id"]

def network_deleter(netid):
    try:
        response = dashboard.networks.deleteNetwork(netid)
        print (f"{netid} was successfully deleted.")
    except meraki.APIError as error:
            print (error.status)
            print (error.reason)
            print (error.message)

dashboard = meraki_session()
org_networks = organisation_networks(dashboard)
network_id = networks_inquiry(org_networks)
network_deleter(network_id)